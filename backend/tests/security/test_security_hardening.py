import uuid
from datetime import UTC, datetime, timedelta

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.modules.businesses.models import Business
from app.modules.customers.models import Customer
from app.modules.orders.models import Order
from app.modules.users.models import User, UserRole


def test_cross_tenant_isolation_and_idor_prevention(client: TestClient, db_session: Session):
    """
    Verify multi-tenant isolation: User of Business A cannot view or manipulate
    records belonging to Business B (Anti-IDOR).
    """
    # Business A (Outlet Melati)
    biz_a = Business(
        id=uuid.uuid4(),
        name="Laundry Melati",
        phone_e164="+628111111111",
        address="Jl. Melati No. 1",
        timezone="Asia/Jakarta",
        is_active=True,
    )
    user_a = User(
        id=uuid.uuid4(),
        business_id=biz_a.id,
        username="kasir_melati",
        full_name="Kasir Melati",
        password_hash=hash_password("KasirMelati123!"),
        role=UserRole.CASHIER.value,
        is_active=True,
    )
    cust_a = Customer(
        id=uuid.uuid4(),
        business_id=biz_a.id,
        full_name="Pelanggan Melati",
        phone_e164="+628111222333",
    )

    # Business B (Outlet Mawar)
    biz_b = Business(
        id=uuid.uuid4(),
        name="Laundry Mawar",
        phone_e164="+628222222222",
        address="Jl. Mawar No. 2",
        timezone="Asia/Jakarta",
        is_active=True,
    )
    user_b = User(
        id=uuid.uuid4(),
        business_id=biz_b.id,
        username="kasir_mawar",
        full_name="Kasir Mawar",
        password_hash=hash_password("KasirMawar123!"),
        role=UserRole.CASHIER.value,
        is_active=True,
    )
    cust_b = Customer(
        id=uuid.uuid4(),
        business_id=biz_b.id,
        full_name="Pelanggan Rahasia Mawar",
        phone_e164="+628222333444",
    )
    order_b = Order(
        id=uuid.uuid4(),
        business_id=biz_b.id,
        customer_id=cust_b.id,
        created_by=user_b.id,
        order_number="ORD-MAWAR-001",
        operational_status="RECEIVED",
        intake_method="DROP_OFF",
        return_method="SELF_PICKUP",
        total_amount=50000,
        subtotal_amount=50000,
        estimated_completion_at=datetime.now(UTC) + timedelta(days=1),
    )

    db_session.add_all([biz_a, user_a, cust_a, biz_b, user_b, cust_b, order_b])
    db_session.commit()

    # Login as Kasir Melati (Business A)
    login_res = client.post(
        "/api/v1/auth/login",
        json={"username": "kasir_melati", "password": "KasirMelati123!"},
    )
    assert login_res.status_code == 200
    csrf = login_res.json()["data"]["csrf_token"]
    headers_a = {"X-CSRF-Token": csrf}

    # 1. Kasir Melati lists customers -> Should ONLY see Pelanggan Melati, NOT Pelanggan Mawar
    cust_list = client.get("/api/v1/customers", headers=headers_a)
    assert cust_list.status_code == 200
    c_names = [c["full_name"] for c in cust_list.json()["data"]]
    assert "Pelanggan Melati" in c_names
    assert "Pelanggan Rahasia Mawar" not in c_names

    # 2. Kasir Melati attempts direct IDOR fetch of Pelanggan B -> 404 Not Found
    idor_cust = client.get(f"/api/v1/customers/{cust_b.id}", headers=headers_a)
    assert idor_cust.status_code == 404

    # 3. Kasir Melati attempts direct IDOR fetch of Order B -> 404 Not Found
    idor_order = client.get(f"/api/v1/orders/{order_b.id}", headers=headers_a)
    assert idor_order.status_code == 404

    # 4. Kasir Melati attempts direct IDOR mutation of Order B status -> 404 Not Found
    idor_status = client.post(
        f"/api/v1/orders/{order_b.id}/status",
        json={"to_status": "WASHING"},
        headers=headers_a,
    )
    assert idor_status.status_code == 404


def test_csrf_header_strictly_enforced_on_mutations(client: TestClient, db_session: Session):
    """
    Verify that mutating HTTP endpoints strictly reject requests missing valid CSRF tokens.
    """
    biz = Business(
        id=uuid.uuid4(),
        name="Outlet Aman Bersih",
        phone_e164="+6281333333333",
        address="Jl. Keamanan Siber No. 10",
        timezone="Asia/Jakarta",
        is_active=True,
    )
    user = User(
        id=uuid.uuid4(),
        business_id=biz.id,
        username="kasir_aman",
        full_name="Kasir Aman",
        password_hash=hash_password("AmanPass123!"),
        role=UserRole.CASHIER.value,
        is_active=True,
    )
    db_session.add_all([biz, user])
    db_session.commit()

    # Login to establish authenticated session
    client.post(
        "/api/v1/auth/login",
        json={"username": "kasir_aman", "password": "AmanPass123!"},
    )

    # Attempt POST without CSRF header -> 403 Forbidden
    res_no_csrf = client.post(
        "/api/v1/customers",
        json={"full_name": "Pak Budi", "phone_e164": "+628123456789"},
    )
    assert res_no_csrf.status_code == 403
    assert "CSRF" in res_no_csrf.text

    # Attempt POST with forged / invalid CSRF header -> 403 Forbidden
    res_bad_csrf = client.post(
        "/api/v1/customers",
        json={"full_name": "Pak Budi", "phone_e164": "+628123456789"},
        headers={"X-CSRF-Token": "forged_malicious_token_12345"},
    )
    assert res_bad_csrf.status_code == 403
    assert "CSRF" in res_bad_csrf.text


def test_invalid_and_expired_public_tracking_tokens(client: TestClient):
    """
    Verify that guessing non-existent or malformed public tracking tokens
    safely yields 404 without database leaks or stack traces.
    """
    # 1. Non-existent token
    fake_token = "completely_non_existent_token_random_entropy_xyz123"
    res_fake = client.get(f"/api/v1/tracking/{fake_token}")
    assert res_fake.status_code == 404
    assert res_fake.headers.get("Cache-Control") == "no-store, no-cache, must-revalidate, max-age=0"
    assert res_fake.headers.get("Referrer-Policy") == "no-referrer"

    # 2. SQL injection payload as token
    sqli_token = "' OR '1'='1"
    res_sqli = client.get(f"/api/v1/tracking/{sqli_token}")
    assert res_sqli.status_code == 404

