import uuid
from datetime import datetime

from sqlalchemy import (
    DateTime,
    Integer,
    String,
    Text,
    UniqueConstraint,
    Uuid,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class IdempotencyRecord(Base):
    """Prevents duplicate execution from network retry / double click according to BSD.md Section 24."""

    __tablename__ = "idempotency_records"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    scope_key: Mapped[str] = mapped_column(String(150), nullable=False)
    operation: Mapped[str] = mapped_column(String(100), nullable=False)
    idempotency_key_hash: Mapped[str] = mapped_column(String(128), nullable=False)
    request_hash: Mapped[str] = mapped_column(String(128), nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False)  # PROCESSING, COMPLETED, FAILED
    response_status_code: Mapped[int | None] = mapped_column(Integer, nullable=True)
    response_reference: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=func.now,
    )
    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    __table_args__ = (
        UniqueConstraint(
            "scope_key",
            "operation",
            "idempotency_key_hash",
            name="uq_idempotency_scope_op_key",
        ),
    )

