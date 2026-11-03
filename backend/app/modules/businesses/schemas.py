import uuid
from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class BusinessRead(BaseModel):
    id: uuid.UUID
    name: str
    phone_e164: str
    address: str
    logo_path: str | None = None
    timezone: str
    is_active: bool
    created_at: datetime
    updated_at: datetime


class BusinessUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=150)
    phone_e164: str | None = Field(default=None, max_length=20)
    address: str | None = None
    logo_path: str | None = None
    timezone: str | None = Field(default=None, max_length=64)


class BusinessSettingsRead(BaseModel):
    id: uuid.UUID
    business_id: uuid.UUID
    pickup_enabled: bool
    delivery_enabled: bool
    default_delivery_fee: int
    default_completion_hours: int
    weight_precision: int
    weight_rounding_mode: str
    operating_hours: dict[str, Any] | None = None
    updated_by: uuid.UUID | None = None
    updated_at: datetime


class BusinessSettingsUpdate(BaseModel):
    pickup_enabled: bool | None = None
    delivery_enabled: bool | None = None
    default_delivery_fee: int | None = Field(default=None, ge=0)
    default_completion_hours: int | None = Field(default=None, gt=0)
    weight_precision: int | None = Field(default=None, ge=0, le=3)
    weight_rounding_mode: str | None = None
    operating_hours: dict[str, Any] | None = None
