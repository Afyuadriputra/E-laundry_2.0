"""
Security test suite for Public Customer Tracking Token Access.
Verifies cryptographic token entropy, SHA-256 token hashing, IDOR prevention,
PII minimization, caching header security, and token cancellation guards.
"""

import hashlib
import uuid
from datetime import UTC, datetime, timedelta

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.modules.businesses.models import Business
from app.modules.customers.models import Customer
from app.modules.orders.models import Order
from app.modules.tracking.models import TrackingToken
from app.modules.tracking.service import TrackingService
from app.modules.users.models import User, UserRole


def _setup_order_with_tracking(
    db_session: Session,
    operational_status: str = "RECEIVED",
    expires_in_hours: int = 72,
) -> tuple[Business, Order, str]:
    biz = Business(
        id=uuid.uuid4(),
        name="Crypto Tracking Laundry",
        phone_e164="+6281200007777",
        address="Jl. Kripto No. 1",
        timezone="Asia/Jakarta",
        is_active=True,
    )
    user = User(
        id=uuid.uuid4(),
        business_id=biz.id,
        username=f"cashier_{uuid.uuid4().hex[:6]}",
        full_name="Kasir Tracking",
        password_hash=hash_password("KasirPass123!"),
        role=UserRole.CASHIER.value,
        is_active=True,
    )
    cust = Customer(
        id=uuid.uuid4(),
        business_id=biz.id,
        full_name="Raden Mas Danang",
        phone_e164="+6281233445566",
        is_active=True,
    )
    db_session.add_all([biz, user, cust])
    db_session.flush()

    now = datetime.now(UTC)
    order = Order(
        id=uuid.uuid4(),
        business_id=biz.id,
        customer_id=cust.id,
        created_by=user.id,
        order_number=f"TRK-{uuid.uuid4().hex[:6].upper()}",
        operational_status=operational_status,
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
    db_session.flush()

    token_record, raw_token = TrackingService.create_order_tracking_token(
        db_session,
        order.id,
        created_by=user.id,
        ttl_days=3,
    )
    return biz, order, raw_token


def test_tracking_token_entropy_and_hash_storage(db_session: Session):
    """Verify raw token has >= 256 bits entropy and DB stores SHA-256 hash."""
    _, order, raw_token = _setup_order_with_tracking(db_session)

    # 32 bytes URL-safe base64 is 43+ chars (256 bits entropy)
    assert len(raw_token) >= 43

    # Database record must NOT store plaintext token
    token_record = db_session.query(TrackingToken).filter(TrackingToken.order_id == order.id).first()
    assert token_record is not None
    assert token_record.token_hash != raw_token
    # Verify hash matches sha256(raw_token)
    expected_hash = hashlib.sha256(raw_token.encode("utf-8")).hexdigest()
    assert token_record.token_hash == expected_hash


def test_public_tracking_headers_and_pii_minimization(client: TestClient, db_session: Session):
    """Verify security headers (no-store, no-referrer) and PII masking."""
    _, _, raw_token = _setup_order_with_tracking(db_session)

    resp = client.get(f"/api/v1/tracking/{raw_token}")
    assert resp.status_code == 200

    # Privacy and Anti-Leak Headers per BSD §34.4
    assert "no-store" in resp.headers.get("Cache-Control", "")
    assert resp.headers.get("Referrer-Policy") == "no-referrer"

    # PII Minimization
    body = resp.json()["data"]
    # Name must be masked
    assert body.get("customer_name_masked") == "R**** M** D*****"
    # Full phone must NOT appear in customer payload
    assert "+6281233445566" not in str(resp.json())


def test_anti_idor_access_prevention(client: TestClient, db_session: Session):
    """Verify access using order_id or random token is rejected with 404."""
    _, order, _ = _setup_order_with_tracking(db_session)

    # 1. Attempting to use internal order UUID
    res_idor = client.get(f"/api/v1/tracking/{order.id}")
    assert res_idor.status_code == 404

    # 2. Attempting to use non-existent token
    res_fake = client.get("/api/v1/tracking/fake_nonexistent_tracking_token_value_xyz")
    assert res_fake.status_code == 404


def test_customer_cancellation_guards(client: TestClient, db_session: Session):
    """Verify customer cannot cancel order once WASHING has begun."""
    _, _, washing_token = _setup_order_with_tracking(db_session, operational_status="WASHING")

    # Cancellation during WASHING must fail with 403 Forbidden
    res_cancel = client.post(
        f"/api/v1/tracking/{washing_token}/cancel",
        json={"reason": "Mau batalkan cucian yang sedang diputar mesin"},
    )
    assert res_cancel.status_code in (400, 403, 422)
