import uuid
from datetime import datetime
from typing import TYPE_CHECKING, Any

from sqlalchemy import (
    JSON,
    BigInteger,
    Boolean,
    DateTime,
    ForeignKey,
    Integer,
    SmallInteger,
    String,
    Text,
    Uuid,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.modules.users.models import User


class Business(Base, TimestampMixin):
    __tablename__ = "businesses"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    phone_e164: Mapped[str] = mapped_column(String(20), nullable=False)
    address: Mapped[str] = mapped_column(Text, nullable=False)
    logo_path: Mapped[str | None] = mapped_column(Text, nullable=True)
    timezone: Mapped[str] = mapped_column(String(64), nullable=False, default="Asia/Jakarta")
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    settings: Mapped["BusinessSettings"] = relationship(
        "BusinessSettings",
        back_populates="business",
        uselist=False,
        cascade="all, delete-orphan",
    )
    users: Mapped[list["User"]] = relationship(
        "User",
        back_populates="business",
        cascade="all, delete-orphan",
    )


class BusinessSettings(Base):
    __tablename__ = "business_settings"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    business_id: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        ForeignKey("businesses.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
    )
    pickup_enabled: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    delivery_enabled: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    default_delivery_fee: Mapped[int] = mapped_column(BigInteger, nullable=False, default=5000)
    default_completion_hours: Mapped[int] = mapped_column(Integer, nullable=False, default=48)
    weight_precision: Mapped[int] = mapped_column(SmallInteger, nullable=False, default=1)
    weight_rounding_mode: Mapped[str] = mapped_column(String(32), nullable=False, default="HALF_UP")
    operating_hours: Mapped[dict[str, Any] | None] = mapped_column(JSON, nullable=True)
    updated_by: Mapped[uuid.UUID | None] = mapped_column(
        Uuid,
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    business: Mapped["Business"] = relationship(
        "Business",
        back_populates="settings",
    )
