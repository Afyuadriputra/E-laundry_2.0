from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.permissions import require_any_authenticated, require_owner
from app.db.session import get_db
from app.modules.auth.dependencies import verify_csrf
from app.modules.businesses.schemas import (
    BusinessRead,
    BusinessSettingsRead,
    BusinessSettingsUpdate,
    BusinessUpdate,
)
from app.modules.businesses.service import BusinessService
from app.modules.users.models import User
from app.shared.schemas.responses import StandardResponse

business_router = APIRouter(prefix="/business", tags=["Business Profile"])
settings_router = APIRouter(prefix="/settings", tags=["Business Settings"])


@business_router.get("", response_model=StandardResponse[BusinessRead])
def get_business(
    current_user: Annotated[User, Depends(require_any_authenticated)],
    db: Annotated[Session, Depends(get_db)],
) -> StandardResponse[BusinessRead]:
    """Get business profile for the current user's business."""
    b = BusinessService.get_business(db, current_user.business_id)
    return StandardResponse(
        data=BusinessRead(
            id=b.id,
            name=b.name,
            phone_e164=b.phone_e164,
            address=b.address,
            logo_path=b.logo_path,
            timezone=b.timezone,
            is_active=b.is_active,
            created_at=b.created_at,
            updated_at=b.updated_at,
        )
    )


@business_router.patch(
    "",
    response_model=StandardResponse[BusinessRead],
    dependencies=[Depends(verify_csrf)],
)
def update_business(
    payload: BusinessUpdate,
    current_user: Annotated[User, Depends(require_owner)],
    db: Annotated[Session, Depends(get_db)],
) -> StandardResponse[BusinessRead]:
    """Update business profile (Owner only)."""
    b = BusinessService.update_business(db, current_user.business_id, payload)
    return StandardResponse(
        data=BusinessRead(
            id=b.id,
            name=b.name,
            phone_e164=b.phone_e164,
            address=b.address,
            logo_path=b.logo_path,
            timezone=b.timezone,
            is_active=b.is_active,
            created_at=b.created_at,
            updated_at=b.updated_at,
        )
    )


@settings_router.get("", response_model=StandardResponse[BusinessSettingsRead])
def get_settings(
    current_user: Annotated[User, Depends(require_any_authenticated)],
    db: Annotated[Session, Depends(get_db)],
) -> StandardResponse[BusinessSettingsRead]:
    """Get operational settings for the current user's business."""
    s = BusinessService.get_settings(db, current_user.business_id)
    return StandardResponse(
        data=BusinessSettingsRead(
            id=s.id,
            business_id=s.business_id,
            pickup_enabled=s.pickup_enabled,
            delivery_enabled=s.delivery_enabled,
            default_delivery_fee=s.default_delivery_fee,
            default_completion_hours=s.default_completion_hours,
            weight_precision=s.weight_precision,
            weight_rounding_mode=s.weight_rounding_mode,
            operating_hours=s.operating_hours,
            updated_by=s.updated_by,
            updated_at=s.updated_at,
        )
    )


@settings_router.patch(
    "",
    response_model=StandardResponse[BusinessSettingsRead],
    dependencies=[Depends(verify_csrf)],
)
def update_settings(
    payload: BusinessSettingsUpdate,
    current_user: Annotated[User, Depends(require_owner)],
    db: Annotated[Session, Depends(get_db)],
) -> StandardResponse[BusinessSettingsRead]:
    """Update operational settings (Owner only)."""
    s = BusinessService.update_settings(
        db,
        business_id=current_user.business_id,
        user_id=current_user.id,
        payload=payload,
    )
    return StandardResponse(
        data=BusinessSettingsRead(
            id=s.id,
            business_id=s.business_id,
            pickup_enabled=s.pickup_enabled,
            delivery_enabled=s.delivery_enabled,
            default_delivery_fee=s.default_delivery_fee,
            default_completion_hours=s.default_completion_hours,
            weight_precision=s.weight_precision,
            weight_rounding_mode=s.weight_rounding_mode,
            operating_hours=s.operating_hours,
            updated_by=s.updated_by,
            updated_at=s.updated_at,
        )
    )
