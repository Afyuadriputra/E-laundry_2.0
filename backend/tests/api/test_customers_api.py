import uuid

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.modules.businesses.models import Business, BusinessSettings
from app.modules.customers.schemas import normalize_phone_e164
from app.modules.users.models import User, UserRole


def _login(client: TestClient, username: str, password: str) -> dict[str, str]:
    res = client.post("/api/v1/auth/login", json={"username": username, "password": password})
    assert res.status_code == 200
    csrf = res.headers.get("X-CSRF-Token") or res.json()["data"]["csrf_token"]
    return {"X-CSRF-Token": csrf}


def test_phone_normalizer():
    assert normalize_phone_e164("08123456789") == "+628123456789"
    assert normalize_phone_e164("+628123456789") == "+628123456789"
    assert normalize_phone_e164("628123456789") == "+628123456789"
    assert normalize_phone_e164(" 0812-3456-789 ") == "+628123456789"


def test_customer_crud_and_search(client: TestClient, db_session: Session):
    business_id = uuid.uuid4()
    business = Business(
        id=business_id,
        name="Laundry Jaya",
        phone_e164="+62811112222",
        address="Jl. Melati",
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

    cashier = User(
        id=uuid.uuid4(),
        business_id=business_id,
        username="kasir_siti",
        full_name="Siti Rahma",
        password_hash=hash_password("KasirPass123!"),
        role=UserRole.CASHIER.value,
        is_active=True,
    )
    db_session.add(cashier)
    db_session.commit()

    headers = _login(client, "kasir_siti", "KasirPass123!")

    # 1. Create Customer
    payload = {
        "full_name": "Pak Ahmad Yani",
        "phone_e164": "081234567890",
        "address": "Jl. Mawar No. 12",
        "notes": "Pelanggan prioritas",
    }
    create_res = client.post("/api/v1/customers", json=payload, headers=headers)
    assert create_res.status_code == 200
    created = create_res.json()["data"]
    customer_id = created["id"]
    assert created["full_name"] == "Pak Ahmad Yani"
    assert created["phone_e164"] == "+6281234567890"

    # 2. Get Customer Detail
    get_res = client.get(f"/api/v1/customers/{customer_id}")
    assert get_res.status_code == 200
    assert get_res.json()["data"]["total_orders"] == 0

    # 3. List Customers with search
    search_res = client.get("/api/v1/customers?search=Ahmad")
    assert search_res.status_code == 200
    assert len(search_res.json()["data"]) == 1

    search_phone_res = client.get("/api/v1/customers?search=081234567890")
    assert search_phone_res.status_code == 200
    assert len(search_phone_res.json()["data"]) == 1

    # 4. Update Customer
    update_res = client.put(
        f"/api/v1/customers/{customer_id}",
        json={"notes": "Diperbarui: sering request pewangi lavender"},
        headers=headers,
    )
    assert update_res.status_code == 200
    assert "lavender" in update_res.json()["data"]["notes"]

