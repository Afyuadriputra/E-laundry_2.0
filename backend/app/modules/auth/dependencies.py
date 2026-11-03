from typing import Annotated

from fastapi import Depends, Request
from sqlalchemy.orm import Session

from app.core.exceptions import ForbiddenException, UnauthenticatedException
from app.core.security import verify_csrf_token
from app.db.session import get_db
from app.modules.auth.models import UserSession
from app.modules.auth.service import AuthService
from app.modules.users.models import User


def get_current_user_and_session(
    request: Request,
    db: Annotated[Session, Depends(get_db)],
) -> tuple[User, UserSession]:
    # Extract session token from cookie first, then fallback to Authorization header
    raw_token = request.cookies.get("session_id")
    if not raw_token:
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            raw_token = auth_header.split(" ", 1)[1].strip()

    if not raw_token:
        raise UnauthenticatedException("Sesi autentikasi tidak ditemukan. Silakan login.")

    result = AuthService.get_active_session(db, raw_token)
    if not result:
        raise UnauthenticatedException(
            "Sesi telah berakhir atau tidak valid. Silakan login kembali."
        )

    session, user = result
    return user, session


def get_current_user(
    auth: Annotated[tuple[User, UserSession], Depends(get_current_user_and_session)],
) -> User:
    return auth[0]


def get_current_session(
    auth: Annotated[tuple[User, UserSession], Depends(get_current_user_and_session)],
) -> UserSession:
    return auth[1]


def verify_csrf(
    request: Request,
    auth: Annotated[tuple[User, UserSession], Depends(get_current_user_and_session)],
) -> None:
    # State-changing HTTP methods require CSRF validation
    if request.method in ("POST", "PUT", "PATCH", "DELETE"):
        csrf_header = request.headers.get("X-CSRF-Token")
        _, session = auth
        expected_csrf = session.csrf_secret_hash_or_reference or ""

        if not csrf_header or not verify_csrf_token(csrf_header, expected_csrf):
            raise ForbiddenException("Token CSRF tidak valid atau tidak cocok.")
