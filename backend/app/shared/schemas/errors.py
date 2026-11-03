from typing import Any

from pydantic import BaseModel, Field


class ErrorDetail(BaseModel):
    field: str | None = None
    issue: str
    location: str | None = None


class ErrorBody(BaseModel):
    code: str = Field(description="Stable machine-readable error code")
    message: str = Field(description="Human readable explanation")
    details: list[ErrorDetail] | list[dict[str, Any]] | None = None


class ErrorResponse(BaseModel):
    error: ErrorBody
    request_id: str
