import uuid

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.modules.businesses.models import Business, BusinessSettings
from app.modules.customers.models import Customer
from app.modules.services.models import Service
from app.modules.users.models import User, UserRole


def _login(client: TestClient, username: str, password: str) -> dict[str, str]:
    res = client.post("/api/v1/auth/login", json={"username": username, "password": password})
    assert res.status_code == 200
    csrf = res.headers.get("X-CSRF-Token") or res.json()["data"]["csrf_token"]
    return {"X-CSRF-Token": csrf}


def test_order_full_lifecycle_and_invariants(client: TestClient, db_session: Session):
    business_id = uuid.uuid4()
    business = Business(
        id=business_id,
        name="Laundry Operasional Sukses",
        phone_e164="+6281200001111",
        address="Jl. Melati 10",
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

    # Seed User (Cashier)
    cashier = User(
        id=uuid.uuid4(),
        business_id=business_id,
        username="kasir_rudi",
        full_name="Rudi Hartono",
        password_hash=hash_password("KasirRudi123!"),
        role=UserRole.CASHIER.value,
        is_active=True,
    )
    db_session.add(cashier)

    # Seed Customer
    customer = Customer(
        id=uuid.uuid4(),
        business_id=business_id,
        full_name="Ibu Ratna",
        phone_e164="+6281234567899",
        address="Kompleks Indah No. 5",
        is_active=True,
    )
    db_session.add(customer)

    # Seed Services: Kiloan (requires ironing) & Bedcover (per item, no ironing)
    service_kiloan = Service(
        id=uuid.uuid4(),
        business_id=business_id,
        name="Cuci Setrika Kiloan",
        pricing_type="PER_KG",
        unit="KG",
        unit_price=10000,
        estimated_hours=24,
        requires_ironing=True,
        is_active=True,
        version=1,
    )
    service_bedcover = Service(
        id=uuid.uuid4(),
        business_id=business_id,
        name="Cuci Bedcover Besar",
        pricing_type="PER_ITEM",
        unit="PCS",
        unit_price=35000,
        estimated_hours=48,
        requires_ironing=False,
        is_active=True,
        version=1,
    )
    db_session.add(service_kiloan)
    db_session.add(service_bedcover)
    db_session.commit()

    headers = _login(client, "kasir_rudi", "KasirRudi123!")

    # 1. Create Order with 2.4 kg kiloan (DEC-02 floor applies: billed as 3.0 kg = 30,000)
    # and 1 bedcover (35,000) + extra charge 5,000 + delivery fee 5,000 -> Total = 75,000
    create_payload = {
        "customer_id": str(customer.id),
        "items": [
            {"service_id": str(service_kiloan.id), "quantity": "2.4"},
            {"service_id": str(service_bedcover.id), "quantity": "1"},
        ],
        "intake_method": "DROP_OFF",
        "return_method": "HOME_DELIVERY",
        "extra_charge_amount": 5000,
        "delivery_fee_amount": 5000,
        "customer_notes": "Tolong pakaian putih dipisah",
    }
    create_res = client.post("/api/v1/orders", json=create_payload, headers=headers)
    assert create_res.status_code == 200, create_res.text
    order = create_res.json()["data"]
    order_id = order["id"]

    # Verify sequential order number format ORD-YYYYMMDD-0001
    assert order["order_number"].startswith("ORD-")
    assert order["order_number"].endswith("-0001")
    assert order["operational_status"] == "RECEIVED"
    assert order["subtotal_amount"] == 65000  # 30,000 (3.0 kg * 10,000) + 35,000 (1 * 35,000)
    assert order["total_amount"] == 75000  # 65,000 + 5,000 + 5,000
    assert order["version"] == 1
    assert len(order["items"]) == 2
    assert len(order["status_history"]) == 1

    # 2. Create Second Order to verify sequential numbering (-0002)
    create_res_2 = client.post(
        "/api/v1/orders",
        json={
            "customer_id": str(customer.id),
            "items": [{"service_id": str(service_bedcover.id), "quantity": "1"}],
        },
        headers=headers,
    )
    assert create_res_2.status_code == 200
    order_2 = create_res_2.json()["data"]
    assert order_2["order_number"].endswith("-0002")

    # 3. Transition Order 1 through the operational state machine
    current_version = order["version"]

    def transition(to_status: str, expected_v: int) -> dict:
        nonlocal current_version
        t_res = client.post(
            f"/api/v1/orders/{order_id}/transition",
            json={
                "to_status": to_status,
                "reason": f"Pindah ke {to_status}",
                "expected_version": expected_v,
            },
            headers=headers,
        )
        assert t_res.status_code == 200, t_res.text
        updated = t_res.json()["data"]
        current_version = updated["version"]
        assert updated["operational_status"] == to_status
        return updated

    transition("QUEUED", current_version)
    transition("WASHING", current_version)
    transition("DRYING", current_version)
    transition("IRONING", current_version)
    transition("QC_PACKING", current_version)
    transition("READY", current_version)

    # 4. Invariant Test: Attempt transition READY -> COMPLETED without handoff/payment
    # MUST be rejected with HTTP 422 Unprocessable Entity
    fail_complete_res = client.post(
        f"/api/v1/orders/{order_id}/transition",
        json={
            "to_status": "COMPLETED",
            "reason": "Mencoba selesaikan langsung",
            "expected_version": current_version,
        },
        headers=headers,
    )
    assert fail_complete_res.status_code == 422
    err_body = fail_complete_res.json()
    assert err_body["error"]["code"] == "BUSINESS_INVARIANT_VIOLATION"

    # 5. Optimistic Concurrency Collision Test (M2-13): Passing outdated expected_version
    # MUST be rejected with HTTP 409 Conflict
    conflict_res = client.post(
        f"/api/v1/orders/{order_id}/transition",
        json={
            "to_status": "CANCELLED",
            "cancellation_reason": "Dibatalkan",
            "expected_version": current_version - 2,  # Outdated version
        },
        headers=headers,
    )
    assert conflict_res.status_code == 409
    assert conflict_res.json()["error"]["code"] == "VERSION_CONFLICT"

    # 6. Cancellation with reason test
    cancel_res = client.post(
        f"/api/v1/orders/{order_id}/cancel",
        json={
            "cancellation_reason": "Pelanggan meminta dibatalkan karena pindah domisili",
            "expected_version": current_version,
        },
        headers=headers,
    )
    assert cancel_res.status_code == 200
    cancelled_order = cancel_res.json()["data"]
    assert cancelled_order["operational_status"] == "CANCELLED"
    assert cancelled_order["cancelled_at"] is not None
    assert "pindah domisili" in cancelled_order["cancellation_reason"]
