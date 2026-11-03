import uuid
from typing import Annotated

from fastapi import APIRouter, Body, Depends, Query, Request
from sqlalchemy.orm import Session

from app.core.permissions import require_owner_or_cashier, require_staff_or_above
from app.db.session import get_db
from app.modules.auth.dependencies import verify_csrf
from app.modules.customers.schemas import CustomerResponse
from app.modules.orders.domain.state_machine import OperationalStatus
from app.modules.orders.models import Order
from app.modules.orders.schemas import (
    OrderCreate,
    OrderDetailResponse,
    OrderHandoffResponse,
    OrderItemResponse,
    OrderListItemResponse,
    OrderStatusHistoryResponse,
    OrderStatusTransitionRequest,
)
from app.modules.orders.service import OrderService
from app.modules.users.models import User
from app.shared.schemas.responses import StandardResponse

router = APIRouter(prefix="/orders", tags=["Orders"])


def _to_list_item(order: Order) -> OrderListItemResponse:
    return OrderListItemResponse(
        id=order.id,
        business_id=order.business_id,
        order_number=order.order_number,
        customer_id=order.customer_id,
        customer_name=order.customer.full_name if order.customer else "-",
        customer_phone=order.customer.phone_e164 if order.customer else "-",
        operational_status=order.operational_status,
        intake_method=order.intake_method,
        return_method=order.return_method,
        total_amount=order.total_amount,
        subtotal_amount=order.subtotal_amount,
        extra_charge_amount=order.extra_charge_amount,
        delivery_fee_amount=order.delivery_fee_amount,
        estimated_completion_at=order.estimated_completion_at,
        version=order.version,
        created_at=order.created_at,
        updated_at=order.updated_at,
        completed_at=order.completed_at,
        cancelled_at=order.cancelled_at,
    )


def _to_detail(order: Order) -> OrderDetailResponse:
    return OrderDetailResponse(
        id=order.id,
        business_id=order.business_id,
        order_number=order.order_number,
        customer_id=order.customer_id,
        customer_name=order.customer.full_name if order.customer else "-",
        customer_phone=order.customer.phone_e164 if order.customer else "-",
        operational_status=order.operational_status,
        intake_method=order.intake_method,
        return_method=order.return_method,
        total_amount=order.total_amount,
        subtotal_amount=order.subtotal_amount,
        extra_charge_amount=order.extra_charge_amount,
        delivery_fee_amount=order.delivery_fee_amount,
        estimated_completion_at=order.estimated_completion_at,
        version=order.version,
        created_at=order.created_at,
        updated_at=order.updated_at,
        completed_at=order.completed_at,
        cancelled_at=order.cancelled_at,
        customer=CustomerResponse.model_validate(order.customer),
        items=[OrderItemResponse.model_validate(item) for item in order.items],
        status_history=[
            OrderStatusHistoryResponse.model_validate(hist) for hist in order.status_history
        ],
        handoff=(OrderHandoffResponse.model_validate(order.handoff) if order.handoff else None),
        customer_notes=order.customer_notes,
        internal_notes=order.internal_notes,
        cancellation_reason=order.cancellation_reason,
    )


@router.post(
    "",
    response_model=StandardResponse[OrderDetailResponse],
    dependencies=[Depends(verify_csrf)],
)
def create_order(
    request: Request,
    data: OrderCreate,
    current_user: Annotated[User, Depends(require_owner_or_cashier)],
    db: Annotated[Session, Depends(get_db)],
) -> StandardResponse[OrderDetailResponse]:
    order = OrderService.create_order(
        db=db,
        business_id=current_user.business_id,
        user_id=current_user.id,
        data=data,
    )
    # Refresh to load full relationships for detail
    detailed = OrderService.get_by_id(db, current_user.business_id, order.id)
    return StandardResponse(
        data=_to_detail(detailed),
        request_id=getattr(request.state, "request_id", ""),
    )


@router.get("", response_model=StandardResponse[list[OrderListItemResponse]])
def list_orders(
    request: Request,
    current_user: Annotated[User, Depends(require_staff_or_above)],
    db: Annotated[Session, Depends(get_db)],
    operational_status: str | None = Query(None, description="Filter status operasional"),
    customer_id: uuid.UUID | None = Query(None, description="Filter ID pelanggan"),
    search: str | None = Query(None, description="Cari nomor nota atau data pelanggan"),
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
) -> StandardResponse[list[OrderListItemResponse]]:
    orders, total = OrderService.list_orders(
        db=db,
        business_id=current_user.business_id,
        operational_status=operational_status,
        customer_id=customer_id,
        search=search,
        limit=limit,
        offset=offset,
    )
    return StandardResponse(
        data=[_to_list_item(o) for o in orders],
        meta={"total": total, "limit": limit, "offset": offset},
        request_id=getattr(request.state, "request_id", ""),
    )


@router.get("/{order_id}", response_model=StandardResponse[OrderDetailResponse])
def get_order(
    request: Request,
    order_id: uuid.UUID,
    current_user: Annotated[User, Depends(require_staff_or_above)],
    db: Annotated[Session, Depends(get_db)],
) -> StandardResponse[OrderDetailResponse]:
    order = OrderService.get_by_id(db, current_user.business_id, order_id)
    return StandardResponse(
        data=_to_detail(order),
        request_id=getattr(request.state, "request_id", ""),
    )


@router.post(
    "/{order_id}/transition",
    response_model=StandardResponse[OrderDetailResponse],
    dependencies=[Depends(verify_csrf)],
)
def transition_order_status(
    request: Request,
    order_id: uuid.UUID,
    body: OrderStatusTransitionRequest,
    current_user: Annotated[User, Depends(require_staff_or_above)],
    db: Annotated[Session, Depends(get_db)],
) -> StandardResponse[OrderDetailResponse]:
    updated_order = OrderService.transition_status(
        db=db,
        business_id=current_user.business_id,
        user_id=current_user.id,
        order_id=order_id,
        request=body,
    )
    return StandardResponse(
        data=_to_detail(updated_order),
        request_id=getattr(request.state, "request_id", ""),
    )


@router.post(
    "/{order_id}/cancel",
    response_model=StandardResponse[OrderDetailResponse],
    dependencies=[Depends(verify_csrf)],
)
def cancel_order(
    request: Request,
    order_id: uuid.UUID,
    cancellation_reason: Annotated[str, Body(embed=True)],
    expected_version: Annotated[int, Body(embed=True)],
    current_user: Annotated[User, Depends(require_owner_or_cashier)],
    db: Annotated[Session, Depends(get_db)],
) -> StandardResponse[OrderDetailResponse]:
    req = OrderStatusTransitionRequest(
        to_status=OperationalStatus.CANCELLED,
        reason=cancellation_reason,
        cancellation_reason=cancellation_reason,
        expected_version=expected_version,
    )
    updated_order = OrderService.transition_status(
        db=db,
        business_id=current_user.business_id,
        user_id=current_user.id,
        order_id=order_id,
        request=req,
    )
    return StandardResponse(
        data=_to_detail(updated_order),
        request_id=getattr(request.state, "request_id", ""),
    )
