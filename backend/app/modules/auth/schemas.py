import uuid

from pydantic import BaseModel, Field


class UserSummary(BaseModel):
    id: uuid.UUID
    username: str
    full_name: str
    role: str
    business_id: uuid.UUID
    phone_e164: str | None = None
    is_active: bool = True


class LoginRequest(BaseModel):
    username: str = Field(min_length=1, max_length=80)
    password: str = Field(min_length=6, max_length=128)


class LoginResponse(BaseModel):
    user: UserSummary
    csrf_token: str


class CsrfResponse(BaseModel):
    csrf_token: str


class ChangePasswordRequest(BaseModel):
    old_password: str = Field(min_length=1)
    new_password: str = Field(min_length=8, max_length=128)


class MessageResponse(BaseModel):
    message: str
