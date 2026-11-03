from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


class ServiceItemSummary(BaseModel):
    service_name: str
    quantity: str
    unit: str
    unit_price: int
    line_total: int


class FinancialSummary(BaseModel):
    total_amount: int
    paid_amount: int
    remaining_amount: int
    payment_status: str


class TimelineEvent(BaseModel):
    status: str
    status_label: str
    timestamp: datetime
    note: str | None = None


class BusinessContact(BaseModel):
    name: str
    phone: str
    address: str
    whatsapp_url: str


class PublicTrackingRead(BaseModel):
    """
    Public Tracking Read model (BSD.md §28.8 & §34.3).
    Strict allowlist for customer tracking without authentication.
    PII is masked; internal audit notes, staff passwords, and sensitive costs are omitted.
    """
    tracking_type: Literal["ORDER", "PICKUP_REQUEST"]
    order_number: str | None = None
    current_status: str
    status_label: str
    can_cancel: bool
    created_at: datetime
    estimated_completion_at: datetime | None = None
    customer_name_masked: str
    customer_phone_masked: str
    service_summary: list[ServiceItemSummary] = Field(default_factory=list)
    financial_summary: FinancialSummary
    timeline: list[TimelineEvent] = Field(default_factory=list)
    business_contact: BusinessContact
    intake_method: str | None = None
    return_method: str | None = None


class CancelTrackingOrderRequest(BaseModel):
    reason: str | None = Field(default=None, max_length=255)


class PublicCancellationResponse(BaseModel):
    success: bool = True
    order_number: str
    new_status: str = "CANCELLED"
    message: str
    cancelled_at: datetime
