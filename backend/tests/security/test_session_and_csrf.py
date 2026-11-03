import uuid
from datetime import UTC, datetime, timedelta

from sqlalchemy.orm import Session

from app.core.security import generate_csrf_token, verify_csrf_token
from app.modules.auth.service import AuthService
from app.modules.businesses.models import Business
from app.modules.users.models import User, UserRole


def test_session_lifecycle(db_session: Session):
    # Setup test business & user
    business = Business(
        id=uuid.uuid4(),
        name="Test Laundry Express",
        phone_e164="+6281234567890",
        address="Jl. Test No. 1",
        timezone="Asia/Jakarta",
        is_active=True,
    )
    db_session.add(business)
    db_session.commit()

    user = User(
        id=uuid.uuid4(),
        business_id=business.id,
        username="owner_session_test",
        full_name="Owner Test",
        password_hash="fake_hash",
        role=UserRole.OWNER.value,
        is_active=True,
    )
    db_session.add(user)
    db_session.commit()

    # Create session
    raw_token, csrf_secret, session_record = AuthService.create_session(
        db_session, user.id, user_agent="Pytest Agent"
    )

    assert len(raw_token) >= 32
    assert session_record.user_id == user.id
    assert session_record.revoked_at is None

    # Validate active session
    active = AuthService.get_active_session(db_session, raw_token)
    assert active is not None
    sess, u = active
    assert u.id == user.id
    assert sess.session_token_hash == session_record.session_token_hash

    # Revoke session
    revoked = AuthService.revoke_session(db_session, raw_token)
    assert revoked is True

    # Validate after revocation
    assert AuthService.get_active_session(db_session, raw_token) is None


def test_session_expiration(db_session: Session):
    business = Business(
        id=uuid.uuid4(),
        name="Test Expiry Laundry",
        phone_e164="+6281234567891",
        address="Jl. Expiry No. 2",
        timezone="Asia/Jakarta",
        is_active=True,
    )
    db_session.add(business)
    db_session.commit()

    user = User(
        id=uuid.uuid4(),
        business_id=business.id,
        username="user_expired",
        full_name="Expired User",
        password_hash="fake_hash",
        role=UserRole.CASHIER.value,
        is_active=True,
    )
    db_session.add(user)
    db_session.commit()

    raw_token, _, session_rec = AuthService.create_session(db_session, user.id)

    # Force expiration in past
    session_rec.expires_at = datetime.now(UTC) - timedelta(minutes=5)
    db_session.commit()

    assert AuthService.get_active_session(db_session, raw_token) is None


def test_csrf_token_generation_and_verification():
    token_1 = generate_csrf_token()
    token_2 = generate_csrf_token()

    assert len(token_1) >= 32
    assert token_1 != token_2
    assert verify_csrf_token(token_1, token_1) is True
    assert verify_csrf_token(token_1, token_2) is False
    assert verify_csrf_token("", token_1) is False
