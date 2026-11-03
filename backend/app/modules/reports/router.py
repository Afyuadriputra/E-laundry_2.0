from datetime import date
from typing import Annotated

from fastapi import APIRouter, Depends, Query, Response
from sqlalchemy.orm import Session

from app.core.permissions import require_roles
from app.db.session import get_db
from app.modules.reports.csv_export import (
    generate_expenses_csv,
    generate_orders_csv,
    generate_payments_csv,
)
from app.modules.reports.schemas import (
    DashboardSummaryRead,
    FinancialReportSummaryRead,
    OrdersReportSummaryRead,
    OutstandingBalanceItemRead,
    OverdueOrderRead,
)
from app.modules.reports.service import ReportsService
from app.modules.users.models import User, UserRole
from app.shared.schemas.responses import StandardResponse

router = APIRouter(prefix="/reports", tags=["Dashboard & Reporting"])


@router.get("/dashboard", response_model=StandardResponse[DashboardSummaryRead])
def get_dashboard_summary(
    current_user: Annotated[
        User, Depends(require_roles(UserRole.OWNER, UserRole.CASHIER))
    ],
    db: Annotated[Session, Depends(get_db)],
    start_date: Annotated[date | None, Query()] = None,
    end_date: Annotated[date | None, Query()] = None,
) -> StandardResponse[DashboardSummaryRead]:
    summary = ReportsService.get_dashboard_summary(
        db=db,
        business_id=current_user.business_id,
        role=current_user.role,
        start_date=start_date,
        end_date=end_date,
    )
    return StandardResponse(data=summary)


@router.get("/overdue", response_model=StandardResponse[list[OverdueOrderRead]])
def get_overdue_orders(
    current_user: Annotated[
        User,
        Depends(require_roles(UserRole.OWNER, UserRole.CASHIER, UserRole.STAFF)),
    ],
    db: Annotated[Session, Depends(get_db)],
) -> StandardResponse[list[OverdueOrderRead]]:
    overdue_list = ReportsService.get_overdue_orders(
        db=db, business_id=current_user.business_id
    )
    return StandardResponse(data=overdue_list)


@router.get("/orders", response_model=StandardResponse[OrdersReportSummaryRead])
def get_orders_report(
    current_user: Annotated[
        User, Depends(require_roles(UserRole.OWNER, UserRole.CASHIER))
    ],
    db: Annotated[Session, Depends(get_db)],
    start_date: Annotated[date | None, Query()] = None,
    end_date: Annotated[date | None, Query()] = None,
    operational_status: Annotated[str | None, Query()] = None,
    payment_status: Annotated[str | None, Query()] = None,
) -> StandardResponse[OrdersReportSummaryRead]:
    summary = ReportsService.get_orders_report(
        db=db,
        business_id=current_user.business_id,
        start_date=start_date,
        end_date=end_date,
        operational_status=operational_status,
        payment_status=payment_status,
    )
    return StandardResponse(data=summary)


@router.get("/finances", response_model=StandardResponse[FinancialReportSummaryRead])
def get_financial_report(
    current_user: Annotated[User, Depends(require_roles(UserRole.OWNER))],
    db: Annotated[Session, Depends(get_db)],
    start_date: Annotated[date | None, Query()] = None,
    end_date: Annotated[date | None, Query()] = None,
) -> StandardResponse[FinancialReportSummaryRead]:
    finances = ReportsService.get_financial_report(
        db=db,
        business_id=current_user.business_id,
        start_date=start_date,
        end_date=end_date,
    )
    return StandardResponse(data=finances)


@router.get(
    "/outstanding",
    response_model=StandardResponse[list[OutstandingBalanceItemRead]],
)
def get_outstanding_report(
    current_user: Annotated[
        User, Depends(require_roles(UserRole.OWNER, UserRole.CASHIER))
    ],
    db: Annotated[Session, Depends(get_db)],
) -> StandardResponse[list[OutstandingBalanceItemRead]]:
    outstanding_list = ReportsService.get_outstanding_report(
        db=db, business_id=current_user.business_id
    )
    return StandardResponse(data=outstanding_list)


@router.get("/export/orders.csv")
def export_orders_csv(
    current_user: Annotated[
        User, Depends(require_roles(UserRole.OWNER, UserRole.CASHIER))
    ],
    db: Annotated[Session, Depends(get_db)],
    start_date: Annotated[date | None, Query()] = None,
    end_date: Annotated[date | None, Query()] = None,
) -> Response:
    orders_data = ReportsService.get_orders_export_data(
        db=db,
        business_id=current_user.business_id,
        start_date=start_date,
        end_date=end_date,
    )
    csv_content = generate_orders_csv(orders_data)
    filename = f"laporan_pesanan_{date.today().isoformat()}.csv"
    return Response(
        content=csv_content,
        media_type="text/csv",
        headers={
            "Content-Disposition": f'attachment; filename="{filename}"',
            "Cache-Control": "no-store",
        },
    )


@router.get("/export/payments.csv")
def export_payments_csv(
    current_user: Annotated[User, Depends(require_roles(UserRole.OWNER))],
    db: Annotated[Session, Depends(get_db)],
    start_date: Annotated[date | None, Query()] = None,
    end_date: Annotated[date | None, Query()] = None,
) -> Response:
    payments_data = ReportsService.get_payments_export_data(
        db=db,
        business_id=current_user.business_id,
        start_date=start_date,
        end_date=end_date,
    )
    csv_content = generate_payments_csv(payments_data)
    filename = f"laporan_pembayaran_{date.today().isoformat()}.csv"
    return Response(
        content=csv_content,
        media_type="text/csv",
        headers={
            "Content-Disposition": f'attachment; filename="{filename}"',
            "Cache-Control": "no-store",
        },
    )


@router.get("/export/expenses.csv")
def export_expenses_csv(
    current_user: Annotated[User, Depends(require_roles(UserRole.OWNER))],
    db: Annotated[Session, Depends(get_db)],
    start_date: Annotated[date | None, Query()] = None,
    end_date: Annotated[date | None, Query()] = None,
) -> Response:
    expenses_data = ReportsService.get_expenses_export_data(
        db=db,
        business_id=current_user.business_id,
        start_date=start_date,
        end_date=end_date,
    )
    csv_content = generate_expenses_csv(expenses_data)
    filename = f"laporan_pengeluaran_{date.today().isoformat()}.csv"
    return Response(
        content=csv_content,
        media_type="text/csv",
        headers={
            "Content-Disposition": f'attachment; filename="{filename}"',
            "Cache-Control": "no-store",
        },
    )
