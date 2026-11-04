"""
Deep Integration Test Suite for Orders (BE-02 / BE-05).
Covers end-to-end intake of multi-service orders (kiloan + satuan),
snapshot pricing calculations, full operational state progression (RECEIVED -> COMPLETED),
payment prerequisite enforcement, physical handoff recording, and status history audit trail.
"""

import uuid
from decimal import Decimal

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.modules.businesses.models import Business, BusinessSettings
from app.modules.customers.models import Customer
from app.modules.orders.models import OrderHandoff, OrderStatusHistory
from app.modules.services.models import Service
from app.modules.users.models import User, UserRole


def _setup_order_integration_env(
    client: TestClient, db_session: Session
) -> tuple[dict[str, str], Business, Customer, Service, Service]:
    biz_id = uuid.uuid4()
    biz = Business(
        id=biz_id,
        name="Integrasi Laundry Sukses",
        phone_e164="+6281200009999",
        address="Jl. Integrasi No. 42",
        timezone="Asia/Jakarta",
        is_active=True,
    )
    settings = BusinessSettings(
        id=uuid.uuid4(),
        business_id=biz_id,
        pickup_enabled=True,
        delivery_enabled=True,
        weight_precision=1,
        weight_rounding_mode="HALF_UP",
    )
    db_session.add_all([biz, settings])

    cashier = User(
        id=uuid.uuid4(),
        business_id=biz_id,
        username="kasir_integrasi",
        full_name="Kasir Handal",
        password_hash=hash_password("KasirHandal123!"),
        role=UserRole.CASHIER.value,
        is_active=True,
    )
    cust = Customer(
        id=uuid.uuid4(),
        business_id=biz_id,
        full_name="Ibu Hajjah Maryam",
        phone_e164="+6281234567891",
        address="Jl. Melati Blok C No. 4",
        is_active=True,
    )
    srv_kiloan = Service(
        id=uuid.uuid4(),
        business_id=biz_id,
        name="Cuci Setrika Reguler",
        pricing_type="PER_KG",
        unit="KG",
        unit_price=10000,
        estimated_hours=24,
        requires_ironing=True,
        is_active=True,
        version=1,
    )
    srv_satuan = Service(
        id=uuid.uuid4(),
        business_id=biz_id,
        name="Cuci Bedcover King",
        pricing_type="PER_ITEM",
        unit="PCS",
        unit_price=35000,
        estimated_hours=48,
        requires_ironing=False,
        is_active=True,
        version=1,
    )
    db_session.add_all([cashier, cust, srv_kiloan, srv_satuan])
    db_session.commit()

    login_res = client.post(
        "/api/v1/auth/login",
        json={"username": cashier.username, "password": "KasirHandal123!"},
    )
    assert login_res.status_code == 200
    csrf = login_res.headers.get("X-CSRF-Token") or login_res.json()["data"]["csrf_token"]
    headers = {"X-CSRF-Token": csrf}
    return headers, biz, cust, srv_kiloan, srv_satuan


def test_order_full_lifecycle_integration(client: TestClient, db_session: Session):
    headers, biz, cust, srv_kiloan, srv_satuan = _setup_order_integration_env(client, db_session)

    # 1. Create Multi-Service Order: 3.5 kg kiloan + 1 pcs bedcover
    create_payload = {
        "customer_id": str(cust.id),
        "items": [
            {"service_id": str(srv_kiloan.id), "quantity": "3.5"},
            {"service_id": str(srv_satuan.id), "quantity": "1.0"},
        ],
        "intake_method": "DROP_OFF",
        "return_method": "SELF_PICKUP",
        "extra_charge_amount": 5000,
        "delivery_fee_amount": 0,
        "customer_notes": "Tolong jangan dicampur pewangi menyengat",
    }
    res_create = client.post("/api/v1/orders", json=create_payload, headers=headers)
    assert res_create.status_code == 200, res_create.text
    order_data = res_create.json()["data"]
    order_id = order_data["id"]

    # Verify Pricing Snapshot:
    # 3.5 kg * 10,000 = 35,000
    # 1 pcs * 35,000 = 35,000
    # subtotal = 70,000; total = 70,000 + 5,000 = 75,000
    assert order_data["subtotal_amount"] == 70000
    assert order_data["extra_charge_amount"] == 5000
    assert order_data["total_amount"] == 75000
    assert order_data["operational_status"] == "RECEIVED"
    current_ver = order_data["version"]

    # 2. Advance: RECEIVED -> QUEUED
    res_q = client.post(
        f"/api/v1/orders/{order_id}/transition",
        json={"to_status": "QUEUED", "expected_version": current_ver},
        headers=headers,
    )
    assert res_q.status_code == 200
    current_ver = res_q.json()["data"]["version"]
    assert res_q.json()["data"]["operational_status"] == "QUEUED"

    # 3. Advance: QUEUED -> WASHING
    res_w = client.post(
        f"/api/v1/orders/{order_id}/transition",
        json={"to_status": "WASHING", "expected_version": current_ver},
        headers=headers,
    )
    assert res_w.status_code == 200
    current_ver = res_w.json()["data"]["version"]

    # 4. Advance: WASHING -> DRYING
    res_d = client.post(
        f"/api/v1/orders/{order_id}/transition",
        json={"to_status": "DRYING", "expected_version": current_ver},
        headers=headers,
    )
    assert res_d.status_code == 200
    current_ver = res_d.json()["data"]["version"]

    # 5. Advance: DRYING -> IRONING (kiloan service requires ironing)
    res_i = client.post(
        f"/api/v1/orders/{order_id}/transition",
        json={"to_status": "IRONING", "expected_version": current_ver},
        headers=headers,
    )
    assert res_i.status_code == 200
    current_ver = res_i.json()["data"]["version"]

    # 6. Advance: IRONING -> QC_PACKING
    res_qc = client.post(
        f"/api/v1/orders/{order_id}/transition",
        json={"to_status": "QC_PACKING", "expected_version": current_ver},
        headers=headers,
    )
    assert res_qc.status_code == 200
    current_ver = res_qc.json()["data"]["version"]

    # 7. Advance: QC_PACKING -> READY
    res_r = client.post(
        f"/api/v1/orders/{order_id}/transition",
        json={"to_status": "READY", "expected_version": current_ver},
        headers=headers,
    )
    assert res_r.status_code == 200
    current_ver = res_r.json()["data"]["version"]

    # 8. Attempt READY -> COMPLETED while UNPAID -> Must Fail (400)
    res_c_fail = client.post(
        f"/api/v1/orders/{order_id}/transition",
        json={
            "to_status": "COMPLETED",
            "expected_version": current_ver,
            "received_by_name": "Ibu Hajjah Maryam",
        },
        headers=headers,
    )
    assert res_c_fail.status_code in (400, 422)

    # 9. Pay Full Amount (75,000)
    pay_res = client.post(
        f"/api/v1/orders/{order_id}/payments",
        json={"amount": 75000, "method": "CASH", "reference_note": "Lunas di kasir"},
        headers=headers,
    )
    assert pay_res.status_code == 200

    # 10. Complete Order with physical handoff confirmation
    res_complete = client.post(
        f"/api/v1/orders/{order_id}/transition",
        json={
            "to_status": "COMPLETED",
            "expected_version": current_ver,
            "received_by_name": "Pak Maryam (Suami)",
            "reason": "Diambil suami pelanggan di kasir",
        },
        headers=headers,
    )
    assert res_complete.status_code == 200
    comp_data = res_complete.json()["data"]
    assert comp_data["operational_status"] == "COMPLETED"
    assert comp_data["completed_at"] is not None

    # 11. Verify DB Handoff Record & Status History count
    handoff = db_session.query(OrderHandoff).filter(OrderHandoff.order_id == uuid.UUID(order_id)).first()
    assert handoff is not None
    assert handoff.received_by_name == "Pak Maryam (Suami)"
    assert handoff.notes == "Diambil suami pelanggan di kasir"

    history_records = (
        db_session.query(OrderStatusHistory)
        .filter(OrderStatusHistory.order_id == uuid.UUID(order_id))
        .all()
    )
    # At least 7 status progressions recorded in history
    assert len(history_records) >= 7
