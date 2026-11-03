from typing import Any

from pydantic import BaseModel, Field


class StandardResponse[T](BaseModel):
    data: T
    meta: dict[str, Any] | None = None
    request_id: str = Field(default="", description="Request tracing identifier")
