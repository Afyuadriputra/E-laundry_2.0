import logging
from typing import Annotated, Any

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.db.session import get_db

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/health", tags=["health"])


@router.get(
    "/live",
    status_code=status.HTTP_200_OK,
    summary="Liveness Probe",
    description="Memastikan proses server API berjalan aktif.",
)
def liveness() -> dict[str, str]:
    return {"status": "alive"}


@router.get(
    "/ready",
    summary="Readiness Probe",
    description="Memeriksa kesiapan API dan konektivitas database.",
)
def readiness(db: Annotated[Session, Depends(get_db)]) -> Any:
    try:
        db.execute(text("SELECT 1"))
        return {
            "status": "ready",
            "database": "connected",
        }
    except Exception as exc:
        logger.warning(f"Readiness check failed: {exc}")
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={
                "status": "not_ready",
                "database": "disconnected",
                "error": "Database connection unavailable",
            },
        )
