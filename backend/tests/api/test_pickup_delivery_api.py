import uuid
from datetime import UTC, date, datetime, timedelta

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.modules.businesses.models import Business
from app.modules.orders.models import Order
from app.modules.pickup_delivery.models import (
    DeliveryTask,
    PickupRequest,
)
from app.modules.services.models import Service
from app.modules.users.models import User, UserRole


def test_pickup_delivery_full_lifecycle(client: TestClient, db_session: Session):
    # 1. Setup Business, Cashier, Courier, and Service
    business = Business(
        id=uuid.uuid4(),
        name="Laundry Bersih Kilat",
        phone_e164="+6281234567890",
        address="Jl. Dahlia No. 1, Bandung",
        timezone="Asia/Jakarta",
        is_active=True,
    )
    cashier = User(
        id=uuid.uuid4(),
        business_id=business.id,
        username="kasir_rina",
        full_name="Rina Kasir",
        password_hash=hash_password("KasirPass123!"),
        role=UserRole.CASHIER.value,
        is_active=True,
    )
    courier = User(
        id=uuid.uuid4(),
        business_id=business.id,
        username="kurir_dodi",
        full_name="Dodi Kurir",
        password_hash=hash_password("KurirPass123!"),
        role=UserRole.COURIER.value,
        is_active=True,
    )
    service = Service(
        id=uuid.uuid4(),
        business_id=business.id,
        name="Cuci Lipat Reguler",
        pricing_type="PER_KG",
        unit="KG",
        unit_price=7000,
        estimated_hours=24,
        requires_ironing=False,
        is_active=True,
        version=1,
    )
    db_session.add_all([business, cashier, courier, service])
    db_session.commit()

    # Login as Cashier
    login_res = client.post(
        "/api/v1/auth/login",
        json={"username": "kasir_rina", "password": "KasirPass123!"},
    )
    assert login_res.status_code == 200
    csrf_token = login_res.json()["data"]["csrf_token"]
    auth_headers = {"X-CSRF-Token": csrf_token}

    # 2. Public Pickup Intake (No Auth Required)
    tomorrow = date.today() + timedelta(days=1)
    pickup_payload = {
        "requester_name": "Pak Ahmad Yani",
        "phone_e164": "081299887766",
        "pickup_address": "Jl. Mawar No. 8, Bandung",
        "requested_date": str(tomorrow),
        "requested_time_start": "09:00:00",
        "requested_time_end": "11:00:00",
        "notes": "Tolong jemput di lobby kantor",
    }
    public_res = client.post(
        f"/api/v1/pickup-delivery/requests/public?business_id={business.id}",
        json=pickup_payload,
    )
    assert public_res.status_code == 201, public_res.text
    p_data = public_res.json()["data"]
    assert p_data["status"] == "REQUESTED"
    assert p_data["request_number"].startswith("PCK-")
    assert p_data["tracking_token"] is not None
    assert "/track/" in p_data["tracking_url"]
    pickup_id = p_data["id"]

    # 3. List Pickup Requests as Cashier
    list_res = client.get("/api/v1/pickup-delivery/requests")
    assert list_res.status_code == 200
    assert len(list_res.json()["data"]) >= 1

    # 4. Confirm Pickup Request and Dispatch Courier
    now = datetime.now(UTC)
    confirm_payload = {
        "confirmed_start_at": (now + timedelta(hours=2)).isoformat(),
        "confirmed_end_at": (now + timedelta(hours=4)).isoformat(),
        "courier_user_id": str(courier.id),
        "notes": "Kurir Dodi ditugaskan",
    }
    confirm_res = client.post(
        f"/api/v1/pickup-delivery/requests/{pickup_id}/confirm",
        json=confirm_payload,
        headers=auth_headers,
    )
    assert confirm_res.status_code == 200
    assert confirm_res.json()["data"]["status"] == "ASSIGNED"

    # Verify DeliveryTask created automatically
    task = (
        db_session.query(DeliveryTask)
        .filter(DeliveryTask.pickup_request_id == uuid.UUID(pickup_id))
        .first()
    )
    assert task is not None
    assert task.task_type == "PICKUP"
    assert task.courier_user_id == courier.id
    assert task.status == "ASSIGNED"

    # 5. Courier Workflow: Login as Courier & progress task to COMPLETED
    courier_login = client.post(
        "/api/v1/auth/login",
        json={"username": "kurir_dodi", "password": "KurirPass123!"},
    )
    assert courier_login.status_code == 200
    c_csrf = courier_login.json()["data"]["csrf_token"]
    courier_headers = {"X-CSRF-Token": c_csrf}

    # Courier sees assigned task
    my_tasks = client.get("/api/v1/pickup-delivery/tasks/my-tasks")
    assert my_tasks.status_code == 200
    assert len(my_tasks.json()["data"]) == 1

    # Update task to EN_ROUTE
    en_route_res = client.post(
        f"/api/v1/pickup-delivery/tasks/{task.id}/status",
        json={"to_status": "EN_ROUTE", "notes": "Sedang meluncur ke lokasi"},
        headers=courier_headers,
    )
    assert en_route_res.status_code == 200
    assert en_route_res.json()["data"]["status"] == "EN_ROUTE"

    # Complete pickup task (cucian sampai di outlet!)
    complete_res = client.post(
        f"/api/v1/pickup-delivery/tasks/{task.id}/status",
        json={"to_status": "COMPLETED", "proof_photo_path": "/uploads/proof1.jpg"},
        headers=courier_headers,
    )
    assert complete_res.status_code == 200
    assert complete_res.json()["data"]["status"] == "COMPLETED"

    # Verify pickup request status is now AT_LAUNDRY
    pickup_db = db_session.query(PickupRequest).filter(PickupRequest.id == uuid.UUID(pickup_id)).first()
    assert pickup_db.status == "AT_LAUNDRY"

    # 6. Atomic Conversion to Laundry Order (DEC-10)
    # Re-login as cashier
    relogin_res = client.post(
        "/api/v1/auth/login",
        json={"username": "kasir_rina", "password": "KasirPass123!"},
    )
    assert relogin_res.status_code == 200
    auth_headers = {"X-CSRF-Token": relogin_res.headers.get("X-CSRF-Token") or relogin_res.json()["data"]["csrf_token"]}

    convert_payload = {
        "service_id": str(service.id),
        "quantity": "5.0",
        "extra_charge_amount": 0,
        "delivery_fee_amount": 5000,
        "return_method": "HOME_DELIVERY",
        "customer_notes": "Harap jangan dicampur baju putih",
    }
    convert_res = client.post(
        f"/api/v1/pickup-delivery/requests/{pickup_id}/convert-order",
        json=convert_payload,
        headers=auth_headers,
    )
    assert convert_res.status_code == 201, convert_res.text
    conv_data = convert_res.json()["data"]
    order_id = conv_data["order_id"]
    assert conv_data["order_number"].startswith("ORD-")
    assert conv_data["total_amount"] == 40000  # 5kg * 7000 + 5000 delivery fee

    # Verify PickupRequest status is CONVERTED
    db_session.refresh(pickup_db)
    assert pickup_db.status == "CONVERTED"

    # Verify Order in DB has pickup_request_id linked
    order_db = db_session.query(Order).filter(Order.id == uuid.UUID(order_id)).first()
    assert order_db is not None
    assert str(order_db.pickup_request_id) == pickup_id

    # Anti-duplicate check: converting again MUST fail with 422
    dup_res = client.post(
        f"/api/v1/pickup-delivery/requests/{pickup_id}/convert-order",
        json=convert_payload,
        headers=auth_headers,
    )
    assert dup_res.status_code == 422
    assert "sudah pernah dikonversi" in dup_res.json()["error"]["message"]

    # 7. Create DELIVERY Task for Order Return (Home Delivery)
    delivery_task_payload = {
        "task_type": "DELIVERY",
        "order_id": order_id,
        "courier_user_id": str(courier.id),
        "destination_address": "Jl. Mawar No. 8, Bandung",
        "destination_phone": "+6281299887766",
        "recipient_name": "Pak Ahmad Yani",
    }
    dt_res = client.post(
        "/api/v1/pickup-delivery/tasks",
        json=delivery_task_payload,
        headers=auth_headers,
    )
    assert dt_res.status_code == 201
    dt_id = dt_res.json()["data"]["id"]

    # Move order to READY
    order_db.operational_status = "READY"
    db_session.commit()

    # Courier delivers package to customer -> COMPLETED
    courier_login_res = client.post(
        "/api/v1/auth/login",
        json={"username": "kurir_dodi", "password": "KurirPass123!"},
    )
    assert courier_login_res.status_code == 200
    courier_headers = {"X-CSRF-Token": courier_login_res.headers.get("X-CSRF-Token") or courier_login_res.json()["data"]["csrf_token"]}
    deliver_res = client.post(
        f"/api/v1/pickup-delivery/tasks/{dt_id}/status",
        json={
            "to_status": "COMPLETED",
            "received_by_name": "Pak Ahmad Yani (Pribadi)",
            "proof_photo_path": "/uploads/delivery_proof.jpg",
        },
        headers=courier_headers,
    )
    assert deliver_res.status_code == 200
    assert deliver_res.json()["data"]["status"] == "COMPLETED"

    # Verify Order is now COMPLETED via courier delivery handoff
    db_session.refresh(order_db)
    assert order_db.operational_status == "COMPLETED"

