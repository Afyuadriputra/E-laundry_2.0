import re
import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator


def normalize_phone_e164(v: str) -> str:
    """Normalize phone number to E.164 format (+62...)."""
    cleaned = re.sub(r"[^\d+]", "", v.strip())
    if cleaned.startswith("+"):
        digits = cleaned[1:]
    elif cleaned.startswith("0"):
        digits = "62" + cleaned[1:]
    elif cleaned.startswith("62"):
        digits = cleaned
    else:
        digits = "62" + cleaned

    if not digits.isdigit() or len(digits) < 9 or len(digits) > 15:
        raise ValueError("Format nomor telepon tidak valid untuk format internasional E.164.")
    return f"+{digits}"


class CustomerBase(BaseModel):
    full_name: str = Field(..., min_length=2, max_length=150, description="Nama lengkap pelanggan")
    phone_e164: str = Field(..., description="Nomor WhatsApp/telepon pelanggan")
    address: str | None = Field(default=None, description="Alamat pelanggan")
    notes: str | None = Field(default=None, description="Catatan khusus pelanggan")

    @field_validator("phone_e164")
    @classmethod
    def validate_phone(cls, v: str) -> str:
        return normalize_phone_e164(v)


class CustomerCreate(CustomerBase):
    pass


class CustomerUpdate(BaseModel):
    full_name: str | None = Field(default=None, min_length=2, max_length=150)
    phone_e164: str | None = Field(default=None)
    address: str | None = Field(default=None)
    notes: str | None = Field(default=None)
    is_active: bool | None = Field(default=None)

    @field_validator("phone_e164")
    @classmethod
    def validate_phone(cls, v: str | None) -> str | None:
        if v is None:
            return None
        return normalize_phone_e164(v)


class CustomerResponse(CustomerBase):
    id: uuid.UUID
    business_id: uuid.UUID
    is_active: bool
    created_at: datetime
    updated_at: datetime
    total_orders: int = 0

    model_config = ConfigDict(from_attributes=True)

