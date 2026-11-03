import uuid
from datetime import datetime

from pydantic import BaseModel, Field

from app.modules.users.models import UserRole


class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=80)
    full_name: str = Field(min_length=1, max_length=150)
    password: str = Field(min_length=8, max_length=128)
    role: UserRole
    phone_e164: str | None = Field(default=None, max_length=20)


class UserUpdate(BaseModel):
    full_name: str | None = Field(default=None, max_length=150)
    role: UserRole | None = None
    phone_e164: str | None = Field(default=None, max_length=20)
    is_active: bool | None = None


class UserRead(BaseModel):
    id: uuid.UUID
    business_id: uuid.UUID
    username: str
    full_name: str
    role: str
    phone_e164: str | None = None
    is_active: bool
    created_at: datetime
    last_login_at: datetime | None = None
