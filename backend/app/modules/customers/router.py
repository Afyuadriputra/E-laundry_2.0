import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.orm import Session

from app.core.permissions import require_owner_or_cashier, require_staff_or_above
from app.db.session import get_db
from app.modules.auth.dependencies import verify_csrf
from app.modules.customers.schemas import (
    CustomerCreate,
    CustomerResponse,
    CustomerUpdate,
)
from app.modules.customers.service import CustomerService
from app.modules.users.models import User
from app.shared.schemas.responses import StandardResponse

router = APIRouter(prefix="/customers", tags=["Customers"])


@router.get("", response_model=StandardResponse[list[CustomerResponse]])
def list_customers(
    request: Request,
    current_user: Annotated[User, Depends(require_staff_or_above)],
    db: Annotated[Session, Depends(get_db)],
    search: str | None = Query(None, description="Cari nama atau nomor WhatsApp"),
    is_active: bool | None = Query(None, description="Filter status aktif"),
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
) -> StandardResponse[list[CustomerResponse]]:
    customers, total = CustomerService.list_customers(
        db=db,
        business_id=current_user.business_id,
        search=search,
        is_active=is_active,
        limit=limit,
        offset=offset,
    )

    items = []
    for c in customers:
        item = CustomerResponse.model_validate(c)
        item.total_orders = CustomerService.get_order_count(db, c.id)
        items.append(item)

    return StandardResponse(
        data=items,
        meta={"total": total, "limit": limit, "offset": offset},
        request_id=getattr(request.state, "request_id", ""),
    )


@router.get("/{customer_id}", response_model=StandardResponse[CustomerResponse])
def get_customer(
    request: Request,
    customer_id: uuid.UUID,
    current_user: Annotated[User, Depends(require_staff_or_above)],
    db: Annotated[Session, Depends(get_db)],
) -> StandardResponse[CustomerResponse]:
    customer = CustomerService.get_by_id(db, current_user.business_id, customer_id)
    response_data = CustomerResponse.model_validate(customer)
    response_data.total_orders = CustomerService.get_order_count(db, customer.id)

    return StandardResponse(
        data=response_data,
        request_id=getattr(request.state, "request_id", ""),
    )


@router.post(
    "",
    response_model=StandardResponse[CustomerResponse],
    dependencies=[Depends(verify_csrf)],
)
def create_customer(
    request: Request,
    data: CustomerCreate,
    current_user: Annotated[User, Depends(require_owner_or_cashier)],
    db: Annotated[Session, Depends(get_db)],
) -> StandardResponse[CustomerResponse]:
    customer = CustomerService.create_customer(db, current_user.business_id, data)
    return StandardResponse(
        data=CustomerResponse.model_validate(customer),
        request_id=getattr(request.state, "request_id", ""),
    )


@router.put(
    "/{customer_id}",
    response_model=StandardResponse[CustomerResponse],
    dependencies=[Depends(verify_csrf)],
)
def update_customer(
    request: Request,
    customer_id: uuid.UUID,
    data: CustomerUpdate,
    current_user: Annotated[User, Depends(require_owner_or_cashier)],
    db: Annotated[Session, Depends(get_db)],
) -> StandardResponse[CustomerResponse]:
    customer = CustomerService.update_customer(db, current_user.business_id, customer_id, data)
    response_data = CustomerResponse.model_validate(customer)
    response_data.total_orders = CustomerService.get_order_count(db, customer.id)

    return StandardResponse(
        data=response_data,
        request_id=getattr(request.state, "request_id", ""),
    )

