import uuid
from datetime import datetime
from enum import StrEnum
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field

from app.modules.payments.domain.balance import PaymentStatus


class PaymentMethod(StrEnum):
    CASH = "CASH"
    BANK_TRANSFER = "BANK_TRANSFER"
    QRIS_MANUAL = "QRIS_MANUAL"


class PaymentCreate(BaseModel):
    amount: Annotated[int, Field(gt=0, description="Nominal pembayaran dalam rupiah (> 0)")]
    method: PaymentMethod
    reference_note: Annotated[str | None, Field(max_length=255, default=None)]


class PaymentVoidCreate(BaseModel):
    reason: Annotated[str, Field(min_length=3, max_length=500, description="Alasan pembatalan")]


class PaymentRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    order_id: uuid.UUID
    amount: int
    method: str
    verification_status: str
    payment_time: datetime
    verified_by: uuid.UUID
    verified_by_name: str | None = None
    verified_at: datetime
    reference_note: str | None = None
    created_at: datetime
    is_voided: bool = False
    void_reason: str | None = None
    voided_at: datetime | None = None
    voided_by_name: str | None = None


class OrderPaymentSummary(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    order_id: uuid.UUID
    order_number: str
    total_amount: int
    total_paid: int
    remaining_amount: int
    payment_status: PaymentStatus
    payments: list[PaymentRead]
