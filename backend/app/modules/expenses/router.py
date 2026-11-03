import uuid
from datetime import date
from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.exceptions import ForbiddenException
from app.db.session import get_db
from app.modules.auth.dependencies import get_current_user, verify_csrf
from app.modules.expenses.schemas import ExpenseCreate, ExpenseRead, ExpenseUpdate
from app.modules.expenses.service import ExpenseService
from app.modules.users.models import User
from app.shared.schemas.responses import StandardResponse

router = APIRouter(prefix="/expenses", tags=["Expenses"])


def require_owner_or_cashier(current_user: Annotated[User, Depends(get_current_user)]) -> User:
    if current_user.role not in ["OWNER", "CASHIER"]:
        raise ForbiddenException(message="Akses terbatas untuk Owner dan Kasir.")
    return current_user


def require_owner(current_user: Annotated[User, Depends(get_current_user)]) -> User:
    if current_user.role != "OWNER":
        raise ForbiddenException(message="Akses terbatas untuk Owner.")
    return current_user


@router.get("", response_model=StandardResponse[list[ExpenseRead]])
def list_expenses(
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(require_owner_or_cashier)],
    category: Annotated[str | None, Query()] = None,
    start_date: Annotated[date | None, Query()] = None,
    end_date: Annotated[date | None, Query()] = None,
    limit: Annotated[int, Query(ge=1, le=100)] = 50,
    offset: Annotated[int, Query(ge=0)] = 0,
) -> StandardResponse[list[ExpenseRead]]:
    """List operational expenses filtered by date range or category."""
    expenses = ExpenseService.list_expenses(
        db=db,
        business_id=current_user.business_id,
        category=category,
        start_date=start_date,
        end_date=end_date,
        limit=limit,
        offset=offset,
    )
    return StandardResponse(data=list(expenses))


@router.post(
    "",
    response_model=StandardResponse[ExpenseRead],
    dependencies=[Depends(verify_csrf)],
)
def create_expense(
    payload: ExpenseCreate,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(require_owner_or_cashier)],
) -> StandardResponse[ExpenseRead]:
    """Create an operational expense record."""
    expense = ExpenseService.create_expense(
        db=db,
        business_id=current_user.business_id,
        user_id=current_user.id,
        payload=payload,
    )
    return StandardResponse(data=expense)


@router.get("/{expense_id}", response_model=StandardResponse[ExpenseRead])
def get_expense(
    expense_id: uuid.UUID,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(require_owner_or_cashier)],
) -> StandardResponse[ExpenseRead]:
    """Get expense details."""
    expense = ExpenseService.get_expense(
        db=db,
        expense_id=expense_id,
        business_id=current_user.business_id,
    )
    return StandardResponse(data=expense)


@router.put(
    "/{expense_id}",
    response_model=StandardResponse[ExpenseRead],
    dependencies=[Depends(verify_csrf)],
)
def update_expense(
    expense_id: uuid.UUID,
    payload: ExpenseUpdate,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(require_owner)],
) -> StandardResponse[ExpenseRead]:
    """Update expense details (Owner only)."""
    expense = ExpenseService.update_expense(
        db=db,
        expense_id=expense_id,
        business_id=current_user.business_id,
        payload=payload,
    )
    return StandardResponse(data=expense)


@router.delete(
    "/{expense_id}",
    response_model=StandardResponse[dict[str, str]],
    dependencies=[Depends(verify_csrf)],
)
def delete_expense(
    expense_id: uuid.UUID,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(require_owner)],
) -> StandardResponse[dict[str, str]]:
    """Delete expense (Owner only)."""
    ExpenseService.delete_expense(
        db=db,
        expense_id=expense_id,
        business_id=current_user.business_id,
    )
    return StandardResponse(data={"message": "Pengeluaran berhasil dihapus."})
