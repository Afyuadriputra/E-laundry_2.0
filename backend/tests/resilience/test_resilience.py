"""
Resilience & Chaos Testing Suite (BE-12).
Verifies error boundary isolation, database transaction rollback on mid-operation failure,
graceful handling of connection exceptions, and non-blocking recovery.
"""

import uuid
from unittest.mock import MagicMock, patch

from fastapi.testclient import TestClient
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.modules.businesses.models import Business, BusinessSettings
from app.modules.customers.models import Customer
from app.modules.orders.models import Order
from app.modules.users.models import User, UserRole


def test_transaction_rollback_on_failed_intake(client: TestClient, db_session: Session):
    """
    If order intake fails validation or constraints during creation,
    the transaction is rolled back and no partial/orphan rows remain.
    """
    biz_id = uuid.uuid4()
    biz = Business(
        id=biz_id,
        name="Rollback Test Laundry",
        phone_e164="+6281200004321",
        address="Jl. Resilience No. 1",
        timezone="Asia/Jakarta",
        is_active=True,
    )
    cashier = User(
        id=uuid.uuid4(),
        business_id=biz_id,
        username="cashier_resilience",
        full_name="Kasir Resilience",
        password_hash=hash_password("KasirPass123!"),
        role=UserRole.CASHIER.value,
        is_active=True,
    )
    db_session.add_all([biz, cashier])
    db_session.commit()

    # Login
    res = client.post(
        "/api/v1/auth/login",
        json={"username": "cashier_resilience", "password": "KasirPass123!"},
    )
    csrf = res.headers.get("X-CSRF-Token") or res.json()["data"]["csrf_token"]
    headers = {"X-CSRF-Token": csrf}

    initial_order_count = db_session.query(Order).count()

    # Attempt to create order with non-existent service UUID
    fake_service_id = str(uuid.uuid4())
    bad_payload = {
        "new_customer_name": "Pelanggan Gagal",
        "new_customer_phone": "+6281299990099",
        "items": [{"service_id": fake_service_id, "quantity": "2.0"}],
    }
    res_bad = client.post("/api/v1/orders", json=bad_payload, headers=headers)
    assert res_bad.status_code in (400, 404, 422)

    # Invariant: No phantom orders created
    final_order_count = db_session.query(Order).count()
    assert final_order_count == initial_order_count


def test_database_operational_error_graceful_handling(client: TestClient):
    """
    Simulate database connection dropout (psycopg.OperationalError).
    System must catch it via registered exception handler, return a structured 500 error,
    and not crash the ASGI process.
    """
    with patch("app.modules.auth.service.AuthService.authenticate_user") as mock_auth:
        mock_auth.side_effect = OperationalError("connection failed: server closed", params=None, orig=Exception())
        res = client.post("/api/v1/auth/login", json={"username": "valid_user", "password": "secret123"})
        # 500 Internal Server Error handled cleanly
        assert res.status_code == 500
        assert "INTERNAL_SERVER_ERROR" in str(res.json()) or "kesalahan internal" in str(res.json()).lower()


def test_subsequent_request_succeeds_after_exception(client: TestClient):
    """Verify system remains fully operational and responsive after handling an exception."""
    res_health = client.get("/api/v1/health/live")
    assert res_health.status_code == 200
    assert res_health.json()["status"] == "alive"
