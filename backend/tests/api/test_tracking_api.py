import uuid
from datetime import UTC, datetime, timedelta
from decimal import Decimal

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.modules.businesses.models import Business
from app.modules.customers.models import Customer
from app.modules.orders.models import Order, OrderItem, OrderStatusHistory
from app.modules.services.models import Service
from app.modules.tracking.service import TrackingService, mask_customer_name, mask_phone_number
from app.modules.users.models import User, UserRole


def test_pii_masking_logic():
    assert mask_customer_name("Ibu Ratna") == "I** R****"
    assert mask_customer_name("Budi") == "B***"
    assert mask_customer_name("A B C") == "A B C"
    assert mask_customer_name("") == "Pelanggan"
    assert mask_customer_name(None) == "Pelanggan"

    assert mask_phone_number("+6281234567890") == "+62812****7890"
    assert mask_phone_number("+6281234") == "+62812****34"
    assert mask_phone_number("123") == "12****"
    assert mask_phone_number(None) == "-"


def test_tracking_api_full_flow(client: TestClient, db_session: Session):
    # 1. Setup Business & User
    business = Business(
        id=uuid.uuid4(),
        name="Laundry Bersih Sejahtera",
        phone_e164="+6281234567890",
        address="Jl. Melati No. 45, Jakarta",
        timezone="Asia/Jakarta",
        is_active=True,
    )
    cashier = User(
        id=uuid.uuid4(),
        business_id=business.id,
        username="kasir_ani",
        full_name="Ani Kasir",
        password_hash=hash_password("KasirPass123!"),
        role=UserRole.CASHIER.value,
        is_active=True,
    )
    customer = Customer(
        id=uuid.uuid4(),
        business_id=business.id,
        full_name="Ibu Siti Nurhaliza",
        phone_e164="+6281298765432",
        address="Jl. Anggrek No. 12",
        is_active=True,
    )
    service = Service(
        id=uuid.uuid4(),
        business_id=business.id,
        name="Cuci Komplit Reguler",
        pricing_type="PER_KG",
        unit="KG",
        unit_price=8000,
        estimated_hours=24,
        requires_ironing=True,
        is_active=True,
        version=1,
    )
    db_session.add_all([business, cashier, customer, service])
    db_session.commit()

    # 2. Setup Order in RECEIVED status
    order = Order(
        id=uuid.uuid4(),
        business_id=business.id,
        order_number="ORD-20261103-TRK1",
        customer_id=customer.id,
        created_by=cashier.id,
        operational_status="RECEIVED",
        intake_method="DROP_OFF",
        return_method="SELF_PICKUP",
        subtotal_amount=24000,
        extra_charge_amount=0,
        delivery_fee_amount=0,
        total_amount=24000,
        estimated_completion_at=datetime.now(UTC) + timedelta(hours=24),
        version=1,
    )
    db_session.add(order)
    db_session.flush()

    item = OrderItem(
        order_id=order.id,
        service_id=service.id,
        service_name_snapshot=service.name,
        pricing_type_snapshot=service.pricing_type,
        unit_snapshot=service.unit,
        quantity=Decimal("3.0"),
        unit_price_snapshot=service.unit_price,
        line_total_amount=24000,
        requires_ironing_snapshot=service.requires_ironing,
    )
    hist = OrderStatusHistory(
        order_id=order.id,
        from_status=None,
        to_status="RECEIVED",
        changed_by=cashier.id,
        reason="Pesanan diterima di kasir",
    )
    db_session.add_all([item, hist])
    db_session.commit()

    # 3. Create Tracking Token via Service
    token_record, raw_token = TrackingService.create_order_tracking_token(
        db=db_session,
        order_id=order.id,
        created_by=cashier.id,
    )
    assert token_record.token_hash is not None
    exp_at = token_record.expires_at
    if exp_at.tzinfo is None:
        exp_at = exp_at.replace(tzinfo=UTC)
    assert exp_at > datetime.now(UTC)

    # 4. Fetch Public Tracking via API (No Auth / Cookie required)
    res = client.get(f"/api/v1/tracking/{raw_token}")
    assert res.status_code == 200, res.text
    data = res.json()["data"]

    # Verify Response Headers per BSD §34.4
    assert "no-store" in res.headers.get("Cache-Control", "")
    assert res.headers.get("Referrer-Policy") == "no-referrer"

    # Verify Strict Allowlist Schema and Masked PII
    assert data["tracking_type"] == "ORDER"
    assert data["order_number"] == "ORD-20261103-TRK1"
    assert data["current_status"] == "RECEIVED"
    assert data["status_label"] == "Diterima Kasir"
    assert data["can_cancel"] is False
    assert data["customer_name_masked"] == "I** S*** N********"
    assert data["customer_phone_masked"] == "+62812****5432"

    # Verify Financial & Business Summary
    assert data["financial_summary"]["total_amount"] == 24000
    assert data["financial_summary"]["paid_amount"] == 0
    assert data["financial_summary"]["remaining_amount"] == 24000
    assert data["financial_summary"]["payment_status"] == "UNPAID"
    assert data["business_contact"]["name"] == "Laundry Bersih Sejahtera"
    assert "wa.me" in data["business_contact"]["whatsapp_url"]

    # Verify Items & Timeline
    assert len(data["service_summary"]) == 1
    assert data["service_summary"][0]["service_name"] == "Cuci Komplit Reguler"
    assert len(data["timeline"]) == 1
    assert data["timeline"][0]["status"] == "RECEIVED"

    # 5. Test Invalid, Expired, and Revoked Tokens
    # Malformed / short token -> 404
    bad_res = client.get("/api/v1/tracking/short")
    assert bad_res.status_code == 404

    # Non-existent valid-length token -> 404
    fake_token = "a" * 43
    notFound_res = client.get(f"/api/v1/tracking/{fake_token}")
    assert notFound_res.status_code == 404

    # Expired token -> 410 Gone
    expired_token_record, expired_raw_token = TrackingService.create_order_tracking_token(
        db=db_session,
        order_id=order.id,
        ttl_days=-1,  # expired in past
    )
    exp_res = client.get(f"/api/v1/tracking/{expired_raw_token}")
    assert exp_res.status_code == 410

    # Revoked token -> 410 Gone
    revoked_token_record, revoked_raw_token = TrackingService.create_order_tracking_token(
        db=db_session,
        order_id=order.id,
    )
    revoked_token_record.revoked_at = datetime.now(UTC)
    db_session.commit()
    rev_res = client.get(f"/api/v1/tracking/{revoked_raw_token}")
    assert rev_res.status_code == 410

    # 6. Test Public Direct Cancellation Rejection per PRD §5.7 #9 & BSD §34.1
    # Customers cannot mutate order status directly via tracking link -> 403 Forbidden
    cancel_attempt_res = client.post(
        f"/api/v1/tracking/{raw_token}/cancel",
        json={"reason": "Mau batalkan cucian secara mandiri"},
    )
    assert cancel_attempt_res.status_code == 403
    assert "tidak dapat mengubah status pesanan secara mandiri" in cancel_attempt_res.json()["error"]["message"]

    # 7. Authorized Internal Cancellation by Cashier (PRD §5.2 ORD-13)
    login_res = client.post(
        "/api/v1/auth/login",
        json={"username": "kasir_ani", "password": "KasirPass123!"},
    )
    assert login_res.status_code == 200
    csrf_token = login_res.headers.get("X-CSRF-Token") or login_res.json()["data"]["csrf_token"]
    cashier_headers = {"X-CSRF-Token": csrf_token}

    cancel_order_res = client.post(
        f"/api/v1/orders/{order.id}/cancel",
        json={"cancellation_reason": "Pelanggan meminta pembatalan melalui WhatsApp", "expected_version": 1},
        headers=cashier_headers,
    )
    assert cancel_order_res.status_code == 200

    # 8. Re-fetch tracking endpoint to confirm CANCELLED reflects publicly
    track_after_cancel = client.get(f"/api/v1/tracking/{raw_token}")
    assert track_after_cancel.status_code == 200
    assert track_after_cancel.json()["data"]["current_status"] == "CANCELLED"
    assert track_after_cancel.json()["data"]["can_cancel"] is False
