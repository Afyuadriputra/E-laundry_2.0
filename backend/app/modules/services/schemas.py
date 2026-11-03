import uuid
from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field


class PricingType(StrEnum):
    PER_KG = "PER_KG"
    PER_ITEM = "PER_ITEM"


class ServiceUnit(StrEnum):
    KG = "KG"
    PCS = "PCS"


class ServiceBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=150, description="Nama layanan laundry")
    pricing_type: PricingType = Field(..., description="Metode tarif: PER_KG atau PER_ITEM")
    unit: ServiceUnit = Field(..., description="Satuan ukuran: KG atau PCS")
    unit_price: int = Field(..., ge=0, description="Tarif per unit dalam Rupiah (integer)")
    estimated_hours: int | None = Field(
        default=None, gt=0, description="Estimasi waktu pengerjaan (jam)"
    )
    requires_ironing: bool = Field(default=False, description="Apakah mencakup proses setrika")


class ServiceCreate(ServiceBase):
    pass


class ServiceUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=150)
    pricing_type: PricingType | None = None
    unit: ServiceUnit | None = None
    unit_price: int | None = Field(default=None, ge=0)
    estimated_hours: int | None = Field(default=None, gt=0)
    requires_ironing: bool | None = None
    is_active: bool | None = None


class ServiceResponse(ServiceBase):
    id: uuid.UUID
    business_id: uuid.UUID
    is_active: bool
    version: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
