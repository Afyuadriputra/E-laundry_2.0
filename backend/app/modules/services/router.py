import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.orm import Session

from app.core.permissions import require_owner, require_staff_or_above
from app.db.session import get_db
from app.modules.auth.dependencies import verify_csrf
from app.modules.services.schemas import ServiceCreate, ServiceResponse, ServiceUpdate
from app.modules.services.service import ServiceCatalogService
from app.modules.users.models import User
from app.shared.schemas.responses import StandardResponse

router = APIRouter(prefix="/services", tags=["Services"])


@router.get("", response_model=StandardResponse[list[ServiceResponse]])
def list_services(
    request: Request,
    current_user: Annotated[User, Depends(require_staff_or_above)],
    db: Annotated[Session, Depends(get_db)],
    is_active: bool | None = Query(None, description="Filter status aktif"),
) -> StandardResponse[list[ServiceResponse]]:
    services = ServiceCatalogService.list_services(
        db=db,
        business_id=current_user.business_id,
        is_active=is_active,
    )
    return StandardResponse(
        data=[ServiceResponse.model_validate(s) for s in services],
        meta={"total": len(services)},
        request_id=getattr(request.state, "request_id", ""),
    )


@router.get("/{service_id}", response_model=StandardResponse[ServiceResponse])
def get_service(
    request: Request,
    service_id: uuid.UUID,
    current_user: Annotated[User, Depends(require_staff_or_above)],
    db: Annotated[Session, Depends(get_db)],
) -> StandardResponse[ServiceResponse]:
    service = ServiceCatalogService.get_by_id(db, current_user.business_id, service_id)
    return StandardResponse(
        data=ServiceResponse.model_validate(service),
        request_id=getattr(request.state, "request_id", ""),
    )


@router.post(
    "",
    response_model=StandardResponse[ServiceResponse],
    dependencies=[Depends(verify_csrf)],
)
def create_service(
    request: Request,
    data: ServiceCreate,
    current_user: Annotated[User, Depends(require_owner)],
    db: Annotated[Session, Depends(get_db)],
) -> StandardResponse[ServiceResponse]:
    service = ServiceCatalogService.create_service(db, current_user.business_id, data)
    return StandardResponse(
        data=ServiceResponse.model_validate(service),
        request_id=getattr(request.state, "request_id", ""),
    )


@router.put(
    "/{service_id}",
    response_model=StandardResponse[ServiceResponse],
    dependencies=[Depends(verify_csrf)],
)
def update_service(
    request: Request,
    service_id: uuid.UUID,
    data: ServiceUpdate,
    current_user: Annotated[User, Depends(require_owner)],
    db: Annotated[Session, Depends(get_db)],
) -> StandardResponse[ServiceResponse]:
    service = ServiceCatalogService.update_service(db, current_user.business_id, service_id, data)
    return StandardResponse(
        data=ServiceResponse.model_validate(service),
        request_id=getattr(request.state, "request_id", ""),
    )

