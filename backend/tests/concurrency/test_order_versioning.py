"""
Concurrency & Optimistic Locking Test Suite (BE-06 / BSD §33 / PRD DEC-11).
Verifies that Order entity optimistic locking (version column) rejects stale writes
with HTTP 409 Conflict (VERSION_CONFLICT) and accepts updates with the current version.
"""

import uuid
from datetime import UTC, datetime, timedelta

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.modules.businesses.models import Business, BusinessSettings
from app.modules.customers.models import Customer
from app.modules.orders.models import Order
from app.modules.users.models import User, UserRole


def _setup_concurrency_order(
    client: TestClient, db_session: Session
) -> tuple[dict[str, str], Order]:
    biz_id = uuid.uuid4()
    biz = Business(
        id=biz_id,
        name="OCC Laundry Test",
        phone_e164="+6281200007788",
        address="Jl. Optimistic No. 7",
        timezone="Asia/Jakarta",
        is_active=True,
    )
    settings = BusinessSettings(id=uuid.uuid4(), business_id=biz_id)
    cashier = User(
        id=uuid.uuid4(),
        business_id=biz_id,
        username="cashier_occ",
        full_name="Kasir OCC",
        password_hash=hash_password("KasirPass123!"),
        role=UserRole.CASHIER.value,
        is_active=True,
    )
    cust = Customer(
        id=uuid.uuid4(),
        business_id=biz_id,
        full_name="Customer OCC",
        phone_e164="+6281277665544",
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
        order_number=f"OCC-{uuid.uuid4().hex[:6].upper()}",
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

    res = client.post("/api/v1/auth/login", json={"username": "cashier_occ", "password": "KasirPass123!"})
    csrf = res.headers.get("X-CSRF-Token") or res.json()["data"]["csrf_token"]
    headers = {"X-CSRF-Token": csrf}
    return headers, order


def test_optimistic_locking_stale_update_rejected_with_409(client: TestClient, db_session: Session):
    headers, order = _setup_concurrency_order(client, db_session)

    # Both Client A and Client B read order at version=1
    assert order.version == 1

    # Client A updates status: RECEIVED -> QUEUED (expected_version=1)
    res_a = client.post(
        f"/api/v1/orders/{order.id}/transition",
        json={"to_status": "QUEUED", "expected_version": 1},
        headers=headers,
    )
    assert res_a.status_code == 200
    assert res_a.json()["data"]["version"] == 2
    assert res_a.json()["data"]["operational_status"] == "QUEUED"

    # Client B attempts update with stale expected_version=1 -> Must Fail (409 Conflict)
    res_b = client.post(
        f"/api/v1/orders/{order.id}/transition",
        json={"to_status": "WASHING", "expected_version": 1},
        headers=headers,
    )
    assert res_b.status_code == 409
    body_b = res_b.json()
    assert "VERSION_CONFLICT" in str(body_b) or "Konflik versi" in str(body_b)

    # Client B refetches latest order version (2) and retries -> Succeeded
    res_b_retry = client.post(
        f"/api/v1/orders/{order.id}/transition",
        json={"to_status": "WASHING", "expected_version": 2},
        headers=headers,
    )
    assert res_b_retry.status_code == 200
    assert res_b_retry.json()["data"]["version"] == 3
    assert res_b_retry.json()["data"]["operational_status"] == "WASHING"

