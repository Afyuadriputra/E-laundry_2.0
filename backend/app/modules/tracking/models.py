import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import (
    CheckConstraint,
    DateTime,
    ForeignKey,
    String,
    Uuid,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.modules.orders.models import Order
    from app.modules.pickup_delivery.models import PickupRequest
    from app.modules.users.models import User


class TrackingToken(Base):
    """
    Tracking Token Entity (BSD.md §23).
    Provides customers with secure, unauthenticated access to view their order or pickup status.
    Stores only the SHA-256 hash of the random 256-bit URL-safe token.
    Enforces that exactly one resource (order_id OR pickup_request_id) is referenced.
    """
    __tablename__ = "tracking_tokens"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    order_id: Mapped[uuid.UUID | None] = mapped_column(
        Uuid,
        ForeignKey("orders.id", ondelete="CASCADE"),
        nullable=True,
        index=True,
    )
    pickup_request_id: Mapped[uuid.UUID | None] = mapped_column(
        Uuid,
        ForeignKey("pickup_requests.id", ondelete="CASCADE"),
        nullable=True,
        index=True,
    )
    token_hash: Mapped[str] = mapped_column(String(128), unique=True, nullable=False, index=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    revoked_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_by: Mapped[uuid.UUID | None] = mapped_column(
        Uuid,
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
    )

    __table_args__ = (
        CheckConstraint(
            "num_nonnulls(order_id, pickup_request_id) = 1",
            name="chk_tracking_tokens_single_target",
        ),
    )

    # Relationships
    order: Mapped["Order | None"] = relationship("Order", back_populates="tracking_tokens", lazy="joined")
    pickup_request: Mapped["PickupRequest | None"] = relationship(
        "PickupRequest",
        back_populates="tracking_tokens",
        lazy="joined",
    )
    creator: Mapped["User | None"] = relationship("User", lazy="select")
