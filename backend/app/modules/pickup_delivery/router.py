import uuid
from datetime import date
from typing import Annotated, Any

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.permissions import require_roles
from app.db.session import get_db
from app.modules.auth.dependencies import get_current_user, verify_csrf
from app.modules.businesses.models import Business
from app.modules.pickup_delivery.models import DeliveryTask, PickupRequest
from app.modules.pickup_delivery.schemas import (
    DeliveryStatusHistoryRead,
    DeliveryTaskCreate,
    DeliveryTaskRead,
    DeliveryTaskStatusUpdate,
    PickupConfirmPayload,
    PickupConvertToOrderPayload,
    PickupRejectPayload,
    PickupRequestRead,
    PublicPickupRequestCreate,
)
from app.modules.pickup_delivery.service import PickupDeliveryService
from app.modules.users.models import User, UserRole
from app.shared.schemas.responses import StandardResponse

router = APIRouter(prefix="/pickup-delivery", tags=["Pickup & Delivery Logistics"])


def _serialize_pickup(pickup: PickupRequest, raw_token: str | None = None) -> PickupRequestRead:
    base_url = settings.allowed_origins_list[0] if settings.allowed_origins_list else "http://localhost:5173"
    tracking_url = f"{base_url}/track/{raw_token}" if raw_token else None

    return PickupRequestRead(
        id=pickup.id,
        business_id=pickup.business_id,
        customer_id=pickup.customer_id,
        request_number=pickup.request_number,
        requester_name=pickup.requester_name,
        phone_e164=pickup.phone_e164,
        pickup_address=pickup.pickup_address,
        requested_date=pickup.requested_date,
        requested_time_start=pickup.requested_time_start,
        requested_time_end=pickup.requested_time_end,
        confirmed_start_at=pickup.confirmed_start_at,
        confirmed_end_at=pickup.confirmed_end_at,
        status=pickup.status,
        notes=pickup.notes,
        rejection_reason=pickup.rejection_reason,
        created_at=pickup.created_at,
        updated_at=pickup.updated_at,
        tracking_token=raw_token,
        tracking_url=tracking_url,
    )


def _serialize_task(task: DeliveryTask) -> DeliveryTaskRead:
    history_reads = [
        DeliveryStatusHistoryRead(
            id=h.id,
            from_status=h.from_status,
            to_status=h.to_status,
            changed_by_name=h.user.full_name if h.user else None,
            reason=h.reason,
            created_at=h.created_at,
        )
        for h in task.status_history
    ]

    return DeliveryTaskRead(
        id=task.id,
        business_id=task.business_id,
        task_type=task.task_type,
        pickup_request_id=task.pickup_request_id,
        order_id=task.order_id,
        order_number=task.order.order_number if task.order else None,
        courier_user_id=task.courier_user_id,
        courier_name=task.courier.full_name if task.courier else None,
        scheduled_start_at=task.scheduled_start_at,
        scheduled_end_at=task.scheduled_end_at,
        status=task.status,
        recipient_name=task.recipient_name,
        destination_address=task.destination_address,
        destination_phone=task.destination_phone,
        proof_photo_path=task.proof_photo_path,
        completed_at=task.completed_at,
        failure_reason=task.failure_reason,
        created_at=task.created_at,
        updated_at=task.updated_at,
        history=history_reads,
    )


# -------------------------------------------------------------
# Public Customer Pickup Intake (No Auth Required)
# -------------------------------------------------------------
@router.post(
    "/requests/public",
    response_model=StandardResponse[PickupRequestRead],
    status_code=status.HTTP_201_CREATED,
    summary="Public pickup intake request (no login required)",
)
def create_public_pickup_request(
    payload: PublicPickupRequestCreate,
    db: Annotated[Session, Depends(get_db)],
    business_id: uuid.UUID | None = Query(default=None),
) -> StandardResponse[PickupRequestRead]:
    if not business_id:
        active_biz = db.query(Business).filter(Business.is_active.is_(True)).first()
        if not active_biz:
            active_biz = db.query(Business).first()
        target_business_id = active_biz.id if active_biz else uuid.uuid4()
    else:
        target_business_id = business_id

    pickup, raw_token = PickupDeliveryService.create_public_pickup_request(
        db, target_business_id, payload
    )
    return StandardResponse(data=_serialize_pickup(pickup, raw_token))


# -------------------------------------------------------------
# Staff Pickup Management (CASHIER, OWNER, STAFF)
# -------------------------------------------------------------
@router.get(
    "/requests",
    response_model=StandardResponse[list[PickupRequestRead]],
    summary="List pickup requests for outlet",
)
def list_pickup_requests(
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(require_roles(UserRole.OWNER, UserRole.CASHIER, UserRole.STAFF))],
    status_filter: str | None = Query(default=None, alias="status"),
    date_filter: date | None = Query(default=None, alias="date"),
) -> StandardResponse[list[PickupRequestRead]]:
    pickups = PickupDeliveryService.list_pickup_requests(
        db, current_user.business_id, status_filter, date_filter
    )
    return StandardResponse(data=[_serialize_pickup(p) for p in pickups])


@router.get(
    "/requests/{pickup_id}",
    response_model=StandardResponse[PickupRequestRead],
    summary="Get single pickup request details",
)
def get_pickup_request(
    pickup_id: uuid.UUID,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(require_roles(UserRole.OWNER, UserRole.CASHIER, UserRole.STAFF))],
) -> StandardResponse[PickupRequestRead]:
    pickup = PickupDeliveryService.get_pickup_request(
        db, pickup_id, current_user.business_id
    )
    return StandardResponse(data=_serialize_pickup(pickup))


@router.post(
    "/requests/{pickup_id}/confirm",
    response_model=StandardResponse[PickupRequestRead],
    dependencies=[Depends(verify_csrf)],
    summary="Confirm pickup request schedule & dispatch courier",
)
def confirm_pickup_request(
    pickup_id: uuid.UUID,
    payload: PickupConfirmPayload,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(require_roles(UserRole.OWNER, UserRole.CASHIER, UserRole.STAFF))],
) -> StandardResponse[PickupRequestRead]:
    pickup = PickupDeliveryService.confirm_pickup_request(
        db, pickup_id, current_user.business_id, payload, current_user.id
    )
    return StandardResponse(data=_serialize_pickup(pickup))


@router.post(
    "/requests/{pickup_id}/reject",
    response_model=StandardResponse[PickupRequestRead],
    dependencies=[Depends(verify_csrf)],
    summary="Reject pickup request with mandatory reason",
)
def reject_pickup_request(
    pickup_id: uuid.UUID,
    payload: PickupRejectPayload,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(require_roles(UserRole.OWNER, UserRole.CASHIER, UserRole.STAFF))],
) -> StandardResponse[PickupRequestRead]:
    pickup = PickupDeliveryService.reject_pickup_request(
        db, pickup_id, current_user.business_id, payload
    )
    return StandardResponse(data=_serialize_pickup(pickup))


@router.post(
    "/requests/{pickup_id}/convert-order",
    response_model=StandardResponse[dict[str, Any]],
    dependencies=[Depends(verify_csrf)],
    status_code=status.HTTP_201_CREATED,
    summary="Atomic conversion from pickup to laundry order (DEC-10)",
)
def convert_pickup_to_order(
    pickup_id: uuid.UUID,
    payload: PickupConvertToOrderPayload,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(require_roles(UserRole.OWNER, UserRole.CASHIER, UserRole.STAFF))],
) -> StandardResponse[dict[str, Any]]:
    order = PickupDeliveryService.convert_pickup_to_order(
        db, pickup_id, current_user.business_id, payload, current_user.id
    )
    return StandardResponse(
        data={
            "order_id": str(order.id),
            "order_number": order.order_number,
            "total_amount": order.total_amount,
            "operational_status": order.operational_status,
            "message": "Permintaan penjemputan berhasil dikonversi menjadi nota pesanan.",
        }
    )


# -------------------------------------------------------------
# Delivery Tasks & Courier Dispatch
# -------------------------------------------------------------
@router.get(
    "/tasks",
    response_model=StandardResponse[list[DeliveryTaskRead]],
    summary="List all delivery tasks for outlet",
)
def list_delivery_tasks(
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(require_roles(UserRole.OWNER, UserRole.CASHIER, UserRole.STAFF, UserRole.COURIER))],
    courier_id: uuid.UUID | None = Query(default=None),
    status_filter: str | None = Query(default=None, alias="status"),
) -> StandardResponse[list[DeliveryTaskRead]]:
    # If courier user, restrict to their tasks
    target_courier_id = current_user.id if current_user.role == UserRole.COURIER.value else courier_id
    tasks = PickupDeliveryService.list_delivery_tasks(
        db, current_user.business_id, target_courier_id, status_filter
    )
    return StandardResponse(data=[_serialize_task(t) for t in tasks])


@router.post(
    "/tasks",
    response_model=StandardResponse[DeliveryTaskRead],
    dependencies=[Depends(verify_csrf)],
    status_code=status.HTTP_201_CREATED,
    summary="Create and dispatch a delivery task",
)
def create_delivery_task(
    payload: DeliveryTaskCreate,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(require_roles(UserRole.OWNER, UserRole.CASHIER, UserRole.STAFF))],
) -> StandardResponse[DeliveryTaskRead]:
    task = PickupDeliveryService.create_delivery_task(
        db, current_user.business_id, payload, current_user.id
    )
    return StandardResponse(data=_serialize_task(task))


@router.get(
    "/tasks/my-tasks",
    response_model=StandardResponse[list[DeliveryTaskRead]],
    summary="Courier self-service task list",
)
def get_courier_my_tasks(
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> StandardResponse[list[DeliveryTaskRead]]:
    tasks = PickupDeliveryService.list_delivery_tasks(
        db, current_user.business_id, current_user.id
    )
    return StandardResponse(data=[_serialize_task(t) for t in tasks])


@router.post(
    "/tasks/{task_id}/status",
    response_model=StandardResponse[DeliveryTaskRead],
    dependencies=[Depends(verify_csrf)],
    summary="Update courier task status (EN_ROUTE, ARRIVED, COMPLETED, FAILED)",
)
def update_task_status(
    task_id: uuid.UUID,
    payload: DeliveryTaskStatusUpdate,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> StandardResponse[DeliveryTaskRead]:
    task = PickupDeliveryService.update_delivery_task_status(
        db, task_id, current_user.business_id, payload, current_user.id
    )
    return StandardResponse(data=_serialize_task(task))
