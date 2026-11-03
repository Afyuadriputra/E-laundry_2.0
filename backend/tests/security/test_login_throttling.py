import uuid

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.modules.businesses.models import Business
from app.modules.users.models import User, UserRole


def test_login_throttling_after_five_failed_attempts(
    client: TestClient,
    db_session: Session,
):
    business = Business(
        id=uuid.uuid4(),
        name="Throttled Laundry",
        phone_e164="+628111999888",
        address="Jl. Throttling No. 1",
        timezone="Asia/Jakarta",
        is_active=True,
    )
    db_session.add(business)
    db_session.commit()

    username = "target_user_throttle"
    correct_password = "CorrectPass123!"
    user = User(
        id=uuid.uuid4(),
        business_id=business.id,
        username=username,
        full_name="Target Throttle",
        password_hash=hash_password(correct_password),
        role=UserRole.CASHIER.value,
        is_active=True,
    )
    db_session.add(user)
    db_session.commit()

    # Attempt 5 incorrect logins
    for i in range(5):
        res = client.post(
            "/api/v1/auth/login",
            json={"username": username, "password": f"WrongPass{i}!"},
        )
        assert res.status_code == 401

    # 6th attempt should be blocked by rate limiter with 429
    res_blocked = client.post(
        "/api/v1/auth/login",
        json={"username": username, "password": correct_password},
    )
    assert res_blocked.status_code == 429
    assert res_blocked.json()["error"]["code"] == "RATE_LIMIT_EXCEEDED"
