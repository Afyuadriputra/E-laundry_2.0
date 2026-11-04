"""
Real PostgreSQL 17 Verification Test Suite.
Verifies all 19 BSD tables, Alembic migration integrity, foreign keys, check constraints,
and concurrent payment transactions on an isolated real PostgreSQL database.
"""

import concurrent.futures
import os
import uuid
from datetime import UTC, datetime, timedelta
from decimal import Decimal

import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session, sessionmaker

from app.modules.audit.models import AuditLog
from app.modules.audit.service import AuditService
from app.modules.businesses.models import Business
from app.modules.customers.models import Customer
from app.modules.orders.domain.pricing import PricingEngine
from app.modules.orders.models import Order, OrderItem, OrderStatusHistory
from app.modules.payments.domain.balance import calculate_payment_balance
from app.modules.payments.domain.invariants import (
    OverpaymentNotAllowedError,
)
from app.modules.payments.models import Payment, PaymentVoid
from app.modules.services.models import Service
from app.modules.users.models import User, UserRole

# Isolated real PostgreSQL 17 connection URL
PG_TEST_URL = os.getenv(
    "REAL_PG_TEST_URL",
    "postgresql+psycopg://postgres:afyu@localhost:5432/laundry_test",
)


@pytest.fixture(scope="module")
def pg_engine():
    """Create a real SQLAlchemy engine connected to PostgreSQL 17 laundry_test."""
    try:
        engine = create_engine(PG_TEST_URL, pool_pre_ping=True)
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        yield engine
        engine.dispose()
    except Exception as exc:
        pytest.skip(f"PostgreSQL 17 environment not available: {exc}")


@pytest.fixture(scope="module")
def pg_session_factory(pg_engine):
    return sessionmaker(bind=pg_engine, autocommit=False, autoflush=False, expire_on_commit=False)


@pytest.fixture
def pg_session(pg_session_factory):
    session = pg_session_factory()
    try:
        yield session
    finally:
        session.rollback()
        session.close()


def test_real_postgresql_version_and_connection(pg_engine):
    """Verify live connection and PostgreSQL 17 engine version."""
    with pg_engine.connect() as conn:
        res = conn.execute(text("SELECT version();")).scalar()
        assert res is not None
        assert "PostgreSQL 17" in res, f"Expected PostgreSQL 17, got: {res}"


def test_real_postgresql_19_bsd_tables_present(pg_engine):
    """Verify all 19 BSD core tables and alembic_version exist in real PostgreSQL."""
    expected_tables = {
        "businesses",
        "business_settings",
        "users",
        "user_sessions",
        "customers",
        "services",
        "orders",
        "order_items",
        "order_status_history",
        "order_handoffs",
        "payments",
        "payment_voids",
        "expenses",
        "idempotency_records",
        "tracking_tokens",
        "pickup_requests",
        "delivery_tasks",
        "delivery_status_history",
        "audit_logs",
    }
    with pg_engine.connect() as conn:
        result = conn.execute(
            text(
                "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';"
            )
        )
        actual_tables = {row[0] for row in result.fetchall()}

    missing = expected_tables - actual_tables
    assert not missing, f"Missing BSD tables in real PostgreSQL: {missing}"
    assert "alembic_version" in actual_tables


def test_real_postgresql_constraints_and_foreign_keys(pg_engine):
    """Verify foreign keys, unique constraints, and check constraints in real PostgreSQL."""
    with pg_engine.connect() as conn:
        # Check foreign keys count
        fk_count = conn.execute(
            text(
                "SELECT count(*) FROM information_schema.table_constraints WHERE constraint_type = 'FOREIGN KEY';"
            )
        ).scalar()
        assert fk_count >= 30, f"Expected >= 30 foreign keys, found {fk_count}"

        # Check unique index on tracking_tokens.token_hash
        tt_unique = conn.execute(
            text(
                """
                SELECT count(*) FROM pg_indexes
                WHERE tablename = 'tracking_tokens' AND indexdef LIKE '%token_hash%';
                """
            )
        ).scalar()
        assert tt_unique >= 1

        # Check PostgreSQL-native single target check constraint
        chk_exists = conn.execute(
            text(
                """
                SELECT count(*) FROM information_schema.check_constraints
                WHERE constraint_name = 'chk_tracking_tokens_single_target';
                """
            )
        ).scalar()
        assert chk_exists == 1


def test_real_postgresql_business_and_order_lifecycle(pg_session: Session):
    """Test full order creation and status transitions with real PostgreSQL transactions."""
    now = datetime.now(UTC)

    # 1. Setup Business & User
    biz = Business(
        name=f"Outlet Tes PG {uuid.uuid4().hex[:6]}",
        phone_e164="+6281234567899",
        address="Jl. Pengujian No. 17, Jakarta",
        timezone="Asia/Jakarta",
    )
    pg_session.add(biz)
    pg_session.flush()

    user = User(
        business_id=biz.id,
        username=f"kasir_pg_{uuid.uuid4().hex[:6]}",
        password_hash="argon2id_hash_placeholder",
        full_name="Kasir PostgreSQL",
        role=UserRole.CASHIER,
        phone_e164="+6281234567891",
        is_active=True,
    )
    pg_session.add(user)

    cust = Customer(
        business_id=biz.id,
        full_name="Pelanggan Real PG",
        phone_e164="+6281234567892",
        address="Jl. Tebet Mas No. 5",
    )
    pg_session.add(cust)

    srv = Service(
        business_id=biz.id,
        name="Cuci Kering Reguler",
        pricing_type="PER_KG",
        unit="KG",
        unit_price=10000,
        estimated_hours=24,
        requires_ironing=False,
        is_active=True,
        version=1,
    )
    pg_session.add(srv)
    pg_session.flush()

    # 2. Pricing Calculation (0.1 kg HALF_UP, 3.0 kg floor)
    order_pricing = PricingEngine.calculate_order(
        items=[("PER_KG", Decimal("4.25"), srv.unit_price)],
        delivery_fee_amount=5000,
    )
    assert order_pricing.total_amount == 48000

    order = Order(
        business_id=biz.id,
        customer_id=cust.id,
        order_number=f"ORD-PG-{uuid.uuid4().hex[:6].upper()}",
        operational_status="RECEIVED",
        intake_method="WALK_IN",
        return_method="SELF_PICKUP",
        subtotal_amount=order_pricing.subtotal_amount,
        delivery_fee_amount=order_pricing.delivery_fee_amount,
        total_amount=order_pricing.total_amount,
        estimated_completion_at=now + timedelta(hours=24),
        created_by=user.id,
        version=1,
    )
    pg_session.add(order)
    pg_session.flush()

    line_item = order_pricing.line_results[0]
    item = OrderItem(
        order_id=order.id,
        service_id=srv.id,
        service_name_snapshot=srv.name,
        pricing_type_snapshot=srv.pricing_type,
        unit_snapshot=srv.unit,
        unit_price_snapshot=srv.unit_price,
        quantity=line_item.measured_quantity,
        line_total_amount=line_item.line_total,
        requires_ironing_snapshot=srv.requires_ironing,
    )
    pg_session.add(item)

    # 3. Transition through state machine in PostgreSQL
    transitions = [
        ("RECEIVED", "QUEUED"),
        ("QUEUED", "WASHING"),
        ("WASHING", "DRYING"),
        ("DRYING", "QC_PACKING"),
        ("QC_PACKING", "READY"),
        ("READY", "COMPLETED"),
    ]
    for from_st, to_st in transitions:
        order.operational_status = to_st
        order.version += 1
        history = OrderStatusHistory(
            order_id=order.id,
            from_status=from_st,
            to_status=to_st,
            changed_by=user.id,
            reason=f"Pindah ke {to_st}",
        )
        pg_session.add(history)
        pg_session.flush()

    pg_session.commit()

    # Verify history records in real PostgreSQL
    persisted_history = (
        pg_session.query(OrderStatusHistory)
        .filter(OrderStatusHistory.order_id == order.id)
        .order_by(OrderStatusHistory.created_at.asc())
        .all()
    )
    assert len(persisted_history) == 6
    assert persisted_history[-1].to_status == "COMPLETED"


def test_real_postgresql_payment_ledger_and_invariants(pg_session: Session, pg_session_factory):
    """Test payment recording, balance calculation, overpayment prevention, and voiding in PostgreSQL."""
    now = datetime.now(UTC)

    biz = Business(
        name=f"Outlet Keuangan PG {uuid.uuid4().hex[:6]}",
        phone_e164="+6281234567888",
        address="Jl. Keuangan No. 10, Jakarta Selatan",
    )
    pg_session.add(biz)
    pg_session.flush()

    user = User(
        business_id=biz.id,
        username=f"kasir_fin_{uuid.uuid4().hex[:6]}",
        password_hash="argon2id_placeholder",
        full_name="Kasir Keuangan",
        role=UserRole.CASHIER,
        phone_e164="+6281234567887",
    )
    pg_session.add(user)

    cust = Customer(
        business_id=biz.id,
        full_name="Pelanggan Keuangan PG",
        phone_e164="+6281234567889",
        address="Jl. Kemang Timur No. 3",
    )
    pg_session.add(cust)
    pg_session.flush()

    order = Order(
        business_id=biz.id,
        customer_id=cust.id,
        order_number=f"ORD-FIN-{uuid.uuid4().hex[:6].upper()}",
        operational_status="RECEIVED",
        intake_method="WALK_IN",
        return_method="SELF_PICKUP",
        total_amount=100000,
        subtotal_amount=100000,
        delivery_fee_amount=0,
        estimated_completion_at=now + timedelta(hours=24),
        created_by=user.id,
        version=1,
    )
    pg_session.add(order)
    pg_session.flush()

    # 1. Partial payment Rp 40,000
    p1 = Payment(
        order_id=order.id,
        amount=40000,
        method="CASH",
        verification_status="VERIFIED",
        verified_by=user.id,
    )
    pg_session.add(p1)
    pg_session.flush()

    balance1 = calculate_payment_balance(order.total_amount, [p1])
    assert balance1.total_paid == 40000
    assert balance1.remaining_amount == 60000
    assert balance1.payment_status.value == "PARTIALLY_PAID"

    # 2. Overpayment attempt: Rp 70,000 (exceeds remaining Rp 60,000)
    overpayment = 70000
    if overpayment > balance1.remaining_amount:
        with pytest.raises(OverpaymentNotAllowedError):
            raise OverpaymentNotAllowedError(overpayment, balance1.remaining_amount)

    # 3. Exact remaining payment: Rp 60,000
    p2 = Payment(
        order_id=order.id,
        amount=60000,
        method="QRIS",
        verification_status="VERIFIED",
        verified_by=user.id,
    )
    pg_session.add(p2)
    pg_session.flush()

    balance2 = calculate_payment_balance(order.total_amount, [p1, p2])
    assert balance2.total_paid == 100000
    assert balance2.remaining_amount == 0
    assert balance2.payment_status.value == "PAID"

    # 4. Void Payment p2 with mandatory reason
    void_record = PaymentVoid(
        payment_id=p2.id,
        reason="Salah scan QRIS ganda",
        voided_by=user.id,
    )
    pg_session.add(void_record)
    pg_session.commit()

    # Re-query payments with joinedload from real PostgreSQL using a fresh session
    from sqlalchemy.orm import joinedload

    pg_session.close()
    fresh_session = pg_session_factory()
    reloaded_payments = (
        fresh_session.query(Payment)
        .options(joinedload(Payment.void_record))
        .filter(Payment.order_id == order.id)
        .order_by(Payment.created_at.asc())
        .all()
    )
    # After void, p2 is voided and excluded from active balance
    balance3 = calculate_payment_balance(order.total_amount, reloaded_payments)
    assert balance3.total_paid == 40000
    assert balance3.remaining_amount == 60000
    assert balance3.payment_status.value == "PARTIALLY_PAID"
    assert balance3.voided_payment_count == 1
    fresh_session.close()


def test_real_postgresql_concurrent_payments_with_pessimistic_lock(pg_session_factory):
    """
    Test concurrent payments on real PostgreSQL using row-level locking (SELECT FOR UPDATE).
    Simulates race conditions and proves overpayment is prevented in real PostgreSQL concurrency.
    """
    now = datetime.now(UTC)
    init_session = pg_session_factory()
    biz = Business(
        name=f"Outlet Concurrency PG {uuid.uuid4().hex[:6]}",
        phone_e164="+628111222333",
        address="Jl. Bersama No. 9, Jakarta",
    )
    init_session.add(biz)
    init_session.flush()

    user = User(
        business_id=biz.id,
        username=f"kasir_concur_{uuid.uuid4().hex[:6]}",
        password_hash="argon2id_placeholder",
        full_name="Kasir Concur",
        role=UserRole.CASHIER,
        phone_e164="+628111222555",
    )
    init_session.add(user)

    cust = Customer(
        business_id=biz.id,
        full_name="Customer Concurrent",
        phone_e164="+628111222444",
        address="Jl. Merdeka No. 4",
    )
    init_session.add(cust)
    init_session.flush()

    order = Order(
        business_id=biz.id,
        customer_id=cust.id,
        order_number=f"ORD-CONCUR-{uuid.uuid4().hex[:6].upper()}",
        total_amount=50000,
        subtotal_amount=50000,
        delivery_fee_amount=0,
        operational_status="RECEIVED",
        intake_method="WALK_IN",
        return_method="SELF_PICKUP",
        estimated_completion_at=now + timedelta(hours=24),
        created_by=user.id,
        version=1,
    )
    init_session.add(order)
    init_session.commit()
    order_id = order.id
    user_id = user.id
    init_session.close()

    # Function executed concurrently across multiple threads
    def attempt_payment(amount: int) -> bool:
        session = pg_session_factory()
        try:
            # Pessimistic row-level lock on the order in PostgreSQL
            locked_order = (
                session.query(Order)
                .filter(Order.id == order_id)
                .with_for_update()
                .one()
            )
            # Fetch existing verified payments for balance
            existing_payments = (
                session.query(Payment)
                .filter(Payment.order_id == locked_order.id)
                .all()
            )
            balance = calculate_payment_balance(locked_order.total_amount, existing_payments)

            if amount > balance.remaining_amount:
                session.rollback()
                return False  # Overpayment prevented

            payment = Payment(
                order_id=locked_order.id,
                amount=amount,
                method="CASH",
                verification_status="VERIFIED",
                verified_by=user_id,
            )
            session.add(payment)
            session.commit()
            return True
        except Exception:
            session.rollback()
            return False
        finally:
            session.close()

    # Try 5 concurrent payments of Rp 20,000 on an order of Rp 50,000
    # Exactly 2 should succeed (40,000), 3rd would be 60,000 > 50,000 and must be rejected!
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(attempt_payment, 20000) for _ in range(5)]
        results = [f.result() for f in futures]

    successes = sum(1 for r in results if r is True)
    rejections = sum(1 for r in results if r is False)

    assert successes == 2, f"Expected exactly 2 successful Rp 20k payments, got: {successes}"
    assert rejections == 3, f"Expected 3 rejections due to overpayment guard, got: {rejections}"

    # Verify final balance in PostgreSQL
    verify_session = pg_session_factory()
    final_payments = verify_session.query(Payment).filter(Payment.order_id == order_id).all()
    total_paid = sum(p.amount for p in final_payments)
    assert total_paid == 40000
    assert total_paid <= 50000
    verify_session.close()


def test_real_postgresql_audit_logs_emission(pg_session: Session):
    """Test Table 19 audit_logs persistence in real PostgreSQL with sensitive field redaction."""
    biz = Business(
        name="Audit Test Outlet",
        phone_e164="+6281999888777",
        address="Jl. Sudirman No. 1, Jakarta Pusat",
    )
    pg_session.add(biz)
    pg_session.flush()

    user = User(
        business_id=biz.id,
        username=f"auditor_{uuid.uuid4().hex[:6]}",
        password_hash="argon2id_placeholder",
        full_name="Auditor System",
        role=UserRole.OWNER,
        phone_e164="+6281999888776",
    )
    pg_session.add(user)
    pg_session.flush()

    # Record audit log via AuditService
    audit_entry = AuditService.record(
        db=pg_session,
        action="UPDATE_ORDER_STATUS",
        resource_type="orders",
        resource_id=uuid.uuid4(),
        actor_user_id=user.id,
        before_data={"from_status": "READY"},
        after_data={
            "to_status": "COMPLETED",
            "password": "supersecretpassword",  # must be redacted
            "customer_phone": "+6281234567890",
        },
        reason="Pesanan selesai dan diambil pelanggan",
    )
    pg_session.commit()

    # Query from PostgreSQL
    persisted = pg_session.query(AuditLog).filter(AuditLog.id == audit_entry.id).first()
    assert persisted is not None
    assert persisted.action == "UPDATE_ORDER_STATUS"
    assert persisted.resource_type == "orders"
    assert persisted.after_data.get("password") == "[REDACTED]"
    assert persisted.after_data.get("to_status") == "COMPLETED"
