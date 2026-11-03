import uuid
from datetime import datetime
from decimal import Decimal
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.modules.customers.schemas import CustomerResponse
from app.modules.orders.domain.state_machine import OperationalStatus


class IntakeMethod(StrEnum):
    DROP_OFF = "DROP_OFF"
    COURIER_PICKUP = "COURIER_PICKUP"


class ReturnMethod(StrEnum):
    SELF_PICKUP = "SELF_PICKUP"
    HOME_DELIVERY = "HOME_DELIVERY"


class OrderItemCreate(BaseModel):
    service_id: uuid.UUID = Field(..., description="ID layanan yang dipilih")
    quantity: Decimal = Field(
        ..., gt=0, description="Kuantitas (kg untuk kiloan, pcs untuk satuan)"
    )

    @field_validator("quantity")
    @classmethod
    def validate_positive(cls, v: Decimal) -> Decimal:
        if v <= Decimal(0):
            raise ValueError("Kuantitas harus lebih besar dari 0.")
        return v


class OrderCreate(BaseModel):
    customer_id: uuid.UUID | None = Field(
        default=None,
        description="ID pelanggan terdaftar (opsional jika mengisi data pelanggan baru)",
    )
    # Inline new customer fields if customer_id not provided
    new_customer_name: str | None = Field(default=None, description="Nama pelanggan baru")
    new_customer_phone: str | None = Field(
        default=None, description="Nomor WhatsApp pelanggan baru"
    )
    new_customer_address: str | None = Field(default=None, description="Alamat pelanggan baru")

    items: list[OrderItemCreate] = Field(..., min_length=1, description="Daftar item cucian")
    intake_method: IntakeMethod = Field(default=IntakeMethod.DROP_OFF)
    return_method: ReturnMethod = Field(default=ReturnMethod.SELF_PICKUP)
    extra_charge_amount: int = Field(default=0, ge=0, description="Biaya tambahan (Rupiah)")
    delivery_fee_amount: int = Field(default=0, ge=0, description="Biaya ongkir/kurir (Rupiah)")
    estimated_completion_at: datetime | None = Field(
        default=None,
        description="Estimasi selesai (default: kalkulasi otomatis berdasarkan layanan)",
    )
    customer_notes: str | None = Field(default=None)
    internal_notes: str | None = Field(default=None)


class OrderStatusTransitionRequest(BaseModel):
    to_status: OperationalStatus = Field(..., description="Status operasional tujuan")
    reason: str | None = Field(default=None, description="Alasan transisi (opsional)")
    cancellation_reason: str | None = Field(
        default=None, description="Wajib jika to_status == CANCELLED"
    )
    expected_version: int = Field(
        ..., description="Versi record saat dibaca untuk optimistic locking"
    )


class OrderItemResponse(BaseModel):
    id: uuid.UUID
    service_id: uuid.UUID
    service_name_snapshot: str
    pricing_type_snapshot: str
    unit_snapshot: str
    quantity: Decimal
    unit_price_snapshot: int
    line_total_amount: int
    requires_ironing_snapshot: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class OrderStatusHistoryResponse(BaseModel):
    id: uuid.UUID
    from_status: str | None
    to_status: str
    changed_by: uuid.UUID
    reason: str | None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class OrderHandoffResponse(BaseModel):
    id: uuid.UUID
    handoff_method: str
    received_by_name: str | None
    confirmed_by_user_id: uuid.UUID
    confirmed_at: datetime
    notes: str | None

    model_config = ConfigDict(from_attributes=True)


class OrderListItemResponse(BaseModel):
    id: uuid.UUID
    business_id: uuid.UUID
    order_number: str
    customer_id: uuid.UUID
    customer_name: str
    customer_phone: str
    operational_status: str
    intake_method: str
    return_method: str
    total_amount: int
    subtotal_amount: int
    extra_charge_amount: int
    delivery_fee_amount: int
    estimated_completion_at: datetime
    version: int
    created_at: datetime
    updated_at: datetime
    completed_at: datetime | None
    cancelled_at: datetime | None

    model_config = ConfigDict(from_attributes=True)


class OrderDetailResponse(OrderListItemResponse):
    customer: CustomerResponse
    items: list[OrderItemResponse]
    status_history: list[OrderStatusHistoryResponse]
    handoff: OrderHandoffResponse | None
    customer_notes: str | None
    internal_notes: str | None
    cancellation_reason: str | None

    model_config = ConfigDict(from_attributes=True)
