import json
import uuid
from datetime import UTC, datetime

from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from app.core.exceptions import NotFoundException
from app.modules.audit.service import AuditService
from app.modules.idempotency.service import IdempotencyService
from app.modules.orders.models import Order
from app.modules.payments.domain.balance import calculate_payment_balance
from app.modules.payments.domain.invariants import (
    AmountMustBePositiveError,
    OrderCancelledPaymentError,
    OverpaymentNotAllowedError,
    PaymentAlreadyVoidedError,
    VoidReasonRequiredError,
)
from app.modules.payments.models import Payment, PaymentVoid
from app.modules.payments.schemas import (
    OrderPaymentSummary,
    PaymentCreate,
    PaymentRead,
    PaymentVoidCreate,
)


class PaymentService:
    @classmethod
    def _map_payment_to_read(cls, payment: Payment) -> PaymentRead:
        is_voided = payment.is_voided
        void_record = payment.void_record
        voider_name = None
        if void_record and void_record.voider:
            voider_name = void_record.voider.full_name

        return PaymentRead(
            id=payment.id,
            order_id=payment.order_id,
            amount=payment.amount,
            method=payment.method,
            verification_status=payment.verification_status,
            payment_time=payment.payment_time,
            verified_by=payment.verified_by,
            verified_by_name=payment.verifier.full_name if payment.verifier else None,
            verified_at=payment.verified_at,
            reference_note=payment.reference_note,
            created_at=payment.created_at,
            is_voided=is_voided,
            void_reason=void_record.reason if void_record else None,
            voided_at=void_record.voided_at if void_record else None,
            voided_by_name=voider_name,
        )

    @classmethod
    def record_payment(
        cls,
        db: Session,
        order_id: uuid.UUID,
        business_id: uuid.UUID,
        verified_by_user_id: uuid.UUID,
        payload: PaymentCreate,
        idempotency_key: str | None = None,
    ) -> PaymentRead:
        """Records a manual verified payment for an order with row-level locking."""
        # 1. Idempotency handling (M3-05)
        idem_record = None
        if idempotency_key:
            idem_record, is_fresh = IdempotencyService.acquire(
                db,
                scope_key=str(business_id),
                operation="RECORD_PAYMENT",
                idempotency_key=idempotency_key,
                payload={"order_id": str(order_id), **payload.model_dump()},
            )
            if not is_fresh and idem_record and idem_record.response_reference:
                saved_data = json.loads(idem_record.response_reference)
                return PaymentRead(**saved_data)

        # 2. Pessimistic Row Lock on Order
        stmt = (
            select(Order)
            .where(Order.id == order_id, Order.business_id == business_id)
            .with_for_update()
        )
        order = db.scalar(stmt)
        if not order:
            if idem_record:
                IdempotencyService.fail(db, idem_record.id)
            raise NotFoundException(message="Pesanan tidak ditemukan.")

        # 3. Check Order Invariants
        if order.operational_status == "CANCELLED":
            if idem_record:
                IdempotencyService.fail(db, idem_record.id)
            raise OrderCancelledPaymentError(order.order_number)

        if payload.amount <= 0:
            if idem_record:
                IdempotencyService.fail(db, idem_record.id)
            raise AmountMustBePositiveError(payload.amount)

        # 4. Fetch existing payments and calculate balance
        existing_payments = (
            db.query(Payment)
            .options(joinedload(Payment.void_record))
            .filter(Payment.order_id == order_id)
            .all()
        )
        balance = calculate_payment_balance(order.total_amount, existing_payments)

        # 5. Financial Invariant: Overpayment Check
        if payload.amount > balance.remaining_amount:
            if idem_record:
                IdempotencyService.fail(db, idem_record.id)
            raise OverpaymentNotAllowedError(payload.amount, balance.remaining_amount)

        # 6. Create Payment Record
        now = datetime.now(UTC)
        payment = Payment(
            id=uuid.uuid4(),
            order_id=order.id,
            amount=payload.amount,
            method=payload.method.value,
            verification_status="VERIFIED",
            payment_time=now,
            verified_by=verified_by_user_id,
            verified_at=now,
            reference_note=payload.reference_note,
            created_at=now,
        )
        db.add(payment)
        db.commit()
        db.refresh(payment)

        result = cls._map_payment_to_read(payment)

        # Complete idempotency record
        if idem_record:
            IdempotencyService.complete(
                db,
                idem_record.id,
                status_code=200,
                response_body=result.model_dump_json(),
            )
            db.commit()

        return result

    @classmethod
    def void_payment(
        cls,
        db: Session,
        payment_id: uuid.UUID,
        business_id: uuid.UUID,
        voided_by_user_id: uuid.UUID,
        payload: PaymentVoidCreate,
    ) -> PaymentRead:
        """Voids a previously recorded payment entry (Owner only, non-destructive)."""
        if not payload.reason or not payload.reason.strip():
            raise VoidReasonRequiredError()

        payment = (
            db.query(Payment)
            .join(Order, Payment.order_id == Order.id)
            .filter(Payment.id == payment_id, Order.business_id == business_id)
            .options(
                joinedload(Payment.void_record),
                joinedload(Payment.order),
                joinedload(Payment.verifier),
            )
            .first()
        )
        if not payment:
            raise NotFoundException(
                message="Transaksi pembayaran tidak ditemukan.",
            )

        # Lock the associated order row
        _ = db.query(Order).filter(Order.id == payment.order_id).with_for_update().first()

        if payment.is_voided:
            raise PaymentAlreadyVoidedError(str(payment_id))

        now = datetime.now(UTC)
        void_record = PaymentVoid(
            id=uuid.uuid4(),
            payment_id=payment.id,
            reason=payload.reason.strip(),
            voided_by=voided_by_user_id,
            voided_at=now,
            created_at=now,
        )
        db.add(void_record)

        AuditService.record(
            db=db,
            action="PAYMENT_VOIDED",
            resource_type="payment",
            actor_user_id=voided_by_user_id,
            resource_id=payment.id,
            before_data={"amount": payment.amount, "method": payment.method},
            after_data={"is_voided": True, "void_reason": payload.reason.strip()},
            reason=payload.reason.strip(),
        )

        db.commit()
        db.refresh(payment)

        return cls._map_payment_to_read(payment)

    @classmethod
    def get_order_payment_summary(
        cls,
        db: Session,
        order_id: uuid.UUID,
        business_id: uuid.UUID,
    ) -> OrderPaymentSummary:
        order = (
            db.query(Order)
            .filter(Order.id == order_id, Order.business_id == business_id)
            .first()
        )
        if not order:
            raise NotFoundException(message="Pesanan tidak ditemukan.")

        payments = (
            db.query(Payment)
            .options(
                joinedload(Payment.void_record).joinedload(PaymentVoid.voider),
                joinedload(Payment.verifier),
            )
            .filter(Payment.order_id == order_id)
            .order_by(Payment.payment_time.asc())
            .all()
        )

        balance = calculate_payment_balance(order.total_amount, payments)
        mapped_payments = [cls._map_payment_to_read(p) for p in payments]

        return OrderPaymentSummary(
            order_id=order.id,
            order_number=order.order_number,
            total_amount=order.total_amount,
            total_paid=balance.total_paid,
            remaining_amount=balance.remaining_amount,
            payment_status=balance.payment_status,
            payments=mapped_payments,
        )

    @classmethod
    def get_payment_detail(
        cls,
        db: Session,
        payment_id: uuid.UUID,
        business_id: uuid.UUID,
    ) -> PaymentRead:
        payment = (
            db.query(Payment)
            .join(Order, Payment.order_id == Order.id)
            .filter(Payment.id == payment_id, Order.business_id == business_id)
            .options(
                joinedload(Payment.void_record).joinedload(PaymentVoid.voider),
                joinedload(Payment.verifier),
            )
            .first()
        )
        if not payment:
            raise NotFoundException(
                message="Transaksi pembayaran tidak ditemukan.",
            )
        return cls._map_payment_to_read(payment)
