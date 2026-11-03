import uuid
from datetime import date, datetime
from enum import StrEnum
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field


class ExpenseCategory(StrEnum):
    DETERGENT = "DETERGENT"
    FRAGRANCE = "FRAGRANCE"
    PACKAGING = "PACKAGING"
    ELECTRICITY = "ELECTRICITY"
    WATER = "WATER"
    TRANSPORT = "TRANSPORT"
    EQUIPMENT_MAINTENANCE = "EQUIPMENT_MAINTENANCE"
    OTHER = "OTHER"


class ExpenseCreate(BaseModel):
    category: ExpenseCategory
    amount: Annotated[int, Field(gt=0, description="Nominal pengeluaran dalam rupiah (> 0)")]
    expense_date: date
    description: Annotated[str | None, Field(max_length=500, default=None)]


class ExpenseUpdate(BaseModel):
    category: ExpenseCategory | None = None
    amount: Annotated[int | None, Field(gt=0, default=None)]
    expense_date: date | None = None
    description: Annotated[str | None, Field(max_length=500, default=None)]


class ExpenseRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    business_id: uuid.UUID
    category: str
    amount: int
    expense_date: date
    description: str | None = None
    created_by: uuid.UUID
    created_by_name: str | None = None
    created_at: datetime
    updated_at: datetime
