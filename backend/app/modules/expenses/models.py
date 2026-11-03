import uuid
from datetime import date
from typing import TYPE_CHECKING

from sqlalchemy import (
    BigInteger,
    CheckConstraint,
    Date,
    ForeignKey,
    Index,
    String,
    Text,
    Uuid,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.modules.businesses.models import Business
    from app.modules.users.models import User


class Expense(Base, TimestampMixin):
    """Operational expenses according to BSD.md Section 19."""

    __tablename__ = "expenses"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    business_id: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        ForeignKey("businesses.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    category: Mapped[str] = mapped_column(String(60), nullable=False)
    amount: Mapped[int] = mapped_column(BigInteger, nullable=False)
    expense_date: Mapped[date] = mapped_column(Date, nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_by: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        ForeignKey("users.id", ondelete="RESTRICT"),
        nullable=False,
    )

    __table_args__ = (
        CheckConstraint("amount > 0", name="chk_expenses_amount_positive"),
        Index("idx_expenses_business_date", "business_id", "expense_date"),
    )

    # Relationships
    business: Mapped["Business"] = relationship("Business")
    creator: Mapped["User"] = relationship("User", foreign_keys=[created_by])
