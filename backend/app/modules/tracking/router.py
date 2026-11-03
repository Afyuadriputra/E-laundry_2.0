from typing import Annotated

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.modules.tracking.schemas import (
    CancelTrackingOrderRequest,
    PublicCancellationResponse,
    PublicTrackingRead,
)
from app.modules.tracking.service import TrackingService
from app.shared.schemas.responses import StandardResponse

router = APIRouter(prefix="/tracking", tags=["Public Customer Tracking"])


@router.get(
    "/{token}",
    response_model=StandardResponse[PublicTrackingRead],
    summary="Get public order tracking data (no login required)",
    description=(
        "Public allowlist read model for customer order tracking. "
        "PII is masked, internal cashier credentials and notes are excluded. "
        "Enforces Cache-Control: no-store and Referrer-Policy: no-referrer."
    ),
)
def get_public_tracking(
    token: str,
    response: Response,
    db: Annotated[Session, Depends(get_db)],
) -> StandardResponse[PublicTrackingRead]:
    # Set privacy and caching security headers per BSD §34.4
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Referrer-Policy"] = "no-referrer"

    tracking_data = TrackingService.get_public_tracking_data(db, token)
    return StandardResponse(data=tracking_data)


@router.post(
    "/{token}/cancel",
    response_model=StandardResponse[PublicCancellationResponse],
    status_code=status.HTTP_200_OK,
    summary="Cancel order via tracking token (if eligible)",
    description=(
        "Allows a customer to cancel their order if it is in RECEIVED or QUEUED status "
        "and has no recorded payments."
    ),
)
def cancel_public_order(
    token: str,
    payload: CancelTrackingOrderRequest,
    db: Annotated[Session, Depends(get_db)],
) -> StandardResponse[PublicCancellationResponse]:
    result = TrackingService.cancel_order_by_customer(db, token, payload.reason)
    return StandardResponse(data=result)
