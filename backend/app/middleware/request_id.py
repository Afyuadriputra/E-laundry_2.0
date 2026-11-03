import contextvars
import uuid
from collections.abc import Awaitable, Callable
from typing import cast

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

request_id_ctx_var: contextvars.ContextVar[str] = contextvars.ContextVar("request_id", default="")


class RequestIdMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        incoming_id = request.headers.get("X-Request-ID")
        req_id = incoming_id if incoming_id else str(uuid.uuid4())

        request.state.request_id = req_id
        token = request_id_ctx_var.set(req_id)

        try:
            response = cast(Response, await call_next(request))
            response.headers["X-Request-ID"] = req_id
            return response
        finally:
            request_id_ctx_var.reset(token)
