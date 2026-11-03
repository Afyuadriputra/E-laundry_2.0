import uuid

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.modules.businesses.models import Business, BusinessSettings
from app.modules.users.models import User, UserRole


def _login(client: TestClient, username: str, password: str) -> dict[str, str]:
    res = client.post("/api/v1/auth/login", json={"username": username, "password": password})
    assert res.status_code == 200
    csrf = res.headers.get("X-CSRF-Token") or res.json()["data"]["csrf_token"]
    return {"X-CSRF-Token": csrf}


def test_services_catalog_lifecycle(client: TestClient, db_session: Session):
    business_id = uuid.uuid4()
    business = Business(
        id=business_id,
        name="Laundry Bersih Wangi",
        phone_e164="+62811113333",
        address="Jl. Melati 2",
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

    owner = User(
        id=uuid.uuid4(),
        business_id=business_id,
        username="owner_wangi",
        full_name="Ibu Wahyu",
        password_hash=hash_password("OwnerWangi123!"),
        role=UserRole.OWNER.value,
        is_active=True,
    )
    staff = User(
        id=uuid.uuid4(),
        business_id=business_id,
        username="staff_wangi",
        full_name="Joko",
        password_hash=hash_password("StaffWangi123!"),
        role=UserRole.STAFF.value,
        is_active=True,
    )
    db_session.add(owner)
    db_session.add(staff)
    db_session.commit()

    # 1. Staff cannot create service (403 Forbidden)
    staff_headers = _login(client, "staff_wangi", "StaffWangi123!")
    create_payload = {
        "name": "Cuci Komplit Reguler",
        "pricing_type": "PER_KG",
        "unit": "KG",
        "unit_price": 8000,
        "estimated_hours": 48,
        "requires_ironing": True,
    }
    res_forbidden = client.post("/api/v1/services", json=create_payload, headers=staff_headers)
    assert res_forbidden.status_code == 403

    # 2. Owner creates service
    owner_headers = _login(client, "owner_wangi", "OwnerWangi123!")
    create_res = client.post("/api/v1/services", json=create_payload, headers=owner_headers)
    assert create_res.status_code == 200
    service = create_res.json()["data"]
    service_id = service["id"]
    assert service["unit_price"] == 8000
    assert service["version"] == 1

    # 3. Owner updates service price -> Version increments to 2
    update_res = client.put(
        f"/api/v1/services/{service_id}",
        json={"unit_price": 9000},
        headers=owner_headers,
    )
    assert update_res.status_code == 200
    updated = update_res.json()["data"]
    assert updated["unit_price"] == 9000
    assert updated["version"] == 2

    # 4. List services
    list_res = client.get("/api/v1/services")
    assert list_res.status_code == 200
    assert len(list_res.json()["data"]) >= 1

