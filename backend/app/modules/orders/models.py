import uuid
from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import (
    BigInteger,
    Boolean,
    CheckConstraint,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    Numeric,
    String,
    Text,
    Uuid,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.modules.businesses.models import Business
    from app.modules.customers.models import Customer
    from app.modules.payments.models import Payment
    from app.modules.pickup_delivery.models import DeliveryTask, PickupRequest
    from app.modules.services.models import Service
    from app.modules.tracking.models import TrackingToken
    from app.modules.users.models import User


class Order(Base, TimestampMixin):
    __tablename__ = "orders"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    business_id: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        ForeignKey("businesses.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    order_number: Mapped[str] = mapped_column(
        String(40),
        nullable=False,
        unique=True,
        index=True,
    )
    customer_id: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        ForeignKey("customers.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    pickup_request_id: Mapped[uuid.UUID | None] = mapped_column(
        Uuid,
        ForeignKey("pickup_requests.id", ondelete="SET NULL"),
        nullable=True,
        unique=True,
    )
    created_by: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        ForeignKey("users.id", ondelete="RESTRICT"),
        nullable=False,
    )
    operational_status: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        default="RECEIVED",
        index=True,
    )
    intake_method: Mapped[str] = mapped_column(String(30), nullable=False)
    return_method: Mapped[str] = mapped_column(String(30), nullable=False)
    subtotal_amount: Mapped[int] = mapped_column(BigInteger, nullable=False, default=0)
    extra_charge_amount: Mapped[int] = mapped_column(BigInteger, nullable=False, default=0)
    delivery_fee_amount: Mapped[int] = mapped_column(BigInteger, nullable=False, default=0)
    total_amount: Mapped[int] = mapped_column(BigInteger, nullable=False, default=0)
    estimated_completion_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )
    customer_notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    internal_notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    version: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    completed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    cancelled_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    cancellation_reason: Mapped[str | None] = mapped_column(Text, nullable=True)

    business: Mapped["Business"] = relationship("Business")
    customer: Mapped["Customer"] = relationship("Customer", back_populates="orders")
    creator: Mapped["User"] = relationship("User", foreign_keys=[created_by])
    items: Mapped[list["OrderItem"]] = relationship(
        "OrderItem",
        back_populates="order",
        cascade="all, delete-orphan",
    )
    status_history: Mapped[list["OrderStatusHistory"]] = relationship(
        "OrderStatusHistory",
        back_populates="order",
        cascade="all, delete-orphan",
        order_by="OrderStatusHistory.created_at",
    )
    handoff: Mapped["OrderHandoff | None"] = relationship(
        "OrderHandoff",
        back_populates="order",
        uselist=False,
        cascade="all, delete-orphan",
    )
    payments: Mapped[list["Payment"]] = relationship(
        "Payment",
        back_populates="order",
        cascade="all, delete-orphan",
        order_by="Payment.payment_time",
    )
    tracking_tokens: Mapped[list["TrackingToken"]] = relationship(
        "TrackingToken",
        back_populates="order",
        cascade="all, delete-orphan",
    )
    pickup_request: Mapped["PickupRequest | None"] = relationship(
        "PickupRequest",
        back_populates="order",
    )

    __table_args__ = (
        CheckConstraint("subtotal_amount >= 0", name="ck_orders_subtotal_amount"),
        CheckConstraint("extra_charge_amount >= 0", name="ck_orders_extra_charge_amount"),
        CheckConstraint("delivery_fee_amount >= 0", name="ck_orders_delivery_fee_amount"),
        CheckConstraint("total_amount >= 0", name="ck_orders_total_amount"),
        Index("ix_orders_business_status", "business_id", "operational_status"),
        Index("ix_orders_business_created", "business_id", "created_at"),
    )


class OrderItem(Base):
    __tablename__ = "order_items"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    order_id: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        ForeignKey("orders.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    service_id: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        ForeignKey("services.id", ondelete="RESTRICT"),
        nullable=False,
    )
    service_name_snapshot: Mapped[str] = mapped_column(String(150), nullable=False)
    pricing_type_snapshot: Mapped[str] = mapped_column(String(20), nullable=False)
    unit_snapshot: Mapped[str] = mapped_column(String(20), nullable=False)
    quantity: Mapped[Decimal] = mapped_column(Numeric(10, 3), nullable=False)
    unit_price_snapshot: Mapped[int] = mapped_column(BigInteger, nullable=False)
    line_total_amount: Mapped[int] = mapped_column(BigInteger, nullable=False)
    requires_ironing_snapshot: Mapped[bool] = mapped_column(Boolean, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    order: Mapped["Order"] = relationship("Order", back_populates="items")
    service: Mapped["Service"] = relationship("Service")

    __table_args__ = (
        CheckConstraint("quantity > 0", name="ck_order_items_quantity"),
        CheckConstraint("unit_price_snapshot >= 0", name="ck_order_items_unit_price"),
        CheckConstraint("line_total_amount >= 0", name="ck_order_items_line_total"),
    )


class OrderStatusHistory(Base):
    __tablename__ = "order_status_history"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    order_id: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        ForeignKey("orders.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    from_status: Mapped[str | None] = mapped_column(String(30), nullable=True)
    to_status: Mapped[str] = mapped_column(String(30), nullable=False)
    changed_by: Mapped[uuid.UUID | None] = mapped_column(
        Uuid,
        ForeignKey("users.id", ondelete="RESTRICT"),
        nullable=True,
    )
    reason: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    order: Mapped["Order"] = relationship("Order", back_populates="status_history")
    user: Mapped["User"] = relationship("User")


class OrderHandoff(Base):
    __tablename__ = "order_handoffs"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    order_id: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        ForeignKey("orders.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
    )
    delivery_task_id: Mapped[uuid.UUID | None] = mapped_column(
        Uuid,
        ForeignKey("delivery_tasks.id", ondelete="SET NULL"),
        nullable=True,
    )
    handoff_method: Mapped[str] = mapped_column(String(30), nullable=False)
    received_by_name: Mapped[str | None] = mapped_column(String(150), nullable=True)
    confirmed_by_user_id: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        ForeignKey("users.id", ondelete="RESTRICT"),
        nullable=False,
    )
    confirmed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    order: Mapped["Order"] = relationship("Order", back_populates="handoff")
    delivery_task: Mapped["DeliveryTask | None"] = relationship(
        "DeliveryTask",
        back_populates="order_handoff",
    )
    confirmed_by: Mapped["User"] = relationship("User")

