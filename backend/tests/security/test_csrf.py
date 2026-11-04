"""
Security test suite for Double Submit CSRF token protection.
Verifies that mutating HTTP endpoints require valid X-CSRF-Token headers
matching the authenticated session, while safe methods and exempt public
endpoints operate properly.
"""

import uuid

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.modules.businesses.models import Business, BusinessSettings
from app.modules.users.models import User, UserRole


def _create_authenticated_owner(
    client: TestClient, db_session: Session
) -> tuple[dict[str, str], Business, User]:
    business = Business(
        id=uuid.uuid4(),
        name="CSRF Guard Laundry",
        phone_e164="+628111999888",
        address="Jl. Keamanan No. 1",
        timezone="Asia/Jakarta",
        is_active=True,
    )
    settings = BusinessSettings(
        id=uuid.uuid4(),
        business_id=business.id,
    )
    db_session.add(business)
    db_session.add(settings)

    raw_password = "OwnerSecurePass123!"
    user = User(
        id=uuid.uuid4(),
        business_id=business.id,
        username="owner_csrf_test",
        full_name="Bapak CSRF",
        password_hash=hash_password(raw_password),
        role=UserRole.OWNER.value,
        is_active=True,
    )
    db_session.add(user)
    db_session.commit()

    login_resp = client.post(
        "/api/v1/auth/login",
        json={"username": user.username, "password": raw_password},
    )
    assert login_resp.status_code == 200
    csrf_token = login_resp.headers.get("X-CSRF-Token") or login_resp.json()["data"]["csrf_token"]
    headers = {"X-CSRF-Token": csrf_token}
    return headers, business, user


def test_get_csrf_endpoint(client: TestClient):
    """GET /api/v1/auth/csrf returns a valid CSRF token in header and body."""
    resp = client.get("/api/v1/auth/csrf")
    assert resp.status_code == 200
    data = resp.json()["data"]
    assert "csrf_token" in data
    assert len(data["csrf_token"]) >= 20
    assert resp.headers.get("X-CSRF-Token") == data["csrf_token"]


def test_mutating_request_missing_csrf_rejected(client: TestClient, db_session: Session):
    """POST /api/v1/customers without X-CSRF-Token must be rejected with 403 Forbidden."""
    headers, _, _ = _create_authenticated_owner(client, db_session)

    # Attempt customer creation without CSRF header
    customer_payload = {
        "full_name": "Pelanggan Tanpa CSRF",
        "phone_e164": "+6281299990001",
        "address": "Jl. Bypass",
    }
    resp = client.post("/api/v1/customers", json=customer_payload)
    assert resp.status_code == 403
    assert "CSRF" in resp.json().get("detail", "") or "CSRF" in str(resp.json())


def test_mutating_request_invalid_csrf_rejected(client: TestClient, db_session: Session):
    """POST /api/v1/customers with invalid X-CSRF-Token must be rejected with 403 Forbidden."""
    headers, _, _ = _create_authenticated_owner(client, db_session)

    customer_payload = {
        "full_name": "Pelanggan Invalid CSRF",
        "phone_e164": "+6281299990002",
        "address": "Jl. Bypass",
    }
    resp = client.post(
        "/api/v1/customers",
        json=customer_payload,
        headers={"X-CSRF-Token": "completely_fake_invalid_csrf_token_value"},
    )
    assert resp.status_code == 403


def test_mutating_request_valid_csrf_accepted(client: TestClient, db_session: Session):
    """POST /api/v1/customers with valid X-CSRF-Token succeeds."""
    headers, _, _ = _create_authenticated_owner(client, db_session)

    customer_payload = {
        "full_name": "Pelanggan Valid CSRF",
        "phone_e164": "+6281299990003",
        "address": "Jl. Bypass",
    }
    resp = client.post("/api/v1/customers", json=customer_payload, headers=headers)
    assert resp.status_code in (200, 201)
    assert resp.json()["data"]["full_name"] == "Pelanggan Valid CSRF"


def test_safe_get_method_does_not_require_csrf(client: TestClient, db_session: Session):
    """GET /api/v1/customers does not require X-CSRF-Token."""
    _, _, _ = _create_authenticated_owner(client, db_session)

    # Calling GET without X-CSRF-Token header
    resp = client.get("/api/v1/customers")
    assert resp.status_code == 200
    assert isinstance(resp.json()["data"], list)
