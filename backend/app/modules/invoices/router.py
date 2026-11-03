import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session

from app.core.exceptions import ForbiddenException
from app.db.session import get_db
from app.modules.auth.dependencies import get_current_user
from app.modules.invoices.pdf_renderer import (
    render_html_invoice,
    render_thermal_receipt,
)
from app.modules.invoices.schemas import InvoiceRead
from app.modules.invoices.service import InvoiceService
from app.modules.users.models import User
from app.shared.schemas.responses import StandardResponse

router = APIRouter(prefix="/invoices", tags=["Invoices"])


def require_order_access(current_user: Annotated[User, Depends(get_current_user)]) -> User:
    if current_user.role not in ["OWNER", "CASHIER", "STAFF"]:
        raise ForbiddenException(message="Akses terbatas untuk staf laundry.")
    return current_user


@router.get("/{order_id}", response_model=StandardResponse[InvoiceRead])
def get_invoice(
    order_id: uuid.UUID,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(require_order_access)],
) -> StandardResponse[InvoiceRead]:
    """Retrieve digital invoice read model, excluding internal sensitive notes."""
    invoice = InvoiceService.get_invoice_for_order(
        db=db,
        order_id=order_id,
        business_id=current_user.business_id,
    )
    return StandardResponse(data=invoice)


@router.get("/{order_id}/thermal")
def get_thermal_invoice(
    order_id: uuid.UUID,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(require_order_access)],
) -> Response:
    """Retrieve 58mm POS thermal receipt text format."""
    invoice = InvoiceService.get_invoice_for_order(
        db=db,
        order_id=order_id,
        business_id=current_user.business_id,
    )
    receipt_text = render_thermal_receipt(invoice, width_chars=32)
    return Response(content=receipt_text, media_type="text/plain; charset=utf-8")


@router.get("/{order_id}/html")
def get_html_invoice(
    order_id: uuid.UUID,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(require_order_access)],
) -> Response:
    """Retrieve printable/PDF-ready HTML invoice."""
    invoice = InvoiceService.get_invoice_for_order(
        db=db,
        order_id=order_id,
        business_id=current_user.business_id,
    )
    html_content = render_html_invoice(invoice)
    return Response(content=html_content, media_type="text/html; charset=utf-8")
