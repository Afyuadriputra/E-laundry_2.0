import uuid
from datetime import date, datetime, time
from enum import StrEnum
from typing import TYPE_CHECKING

from sqlalchemy import (
    CheckConstraint,
    Date,
    DateTime,
    ForeignKey,
    Index,
    String,
    Text,
    Time,
    Uuid,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.modules.businesses.models import Business
    from app.modules.customers.models import Customer
    from app.modules.orders.models import Order, OrderHandoff
    from app.modules.tracking.models import TrackingToken
    from app.modules.users.models import User


class PickupStatus(StrEnum):
    REQUESTED = "REQUESTED"
    CONFIRMED = "CONFIRMED"
    ASSIGNED = "ASSIGNED"
    EN_ROUTE = "EN_ROUTE"
    PICKED_UP = "PICKED_UP"
    AT_LAUNDRY = "AT_LAUNDRY"
    CONVERTED = "CONVERTED"
    REJECTED = "REJECTED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"


class DeliveryTaskType(StrEnum):
    PICKUP = "PICKUP"
    DELIVERY = "DELIVERY"


class DeliveryTaskStatus(StrEnum):
    PENDING = "PENDING"
    ASSIGNED = "ASSIGNED"
    EN_ROUTE = "EN_ROUTE"
    ARRIVED = "ARRIVED"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"


class PickupRequest(Base, TimestampMixin):
    """
    Pickup Request Entity (BSD.md §20).
    Captures customer laundry pickup requests with or without authentication.
    """
    __tablename__ = "pickup_requests"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    business_id: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        ForeignKey("businesses.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    customer_id: Mapped[uuid.UUID | None] = mapped_column(
        Uuid,
        ForeignKey("customers.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    request_number: Mapped[str] = mapped_column(
        String(40),
        unique=True,
        nullable=False,
        index=True,
    )
    requester_name: Mapped[str] = mapped_column(String(150), nullable=False)
    phone_e164: Mapped[str] = mapped_column(String(20), nullable=False)
    pickup_address: Mapped[str] = mapped_column(Text, nullable=False)
    requested_date: Mapped[date] = mapped_column(Date, nullable=False)
    requested_time_start: Mapped[time] = mapped_column(Time, nullable=False)
    requested_time_end: Mapped[time] = mapped_column(Time, nullable=False)
    confirmed_start_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    confirmed_end_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    status: Mapped[str] = mapped_column(
        String(30),
        default=PickupStatus.REQUESTED.value,
        nullable=False,
        index=True,
    )
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    rejection_reason: Mapped[str | None] = mapped_column(Text, nullable=True)

    __table_args__ = (
        Index("ix_pickup_requests_business_status", "business_id", "status"),
        Index("ix_pickup_requests_requested_date", "requested_date"),
    )

    # Relationships
    business: Mapped["Business"] = relationship("Business", lazy="select")
    customer: Mapped["Customer | None"] = relationship("Customer", lazy="select")
    delivery_tasks: Mapped[list["DeliveryTask"]] = relationship(
        "DeliveryTask",
        back_populates="pickup_request",
        cascade="all, delete-orphan",
    )
    order: Mapped["Order | None"] = relationship(
        "Order",
        back_populates="pickup_request",
        uselist=False,
    )
    tracking_tokens: Mapped[list["TrackingToken"]] = relationship(
        "TrackingToken",
        back_populates="pickup_request",
        cascade="all, delete-orphan",
    )


class DeliveryTask(Base, TimestampMixin):
    """
    Delivery Task Entity (BSD.md §21).
    Stores courier assignments for laundry pickup from customer or delivery to customer.
    """
    __tablename__ = "delivery_tasks"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    business_id: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        ForeignKey("businesses.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    task_type: Mapped[str] = mapped_column(String(20), nullable=False)  # PICKUP or DELIVERY
    pickup_request_id: Mapped[uuid.UUID | None] = mapped_column(
        Uuid,
        ForeignKey("pickup_requests.id", ondelete="CASCADE"),
        nullable=True,
        index=True,
    )
    order_id: Mapped[uuid.UUID | None] = mapped_column(
        Uuid,
        ForeignKey("orders.id", ondelete="RESTRICT"),
        nullable=True,
        index=True,
    )
    courier_user_id: Mapped[uuid.UUID | None] = mapped_column(
        Uuid,
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    scheduled_start_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    scheduled_end_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    status: Mapped[str] = mapped_column(
        String(30),
        default=DeliveryTaskStatus.PENDING.value,
        nullable=False,
        index=True,
    )
    recipient_name: Mapped[str | None] = mapped_column(String(150), nullable=True)
    destination_address: Mapped[str] = mapped_column(Text, nullable=False)
    destination_phone: Mapped[str | None] = mapped_column(String(20), nullable=True)
    proof_photo_path: Mapped[str | None] = mapped_column(Text, nullable=True)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    failure_reason: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_by: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        ForeignKey("users.id", ondelete="RESTRICT"),
        nullable=False,
    )

    __table_args__ = (
        CheckConstraint(
            "(task_type = 'PICKUP' AND pickup_request_id IS NOT NULL AND order_id IS NULL) OR "
            "(task_type = 'DELIVERY' AND order_id IS NOT NULL AND pickup_request_id IS NULL)",
            name="chk_delivery_tasks_type_target",
        ),
        Index("ix_delivery_tasks_courier_status", "courier_user_id", "status"),
    )

    # Relationships
    business: Mapped["Business"] = relationship("Business", lazy="select")
    pickup_request: Mapped["PickupRequest | None"] = relationship(
        "PickupRequest",
        back_populates="delivery_tasks",
    )
    order: Mapped["Order | None"] = relationship("Order", lazy="select")
    courier: Mapped["User | None"] = relationship("User", foreign_keys=[courier_user_id], lazy="select")
    creator: Mapped["User"] = relationship("User", foreign_keys=[created_by], lazy="select")
    status_history: Mapped[list["DeliveryStatusHistory"]] = relationship(
        "DeliveryStatusHistory",
        back_populates="delivery_task",
        cascade="all, delete-orphan",
        order_by="DeliveryStatusHistory.created_at",
    )
    order_handoff: Mapped["OrderHandoff | None"] = relationship(
        "OrderHandoff",
        back_populates="delivery_task",
        uselist=False,
    )


class DeliveryStatusHistory(Base):
    """
    Delivery Status History (BSD.md §22).
    Tracks every status change of a courier pickup or delivery task.
    """
    __tablename__ = "delivery_status_history"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    delivery_task_id: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        ForeignKey("delivery_tasks.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    from_status: Mapped[str | None] = mapped_column(String(30), nullable=True)
    to_status: Mapped[str] = mapped_column(String(30), nullable=False)
    changed_by: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        ForeignKey("users.id", ondelete="RESTRICT"),
        nullable=False,
    )
    reason: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    # Relationships
    delivery_task: Mapped["DeliveryTask"] = relationship(
        "DeliveryTask",
        back_populates="status_history",
    )
    user: Mapped["User"] = relationship("User", lazy="select")
