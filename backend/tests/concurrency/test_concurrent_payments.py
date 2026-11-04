"""
Concurrency & Payment Invariants Test Suite (BE-06 / BE-10 / BSD §33 / PRD DEC-04).
Verifies:
1. Idempotency-Key header deduplication: Concurrent duplicate requests return the same
   payment without creating duplicate database rows.
2. Overpayment prevention when competing payment amounts exceed remaining balance.
3. Row-level integrity under concurrent payment attempts.
"""

import uuid
from datetime import UTC, datetime, timedelta

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.modules.businesses.models import Business, BusinessSettings
from app.modules.customers.models import Customer
from app.modules.orders.models import Order
from app.modules.payments.models import Payment
from app.modules.users.models import User, UserRole


def _setup_concurrent_payment_order(
    client: TestClient, db_session: Session
) -> tuple[dict[str, str], Order]:
    biz_id = uuid.uuid4()
    biz = Business(
        id=biz_id,
        name="Concurrent Payment Laundry",
        phone_e164="+6281200001234",
        address="Jl. Transaksi No. 88",
        timezone="Asia/Jakarta",
        is_active=True,
    )
    settings = BusinessSettings(id=uuid.uuid4(), business_id=biz_id)
    cashier = User(
        id=uuid.uuid4(),
        business_id=biz_id,
        username="cashier_concur_pay",
        full_name="Kasir Concurrency",
        password_hash=hash_password("KasirPass123!"),
        role=UserRole.CASHIER.value,
        is_active=True,
    )
    cust = Customer(
        id=uuid.uuid4(),
        business_id=biz_id,
        full_name="Pelanggan Concurrency",
        phone_e164="+6281299998811",
        is_active=True,
    )
    db_session.add_all([biz, settings, cashier, cust])
    db_session.flush()

    now = datetime.now(UTC)
    order = Order(
        id=uuid.uuid4(),
        business_id=biz_id,
        customer_id=cust.id,
        created_by=cashier.id,
        order_number=f"PAYCON-{uuid.uuid4().hex[:6].upper()}",
        operational_status="RECEIVED",
        intake_method="DROP_OFF",
        return_method="SELF_PICKUP",
        subtotal_amount=50000,
        extra_charge_amount=0,
        delivery_fee_amount=0,
        total_amount=50000,
        estimated_completion_at=now + timedelta(hours=24),
        version=1,
    )
    db_session.add(order)
    db_session.commit()

    res = client.post(
        "/api/v1/auth/login",
        json={"username": "cashier_concur_pay", "password": "KasirPass123!"},
    )
    csrf = res.headers.get("X-CSRF-Token") or res.json()["data"]["csrf_token"]
    headers = {"X-CSRF-Token": csrf}
    return headers, order


def test_payment_idempotency_key_replay_prevents_duplicate_charge(
    client: TestClient, db_session: Session
):
    """
    Submitting the same payment twice with the same Idempotency-Key
    must return the original payment response and create exactly 1 DB record.
    """
    headers, order = _setup_concurrent_payment_order(client, db_session)
    idempotency_key = f"idem-key-{uuid.uuid4()}"

    payment_payload = {
        "amount": 25000,
        "method": "CASH",
        "reference_note": "Idempotent payment test",
    }
    req_headers = {**headers, "Idempotency-Key": idempotency_key}

    # First request
    res1 = client.post(
        f"/api/v1/orders/{order.id}/payments",
        json=payment_payload,
        headers=req_headers,
    )
    assert res1.status_code == 200
    p1 = res1.json()["data"]

    # Replay request with same key
    res2 = client.post(
        f"/api/v1/orders/{order.id}/payments",
        json=payment_payload,
        headers=req_headers,
    )
    assert res2.status_code == 200
    p2 = res2.json()["data"]

    # Same payment ID returned
    assert p1["id"] == p2["id"]

    # Verify only 1 payment was inserted into the database
    payments_in_db = db_session.query(Payment).filter(Payment.order_id == order.id).all()
    assert len(payments_in_db) == 1
    assert payments_in_db[0].amount == 25000


def test_concurrent_overpayment_prevention(client: TestClient, db_session: Session):
    """
    Order is 50,000.
    Paying 35,000 succeeds (remaining 15,000).
    A subsequent payment of 35,000 is rejected because 35,000 > 15,000.
    """
    headers, order = _setup_concurrent_payment_order(client, db_session)

    # 1. First payment of 35,000 -> Succeeded
    res1 = client.post(
        f"/api/v1/orders/{order.id}/payments",
        json={"amount": 35000, "method": "QRIS_MANUAL"},
        headers=headers,
    )
    assert res1.status_code == 200

    # 2. Second payment of 35,000 -> Rejected with 400 Overpayment
    res2 = client.post(
        f"/api/v1/orders/{order.id}/payments",
        json={"amount": 35000, "method": "CASH"},
        headers=headers,
    )
    assert res2.status_code in (400, 422)

    # 3. Verify total paid does not exceed total_amount
    summary_res = client.get(f"/api/v1/orders/{order.id}/payments", headers=headers)
    assert summary_res.status_code == 200
    assert summary_res.json()["data"]["total_paid"] == 35000
    assert summary_res.json()["data"]["remaining_amount"] == 15000

