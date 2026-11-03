import hashlib
import re
import secrets
import uuid
from datetime import UTC, datetime, timedelta

from sqlalchemy.orm import Session

from app.core.exceptions import (
    ForbiddenException,
    GoneException,
    NotFoundException,
    ValidationException,
)
from app.modules.orders.models import Order
from app.modules.payments.domain.balance import calculate_payment_balance
from app.modules.payments.models import Payment
from app.modules.tracking.models import TrackingToken
from app.modules.tracking.schemas import (
    BusinessContact,
    FinancialSummary,
    PublicCancellationResponse,
    PublicTrackingRead,
    ServiceItemSummary,
    TimelineEvent,
)

STATUS_LABELS: dict[str, str] = {
    "RECEIVED": "Diterima Kasir",
    "QUEUED": "Dalam Antrean Cuci",
    "WASHING": "Sedang Dicuci",
    "DRYING": "Sedang Dikeringkan",
    "IRONING": "Sedang Disetrika",
    "QC_PACKING": "Quality Check & Packing",
    "READY": "Siap Diambil / Diantar",
    "COMPLETED": "Pesanan Selesai",
    "CANCELLED": "Pesanan Dibatalkan",
}


def mask_customer_name(name: str | None) -> str:
    """Mask customer name for privacy (e.g. 'Ibu Ratna' -> 'I** R****')."""
    if not name or not name.strip():
        return "Pelanggan"
    words = name.strip().split()
    masked_words: list[str] = []
    for word in words:
        if len(word) <= 1:
            masked_words.append(word)
        elif len(word) == 2:
            masked_words.append(word[0] + "*")
        else:
            masked_words.append(word[0] + "*" * (len(word) - 1))
    return " ".join(masked_words)


def mask_phone_number(phone: str | None) -> str:
    """Mask phone number for privacy (e.g. '+6281234567890' -> '+62812****7890')."""
    if not phone or not phone.strip():
        return "-"
    cleaned = phone.strip()
    if len(cleaned) <= 6:
        return cleaned[:2] + "****"
    # Keep first 6 characters, mask middle, keep last 4 characters
    prefix = cleaned[:6]
    suffix = cleaned[-4:] if len(cleaned) >= 10 else cleaned[-2:]
    return f"{prefix}****{suffix}"


class TrackingService:
    @staticmethod
    def generate_token_pair() -> tuple[str, str]:
        """Generate a random 256-bit URL-safe token and its SHA-256 hash."""
        raw_token = secrets.token_urlsafe(32)
        token_hash = hashlib.sha256(raw_token.encode("utf-8")).hexdigest()
        return raw_token, token_hash

    @staticmethod
    def create_order_tracking_token(
        db: Session,
        order_id: uuid.UUID,
        created_by: uuid.UUID | None = None,
        ttl_days: int = 90,
    ) -> tuple[TrackingToken, str]:
        """Generate and persist a tracking token for an order. Returns (model, raw_token)."""
        raw_token, token_hash = TrackingService.generate_token_pair()
        expires_at = datetime.now(UTC) + timedelta(days=ttl_days)

        token_record = TrackingToken(
            order_id=order_id,
            pickup_request_id=None,
            token_hash=token_hash,
            expires_at=expires_at,
            created_by=created_by,
        )
        db.add(token_record)
        db.commit()
        db.refresh(token_record)
        return token_record, raw_token

    @staticmethod
    def get_or_create_order_token(
        db: Session,
        order_id: uuid.UUID,
        created_by: uuid.UUID | None = None,
    ) -> tuple[TrackingToken, str]:
        """
        Retrieve an existing active tracking token for an order, or generate a new one.
        Note: When generating fresh, raw token is available.
        """
        now = datetime.now(UTC)
        existing = (
            db.query(TrackingToken)
            .filter(
                TrackingToken.order_id == order_id,
                TrackingToken.revoked_at.is_(None),
                TrackingToken.expires_at > now,
            )
            .first()
        )
        if existing:
            # Token exists, but raw token is never stored in DB
            # We generate a renewed token if raw token is needed
            return TrackingService.create_order_tracking_token(db, order_id, created_by)
        return TrackingService.create_order_tracking_token(db, order_id, created_by)

    @staticmethod
    def resolve_tracking_token(db: Session, raw_token: str) -> TrackingToken:
        """
        Validate and resolve a raw tracking token against its SHA-256 hash.
        Validates token format, revocation status, and TTL.
        """
        if not raw_token or len(raw_token) < 20 or len(raw_token) > 128:
            raise NotFoundException(message="Tautan tracking tidak valid atau salah.")

        token_hash = hashlib.sha256(raw_token.encode("utf-8")).hexdigest()
        token_record = (
            db.query(TrackingToken)
            .filter(TrackingToken.token_hash == token_hash)
            .first()
        )

        if not token_record:
            raise NotFoundException(message="Tautan tracking tidak ditemukan.")

        if token_record.revoked_at is not None:
            raise GoneException(message="Tautan tracking ini telah dicabut atau dinonaktifkan.")

        now = datetime.now(UTC)
        expires_at = token_record.expires_at
        if expires_at.tzinfo is None:
            expires_at = expires_at.replace(tzinfo=UTC)

        if expires_at <= now:
            raise GoneException(message="Masa berlaku tautan tracking telah berakhir.")

        return token_record

    @staticmethod
    def get_public_tracking_data(db: Session, raw_token: str) -> PublicTrackingRead:
        """
        Build the strict allowlist PublicTrackingRead response model for customer access.
        """
        token_record = TrackingService.resolve_tracking_token(db, raw_token)

        if not token_record.order_id:
            # Pickup request handling (Milestone 5)
            raise ValidationException(message="Tracking pickup request belum didukung pada tahap ini.")

        order: Order | None = (
            db.query(Order).filter(Order.id == token_record.order_id).first()
        )
        if not order:
            raise NotFoundException(message="Pesanan terkait tracking tidak ditemukan.")

        # Financial balance calculation
        payments = db.query(Payment).filter(Payment.order_id == order.id).all()
        balance = calculate_payment_balance(order.total_amount, payments)

        # Items summary
        service_items = [
            ServiceItemSummary(
                service_name=item.service_name_snapshot,
                quantity=str(item.quantity),
                unit=item.unit_snapshot,
                unit_price=item.unit_price_snapshot,
                line_total=item.line_total_amount,
            )
            for item in order.items
        ]

        # Timeline
        timeline: list[TimelineEvent] = []
        for hist in sorted(order.status_history, key=lambda h: h.created_at):
            created_at = hist.created_at
            if created_at.tzinfo is None:
                created_at = created_at.replace(tzinfo=UTC)
            timeline.append(
                TimelineEvent(
                    status=hist.to_status,
                    status_label=STATUS_LABELS.get(hist.to_status, hist.to_status),
                    timestamp=created_at,
                    note=hist.reason,
                )
            )

        # Business Contact info
        business = order.business
        clean_phone = re.sub(r"[^\d]", "", business.phone_e164) if business.phone_e164 else ""
        wa_text = f"Halo {business.name}, saya ingin menanyakan pesanan saya dengan nomor {order.order_number}."
        from urllib.parse import quote
        wa_url = f"https://wa.me/{clean_phone}?text={quote(wa_text)}"

        business_contact = BusinessContact(
            name=business.name,
            phone=business.phone_e164,
            address=business.address,
            whatsapp_url=wa_url,
        )

        # Invariant: PRD §5.7 #9 strictly forbids customer self-cancellation via public tracking
        can_cancel = False

        created_at = order.created_at
        if created_at.tzinfo is None:
            created_at = created_at.replace(tzinfo=UTC)

        est_completion = order.estimated_completion_at
        if est_completion and est_completion.tzinfo is None:
            est_completion = est_completion.replace(tzinfo=UTC)

        return PublicTrackingRead(
            tracking_type="ORDER",
            order_number=order.order_number,
            current_status=order.operational_status,
            status_label=STATUS_LABELS.get(order.operational_status, order.operational_status),
            can_cancel=can_cancel,
            created_at=created_at,
            estimated_completion_at=est_completion,
            customer_name_masked=mask_customer_name(order.customer.full_name if order.customer else None),
            customer_phone_masked=mask_phone_number(order.customer.phone_e164 if order.customer else None),
            service_summary=service_items,
            financial_summary=FinancialSummary(
                total_amount=balance.total_amount,
                paid_amount=balance.total_paid,
                remaining_amount=balance.remaining_amount,
                payment_status=balance.payment_status,
            ),
            timeline=timeline,
            business_contact=business_contact,
            intake_method=order.intake_method,
            return_method=order.return_method,
        )

    @staticmethod
    def cancel_order_by_customer(
        db: Session,
        raw_token: str,
        reason: str | None = None,
    ) -> PublicCancellationResponse:
        """
        Enforce PRD §5.7 Rule 9 & BSD §34.1:
        Customers cannot mutate order status directly via public tracking links.
        All order cancellations must be performed by authorized cashier/owner.
        """
        # Resolve token first to ensure valid token request
        _ = TrackingService.resolve_tracking_token(db, raw_token)
        raise ForbiddenException(
            message="Pelanggan tidak dapat mengubah status pesanan secara mandiri melalui tautan tracking publik. Silakan hubungi kasir atau pengelola laundry melalui kontak WhatsApp yang tersedia."
        )
