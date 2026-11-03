import uuid

from sqlalchemy.orm import Session, joinedload

from app.core.config import settings
from app.core.exceptions import NotFoundException
from app.modules.invoices.schemas import (
    InvoiceItemRead,
    InvoicePaymentItem,
    InvoiceRead,
)
from app.modules.invoices.whatsapp_message import (
    build_whatsapp_deeplink,
    generate_whatsapp_message,
)
from app.modules.orders.models import Order
from app.modules.payments.domain.balance import calculate_payment_balance
from app.modules.payments.models import Payment


class InvoiceService:
    @classmethod
    def get_invoice_for_order(
        cls,
        db: Session,
        order_id: uuid.UUID,
        business_id: uuid.UUID,
    ) -> InvoiceRead:
        order = (
            db.query(Order)
            .options(
                joinedload(Order.business),
                joinedload(Order.customer),
                joinedload(Order.items),
            )
            .filter(Order.id == order_id, Order.business_id == business_id)
            .first()
        )
        if not order:
            raise NotFoundException(message="Pesanan tidak ditemukan.")

        payments = (
            db.query(Payment)
            .options(joinedload(Payment.void_record))
            .filter(Payment.order_id == order_id)
            .order_by(Payment.payment_time.asc())
            .all()
        )

        balance = calculate_payment_balance(order.total_amount, payments)

        items_read = [
            InvoiceItemRead(
                service_name=it.service_name_snapshot,
                quantity=it.quantity,
                unit=it.unit_snapshot,
                unit_price=it.unit_price_snapshot,
                line_total=it.line_total_amount,
            )
            for it in order.items
        ]

        verified_payments = [
            InvoicePaymentItem(
                payment_time=p.payment_time,
                method=p.method,
                amount=p.amount,
            )
            for p in payments
            if p.verification_status == "VERIFIED" and not p.is_voided
        ]

        # Public tracking URL using cryptographically secure token (M4)
        from app.modules.tracking.service import TrackingService
        _, raw_token = TrackingService.get_or_create_order_token(db, order.id)
        base_url = settings.allowed_origins_list[0] if settings.allowed_origins_list else "http://localhost:5173"
        tracking_url = f"{base_url}/track/{raw_token}"

        # Generate WhatsApp message & deep link
        items_dict = [
            {
                "name": it.service_name_snapshot,
                "quantity": str(it.quantity),
                "unit": it.unit_snapshot,
                "line_total": it.line_total_amount,
            }
            for it in order.items
        ]

        wa_text = generate_whatsapp_message(
            business_name=order.business.name,
            order_number=order.order_number,
            customer_name=order.customer.full_name,
            created_at=order.created_at,
            estimated_completion_at=order.estimated_completion_at,
            items=items_dict,
            total_amount=order.total_amount,
            total_paid=balance.total_paid,
            remaining_amount=balance.remaining_amount,
            payment_status=balance.payment_status.value,
            tracking_url=tracking_url,
        )

        wa_deeplink = build_whatsapp_deeplink(
            phone_e164=order.customer.phone_e164,
            message=wa_text,
        )

        return InvoiceRead(
            order_id=order.id,
            order_number=order.order_number,
            created_at=order.created_at,
            estimated_completion_at=order.estimated_completion_at,
            operational_status=order.operational_status,
            business_name=order.business.name,
            business_phone=order.business.phone_e164,
            business_address=order.business.address,
            customer_name=order.customer.full_name,
            customer_phone=order.customer.phone_e164,
            intake_method=order.intake_method,
            return_method=order.return_method,
            items=items_read,
            subtotal_amount=order.subtotal_amount,
            extra_charge_amount=order.extra_charge_amount,
            delivery_fee_amount=order.delivery_fee_amount,
            total_amount=order.total_amount,
            total_paid=balance.total_paid,
            remaining_amount=balance.remaining_amount,
            payment_status=balance.payment_status.value,
            payments=verified_payments,
            customer_notes=order.customer_notes,
            tracking_url=tracking_url,
            whatsapp_share_url=wa_deeplink,
            whatsapp_share_text=wa_text,
        )
