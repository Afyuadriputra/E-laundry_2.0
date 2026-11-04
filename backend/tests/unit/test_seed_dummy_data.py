"""
Automated unit tests for the E-Laundry 2.0 dummy data seeder.
Verifies that all 19 database tables are populated with consistent, domain-valid data.
"""

from __future__ import annotations

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.core.security import verify_password
from app.modules.audit.models import AuditLog
from app.modules.auth.models import UserSession
from app.modules.businesses.models import Business, BusinessSettings
from app.modules.customers.models import Customer
from app.modules.expenses.models import Expense
from app.modules.idempotency.models import IdempotencyRecord
from app.modules.orders.models import Order, OrderHandoff, OrderItem, OrderStatusHistory
from app.modules.payments.models import Payment, PaymentVoid
from app.modules.pickup_delivery.models import (
    DeliveryStatusHistory,
    DeliveryTask,
    PickupRequest,
)
from app.modules.services.models import Service
from app.modules.tracking.models import TrackingToken
from app.modules.users.models import User
from scripts.seed_dummy_data import seed_database


def test_seed_database_populates_all_19_tables(db_session: Session) -> None:
    """Verifies that seed_database populates every table in the 19-table BSD catalog."""
    counts = seed_database(db_session, customer_count=15, order_count=20)

    # 1. Verify counts dict has all 19 tables with > 0 rows
    expected_tables = [
        "businesses",
        "business_settings",
        "users",
        "user_sessions",
        "customers",
        "services",
        "pickup_requests",
        "orders",
        "order_items",
        "order_status_history",
        "order_handoffs",
        "delivery_tasks",
        "delivery_status_history",
        "tracking_tokens",
        "payments",
        "payment_voids",
        "expenses",
        "idempotency_records",
        "audit_logs",
    ]
    assert len(expected_tables) == 19
    for tbl in expected_tables:
        assert tbl in counts, f"Missing table {tbl} in seeder counts"
        assert counts[tbl] > 0, f"Table {tbl} has 0 rows"

    # 2. Query each model in database to verify physical persistence
    assert db_session.scalar(select(func.count(Business.id))) == counts["businesses"]
    assert db_session.scalar(select(func.count(BusinessSettings.id))) == counts["business_settings"]
    assert db_session.scalar(select(func.count(User.id))) == counts["users"]
    assert db_session.scalar(select(func.count(UserSession.id))) == counts["user_sessions"]
    assert db_session.scalar(select(func.count(Customer.id))) == counts["customers"]
    assert db_session.scalar(select(func.count(Service.id))) == counts["services"]
    assert db_session.scalar(select(func.count(PickupRequest.id))) == counts["pickup_requests"]
    assert db_session.scalar(select(func.count(Order.id))) == counts["orders"]
    assert db_session.scalar(select(func.count(OrderItem.id))) == counts["order_items"]
    assert db_session.scalar(select(func.count(OrderStatusHistory.id))) == counts["order_status_history"]
    assert db_session.scalar(select(func.count(OrderHandoff.id))) == counts["order_handoffs"]
    assert db_session.scalar(select(func.count(DeliveryTask.id))) == counts["delivery_tasks"]
    assert db_session.scalar(select(func.count(DeliveryStatusHistory.id))) == counts["delivery_status_history"]
    assert db_session.scalar(select(func.count(TrackingToken.id))) == counts["tracking_tokens"]
    assert db_session.scalar(select(func.count(Payment.id))) == counts["payments"]
    assert db_session.scalar(select(func.count(PaymentVoid.id))) == counts["payment_voids"]
    assert db_session.scalar(select(func.count(Expense.id))) == counts["expenses"]
    assert db_session.scalar(select(func.count(IdempotencyRecord.id))) == counts["idempotency_records"]
    assert db_session.scalar(select(func.count(AuditLog.id))) == counts["audit_logs"]


def test_seed_user_credentials_authenticatable(db_session: Session) -> None:
    """Verifies that seeded users can be verified with Argon2id passwords."""
    seed_database(db_session, customer_count=5, order_count=5)

    owner = db_session.scalar(select(User).where(User.username == "owner"))
    assert owner is not None
    assert verify_password("Owner123!", owner.password_hash) is True
    assert verify_password("WrongPassword", owner.password_hash) is False

    cashier = db_session.scalar(select(User).where(User.username == "kasir_ani"))
    assert cashier is not None
    assert verify_password("Kasir123!", cashier.password_hash) is True


def test_seed_financial_and_pricing_invariants(db_session: Session) -> None:
    """Verifies that seeded orders have mathematically exact subtotals and totals."""
    seed_database(db_session, customer_count=5, order_count=10)

    orders = db_session.scalars(select(Order)).all()
    for ord_obj in orders:
        # Check subtotal matches items
        calculated_subtotal = sum(item.line_total_amount for item in ord_obj.items)
        assert ord_obj.subtotal_amount == calculated_subtotal
        assert ord_obj.total_amount == (
            ord_obj.subtotal_amount + ord_obj.extra_charge_amount + ord_obj.delivery_fee_amount
        )


def test_seed_delivery_tasks_type_constraints(db_session: Session) -> None:
    """Verifies that delivery_tasks strictly adhere to chk_delivery_tasks_type_target."""
    seed_database(db_session, customer_count=5, order_count=10)

    tasks = db_session.scalars(select(DeliveryTask)).all()
    for task in tasks:
        if task.task_type == "PICKUP":
            assert task.pickup_request_id is not None
            assert task.order_id is None
        elif task.task_type == "DELIVERY":
            assert task.order_id is not None
            assert task.pickup_request_id is None

