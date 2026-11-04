"""
Deep Integration Test Suite for Public Pickup Intake & Atomic Conversion to Order (BE-02 / BE-05 / DEC-10).
Verifies:
1. Unauthenticated customer creates public pickup request with time window validation.
2. Cashier confirms pickup request.
3. Cashier atomically converts pickup into an official laundry Order.
4. Database FK link order.pickup_request_id == pickup.id is established.
5. Invariant enforcement: Double conversion of same pickup request is strictly rejected.
"""

import uuid
from datetime import UTC, date, datetime, timedelta

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.modules.businesses.models import Business, BusinessSettings
from app.modules.orders.models import Order
from app.modules.pickup_delivery.models import PickupRequest, PickupStatus
from app.modules.services.models import Service
from app.modules.users.models import User, UserRole


def _setup_pickup_conversion_env(
    client: TestClient, db_session: Session
) -> tuple[dict[str, str], Business, Service]:
    biz_id = uuid.uuid4()
    biz = Business(
        id=biz_id,
        name="Pickup Conversion Laundry",
        phone_e164="+6281200003344",
        address="Jl. Antar Jemput No. 10",
        timezone="Asia/Jakarta",
        is_active=True,
    )
    settings = BusinessSettings(
        id=uuid.uuid4(),
        business_id=biz_id,
        pickup_enabled=True,
        delivery_enabled=True,
    )
    cashier = User(
        id=uuid.uuid4(),
        business_id=biz_id,
        username="cashier_pickup",
        full_name="Kasir Jemput",
        password_hash=hash_password("CashierPass123!"),
        role=UserRole.CASHIER.value,
        is_active=True,
    )
    service = Service(
        id=uuid.uuid4(),
        business_id=biz_id,
        name="Cuci Lipat Kilat",
        pricing_type="PER_KG",
        unit="KG",
        unit_price=12000,
        estimated_hours=12,
        requires_ironing=False,
        is_active=True,
        version=1,
    )
    db_session.add_all([biz, settings, cashier, service])
    db_session.commit()

    res = client.post("/api/v1/auth/login", json={"username": "cashier_pickup", "password": "CashierPass123!"})
    csrf = res.headers.get("X-CSRF-Token") or res.json()["data"]["csrf_token"]
    cashier_headers = {"X-CSRF-Token": csrf}

    return cashier_headers, biz, service


def test_public_pickup_to_order_atomic_conversion_and_single_use_invariant(
    client: TestClient, db_session: Session
):
    cashier_headers, biz, service = _setup_pickup_conversion_env(client, db_session)

    # 1. Public Customer creates pickup request
    target_date = (date.today() + timedelta(days=1)).isoformat()
    pickup_payload = {
        "requester_name": "Pak Harto Driver",
        "phone_e164": "+6281299887766",
        "pickup_address": "Jl. Gatot Subroto Kav. 12",
        "requested_date": target_date,
        "requested_time_start": "09:00:00",
        "requested_time_end": "11:00:00",
        "notes": "Titip di pos satpam depan",
    }
    res_pub = client.post(
        f"/api/v1/pickup-delivery/requests/public?business_id={biz.id}",
        json=pickup_payload,
    )
    assert res_pub.status_code == 201
    pickup_data = res_pub.json()["data"]
    pickup_id = pickup_data["id"]
    assert pickup_data["status"] == "REQUESTED"
    assert pickup_data["tracking_token"] is not None

    # 2. Cashier confirms pickup request
    now_dt = datetime.now(UTC)
    confirm_payload = {
        "confirmed_start_at": (now_dt + timedelta(hours=1)).isoformat(),
        "confirmed_end_at": (now_dt + timedelta(hours=2)).isoformat(),
        "notes": "Penjemputan disetujui, jadwal jam 09:30",
    }
    res_confirm = client.post(
        f"/api/v1/pickup-delivery/requests/{pickup_id}/confirm",
        json=confirm_payload,
        headers=cashier_headers,
    )
    assert res_confirm.status_code == 200
    assert res_confirm.json()["data"]["status"] == "CONFIRMED"

    # 3. Cashier converts pickup to laundry order (cucian sudah tiba di outlet)
    convert_payload = {
        "service_id": str(service.id),
        "quantity": "5.0",
        "extra_charge_amount": 0,
        "delivery_fee_amount": 5000,
        "return_method": "SELF_PICKUP",
        "customer_notes": "Baju kemeja putih pisahkan",
        "internal_notes": "Dari pickup public satpam",
    }
    res_convert = client.post(
        f"/api/v1/pickup-delivery/requests/{pickup_id}/convert-order",
        json=convert_payload,
        headers=cashier_headers,
    )
    assert res_convert.status_code == 201
    convert_data = res_convert.json()["data"]
    order_id = convert_data["order_id"]
    assert convert_data["total_amount"] == (5 * 12000) + 5000  # 65,000

    # 4. Verify Database Link & Status
    order_in_db = db_session.query(Order).filter(Order.id == uuid.UUID(order_id)).first()
    assert order_in_db is not None
    assert str(order_in_db.pickup_request_id) == pickup_id
    assert order_in_db.customer.phone_e164 == "+6281299887766"
    assert order_in_db.operational_status == "RECEIVED"

    pickup_in_db = db_session.query(PickupRequest).filter(PickupRequest.id == uuid.UUID(pickup_id)).first()
    assert pickup_in_db.status == PickupStatus.CONVERTED.value

    # 5. Invariant Check: Attempt second conversion on the same pickup request -> Must Fail (400)
    res_double = client.post(
        f"/api/v1/pickup-delivery/requests/{pickup_id}/convert-order",
        json=convert_payload,
        headers=cashier_headers,
    )
    assert res_double.status_code in (400, 422)
    assert "sudah pernah dikonversi" in res_double.text
