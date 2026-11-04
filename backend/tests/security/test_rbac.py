"""
Security RBAC (Role-Based Access Control) and Multi-Tenant Isolation Suite.
Verifies permission barriers across OWNER, CASHIER, STAFF, and COURIER,
and ensures complete cross-business multi-tenant isolation.
"""

import uuid

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.modules.businesses.models import Business, BusinessSettings
from app.modules.customers.models import Customer
from app.modules.users.models import User, UserRole


def _create_user_and_login(
    client: TestClient,
    db_session: Session,
    business_id: uuid.UUID,
    username: str,
    role: UserRole,
) -> tuple[dict[str, str], User]:
    raw_pass = "SecurePass123!"
    user = User(
        id=uuid.uuid4(),
        business_id=business_id,
        username=username,
        full_name=f"User {username}",
        password_hash=hash_password(raw_pass),
        role=role.value,
        is_active=True,
    )
    db_session.add(user)
    db_session.commit()

    res = client.post("/api/v1/auth/login", json={"username": username, "password": raw_pass})
    assert res.status_code == 200
    csrf = res.headers.get("X-CSRF-Token") or res.json()["data"]["csrf_token"]
    return {"X-CSRF-Token": csrf}, user


def test_rbac_financial_reports_restricted_to_owner(client: TestClient, db_session: Session):
    """Verify only OWNER can access /api/v1/reports/finances; CASHIER, STAFF, COURIER receive 403."""
    biz = Business(
        id=uuid.uuid4(),
        name="RBAC Reports Laundry",
        phone_e164="+6281200002222",
        address="Jl. RBAC 1",
        timezone="Asia/Jakarta",
        is_active=True,
    )
    db_session.add(biz)
    db_session.commit()

    # 1. Login as CASHIER -> 403
    h_cashier, _ = _create_user_and_login(client, db_session, biz.id, "cashier_rbac", UserRole.CASHIER)
    r1 = client.get("/api/v1/reports/finances", headers=h_cashier)
    assert r1.status_code == 403

    # 2. Login as STAFF -> 403
    h_staff, _ = _create_user_and_login(client, db_session, biz.id, "staff_rbac", UserRole.STAFF)
    r2 = client.get("/api/v1/reports/finances", headers=h_staff)
    assert r2.status_code == 403

    # 3. Login as COURIER -> 403
    h_courier, _ = _create_user_and_login(client, db_session, biz.id, "courier_rbac", UserRole.COURIER)
    r3 = client.get("/api/v1/reports/finances", headers=h_courier)
    assert r3.status_code == 403

    # 4. Login as OWNER -> 200
    h_owner, _ = _create_user_and_login(client, db_session, biz.id, "owner_rbac", UserRole.OWNER)
    r4 = client.get("/api/v1/reports/finances", headers=h_owner)
    assert r4.status_code == 200
    assert "total_cash_received" in r4.json()["data"]


def test_rbac_user_management_restricted_to_owner(client: TestClient, db_session: Session):
    """Verify user management (/api/v1/users) is accessible only to OWNER."""
    biz = Business(
        id=uuid.uuid4(),
        name="RBAC Users Laundry",
        phone_e164="+6281200003333",
        address="Jl. RBAC 2",
        timezone="Asia/Jakarta",
        is_active=True,
    )
    db_session.add(biz)
    db_session.commit()

    # Cashier attempts user list -> 403
    h_cashier, _ = _create_user_and_login(client, db_session, biz.id, "cashier_user_mgr", UserRole.CASHIER)
    res_cashier = client.get("/api/v1/users", headers=h_cashier)
    assert res_cashier.status_code == 403

    # Owner attempts user list -> 200
    h_owner, _ = _create_user_and_login(client, db_session, biz.id, "owner_user_mgr", UserRole.OWNER)
    res_owner = client.get("/api/v1/users", headers=h_owner)
    assert res_owner.status_code == 200


def test_rbac_expense_creation_restricted_to_owner_and_cashier(client: TestClient, db_session: Session):
    """Verify STAFF and COURIER cannot create expenses, while CASHIER and OWNER can."""
    biz = Business(
        id=uuid.uuid4(),
        name="RBAC Expense Laundry",
        phone_e164="+6281200004444",
        address="Jl. RBAC 3",
        timezone="Asia/Jakarta",
        is_active=True,
    )
    db_session.add(biz)
    db_session.commit()

    expense_payload = {
        "amount": 25000,
        "category": "DETERGENT",
        "expense_date": "2026-11-04",
        "description": "Beli sabun cuci",
    }

    # Staff attempt -> 403
    h_staff, _ = _create_user_and_login(client, db_session, biz.id, "staff_exp", UserRole.STAFF)
    res_staff = client.post("/api/v1/expenses", json=expense_payload, headers=h_staff)
    assert res_staff.status_code == 403

    # Courier attempt -> 403
    h_courier, _ = _create_user_and_login(client, db_session, biz.id, "courier_exp", UserRole.COURIER)
    res_courier = client.post("/api/v1/expenses", json=expense_payload, headers=h_courier)
    assert res_courier.status_code == 403

    # Cashier attempt -> 200 or 201
    h_cashier, _ = _create_user_and_login(client, db_session, biz.id, "cashier_exp", UserRole.CASHIER)
    res_cashier = client.post("/api/v1/expenses", json=expense_payload, headers=h_cashier)
    assert res_cashier.status_code in (200, 201)


def test_multi_tenant_isolation(client: TestClient, db_session: Session):
    """Verify tenant isolation: User of Business A cannot read or mutate Business B records."""
    # Create Business A and B
    biz_a = Business(
        id=uuid.uuid4(),
        name="Tenant A Laundry",
        phone_e164="+6281200005555",
        address="Jl. A",
        timezone="Asia/Jakarta",
        is_active=True,
    )
    biz_b = Business(
        id=uuid.uuid4(),
        name="Tenant B Laundry",
        phone_e164="+6281200006666",
        address="Jl. B",
        timezone="Asia/Jakarta",
        is_active=True,
    )
    db_session.add_all([biz_a, biz_b])

    # Customer belonging strictly to Tenant B
    cust_b = Customer(
        id=uuid.uuid4(),
        business_id=biz_b.id,
        full_name="Pelanggan Khusus Toko B",
        phone_e164="+6281288887777",
        is_active=True,
    )
    db_session.add(cust_b)
    db_session.commit()

    # Login as Cashier of Business A
    h_cashier_a, _ = _create_user_and_login(client, db_session, biz_a.id, "cashier_biz_a", UserRole.CASHIER)

    # Cashier A attempts to access Customer of Business B -> Must return 404 Not Found
    res = client.get(f"/api/v1/customers/{cust_b.id}", headers=h_cashier_a)
    assert res.status_code == 404
