import uuid
from datetime import UTC, datetime

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.modules.businesses.models import Business, BusinessSettings
from app.modules.customers.models import Customer
from app.modules.orders.models import Order
from app.modules.users.models import User, UserRole


def _login(client: TestClient, username: str, password: str) -> dict[str, str]:
    res = client.post("/api/v1/auth/login", json={"username": username, "password": password})
    assert res.status_code == 200
    csrf = res.json()["data"]["csrf_token"]
    return {"X-CSRF-Token": csrf}


def test_payments_api_full_flow(client: TestClient, db_session: Session):
    business_id = uuid.uuid4()
    business = Business(
        id=business_id,
        name="Laundry Berkah Finansial",
        phone_e164="+6281299998888",
        address="Jl. Sudirman 45",
        timezone="Asia/Jakarta",
        is_active=True,
    )
    settings = BusinessSettings(
        id=uuid.uuid4(),
        business_id=business_id,
        pickup_enabled=True,
        delivery_enabled=True,
    )
    db_session.add(business)
    db_session.add(settings)

    # Owner
    owner = User(
        id=uuid.uuid4(),
        business_id=business_id,
        username="owner_finance",
        full_name="Pak Bos Finance",
        password_hash=hash_password("OwnerFinance123!"),
        role=UserRole.OWNER.value,
        is_active=True,
    )
    # Cashier
    cashier = User(
        id=uuid.uuid4(),
        business_id=business_id,
        username="kasir_finance",
        full_name="Kasir Finance",
        password_hash=hash_password("KasirFinance123!"),
        role=UserRole.CASHIER.value,
        is_active=True,
    )
    customer = Customer(
        id=uuid.uuid4(),
        business_id=business_id,
        full_name="Pak Hendra",
        phone_e164="+6281234567888",
        is_active=True,
    )
    db_session.add_all([owner, cashier, customer])
    db_session.commit()

    # Create Order (total = 50,000)
    order_id = uuid.uuid4()
    order = Order(
        id=order_id,
        business_id=business_id,
        order_number="ORD-20261103-PAY1",
        customer_id=customer.id,
        created_by=cashier.id,
        operational_status="RECEIVED",
        intake_method="DROP_OFF",
        return_method="SELF_PICKUP",
        subtotal_amount=50000,
        extra_charge_amount=0,
        delivery_fee_amount=0,
        total_amount=50000,
        estimated_completion_at=datetime.now(UTC),
        version=1,
    )
    db_session.add(order)
    db_session.commit()

    # 1. Login as Cashier
    cashier_headers = _login(client, "kasir_finance", "KasirFinance123!")

    # Initial payment summary: UNPAID
    res = client.get(f"/api/v1/orders/{order_id}/payments")
    assert res.status_code == 200
    summary = res.json()["data"]
    assert summary["total_amount"] == 50000
    assert summary["total_paid"] == 0
    assert summary["remaining_amount"] == 50000
    assert summary["payment_status"] == "UNPAID"
    assert len(summary["payments"]) == 0

    # 2. Record Down Payment (DP): 20,000 CASH with Idempotency-Key
    idem_key = "idem-pay-001"
    pay_payload = {
        "amount": 20000,
        "method": "CASH",
        "reference_note": "Uang muka 20rb",
    }
    res_pay1 = client.post(
        f"/api/v1/orders/{order_id}/payments",
        json=pay_payload,
        headers={**cashier_headers, "Idempotency-Key": idem_key},
    )
    assert res_pay1.status_code == 200
    pay1_data = res_pay1.json()["data"]
    pay1_id = pay1_data["id"]
    assert pay1_data["amount"] == 20000
    assert pay1_data["method"] == "CASH"
    assert pay1_data["is_voided"] is False

    # 3. Test Idempotency: retry exact same request
    res_idem = client.post(
        f"/api/v1/orders/{order_id}/payments",
        json=pay_payload,
        headers={**cashier_headers, "Idempotency-Key": idem_key},
    )
    assert res_idem.status_code == 200
    assert res_idem.json()["data"]["id"] == pay1_id

    # Verify balance: PARTIALLY_PAID
    res = client.get(f"/api/v1/orders/{order_id}/payments")
    summary = res.json()["data"]
    assert summary["total_paid"] == 20000
    assert summary["remaining_amount"] == 30000
    assert summary["payment_status"] == "PARTIALLY_PAID"
    assert len(summary["payments"]) == 1

    # 4. Attempt Overpayment: paying 40,000 when remaining is 30,000
    res_over = client.post(
        f"/api/v1/orders/{order_id}/payments",
        json={"amount": 40000, "method": "BANK_TRANSFER"},
        headers=cashier_headers,
    )
    assert res_over.status_code == 422
    assert res_over.json()["error"]["code"] == "OVERPAYMENT_NOT_ALLOWED"

    # 5. Full settlement: pay 30,000 via BANK_TRANSFER
    res_pay2 = client.post(
        f"/api/v1/orders/{order_id}/payments",
        json={"amount": 30000, "method": "BANK_TRANSFER", "reference_note": "Pelunasan transfer"},
        headers=cashier_headers,
    )
    assert res_pay2.status_code == 200
    pay2_data = res_pay2.json()["data"]
    pay2_id = pay2_data["id"]

    # Verify balance: PAID
    res = client.get(f"/api/v1/orders/{order_id}/payments")
    summary = res.json()["data"]
    assert summary["total_paid"] == 50000
    assert summary["remaining_amount"] == 0
    assert summary["payment_status"] == "PAID"

    # 6. Cashier attempts to void payment -> 403 Forbidden
    res_cashier_void = client.post(
        f"/api/v1/payments/{pay2_id}/void",
        json={"reason": "Pembatalan oleh kasir"},
        headers=cashier_headers,
    )
    assert res_cashier_void.status_code == 403

    # 7. Owner voids pay2 (30,000)
    owner_headers = _login(client, "owner_finance", "OwnerFinance123!")
    res_void = client.post(
        f"/api/v1/payments/{pay2_id}/void",
        json={"reason": "Transfer salah nominal ke rekening lain"},
        headers=owner_headers,
    )
    assert res_void.status_code == 200
    void_data = res_void.json()["data"]
    assert void_data["is_voided"] is True
    assert void_data["void_reason"] == "Transfer salah nominal ke rekening lain"

    # Balance after void: PARTIALLY_PAID (remaining: 30,000)
    res = client.get(f"/api/v1/orders/{order_id}/payments")
    summary = res.json()["data"]
    assert summary["total_paid"] == 20000
    assert summary["remaining_amount"] == 30000
    assert summary["payment_status"] == "PARTIALLY_PAID"

    # 8. Attempt double void -> 409 Conflict
    res_double_void = client.post(
        f"/api/v1/payments/{pay2_id}/void",
        json={"reason": "Void ulang"},
        headers=owner_headers,
    )
    assert res_double_void.status_code == 409
    assert res_double_void.json()["error"]["code"] == "PAYMENT_ALREADY_VOIDED"
