import logging

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError

from app.core.exceptions import AppException
from app.middleware.request_id import request_id_ctx_var

logger = logging.getLogger(__name__)


def _get_request_id(request: Request) -> str:
    req_id = getattr(request.state, "request_id", None)
    if not req_id:
        req_id = request_id_ctx_var.get()
    return req_id or ""


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(AppException)
    async def app_exception_handler(request: Request, exc: AppException) -> JSONResponse:
        req_id = _get_request_id(request)
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": {
                    "code": exc.code,
                    "message": exc.message,
                    "details": exc.details,
                },
                "request_id": req_id,
            },
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request, exc: RequestValidationError
    ) -> JSONResponse:
        req_id = _get_request_id(request)
        details = []
        for err in exc.errors():
            loc = ".".join(str(x) for x in err.get("loc", []))
            details.append(
                {
                    "field": loc,
                    "issue": err.get("msg", "Invalid input"),
                    "location": err.get("type", None),
                }
            )

        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "error": {
                    "code": "VALIDATION_ERROR",
                    "message": "Input tidak valid",
                    "details": details,
                },
                "request_id": req_id,
            },
        )

    @app.exception_handler(SQLAlchemyError)
    async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError) -> JSONResponse:
        req_id = _get_request_id(request)
        logger.error(f"Database exception caught on request [{req_id}]: {str(exc)}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "error": {
                    "code": "INTERNAL_ERROR",
                    "message": "Terjadi kesalahan internal pada database",
                    "details": None,
                },
                "request_id": req_id,
            },
        )

    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception) -> JSONResponse:
        req_id = _get_request_id(request)
        logger.exception(f"Unhandled exception caught on request [{req_id}]: {str(exc)}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "error": {
                    "code": "INTERNAL_ERROR",
                    "message": "Terjadi kesalahan internal pada server",
                    "details": None,
                },
                "request_id": req_id,
            },
        )
