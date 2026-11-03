import uuid
from collections.abc import Sequence
from datetime import date

from sqlalchemy.orm import Session, joinedload

from app.core.exceptions import NotFoundException
from app.modules.expenses.models import Expense
from app.modules.expenses.schemas import ExpenseCreate, ExpenseRead, ExpenseUpdate


class ExpenseService:
    @classmethod
    def _map_to_read(cls, expense: Expense) -> ExpenseRead:
        return ExpenseRead(
            id=expense.id,
            business_id=expense.business_id,
            category=expense.category,
            amount=expense.amount,
            expense_date=expense.expense_date,
            description=expense.description,
            created_by=expense.created_by,
            created_by_name=expense.creator.full_name if expense.creator else None,
            created_at=expense.created_at,
            updated_at=expense.updated_at,
        )

    @classmethod
    def list_expenses(
        cls,
        db: Session,
        business_id: uuid.UUID,
        category: str | None = None,
        start_date: date | None = None,
        end_date: date | None = None,
        limit: int = 50,
        offset: int = 0,
    ) -> Sequence[ExpenseRead]:
        query = (
            db.query(Expense)
            .options(joinedload(Expense.creator))
            .filter(Expense.business_id == business_id)
        )
        if category:
            query = query.filter(Expense.category == category)
        if start_date:
            query = query.filter(Expense.expense_date >= start_date)
        if end_date:
            query = query.filter(Expense.expense_date <= end_date)

        expenses = (
            query.order_by(Expense.expense_date.desc(), Expense.created_at.desc())
            .offset(offset)
            .limit(limit)
            .all()
        )
        return [cls._map_to_read(e) for e in expenses]

    @classmethod
    def create_expense(
        cls,
        db: Session,
        business_id: uuid.UUID,
        user_id: uuid.UUID,
        payload: ExpenseCreate,
    ) -> ExpenseRead:
        expense = Expense(
            id=uuid.uuid4(),
            business_id=business_id,
            category=payload.category.value,
            amount=payload.amount,
            expense_date=payload.expense_date,
            description=payload.description,
            created_by=user_id,
        )
        db.add(expense)
        db.commit()
        db.refresh(expense)
        return cls._map_to_read(expense)

    @classmethod
    def get_expense(
        cls,
        db: Session,
        expense_id: uuid.UUID,
        business_id: uuid.UUID,
    ) -> ExpenseRead:
        expense = (
            db.query(Expense)
            .options(joinedload(Expense.creator))
            .filter(Expense.id == expense_id, Expense.business_id == business_id)
            .first()
        )
        if not expense:
            raise NotFoundException(message="Pengeluaran tidak ditemukan.")
        return cls._map_to_read(expense)

    @classmethod
    def update_expense(
        cls,
        db: Session,
        expense_id: uuid.UUID,
        business_id: uuid.UUID,
        payload: ExpenseUpdate,
    ) -> ExpenseRead:
        expense = (
            db.query(Expense)
            .filter(Expense.id == expense_id, Expense.business_id == business_id)
            .first()
        )
        if not expense:
            raise NotFoundException(message="Pengeluaran tidak ditemukan.")

        if payload.category is not None:
            expense.category = payload.category.value
        if payload.amount is not None:
            expense.amount = payload.amount
        if payload.expense_date is not None:
            expense.expense_date = payload.expense_date
        if payload.description is not None:
            expense.description = payload.description

        db.commit()
        db.refresh(expense)
        return cls._map_to_read(expense)

    @classmethod
    def delete_expense(
        cls,
        db: Session,
        expense_id: uuid.UUID,
        business_id: uuid.UUID,
    ) -> None:
        expense = (
            db.query(Expense)
            .filter(Expense.id == expense_id, Expense.business_id == business_id)
            .first()
        )
        if not expense:
            raise NotFoundException(message="Pengeluaran tidak ditemukan.")
        db.delete(expense)
        db.commit()
