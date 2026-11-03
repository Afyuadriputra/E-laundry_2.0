import uuid
from datetime import date

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.modules.businesses.models import Business
from app.modules.users.models import User, UserRole


def _login(client: TestClient, username: str, password: str) -> dict[str, str]:
    res = client.post("/api/v1/auth/login", json={"username": username, "password": password})
    assert res.status_code == 200
    csrf = res.json()["data"]["csrf_token"]
    return {"X-CSRF-Token": csrf}


def test_expenses_lifecycle_and_rbac(client: TestClient, db_session: Session):
    business_id = uuid.uuid4()
    business = Business(
        id=business_id,
        name="Laundry Pengeluaran Bersih",
        phone_e164="+6281277776666",
        address="Jl. Anggrek 12",
        timezone="Asia/Jakarta",
        is_active=True,
    )
    db_session.add(business)

    owner = User(
        id=uuid.uuid4(),
        business_id=business_id,
        username="owner_exp",
        full_name="Pak Bos Exp",
        password_hash=hash_password("OwnerExp123!"),
        role=UserRole.OWNER.value,
        is_active=True,
    )
    cashier = User(
        id=uuid.uuid4(),
        business_id=business_id,
        username="kasir_exp",
        full_name="Kasir Exp",
        password_hash=hash_password("KasirExp123!"),
        role=UserRole.CASHIER.value,
        is_active=True,
    )
    db_session.add_all([owner, cashier])
    db_session.commit()

    # 1. Cashier creates expense
    cashier_headers = _login(client, "kasir_exp", "KasirExp123!")
    res_create = client.post(
        "/api/v1/expenses",
        json={
            "category": "DETERGENT",
            "amount": 150000,
            "expense_date": str(date.today()),
            "description": "Beli deterjen cair 2 jerigen",
        },
        headers=cashier_headers,
    )
    assert res_create.status_code == 200
    exp_data = res_create.json()["data"]
    exp_id = exp_data["id"]
    assert exp_data["category"] == "DETERGENT"
    assert exp_data["amount"] == 150000

    # 2. List expenses
    res_list = client.get("/api/v1/expenses?category=DETERGENT", headers=cashier_headers)
    assert res_list.status_code == 200
    items = res_list.json()["data"]
    assert len(items) == 1
    assert items[0]["id"] == exp_id

    # 3. Cashier tries to update expense -> 403 Forbidden
    res_cashier_update = client.put(
        f"/api/v1/expenses/{exp_id}",
        json={"amount": 160000},
        headers=cashier_headers,
    )
    assert res_cashier_update.status_code == 403

    # 4. Owner updates expense
    owner_headers = _login(client, "owner_exp", "OwnerExp123!")
    res_owner_update = client.put(
        f"/api/v1/expenses/{exp_id}",
        json={"amount": 160000, "description": "Deterjen + pewangi"},
        headers=owner_headers,
    )
    assert res_owner_update.status_code == 200
    assert res_owner_update.json()["data"]["amount"] == 160000

    # 5. Owner deletes expense
    res_del = client.delete(f"/api/v1/expenses/{exp_id}", headers=owner_headers)
    assert res_del.status_code == 200

    # Verify not found after deletion
    res_get = client.get(f"/api/v1/expenses/{exp_id}", headers=owner_headers)
    assert res_get.status_code == 404
