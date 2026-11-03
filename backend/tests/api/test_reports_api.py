import uuid
from datetime import UTC, date, datetime, timedelta
from decimal import Decimal

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.modules.businesses.models import Business
from app.modules.customers.models import Customer
from app.modules.expenses.models import Expense
from app.modules.orders.models import Order, OrderItem
from app.modules.payments.models import Payment, PaymentVoid
from app.modules.services.models import Service
from app.modules.users.models import User, UserRole


def test_reports_reconciliation_and_lifecycle(client: TestClient, db_session: Session):
    # 1. Setup Business, Owner, Cashier
    business = Business(
        id=uuid.uuid4(),
        name="Klinika Laundry Sukses",
        phone_e164="+6281234567890",
        address="Jl. Riau No. 88, Bandung",
        timezone="Asia/Jakarta",
        is_active=True,
    )
    owner = User(
        id=uuid.uuid4(),
        business_id=business.id,
        username="owner_hendra",
        full_name="Hendra Pemilik",
        password_hash=hash_password("OwnerPass123!"),
        role=UserRole.OWNER.value,
        is_active=True,
    )
    cashier = User(
        id=uuid.uuid4(),
        business_id=business.id,
        username="kasir_maya",
        full_name="Maya Kasir",
        password_hash=hash_password("KasirPass123!"),
        role=UserRole.CASHIER.value,
        is_active=True,
    )
    customer = Customer(
        id=uuid.uuid4(),
        business_id=business.id,
        full_name="=HYPERLINK(\"http://evil.com\")",  # Formula injection payload candidate
        phone_e164="+6281211223344",
        address="Kompleks Indah No. 1",
    )
    service = Service(
        id=uuid.uuid4(),
        business_id=business.id,
        name="Cuci Setrika Kilat",
        pricing_type="PER_KG",
        unit="KG",
        unit_price=10000,
        is_active=True,
    )
    db_session.add_all([business, owner, cashier, customer, service])
    db_session.commit()

    now = datetime.now(UTC)

    # 2. Seed Orders:
    # Order 1: Active, Total 50.000, Paid 30.000, Remaining 20.000
    order1 = Order(
        id=uuid.uuid4(),
        business_id=business.id,
        customer_id=customer.id,
        created_by=cashier.id,
        order_number="ORD-20261103-0101",
        operational_status="WASHING",
        intake_method="DROP_OFF",
        return_method="SELF_PICKUP",
        created_at=now - timedelta(hours=2),
        estimated_completion_at=now + timedelta(hours=10),
        subtotal_amount=50000,
        total_amount=50000,
    )
    item1 = OrderItem(
        id=uuid.uuid4(),
        order_id=order1.id,
        service_id=service.id,
        service_name_snapshot="Cuci Setrika Kilat",
        pricing_type_snapshot="PER_KG",
        unit_snapshot="KG",
        unit_price_snapshot=10000,
        quantity=Decimal("5.0"),
        line_total_amount=50000,
        requires_ironing_snapshot=False,
    )
    pay1 = Payment(
        id=uuid.uuid4(),
        order_id=order1.id,
        verified_by=cashier.id,
        amount=30000,
        method="CASH",
        created_at=now - timedelta(hours=2),
    )

    # Order 2: Overdue (estimated_completion_at was 5 hours ago), Total 30.000, Unpaid
    order2 = Order(
        id=uuid.uuid4(),
        business_id=business.id,
        customer_id=customer.id,
        created_by=cashier.id,
        order_number="ORD-20261103-0102",
        operational_status="DRYING",
        intake_method="DROP_OFF",
        return_method="SELF_PICKUP",
        created_at=now - timedelta(hours=12),
        estimated_completion_at=now - timedelta(hours=5),
        subtotal_amount=30000,
        total_amount=30000,
    )

    # Order 3: Cancelled (Should be strictly excluded from order value and outstanding)
    order3 = Order(
        id=uuid.uuid4(),
        business_id=business.id,
        customer_id=customer.id,
        created_by=cashier.id,
        order_number="ORD-20261103-0103",
        operational_status="CANCELLED",
        intake_method="DROP_OFF",
        return_method="SELF_PICKUP",
        created_at=now - timedelta(hours=1),
        estimated_completion_at=now + timedelta(hours=24),
        subtotal_amount=100000,
        total_amount=100000,
    )

    # Order 4: Ready for pickup, Fully paid
    order4 = Order(
        id=uuid.uuid4(),
        business_id=business.id,
        customer_id=customer.id,
        created_by=cashier.id,
        order_number="ORD-20261103-0104",
        operational_status="READY",
        intake_method="DROP_OFF",
        return_method="SELF_PICKUP",
        created_at=now - timedelta(hours=8),
        estimated_completion_at=now + timedelta(hours=2),
        subtotal_amount=25000,
        total_amount=25000,
    )
    pay4 = Payment(
        id=uuid.uuid4(),
        order_id=order4.id,
        verified_by=cashier.id,
        amount=25000,
        method="QRIS",
        created_at=now - timedelta(hours=7),
    )

    # Voided Payment (Should be strictly excluded from cash received)
    pay_voided = Payment(
        id=uuid.uuid4(),
        order_id=order1.id,
        verified_by=cashier.id,
        amount=20000,
        method="TRANSFER",
        created_at=now - timedelta(hours=1),
    )
    void_record = PaymentVoid(
        id=uuid.uuid4(),
        payment_id=pay_voided.id,
        reason="Pelanggan keliru transfer ke rekening lama",
        voided_by=cashier.id,
    )

    # Expenses: 15.000 for Detergent
    expense1 = Expense(
        id=uuid.uuid4(),
        business_id=business.id,
        created_by=owner.id,
        category="DETERGENT",
        amount=15000,
        expense_date=date.today(),
        description="Beli deterjen cair sachet",
    )

    db_session.add_all([order1, item1, pay1, order2, order3, order4, pay4, pay_voided, void_record, expense1])
    db_session.commit()

    # 3. Test Owner Dashboard
    owner_login = client.post(
        "/api/v1/auth/login",
        json={"username": "owner_hendra", "password": "OwnerPass123!"},
    )
    assert owner_login.status_code == 200
    owner_headers = {"X-CSRF-Token": owner_login.json()["data"]["csrf_token"]}

    dash_res = client.get("/api/v1/reports/dashboard", headers=owner_headers)
    assert dash_res.status_code == 200
    d_data = dash_res.json()["data"]

    # Operational metrics
    assert d_data["orders_count_today"] == 3  # order1, order2, order4 (order3 cancelled is excluded)
    assert d_data["active_orders_count"] == 2  # order1 (WASHING), order2 (DRYING)
    assert d_data["ready_orders_count"] == 1   # order4 (READY)
    assert d_data["overdue_orders_count"] == 1 # order2

    # Financial Reconciliation
    # Order Value = 50.000 (order1) + 30.000 (order2) + 25.000 (order4) = 105.000 (order3 cancelled excluded)
    assert d_data["order_value_period"] == 105000

    # Cash Received = 30.000 (pay1) + 25.000 (pay4) = 55.000 (pay_voided 20.000 is excluded!)
    assert d_data["cash_received_period"] == 55000

    # Expenses = 15.000
    assert d_data["expenses_period"] == 15000

    # Simple Cash Difference = 55.000 - 15.000 = 40.000
    assert d_data["simple_cash_difference"] == 40000

    # Outstanding Receivables = 20.000 (order1 remaining) + 30.000 (order2 remaining) = 50.000
    assert d_data["outstanding_receivables"] == 50000

    # 4. Test Overdue Orders Endpoint
    overdue_res = client.get("/api/v1/reports/overdue", headers=owner_headers)
    assert overdue_res.status_code == 200
    ov_data = overdue_res.json()["data"]
    assert len(ov_data) == 1
    assert ov_data[0]["order_number"] == "ORD-20261103-0102"
    assert ov_data[0]["hours_overdue"] >= 4.9

    # 5. Test Financial Breakdown Endpoint
    fin_res = client.get("/api/v1/reports/finances", headers=owner_headers)
    assert fin_res.status_code == 200
    f_data = fin_res.json()["data"]
    assert f_data["total_cash_received"] == 55000
    assert f_data["cash_by_method"]["CASH"] == 30000
    assert f_data["cash_by_method"]["QRIS"] == 25000
    assert f_data["total_expenses"] == 15000
    assert f_data["simple_cash_difference"] == 40000

    # 6. Test Outstanding Report Endpoint
    out_res = client.get("/api/v1/reports/outstanding", headers=owner_headers)
    assert out_res.status_code == 200
    out_data = out_res.json()["data"]
    assert len(out_data) == 2  # order1 (20.000) and order2 (30.000)

    # 7. Test CSV Exports & Formula Sanitization
    csv_orders = client.get("/api/v1/reports/export/orders.csv", headers=owner_headers)
    assert csv_orders.status_code == 200
    assert "text/csv" in csv_orders.headers["Content-Type"]
    csv_text = csv_orders.text
    assert "No. Pesanan" in csv_text
    assert "ORD-20261103-0101" in csv_text
    # Check that customer name with '=' was prepended with single quote
    assert "'=HYPERLINK" in csv_text

    csv_payments = client.get("/api/v1/reports/export/payments.csv", headers=owner_headers)
    assert csv_payments.status_code == 200
    assert "text/csv" in csv_payments.headers["Content-Type"]

    csv_expenses = client.get("/api/v1/reports/export/expenses.csv", headers=owner_headers)
    assert csv_expenses.status_code == 200
    assert "text/csv" in csv_expenses.headers["Content-Type"]

    # 8. Test Cashier Access Restrictions
    cashier_login = client.post(
        "/api/v1/auth/login",
        json={"username": "kasir_maya", "password": "KasirPass123!"},
    )
    assert cashier_login.status_code == 200
    cashier_headers = {"X-CSRF-Token": cashier_login.json()["data"]["csrf_token"]}

    # Cashier sees dashboard operational metrics, but financial KPIs are None!
    c_dash = client.get("/api/v1/reports/dashboard", headers=cashier_headers)
    assert c_dash.status_code == 200
    cd_data = c_dash.json()["data"]
    assert cd_data["orders_count_today"] == 3
    assert cd_data["order_value_period"] is None
    assert cd_data["cash_received_period"] is None
    assert cd_data["simple_cash_difference"] is None

    # Cashier is FORBIDDEN from accessing owner financial report
    c_fin = client.get("/api/v1/reports/finances", headers=cashier_headers)
    assert c_fin.status_code == 403

    # Cashier is FORBIDDEN from exporting payments and expenses
    c_exp_p = client.get("/api/v1/reports/export/payments.csv", headers=cashier_headers)
    assert c_exp_p.status_code == 403

    c_exp_e = client.get("/api/v1/reports/export/expenses.csv", headers=cashier_headers)
    assert c_exp_e.status_code == 403
