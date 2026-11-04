"""
Deep Integration Test Suite for Payments (BE-02 / BE-05 / BE-10).
Covers down payments (DP), multiple installments, overpayment prevention,
owner-only payment voiding with audit reasons, and payment summary ledger accuracy.
"""

import uuid
from datetime import UTC, datetime, timedelta

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.modules.businesses.models import Business, BusinessSettings
from app.modules.customers.models import Customer
from app.modules.orders.models import Order
from app.modules.payments.models import Payment, PaymentVoid
from app.modules.users.models import User, UserRole


def _setup_payment_test_env(
    client: TestClient, db_session: Session
) -> tuple[dict[str, str], dict[str, str], Business, Order]:
    biz_id = uuid.uuid4()
    biz = Business(
        id=biz_id,
        name="Payment Test Laundry",
        phone_e164="+6281200008888",
        address="Jl. Pembayaran No. 1",
        timezone="Asia/Jakarta",
        is_active=True,
    )
    settings = BusinessSettings(
        id=uuid.uuid4(),
        business_id=biz_id,
    )
    db_session.add_all([biz, settings])

    # Owner user
    owner = User(
        id=uuid.uuid4(),
        business_id=biz_id,
        username="owner_pay",
        full_name="Bapak Bos Owner",
        password_hash=hash_password("OwnerPass123!"),
        role=UserRole.OWNER.value,
        is_active=True,
    )
    # Cashier user
    cashier = User(
        id=uuid.uuid4(),
        business_id=biz_id,
        username="cashier_pay",
        full_name="Mbak Kasir Pay",
        password_hash=hash_password("CashierPass123!"),
        role=UserRole.CASHIER.value,
        is_active=True,
    )
    cust = Customer(
        id=uuid.uuid4(),
        business_id=biz_id,
        full_name="Pelanggan Bayar",
        phone_e164="+6281234560001",
        is_active=True,
    )
    db_session.add_all([owner, cashier, cust])
    db_session.flush()

    # Create Order total 100,000
    now = datetime.now(UTC)
    order = Order(
        id=uuid.uuid4(),
        business_id=biz_id,
        customer_id=cust.id,
        created_by=cashier.id,
        order_number=f"PAY-{uuid.uuid4().hex[:6].upper()}",
        operational_status="RECEIVED",
        intake_method="DROP_OFF",
        return_method="SELF_PICKUP",
        subtotal_amount=100000,
        extra_charge_amount=0,
        delivery_fee_amount=0,
        total_amount=100000,
        estimated_completion_at=now + timedelta(hours=24),
        version=1,
    )
    db_session.add(order)
    db_session.commit()

    # Login owner
    res_o = client.post("/api/v1/auth/login", json={"username": "owner_pay", "password": "OwnerPass123!"})
    csrf_o = res_o.headers.get("X-CSRF-Token") or res_o.json()["data"]["csrf_token"]
    owner_headers = {"X-CSRF-Token": csrf_o}

    # Login cashier
    res_c = client.post("/api/v1/auth/login", json={"username": "cashier_pay", "password": "CashierPass123!"})
    csrf_c = res_c.headers.get("X-CSRF-Token") or res_c.json()["data"]["csrf_token"]
    cashier_headers = {"X-CSRF-Token": csrf_c}

    return owner_headers, cashier_headers, biz, order


def test_payment_installments_and_overpayment_prevention(client: TestClient, db_session: Session):
    owner_headers, cashier_headers, biz, order = _setup_payment_test_env(client, db_session)

    # 1. Check initial payment summary: remaining = 100,000, status UNPAID
    sum_res1 = client.get(f"/api/v1/orders/{order.id}/payments", headers=cashier_headers)
    assert sum_res1.status_code == 200
    assert sum_res1.json()["data"]["payment_status"] == "UNPAID"
    assert sum_res1.json()["data"]["remaining_amount"] == 100000

    # 2. Pay DP: 40,000 CASH
    pay1_res = client.post(
        f"/api/v1/orders/{order.id}/payments",
        json={"amount": 40000, "method": "CASH", "reference_note": "Uang muka"},
        headers=cashier_headers,
    )
    assert pay1_res.status_code == 200
    assert pay1_res.json()["data"]["amount"] == 40000

    # Summary after DP: remaining = 60,000, status PARTIALLY_PAID
    sum_res2 = client.get(f"/api/v1/orders/{order.id}/payments", headers=cashier_headers)
    assert sum_res2.status_code == 200
    assert sum_res2.json()["data"]["payment_status"] == "PARTIALLY_PAID"
    assert sum_res2.json()["data"]["total_paid"] == 40000
    assert sum_res2.json()["data"]["remaining_amount"] == 60000

    # 3. Attempt Overpayment: paying 70,000 when remaining is 60,000 -> Must Fail (400)
    overpay_res = client.post(
        f"/api/v1/orders/{order.id}/payments",
        json={"amount": 70000, "method": "QRIS_MANUAL"},
        headers=cashier_headers,
    )
    assert overpay_res.status_code in (400, 422)

    # 4. Pay remaining 60,000 with BANK_TRANSFER
    pay2_res = client.post(
        f"/api/v1/orders/{order.id}/payments",
        json={"amount": 60000, "method": "BANK_TRANSFER", "reference_note": "Pelunasan via BCA"},
        headers=cashier_headers,
    )
    assert pay2_res.status_code == 200

    # Summary after pelunasan: remaining = 0, status PAID
    sum_res3 = client.get(f"/api/v1/orders/{order.id}/payments", headers=cashier_headers)
    assert sum_res3.status_code == 200
    assert sum_res3.json()["data"]["payment_status"] == "PAID"
    assert sum_res3.json()["data"]["total_paid"] == 100000
    assert sum_res3.json()["data"]["remaining_amount"] == 0


def _login(client: TestClient, username: str, password: str) -> dict[str, str]:
    res = client.post("/api/v1/auth/login", json={"username": username, "password": password})
    assert res.status_code == 200
    csrf = res.headers.get("X-CSRF-Token") or res.json()["data"]["csrf_token"]
    return {"X-CSRF-Token": csrf}


def test_payment_void_by_owner_only(client: TestClient, db_session: Session):
    _, _, biz, order = _setup_payment_test_env(client, db_session)

    # 1. Login as Cashier and record a payment of 50,000
    cashier_headers = _login(client, "cashier_pay", "CashierPass123!")
    pay_res = client.post(
        f"/api/v1/orders/{order.id}/payments",
        json={"amount": 50000, "method": "QRIS_MANUAL"},
        headers=cashier_headers,
    )
    assert pay_res.status_code == 200
    payment_id = pay_res.json()["data"]["id"]

    # 2. Cashier attempts to void payment -> Must Fail (403 Forbidden)
    res_cashier_void = client.post(
        f"/api/v1/payments/{payment_id}/void",
        json={"reason": "Kasir salah input nominal"},
        headers=cashier_headers,
    )
    assert res_cashier_void.status_code == 403

    # 3. Switch login to Owner and void payment with valid reason -> 200 OK
    owner_headers = _login(client, "owner_pay", "OwnerPass123!")
    res_owner_void = client.post(
        f"/api/v1/payments/{payment_id}/void",
        json={"reason": "Pembayaran dibatalkan karena mutasi bank tidak masuk"},
        headers=owner_headers,
    )
    assert res_owner_void.status_code == 200

    # 4. Verify Payment summary reflects voided payment
    sum_res = client.get(f"/api/v1/orders/{order.id}/payments", headers=owner_headers)
    assert sum_res.status_code == 200
    # Remaining returned to 100,000, paid returned to 0
    assert sum_res.json()["data"]["total_paid"] == 0
    assert sum_res.json()["data"]["remaining_amount"] == 100000
    assert sum_res.json()["data"]["payment_status"] == "UNPAID"
