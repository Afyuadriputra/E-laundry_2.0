import uuid
from datetime import UTC, date, datetime, time
from typing import Any

from sqlalchemy import func
from sqlalchemy.orm import Session, joinedload

from app.modules.expenses.models import Expense
from app.modules.orders.models import Order
from app.modules.payments.models import Payment, PaymentVoid
from app.modules.reports.schemas import (
    DashboardSummaryRead,
    FinancialReportSummaryRead,
    OrdersReportItemRead,
    OrdersReportSummaryRead,
    OutstandingBalanceItemRead,
    OverdueOrderRead,
)


class ReportsService:
    @staticmethod
    def get_dashboard_summary(
        db: Session,
        business_id: uuid.UUID,
        role: str,
        start_date: date | None = None,
        end_date: date | None = None,
    ) -> DashboardSummaryRead:
        today = date.today()
        start = start_date or today
        end = end_date or today

        start_dt = datetime.combine(start, time.min).replace(tzinfo=UTC)
        end_dt = datetime.combine(end, time.max).replace(tzinfo=UTC)
        today_start_dt = datetime.combine(today, time.min).replace(tzinfo=UTC)
        today_end_dt = datetime.combine(today, time.max).replace(tzinfo=UTC)
        now = datetime.now(UTC)

        # 1. Operational counts
        orders_today = (
            db.query(func.count(Order.id))
            .filter(
                Order.business_id == business_id,
                Order.created_at >= today_start_dt,
                Order.created_at <= today_end_dt,
                Order.operational_status != "CANCELLED",
            )
            .scalar()
            or 0
        )

        active_orders = (
            db.query(func.count(Order.id))
            .filter(
                Order.business_id == business_id,
                Order.operational_status.in_([
                    "RECEIVED",
                    "QUEUED",
                    "WASHING",
                    "DRYING",
                    "IRONING",
                    "PACKING",
                ]),
            )
            .scalar()
            or 0
        )

        ready_orders = (
            db.query(func.count(Order.id))
            .filter(
                Order.business_id == business_id,
                Order.operational_status == "READY",
            )
            .scalar()
            or 0
        )

        completed_today = (
            db.query(func.count(Order.id))
            .filter(
                Order.business_id == business_id,
                Order.operational_status == "COMPLETED",
                Order.updated_at >= today_start_dt,
                Order.updated_at <= today_end_dt,
            )
            .scalar()
            or 0
        )

        overdue_orders = (
            db.query(func.count(Order.id))
            .filter(
                Order.business_id == business_id,
                Order.operational_status.notin_(["COMPLETED", "CANCELLED"]),
                Order.estimated_completion_at < now,
            )
            .scalar()
            or 0
        )

        summary = DashboardSummaryRead(
            orders_count_today=orders_today,
            active_orders_count=active_orders,
            ready_orders_count=ready_orders,
            completed_orders_today=completed_today,
            overdue_orders_count=overdue_orders,
            start_date=start,
            end_date=end,
        )

        # 2. Financial KPIs (Owner only)
        if role == "OWNER":
            # Order value in period (valid non-cancelled orders)
            order_val = (
                db.query(func.coalesce(func.sum(Order.total_amount), 0))
                .filter(
                    Order.business_id == business_id,
                    Order.created_at >= start_dt,
                    Order.created_at <= end_dt,
                    Order.operational_status != "CANCELLED",
                )
                .scalar()
                or 0
            )

            # Cash received in period (strictly valid payments, excluding voided)
            cash_rec = (
                db.query(func.coalesce(func.sum(Payment.amount), 0))
                .join(Order, Payment.order_id == Order.id)
                .outerjoin(PaymentVoid, Payment.id == PaymentVoid.payment_id)
                .filter(
                    Order.business_id == business_id,
                    Payment.created_at >= start_dt,
                    Payment.created_at <= end_dt,
                    PaymentVoid.id.is_(None),
                )
                .scalar()
                or 0
            )

            # Expenses in period
            expenses_tot = (
                db.query(func.coalesce(func.sum(Expense.amount), 0))
                .filter(
                    Expense.business_id == business_id,
                    Expense.expense_date >= start,
                    Expense.expense_date <= end,
                )
                .scalar()
                or 0
            )

            # Calculate outstanding across all non-cancelled orders
            all_active_orders = (
                db.query(Order)
                .filter(
                    Order.business_id == business_id,
                    Order.operational_status != "CANCELLED",
                )
                .all()
            )
            total_outstanding = 0
            for ord in all_active_orders:
                valid_payments = sum(
                    p.amount for p in ord.payments if not p.is_voided
                )
                rem = max(0, ord.total_amount - valid_payments)
                total_outstanding += rem

            summary.order_value_period = int(order_val)
            summary.cash_received_period = int(cash_rec)
            summary.expenses_period = int(expenses_tot)
            summary.simple_cash_difference = int(cash_rec) - int(expenses_tot)
            summary.outstanding_receivables = total_outstanding

        return summary

    @staticmethod
    def get_overdue_orders(
        db: Session, business_id: uuid.UUID
    ) -> list[OverdueOrderRead]:
        now = datetime.now(UTC)
        orders = (
            db.query(Order)
            .options(joinedload(Order.customer), joinedload(Order.payments))
            .filter(
                Order.business_id == business_id,
                Order.operational_status.notin_(["COMPLETED", "CANCELLED"]),
                Order.estimated_completion_at < now,
            )
            .order_by(Order.estimated_completion_at.asc())
            .all()
        )

        res: list[OverdueOrderRead] = []
        for o in orders:
            valid_paid = sum(p.amount for p in o.payments if not p.is_voided)
            rem = max(0, o.total_amount - valid_paid)
            hrs_overdue = (now - o.estimated_completion_at).total_seconds() / 3600.0

            res.append(
                OverdueOrderRead(
                    order_id=o.id,
                    order_number=o.order_number,
                    customer_name=o.customer.full_name if o.customer else "Anonim",
                    customer_phone=o.customer.phone_e164 if o.customer else "-",
                    operational_status=o.operational_status,
                    estimated_completion_at=o.estimated_completion_at,
                    hours_overdue=round(hrs_overdue, 1),
                    total_amount=o.total_amount,
                    remaining_amount=rem,
                )
            )
        return res

    @staticmethod
    def get_orders_report(
        db: Session,
        business_id: uuid.UUID,
        start_date: date | None = None,
        end_date: date | None = None,
        operational_status: str | None = None,
        payment_status: str | None = None,
    ) -> OrdersReportSummaryRead:
        query = (
            db.query(Order)
            .options(
                joinedload(Order.customer),
                joinedload(Order.payments),
                joinedload(Order.items),
            )
            .filter(Order.business_id == business_id)
        )

        if start_date:
            start_dt = datetime.combine(start_date, time.min).replace(tzinfo=UTC)
            query = query.filter(Order.created_at >= start_dt)
        if end_date:
            end_dt = datetime.combine(end_date, time.max).replace(tzinfo=UTC)
            query = query.filter(Order.created_at <= end_dt)
        if operational_status:
            query = query.filter(Order.operational_status == operational_status)

        orders = query.order_by(Order.created_at.desc()).all()

        items: list[OrdersReportItemRead] = []
        total_amt = 0
        total_paid_acc = 0
        total_out_acc = 0

        for o in orders:
            valid_paid = sum(p.amount for p in o.payments if not p.is_voided)
            rem = max(0, o.total_amount - valid_paid)

            if valid_paid >= o.total_amount:
                pay_st = "PAID"
            elif valid_paid > 0:
                pay_st = "PARTIALLY_PAID"
            else:
                pay_st = "UNPAID"

            if payment_status and pay_st != payment_status:
                continue

            # Exclude cancelled orders from total revenue accumulation
            if o.operational_status != "CANCELLED":
                total_amt += o.total_amount
                total_paid_acc += valid_paid
                total_out_acc += rem

            summary_str = ", ".join(
                f"{it.service_name_snapshot} ({it.quantity} {it.unit_snapshot})"
                for it in o.items
            ) or "-"

            items.append(
                OrdersReportItemRead(
                    order_id=o.id,
                    order_number=o.order_number,
                    created_at=o.created_at,
                    customer_name=o.customer.full_name if o.customer else "Anonim",
                    customer_phone=o.customer.phone_e164 if o.customer else "-",
                    operational_status=o.operational_status,
                    payment_status=pay_st,
                    total_amount=o.total_amount,
                    paid_amount=valid_paid,
                    remaining_amount=rem,
                    items_summary=summary_str,
                )
            )

        return OrdersReportSummaryRead(
            total_orders=len(items),
            total_amount=total_amt,
            total_paid=total_paid_acc,
            total_outstanding=total_out_acc,
            items=items,
        )

    @staticmethod
    def get_financial_report(
        db: Session,
        business_id: uuid.UUID,
        start_date: date | None = None,
        end_date: date | None = None,
    ) -> FinancialReportSummaryRead:
        today = date.today()
        start = start_date or today
        end = end_date or today

        start_dt = datetime.combine(start, time.min).replace(tzinfo=UTC)
        end_dt = datetime.combine(end, time.max).replace(tzinfo=UTC)

        # 1. Valid Payments grouped by method
        payments = (
            db.query(Payment)
            .join(Order, Payment.order_id == Order.id)
            .outerjoin(PaymentVoid, Payment.id == PaymentVoid.payment_id)
            .filter(
                Order.business_id == business_id,
                Payment.created_at >= start_dt,
                Payment.created_at <= end_dt,
                PaymentVoid.id.is_(None),
            )
            .all()
        )

        cash_by_method: dict[str, int] = {}
        total_cash = 0
        for p in payments:
            m = p.method
            cash_by_method[m] = cash_by_method.get(m, 0) + p.amount
            total_cash += p.amount

        # 2. Expenses grouped by category
        expenses = (
            db.query(Expense)
            .filter(
                Expense.business_id == business_id,
                Expense.expense_date >= start,
                Expense.expense_date <= end,
            )
            .all()
        )

        exp_by_cat: dict[str, int] = {}
        total_exp = 0
        for e in expenses:
            c = e.category
            exp_by_cat[c] = exp_by_cat.get(c, 0) + e.amount
            total_exp += e.amount

        # 3. Outstanding receivables on all active orders
        all_active_orders = (
            db.query(Order)
            .filter(
                Order.business_id == business_id,
                Order.operational_status != "CANCELLED",
            )
            .all()
        )
        total_outstanding = 0
        for ord in all_active_orders:
            valid_paid = sum(p.amount for p in ord.payments if not p.is_voided)
            rem = max(0, ord.total_amount - valid_paid)
            total_outstanding += rem

        return FinancialReportSummaryRead(
            start_date=start,
            end_date=end,
            total_cash_received=total_cash,
            cash_by_method=cash_by_method,
            total_expenses=total_exp,
            expenses_by_category=exp_by_cat,
            simple_cash_difference=total_cash - total_exp,
            outstanding_receivables=total_outstanding,
        )

    @staticmethod
    def get_outstanding_report(
        db: Session, business_id: uuid.UUID
    ) -> list[OutstandingBalanceItemRead]:
        orders = (
            db.query(Order)
            .options(joinedload(Order.customer), joinedload(Order.payments))
            .filter(
                Order.business_id == business_id,
                Order.operational_status != "CANCELLED",
            )
            .order_by(Order.created_at.desc())
            .all()
        )

        res: list[OutstandingBalanceItemRead] = []
        for o in orders:
            valid_paid = sum(p.amount for p in o.payments if not p.is_voided)
            rem = max(0, o.total_amount - valid_paid)

            if rem > 0:
                pay_st = "PARTIALLY_PAID" if valid_paid > 0 else "UNPAID"
                res.append(
                    OutstandingBalanceItemRead(
                        order_id=o.id,
                        order_number=o.order_number,
                        created_at=o.created_at,
                        customer_name=o.customer.full_name if o.customer else "Anonim",
                        customer_phone=o.customer.phone_e164 if o.customer else "-",
                        total_amount=o.total_amount,
                        paid_amount=valid_paid,
                        remaining_amount=rem,
                        payment_status=pay_st,
                        operational_status=o.operational_status,
                    )
                )
        return res

    @staticmethod
    def get_orders_export_data(
        db: Session,
        business_id: uuid.UUID,
        start_date: date | None = None,
        end_date: date | None = None,
    ) -> list[dict[str, Any]]:
        summary = ReportsService.get_orders_report(
            db, business_id, start_date=start_date, end_date=end_date
        )
        return [
            {
                "order_number": it.order_number,
                "created_at": it.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                "customer_name": it.customer_name,
                "customer_phone": it.customer_phone,
                "operational_status": it.operational_status,
                "payment_status": it.payment_status,
                "total_amount": it.total_amount,
                "paid_amount": it.paid_amount,
                "remaining_amount": it.remaining_amount,
                "items_summary": it.items_summary,
            }
            for it in summary.items
        ]

    @staticmethod
    def get_payments_export_data(
        db: Session,
        business_id: uuid.UUID,
        start_date: date | None = None,
        end_date: date | None = None,
    ) -> list[dict[str, Any]]:
        query = (
            db.query(Payment)
            .join(Order, Payment.order_id == Order.id)
            .options(joinedload(Payment.order), joinedload(Payment.void_record))
            .filter(Order.business_id == business_id)
        )
        if start_date:
            start_dt = datetime.combine(start_date, time.min).replace(tzinfo=UTC)
            query = query.filter(Payment.created_at >= start_dt)
        if end_date:
            end_dt = datetime.combine(end_date, time.max).replace(tzinfo=UTC)
            query = query.filter(Payment.created_at <= end_dt)

        payments = query.order_by(Payment.created_at.desc()).all()
        return [
            {
                "id": str(p.id),
                "created_at": p.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                "order_number": p.order.order_number if p.order else "-",
                "payment_method": p.method,
                "amount": p.amount,
                "is_voided": p.is_voided,
                "notes": p.reference_note or "-",
            }
            for p in payments
        ]

    @staticmethod
    def get_expenses_export_data(
        db: Session,
        business_id: uuid.UUID,
        start_date: date | None = None,
        end_date: date | None = None,
    ) -> list[dict[str, Any]]:
        query = (
            db.query(Expense)
            .options(joinedload(Expense.creator))
            .filter(Expense.business_id == business_id)
        )
        if start_date:
            query = query.filter(Expense.expense_date >= start_date)
        if end_date:
            query = query.filter(Expense.expense_date <= end_date)

        expenses = query.order_by(Expense.expense_date.desc()).all()
        return [
            {
                "id": str(e.id),
                "expense_date": str(e.expense_date),
                "category": e.category,
                "description": e.description or "-",
                "amount": e.amount,
                "created_by_name": e.creator.full_name if e.creator else "-",
            }
            for e in expenses
        ]
