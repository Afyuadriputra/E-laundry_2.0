import time
import uuid
from collections import defaultdict
from datetime import UTC, datetime, timedelta

from sqlalchemy import select, update
from sqlalchemy.orm import Session

from app.core.exceptions import AppException, ForbiddenException, UnauthenticatedException
from app.core.security import (
    generate_csrf_token,
    generate_session_token,
    hash_password,
    hash_session_token,
    verify_password,
)
from app.modules.auth.models import UserSession
from app.modules.users.models import User

# In-memory login attempt tracker for rate limiting: key -> list of float timestamps
_login_failures: dict[str, list[float]] = defaultdict(list)
_MAX_FAILURES = 5
_WINDOW_SECONDS = 300.0  # 5 minutes


def _ensure_utc(dt: datetime) -> datetime:
    """Ensure datetime is timezone-aware UTC for safe comparisons across SQLite and PostgreSQL."""
    if dt.tzinfo is None:
        return dt.replace(tzinfo=UTC)
    return dt


class AuthService:
    @staticmethod
    def check_login_throttle(identifier: str) -> None:
        """Enforce login attempt rate limiting."""
        now = time.time()
        # Clean up older timestamps
        failures = [t for t in _login_failures[identifier] if now - t < _WINDOW_SECONDS]
        _login_failures[identifier] = failures

        if len(failures) >= _MAX_FAILURES:
            raise AppException(
                code="RATE_LIMIT_EXCEEDED",
                message="Terlalu banyak percobaan login yang gagal. Silakan coba 5 menit lagi.",
                status_code=429,
            )

    @staticmethod
    def record_login_failure(identifier: str) -> None:
        _login_failures[identifier].append(time.time())

    @staticmethod
    def reset_login_failures(identifier: str) -> None:
        if identifier in _login_failures:
            del _login_failures[identifier]

    @staticmethod
    def authenticate_user(
        db: Session,
        username: str,
        password: str,
        client_ip: str = "unknown",
    ) -> User:
        throttle_key = f"{client_ip}:{username.lower()}"
        AuthService.check_login_throttle(throttle_key)

        stmt = select(User).where(User.username == username.strip())
        user = db.scalar(stmt)

        if not user or not verify_password(password, user.password_hash):
            AuthService.record_login_failure(throttle_key)
            raise UnauthenticatedException("Username atau password salah")

        if not user.is_active:
            raise ForbiddenException("Akun telah dinonaktifkan. Hubungi pemilik laundry.")

        AuthService.reset_login_failures(throttle_key)

        now = datetime.now(UTC)
        user.last_login_at = now
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def create_session(
        db: Session,
        user_id: uuid.UUID,
        user_agent: str | None = None,
    ) -> tuple[str, str, UserSession]:
        raw_token = generate_session_token()
        token_hash = hash_session_token(raw_token)
        csrf_secret = generate_csrf_token()

        now = datetime.now(UTC)
        expires_at = now + timedelta(hours=12)
        absolute_expires_at = now + timedelta(days=7)

        session = UserSession(
            user_id=user_id,
            session_token_hash=token_hash,
            csrf_secret_hash_or_reference=csrf_secret,
            created_at=now,
            last_activity_at=now,
            expires_at=expires_at,
            absolute_expires_at=absolute_expires_at,
            revoked_at=None,
            user_agent_summary=user_agent[:255] if user_agent else None,
        )
        db.add(session)
        db.commit()
        db.refresh(session)
        return raw_token, csrf_secret, session

    @staticmethod
    def get_active_session(
        db: Session,
        raw_token: str,
    ) -> tuple[UserSession, User] | None:
        token_hash = hash_session_token(raw_token)
        stmt = (
            select(UserSession, User)
            .join(User, UserSession.user_id == User.id)
            .where(
                UserSession.session_token_hash == token_hash,
                UserSession.revoked_at.is_(None),
            )
        )
        result = db.execute(stmt).first()
        if not result:
            return None

        session, user = result
        now = datetime.now(UTC)

        expires_at = _ensure_utc(session.expires_at)
        absolute_expires_at = _ensure_utc(session.absolute_expires_at)

        # Inactivity or absolute timeout check
        if now > absolute_expires_at or now > expires_at:
            session.revoked_at = now
            db.commit()
            return None

        # User status check
        if not user.is_active:
            session.revoked_at = now
            db.commit()
            return None

        # Sliding window update: 12 hours capped at absolute_expires_at
        session.last_activity_at = now
        new_expires_at = min(now + timedelta(hours=12), absolute_expires_at)
        session.expires_at = new_expires_at
        db.commit()

        return session, user

    @staticmethod
    def revoke_session(db: Session, raw_token: str) -> bool:
        token_hash = hash_session_token(raw_token)
        stmt = select(UserSession).where(
            UserSession.session_token_hash == token_hash,
            UserSession.revoked_at.is_(None),
        )
        session = db.scalar(stmt)
        if session:
            session.revoked_at = datetime.now(UTC)
            db.commit()
            return True
        return False

    @staticmethod
    def revoke_all_user_sessions(db: Session, user_id: uuid.UUID) -> None:
        now = datetime.now(UTC)
        stmt = (
            update(UserSession)
            .where(
                UserSession.user_id == user_id,
                UserSession.revoked_at.is_(None),
            )
            .values(revoked_at=now)
        )
        db.execute(stmt)
        db.commit()

    @staticmethod
    def change_password(
        db: Session,
        user: User,
        old_password: str,
        new_password: str,
    ) -> None:
        if not verify_password(old_password, user.password_hash):
            raise AppException(
                code="INVALID_OLD_PASSWORD",
                message="Password lama tidak sesuai",
                status_code=400,
            )

        now = datetime.now(UTC)
        user.password_hash = hash_password(new_password)
        user.password_changed_at = now
        db.commit()

        # Revoke all existing sessions on password change
        AuthService.revoke_all_user_sessions(db, user.id)
