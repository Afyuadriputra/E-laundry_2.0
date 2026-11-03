import uuid
from datetime import date, datetime

from pydantic import BaseModel, Field


class DashboardSummaryRead(BaseModel):
    # Operational metrics (Cashier + Owner)
    orders_count_today: int = 0
    active_orders_count: int = 0
    ready_orders_count: int = 0
    completed_orders_today: int = 0
    overdue_orders_count: int = 0

    # Financial KPIs (Owner only; None for Cashier)
    order_value_period: int | None = None
    cash_received_period: int | None = None
    expenses_period: int | None = None
    simple_cash_difference: int | None = None
    outstanding_receivables: int | None = None

    # Filter metadata
    start_date: date
    end_date: date


class OverdueOrderRead(BaseModel):
    order_id: uuid.UUID
    order_number: str
    customer_name: str
    customer_phone: str
    operational_status: str
    estimated_completion_at: datetime
    hours_overdue: float
    total_amount: int
    remaining_amount: int


class OrdersReportItemRead(BaseModel):
    order_id: uuid.UUID
    order_number: str
    created_at: datetime
    customer_name: str
    customer_phone: str
    operational_status: str
    payment_status: str
    total_amount: int
    paid_amount: int
    remaining_amount: int
    items_summary: str


class OrdersReportSummaryRead(BaseModel):
    total_orders: int
    total_amount: int
    total_paid: int
    total_outstanding: int
    items: list[OrdersReportItemRead] = Field(default_factory=list)


class FinancialReportSummaryRead(BaseModel):
    start_date: date
    end_date: date
    total_cash_received: int
    cash_by_method: dict[str, int] = Field(default_factory=dict)
    total_expenses: int
    expenses_by_category: dict[str, int] = Field(default_factory=dict)
    simple_cash_difference: int
    outstanding_receivables: int


class OutstandingBalanceItemRead(BaseModel):
    order_id: uuid.UUID
    order_number: str
    created_at: datetime
    customer_name: str
    customer_phone: str
    total_amount: int
    paid_amount: int
    remaining_amount: int
    payment_status: str
    operational_status: str
