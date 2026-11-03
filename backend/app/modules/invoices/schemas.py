import uuid
from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class InvoiceItemRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    service_name: str
    quantity: Decimal
    unit: str
    unit_price: int
    line_total: int


class InvoicePaymentItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    payment_time: datetime
    method: str
    amount: int


class InvoiceRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    order_id: uuid.UUID
    order_number: str
    created_at: datetime
    estimated_completion_at: datetime
    operational_status: str

    business_name: str
    business_phone: str
    business_address: str

    customer_name: str
    customer_phone: str
    intake_method: str
    return_method: str

    items: list[InvoiceItemRead]
    subtotal_amount: int
    extra_charge_amount: int
    delivery_fee_amount: int
    total_amount: int
    total_paid: int
    remaining_amount: int
    payment_status: str
    payments: list[InvoicePaymentItem]

    customer_notes: str | None = None
    tracking_url: str
    whatsapp_share_url: str
    whatsapp_share_text: str
