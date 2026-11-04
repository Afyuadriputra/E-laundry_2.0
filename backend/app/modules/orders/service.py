import uuid
from datetime import UTC, datetime, timedelta
from decimal import Decimal

from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session, joinedload

from app.core.exceptions import ConflictException, NotFoundException, ValidationException
from app.modules.audit.service import AuditService
from app.modules.customers.models import Customer
from app.modules.customers.schemas import CustomerCreate
from app.modules.customers.service import CustomerService
from app.modules.orders.domain.invariants import validate_completion_time
from app.modules.orders.domain.pricing import PricingEngine
from app.modules.orders.domain.state_machine import OperationalStatus, OrderStateMachine
from app.modules.orders.models import Order, OrderHandoff, OrderItem, OrderStatusHistory
from app.modules.orders.schemas import (
    OrderCreate,
    OrderStatusTransitionRequest,
)
from app.modules.payments.domain.balance import PaymentStatus, calculate_payment_balance
from app.modules.services.models import Service


class OrderService:
    @staticmethod
    def generate_order_number(db: Session, business_id: uuid.UUID) -> str:
        """Enforces DEC-03: Sequential daily code ORD-YYYYMMDD-XXXX."""
        date_str = datetime.now(UTC).strftime("%Y%m%d")
        prefix = f"ORD-{date_str}-"

        # Query highest order number for today's date within this business
        query = select(func.max(Order.order_number)).where(
            Order.business_id == business_id,
            Order.order_number.like(f"{prefix}%"),
        )
        max_num = db.scalar(query)

        if not max_num:
            seq = 1
        else:
            try:
                seq = int(max_num.split("-")[-1]) + 1
            except (ValueError, IndexError):
                seq = 1

        return f"{prefix}{seq:04d}"

    @classmethod
    def create_order(
        cls,
        db: Session,
        business_id: uuid.UUID,
        user_id: uuid.UUID,
        data: OrderCreate,
    ) -> Order:
        # 1. Resolve customer
        if data.customer_id:
            customer = CustomerService.get_by_id(db, business_id, data.customer_id)
        elif data.new_customer_name and data.new_customer_phone:
            # Inline customer resolution/creation
            customer_in = CustomerCreate(
                full_name=data.new_customer_name,
                phone_e164=data.new_customer_phone,
                address=data.new_customer_address,
            )
            existing = CustomerService.find_by_phone(db, business_id, customer_in.phone_e164)
            if existing:
                customer = existing
            else:
                customer = CustomerService.create_customer(db, business_id, customer_in)
        else:
            raise ValidationException(
                "Harap tentukan pelanggan: sertakan 'customer_id' atau nama & nomor WhatsApp baru."
            )

        # 2. Fetch and validate services
        service_ids = [item.service_id for item in data.items]
        services_map = {
            s.id: s
            for s in db.scalars(
                select(Service).where(
                    Service.id.in_(service_ids),
                    Service.business_id == business_id,
                )
            ).all()
        }

        if len(services_map) != len(set(service_ids)):
            raise NotFoundException(
                "Satu atau lebih layanan yang dipilih tidak ditemukan pada bisnis ini."
            )

        for s in services_map.values():
            if not s.is_active:
                raise ValidationException(
                    f"Layanan '{s.name}' sedang tidak aktif dan tidak dapat dipilih."
                )

        # 3. Calculate pricing using Python Decimal engine
        pricing_inputs: list[tuple[str, Decimal, int]] = []
        for item_in in data.items:
            srv = services_map[item_in.service_id]
            pricing_inputs.append((srv.pricing_type, item_in.quantity, srv.unit_price))

        price_result = PricingEngine.calculate_order(
            items=pricing_inputs,
            extra_charge_amount=data.extra_charge_amount,
            delivery_fee_amount=data.delivery_fee_amount,
        )

        # 4. Determine estimated completion time
        now = datetime.now(UTC)
        if data.estimated_completion_at:
            validate_completion_time(data.estimated_completion_at)
            est_completion = data.estimated_completion_at
        else:
            # Default to max service estimated hours or standard 24 hours
            max_hours = max((s.estimated_hours or 24 for s in services_map.values()), default=24)
            est_completion = now + timedelta(hours=max_hours)

        # 5. Generate daily sequential order code
        order_number = cls.generate_order_number(db, business_id)

        # 6. Instantiate Order
        order = Order(
            business_id=business_id,
            order_number=order_number,
            customer_id=customer.id,
            created_by=user_id,
            operational_status=OperationalStatus.RECEIVED.value,
            intake_method=data.intake_method.value,
            return_method=data.return_method.value,
            subtotal_amount=price_result.subtotal_amount,
            extra_charge_amount=price_result.extra_charge_amount,
            delivery_fee_amount=price_result.delivery_fee_amount,
            total_amount=price_result.total_amount,
            estimated_completion_at=est_completion,
            customer_notes=data.customer_notes.strip() if data.customer_notes else None,
            internal_notes=data.internal_notes.strip() if data.internal_notes else None,
            version=1,
        )
        db.add(order)
        db.flush()  # populate order.id for child entities

        # 7. Add Order Items with snapshot data
        for i, item_in in enumerate(data.items):
            srv = services_map[item_in.service_id]
            line_res = price_result.line_results[i]
            order_item = OrderItem(
                order_id=order.id,
                service_id=srv.id,
                service_name_snapshot=srv.name,
                pricing_type_snapshot=srv.pricing_type,
                unit_snapshot=srv.unit,
                quantity=line_res.measured_quantity,
                unit_price_snapshot=srv.unit_price,
                line_total_amount=line_res.line_total,
                requires_ironing_snapshot=srv.requires_ironing,
            )
            db.add(order_item)

        # 8. Record initial status history
        history = OrderStatusHistory(
            order_id=order.id,
            from_status=None,
            to_status=OperationalStatus.RECEIVED.value,
            changed_by=user_id,
            reason="Pesanan dibuat di kasir",
        )
        db.add(history)

        # 9. Generate public tracking token (M4)
        from app.modules.tracking.models import TrackingToken
        from app.modules.tracking.service import TrackingService
        _, token_hash = TrackingService.generate_token_pair()
        tracking_record = TrackingToken(
            order_id=order.id,
            pickup_request_id=None,
            token_hash=token_hash,
            expires_at=now + timedelta(days=90),
            created_by=user_id,
        )
        db.add(tracking_record)

        db.commit()
        db.refresh(order)
        return order

    @staticmethod
    def get_by_id(db: Session, business_id: uuid.UUID, order_id: uuid.UUID) -> Order:
        order = db.scalar(
            select(Order)
            .options(
                joinedload(Order.customer),
                joinedload(Order.items),
                joinedload(Order.status_history),
                joinedload(Order.handoff),
                joinedload(Order.payments),
            )
            .where(
                Order.id == order_id,
                Order.business_id == business_id,
            )
        )
        if not order:
            raise NotFoundException(f"Pesanan dengan ID '{order_id}' tidak ditemukan.")
        return order

    @staticmethod
    def list_orders(
        db: Session,
        business_id: uuid.UUID,
        operational_status: str | None = None,
        customer_id: uuid.UUID | None = None,
        search: str | None = None,
        limit: int = 50,
        offset: int = 0,
    ) -> tuple[list[Order], int]:
        query = (
            select(Order)
            .join(Customer, Order.customer_id == Customer.id)
            .where(Order.business_id == business_id)
        )

        if operational_status:
            query = query.where(Order.operational_status == operational_status)
        if customer_id:
            query = query.where(Order.customer_id == customer_id)
        if search:
            search_pat = f"%{search.strip()}%"
            query = query.where(
                or_(
                    Order.order_number.ilike(search_pat),
                    Customer.full_name.ilike(search_pat),
                    Customer.phone_e164.ilike(search_pat),
                )
            )

        total = db.scalar(select(func.count()).select_from(query.subquery())) or 0
        orders = list(
            db.scalars(
                query.options(joinedload(Order.customer))
                .order_by(Order.created_at.desc())
                .offset(offset)
                .limit(limit)
            )
            .unique()
            .all()
        )
        return orders, total

    @classmethod
    def transition_status(
        cls,
        db: Session,
        business_id: uuid.UUID,
        user_id: uuid.UUID,
        order_id: uuid.UUID,
        request: OrderStatusTransitionRequest,
    ) -> Order:
        order = cls.get_by_id(db, business_id, order_id)

        # M2-13: Optimistic concurrency locking check
        if order.version != request.expected_version:
            raise ConflictException(
                code="VERSION_CONFLICT",
                message=(
                    f"Konflik versi: pesanan telah diperbarui pengguna lain "
                    f"(versi saat ini: {order.version}, versi Anda: {request.expected_version})."
                ),
            )

        # Check if any item in order requires ironing
        requires_ironing = any(item.requires_ironing_snapshot for item in order.items)
        has_handoff = order.handoff is not None

        # Payment verification: compute actual balance from payments (BSD.md §33 & §18.4)
        is_fully_paid = False
        if order.payments:
            balance = calculate_payment_balance(order.total_amount, order.payments)
            is_fully_paid = balance.payment_status == PaymentStatus.PAID
        elif order.total_amount == 0:
            is_fully_paid = True

        now = datetime.now(UTC)

        # If transitioning to COMPLETED and no handoff exists yet,
        # create customer pickup handoff if payment is valid (BSD.md §33.1)
        if request.to_status == OperationalStatus.COMPLETED and not has_handoff:
            if is_fully_paid:
                handoff = OrderHandoff(
                    order_id=order.id,
                    delivery_task_id=None,
                    handoff_method="CUSTOMER_PICKUP",
                    received_by_name=request.received_by_name
                    or (order.customer.full_name if order.customer else "Pelanggan"),
                    confirmed_by_user_id=user_id,
                    confirmed_at=now,
                    notes=request.reason or "Pengambilan langsung di outlet",
                )
                db.add(handoff)
                db.flush()
                order.handoff = handoff
                has_handoff = True

        OrderStateMachine.validate_transition(
            from_status=order.operational_status,
            to_status=request.to_status.value,
            requires_ironing=requires_ironing,
            has_handoff=has_handoff,
            is_fully_paid=is_fully_paid,
            cancellation_reason=request.cancellation_reason,
        )

        old_status = order.operational_status
        new_status = request.to_status.value

        order.operational_status = new_status
        order.version += 1

        if new_status == OperationalStatus.CANCELLED.value:
            order.cancelled_at = now
            order.cancellation_reason = request.cancellation_reason
            AuditService.record(
                db=db,
                action="ORDER_CANCELLED",
                resource_type="order",
                actor_user_id=user_id,
                resource_id=order.id,
                before_data={"status": old_status},
                after_data={"status": new_status},
                reason=request.cancellation_reason or request.reason,
            )
        elif new_status == OperationalStatus.COMPLETED.value:
            order.completed_at = now
            AuditService.record(
                db=db,
                action="ORDER_COMPLETED",
                resource_type="order",
                actor_user_id=user_id,
                resource_id=order.id,
                before_data={"status": old_status},
                after_data={"status": new_status},
                reason=request.reason or "Pesanan diserahkan kepada pelanggan",
            )

        history = OrderStatusHistory(
            order_id=order.id,
            from_status=old_status,
            to_status=new_status,
            changed_by=user_id,
            reason=request.reason or request.cancellation_reason,
        )
        db.add(history)

        db.commit()
        db.refresh(order)
        return order
