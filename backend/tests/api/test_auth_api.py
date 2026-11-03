import uuid

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.modules.businesses.models import Business
from app.modules.users.models import User, UserRole


def test_auth_full_lifecycle(client: TestClient, db_session: Session):
    # Seed business and user
    business = Business(
        id=uuid.uuid4(),
        name="Bersih Cepat Laundry",
        phone_e164="+628111222333",
        address="Jl. Melati No. 10",
        timezone="Asia/Jakarta",
        is_active=True,
    )
    db_session.add(business)
    db_session.commit()

    raw_password = "Password123!"
    user = User(
        id=uuid.uuid4(),
        business_id=business.id,
        username="kasir_siti",
        full_name="Siti Rahmawati",
        password_hash=hash_password(raw_password),
        role=UserRole.CASHIER.value,
        phone_e164="+628111222334",
        is_active=True,
    )
    db_session.add(user)
    db_session.commit()

    # 1. CSRF token endpoint
    res_csrf = client.get("/api/v1/auth/csrf")
    assert res_csrf.status_code == 200
    csrf_data = res_csrf.json()["data"]
    assert "csrf_token" in csrf_data
    assert len(csrf_data["csrf_token"]) > 20

    # 2. Failed login with wrong password
    res_fail = client.post(
        "/api/v1/auth/login",
        json={"username": "kasir_siti", "password": "WrongPassword!"},
    )
    assert res_fail.status_code == 401
    assert res_fail.json()["error"]["code"] == "UNAUTHENTICATED"

    # 3. Successful login
    res_login = client.post(
        "/api/v1/auth/login",
        json={"username": "kasir_siti", "password": raw_password},
    )
    assert res_login.status_code == 200
    login_data = res_login.json()["data"]
    assert login_data["user"]["username"] == "kasir_siti"
    assert login_data["user"]["role"] == "CASHIER"
    csrf_token = login_data["csrf_token"]

    # Verify session cookie was set
    assert "session_id" in client.cookies

    # 4. Check /auth/me
    res_me = client.get("/api/v1/auth/me")
    assert res_me.status_code == 200
    me_data = res_me.json()["data"]
    assert me_data["username"] == "kasir_siti"
    assert me_data["role"] == "CASHIER"

    # 5. Change password without CSRF header -> must be rejected (403 Forbidden)
    res_pw_no_csrf = client.post(
        "/api/v1/auth/change-password",
        json={"old_password": raw_password, "new_password": "NewSecretPass456!"},
    )
    assert res_pw_no_csrf.status_code == 403
    assert res_pw_no_csrf.json()["error"]["code"] == "FORBIDDEN"

    # 6. Change password with valid CSRF header -> success (200 OK)
    res_pw_ok = client.post(
        "/api/v1/auth/change-password",
        headers={"X-CSRF-Token": csrf_token},
        json={"old_password": raw_password, "new_password": "NewSecretPass456!"},
    )
    assert res_pw_ok.status_code == 200

    # 7. Old session is now invalidated by password change
    res_me_invalid = client.get("/api/v1/auth/me")
    assert res_me_invalid.status_code == 401

    # 8. Login with new password
    res_login_new = client.post(
        "/api/v1/auth/login",
        json={"username": "kasir_siti", "password": "NewSecretPass456!"},
    )
    assert res_login_new.status_code == 200

    # 9. Logout
    res_logout = client.post("/api/v1/auth/logout")
    assert res_logout.status_code == 200

    # Verify session is ended
    res_after_logout = client.get("/api/v1/auth/me")
    assert res_after_logout.status_code == 401


def test_inactive_account_rejection(client: TestClient, db_session: Session):
    business = Business(
        id=uuid.uuid4(),
        name="Laundry Nonaktif Test",
        phone_e164="+628111222444",
        address="Jl. Test No. 99",
        timezone="Asia/Jakarta",
        is_active=True,
    )
    db_session.add(business)
    db_session.commit()

    raw_password = "PasswordBlocked123!"
    blocked_user = User(
        id=uuid.uuid4(),
        business_id=business.id,
        username="pegawai_nonaktif",
        full_name="Pegawai Nonaktif",
        password_hash=hash_password(raw_password),
        role=UserRole.STAFF.value,
        is_active=False,
    )
    db_session.add(blocked_user)
    db_session.commit()

    res = client.post(
        "/api/v1/auth/login",
        json={"username": "pegawai_nonaktif", "password": raw_password},
    )
    assert res.status_code == 403
    assert res.json()["error"]["code"] == "FORBIDDEN"
