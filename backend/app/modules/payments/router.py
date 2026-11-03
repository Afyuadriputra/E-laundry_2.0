import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, Header
from sqlalchemy.orm import Session

from app.core.exceptions import ForbiddenException
from app.db.session import get_db
from app.modules.auth.dependencies import get_current_user, verify_csrf
from app.modules.payments.schemas import (
    OrderPaymentSummary,
    PaymentCreate,
    PaymentRead,
    PaymentVoidCreate,
)
from app.modules.payments.service import PaymentService
from app.modules.users.models import User
from app.shared.schemas.responses import StandardResponse

router = APIRouter(tags=["Payments"])


def require_owner_or_cashier(current_user: Annotated[User, Depends(get_current_user)]) -> User:
    if current_user.role not in ["OWNER", "CASHIER"]:
        raise ForbiddenException(message="Akses terbatas untuk Owner dan Kasir.")
    return current_user


def require_owner(current_user: Annotated[User, Depends(get_current_user)]) -> User:
    if current_user.role != "OWNER":
        raise ForbiddenException(
            message="Hanya Owner yang berwenang melakukan pembatalan (void) pembayaran."
        )
    return current_user


@router.get("/orders/{order_id}/payments", response_model=StandardResponse[OrderPaymentSummary])
def get_order_payments(
    order_id: uuid.UUID,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(require_owner_or_cashier)],
) -> StandardResponse[OrderPaymentSummary]:
    """Retrieve full payment summary and transaction history for an order."""
    summary = PaymentService.get_order_payment_summary(
        db=db,
        order_id=order_id,
        business_id=current_user.business_id,
    )
    return StandardResponse(data=summary)


@router.post(
    "/orders/{order_id}/payments",
    response_model=StandardResponse[PaymentRead],
    dependencies=[Depends(verify_csrf)],
)
def record_order_payment(
    order_id: uuid.UUID,
    payload: PaymentCreate,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(require_owner_or_cashier)],
    idempotency_key: Annotated[str | None, Header(alias="Idempotency-Key")] = None,
) -> StandardResponse[PaymentRead]:
    """Record manual verified payment with pessimistic locking and overpayment checks."""
    payment = PaymentService.record_payment(
        db=db,
        order_id=order_id,
        business_id=current_user.business_id,
        verified_by_user_id=current_user.id,
        payload=payload,
        idempotency_key=idempotency_key,
    )
    return StandardResponse(data=payment)


@router.get("/payments/{payment_id}", response_model=StandardResponse[PaymentRead])
def get_payment_detail(
    payment_id: uuid.UUID,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(require_owner_or_cashier)],
) -> StandardResponse[PaymentRead]:
    """Get single payment record details."""
    payment = PaymentService.get_payment_detail(
        db=db,
        payment_id=payment_id,
        business_id=current_user.business_id,
    )
    return StandardResponse(data=payment)


@router.post(
    "/payments/{payment_id}/void",
    response_model=StandardResponse[PaymentRead],
    dependencies=[Depends(verify_csrf)],
)
def void_payment(
    payment_id: uuid.UUID,
    payload: PaymentVoidCreate,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(require_owner)],
) -> StandardResponse[PaymentRead]:
    """Void an existing payment record (Owner only, audit reason mandatory)."""
    voided = PaymentService.void_payment(
        db=db,
        payment_id=payment_id,
        business_id=current_user.business_id,
        voided_by_user_id=current_user.id,
        payload=payload,
    )
    return StandardResponse(data=voided)
