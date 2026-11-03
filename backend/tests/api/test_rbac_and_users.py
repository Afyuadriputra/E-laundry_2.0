import uuid

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.modules.businesses.models import Business, BusinessSettings
from app.modules.users.models import User, UserRole


def test_rbac_user_management_and_settings(client: TestClient, db_session: Session):
    # Seed business & settings
    business_id = uuid.uuid4()
    business = Business(
        id=business_id,
        name="Laundry Bersih Sejahtera",
        phone_e164="+6281299990000",
        address="Jl. Sudirman No. 45",
        timezone="Asia/Jakarta",
        is_active=True,
    )
    settings = BusinessSettings(
        id=uuid.uuid4(),
        business_id=business_id,
        pickup_enabled=True,
        delivery_enabled=True,
        default_delivery_fee=5000,
        default_completion_hours=48,
        weight_precision=1,
        weight_rounding_mode="HALF_UP",
    )
    db_session.add(business)
    db_session.add(settings)

    # Seed owner and staff
    owner_pass = "OwnerSecret999!"
    owner_user = User(
        id=uuid.uuid4(),
        business_id=business_id,
        username="pak_budi_owner",
        full_name="Budi Santoso",
        password_hash=hash_password(owner_pass),
        role=UserRole.OWNER.value,
        is_active=True,
    )
    staff_pass = "StaffSecret888!"
    staff_user = User(
        id=uuid.uuid4(),
        business_id=business_id,
        username="andi_staff",
        full_name="Andi Cuci",
        password_hash=hash_password(staff_pass),
        role=UserRole.STAFF.value,
        is_active=True,
    )
    db_session.add(owner_user)
    db_session.add(staff_user)
    db_session.commit()

    # 1. Login as Staff and attempt to access /api/v1/users -> Expect 403 Forbidden
    login_staff = client.post(
        "/api/v1/auth/login",
        json={"username": "andi_staff", "password": staff_pass},
    )
    assert login_staff.status_code == 200

    res_forbidden = client.get("/api/v1/users")
    assert res_forbidden.status_code == 403
    assert res_forbidden.json()["error"]["code"] == "FORBIDDEN"

    # Attempt to update settings as Staff -> Expect 403 Forbidden
    res_forbidden_settings = client.patch(
        "/api/v1/settings",
        json={"default_delivery_fee": 10000},
    )
    assert res_forbidden_settings.status_code == 403

    client.post("/api/v1/auth/logout")

    # 2. Login as Owner
    login_owner = client.post(
        "/api/v1/auth/login",
        json={"username": "pak_budi_owner", "password": owner_pass},
    )
    assert login_owner.status_code == 200
    owner_csrf = login_owner.json()["data"]["csrf_token"]

    # 3. Owner lists users -> Expect 200 OK
    res_users = client.get("/api/v1/users")
    assert res_users.status_code == 200
    user_list = res_users.json()["data"]
    assert len(user_list) >= 2

    # 4. Owner creates new courier
    res_new_courier = client.post(
        "/api/v1/users",
        headers={"X-CSRF-Token": owner_csrf},
        json={
            "username": "joko_kurir",
            "full_name": "Joko Susilo",
            "password": "CourierPass123!",
            "role": "COURIER",
            "phone_e164": "+628123456789",
        },
    )
    assert res_new_courier.status_code == 200
    courier_id = res_new_courier.json()["data"]["id"]

    # 5. Owner attempts to deactivate himself (the only owner) -> Must be rejected (403 Forbidden)
    res_deact_owner = client.post(
        f"/api/v1/users/{owner_user.id}/deactivate",
        headers={"X-CSRF-Token": owner_csrf},
    )
    assert res_deact_owner.status_code == 403
    assert "Owner terakhir" in res_deact_owner.json()["error"]["message"]

    # 6. Owner deactivates courier -> Expect 200 OK
    res_deact_courier = client.post(
        f"/api/v1/users/{courier_id}/deactivate",
        headers={"X-CSRF-Token": owner_csrf},
    )
    assert res_deact_courier.status_code == 200
    assert res_deact_courier.json()["data"]["is_active"] is False

    # 7. Owner updates settings
    res_update_settings = client.patch(
        "/api/v1/settings",
        headers={"X-CSRF-Token": owner_csrf},
        json={"default_delivery_fee": 7500, "weight_precision": 2},
    )
    assert res_update_settings.status_code == 200
    assert res_update_settings.json()["data"]["default_delivery_fee"] == 7500
    assert res_update_settings.json()["data"]["weight_precision"] == 2
