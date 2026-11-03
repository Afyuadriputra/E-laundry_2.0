import uuid
from datetime import date, datetime, time
from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, Field, field_validator


class PublicPickupRequestCreate(BaseModel):
    requester_name: str = Field(min_length=2, max_length=150)
    phone_e164: str = Field(min_length=8, max_length=20)
    pickup_address: str = Field(min_length=5)
    requested_date: date
    requested_time_start: time
    requested_time_end: time
    notes: str | None = Field(default=None, max_length=500)

    @field_validator("requested_time_end")
    @classmethod
    def validate_time_window(cls, v: time, info) -> time:
        start = info.data.get("requested_time_start")
        if start and v <= start:
            raise ValueError("Waktu akhir penjemputan harus lebih besar dari waktu mulai.")
        return v


class PickupConfirmPayload(BaseModel):
    confirmed_start_at: datetime
    confirmed_end_at: datetime
    courier_user_id: uuid.UUID | None = None
    notes: str | None = None

    @field_validator("confirmed_end_at")
    @classmethod
    def validate_window(cls, v: datetime, info) -> datetime:
        start = info.data.get("confirmed_start_at")
        if start and v <= start:
            raise ValueError("Waktu konfirmasi akhir harus lebih besar dari waktu mulai.")
        return v


class PickupRejectPayload(BaseModel):
    rejection_reason: str = Field(min_length=3, max_length=500)


class PickupConvertToOrderPayload(BaseModel):
    """
    Atomic conversion of a completed pickup into an official laundry Order (DEC-10).
    """
    service_id: uuid.UUID
    quantity: Decimal = Field(gt=Decimal("0"))
    extra_charge_amount: int = Field(default=0, ge=0)
    delivery_fee_amount: int = Field(default=0, ge=0)
    return_method: Literal["SELF_PICKUP", "HOME_DELIVERY"] = "SELF_PICKUP"
    customer_notes: str | None = None
    internal_notes: str | None = None


class PickupRequestRead(BaseModel):
    id: uuid.UUID
    business_id: uuid.UUID
    customer_id: uuid.UUID | None = None
    request_number: str
    requester_name: str
    phone_e164: str
    pickup_address: str
    requested_date: date
    requested_time_start: time
    requested_time_end: time
    confirmed_start_at: datetime | None = None
    confirmed_end_at: datetime | None = None
    status: str
    notes: str | None = None
    rejection_reason: str | None = None
    created_at: datetime
    updated_at: datetime
    tracking_token: str | None = None
    tracking_url: str | None = None


class DeliveryTaskCreate(BaseModel):
    task_type: Literal["PICKUP", "DELIVERY"]
    pickup_request_id: uuid.UUID | None = None
    order_id: uuid.UUID | None = None
    courier_user_id: uuid.UUID | None = None
    scheduled_start_at: datetime | None = None
    scheduled_end_at: datetime | None = None
    recipient_name: str | None = None
    destination_address: str = Field(min_length=5)
    destination_phone: str | None = None


class DeliveryTaskStatusUpdate(BaseModel):
    to_status: Literal["ASSIGNED", "EN_ROUTE", "ARRIVED", "COMPLETED", "FAILED", "CANCELLED"]
    failure_reason: str | None = None
    proof_photo_path: str | None = None
    received_by_name: str | None = None
    notes: str | None = None


class DeliveryStatusHistoryRead(BaseModel):
    id: uuid.UUID
    from_status: str | None
    to_status: str
    changed_by_name: str | None = None
    reason: str | None = None
    created_at: datetime


class DeliveryTaskRead(BaseModel):
    id: uuid.UUID
    business_id: uuid.UUID
    task_type: str
    pickup_request_id: uuid.UUID | None = None
    order_id: uuid.UUID | None = None
    order_number: str | None = None
    courier_user_id: uuid.UUID | None = None
    courier_name: str | None = None
    scheduled_start_at: datetime | None = None
    scheduled_end_at: datetime | None = None
    status: str
    recipient_name: str | None = None
    destination_address: str
    destination_phone: str | None = None
    proof_photo_path: str | None = None
    completed_at: datetime | None = None
    failure_reason: str | None = None
    created_at: datetime
    updated_at: datetime
    history: list[DeliveryStatusHistoryRead] = Field(default_factory=list)
