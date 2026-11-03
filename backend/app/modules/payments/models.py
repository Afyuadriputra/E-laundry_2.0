import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import (
    BigInteger,
    CheckConstraint,
    DateTime,
    ForeignKey,
    Index,
    String,
    Text,
    Uuid,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.modules.orders.models import Order
    from app.modules.users.models import User


class Payment(Base):
    """Stores manual verified payments for laundry orders according to BSD.md Section 17."""

    __tablename__ = "payments"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    order_id: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        ForeignKey("orders.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    amount: Mapped[int] = mapped_column(BigInteger, nullable=False)
    # Payment methods: CASH, BANK_TRANSFER, QRIS_MANUAL
    method: Mapped[str] = mapped_column(String(30), nullable=False)
    verification_status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        server_default="VERIFIED",
    )  # VERIFIED
    payment_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
    verified_by: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        ForeignKey("users.id", ondelete="RESTRICT"),
        nullable=False,
    )
    verified_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
    reference_note: Mapped[str | None] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    # Invariants
    __table_args__ = (
        CheckConstraint("amount > 0", name="chk_payments_amount_positive"),
        Index("idx_payments_order_time", "order_id", "payment_time"),
    )

    # Relationships
    order: Mapped["Order"] = relationship("Order", back_populates="payments")
    verifier: Mapped["User"] = relationship("User", foreign_keys=[verified_by])
    void_record: Mapped["PaymentVoid | None"] = relationship(
        "PaymentVoid",
        back_populates="payment",
        uselist=False,
        cascade="all, delete-orphan",
    )

    @property
    def is_voided(self) -> bool:
        return self.void_record is not None


class PaymentVoid(Base):
    """Documents the voiding of a payment entry according to BSD.md Section 18."""

    __tablename__ = "payment_voids"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    payment_id: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        ForeignKey("payments.id", ondelete="RESTRICT"),
        nullable=False,
        unique=True,
        index=True,
    )
    reason: Mapped[str] = mapped_column(Text, nullable=False)
    voided_by: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        ForeignKey("users.id", ondelete="RESTRICT"),
        nullable=False,
    )
    voided_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    # Relationships
    payment: Mapped["Payment"] = relationship("Payment", back_populates="void_record")
    voider: Mapped["User"] = relationship("User", foreign_keys=[voided_by])
