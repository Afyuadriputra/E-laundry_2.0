from typing import Annotated

from fastapi import APIRouter, Depends, Request, Response
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import generate_csrf_token
from app.db.session import get_db
from app.modules.auth.dependencies import (
    get_current_user,
    verify_csrf,
)
from app.modules.auth.schemas import (
    ChangePasswordRequest,
    CsrfResponse,
    LoginRequest,
    LoginResponse,
    MessageResponse,
    UserSummary,
)
from app.modules.auth.service import AuthService
from app.modules.users.models import User
from app.shared.schemas.responses import StandardResponse

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.get("/csrf", response_model=StandardResponse[CsrfResponse])
def get_csrf(
    request: Request,
    response: Response,
    db: Annotated[Session, Depends(get_db)],
) -> StandardResponse[CsrfResponse]:
    """Get a CSRF token for the active session, or generate an initial token."""
    raw_token = request.cookies.get("session_id")
    token_str = ""
    if raw_token:
        result = AuthService.get_active_session(db, raw_token)
        if result:
            session, _ = result
            token_str = session.csrf_secret_hash_or_reference or ""

    if not token_str:
        token_str = generate_csrf_token()

    # Expose token via cookie for client-side JavaScript (non-HttpOnly)
    response.set_cookie(
        key="csrf_token",
        value=token_str,
        httponly=False,
        samesite="lax",
        secure=settings.APP_ENV != "development",
        path="/",
    )
    response.headers["X-CSRF-Token"] = token_str
    return StandardResponse(data=CsrfResponse(csrf_token=token_str))


@router.post("/login", response_model=StandardResponse[LoginResponse])
def login(
    payload: LoginRequest,
    request: Request,
    response: Response,
    db: Annotated[Session, Depends(get_db)],
) -> StandardResponse[LoginResponse]:
    """Authenticate user with username and password, issuing an HttpOnly session cookie."""
    client_ip = request.client.host if request.client else "unknown"
    user_agent = request.headers.get("User-Agent")

    user = AuthService.authenticate_user(
        db,
        username=payload.username,
        password=payload.password,
        client_ip=client_ip,
    )

    raw_token, csrf_secret, _ = AuthService.create_session(
        db,
        user_id=user.id,
        user_agent=user_agent,
    )

    # Set secure HttpOnly cookie for session token
    response.set_cookie(
        key="session_id",
        value=raw_token,
        httponly=True,
        samesite="lax",
        secure=settings.APP_ENV != "development",
        max_age=7 * 24 * 3600,
        path="/",
    )

    # Set CSRF token cookie readable by frontend scripts
    response.set_cookie(
        key="csrf_token",
        value=csrf_secret,
        httponly=False,
        samesite="lax",
        secure=settings.APP_ENV != "development",
        max_age=7 * 24 * 3600,
        path="/",
    )
    response.headers["X-CSRF-Token"] = csrf_secret

    user_summary = UserSummary(
        id=user.id,
        username=user.username,
        full_name=user.full_name,
        role=user.role,
        business_id=user.business_id,
        phone_e164=user.phone_e164,
        is_active=user.is_active,
    )

    return StandardResponse(
        data=LoginResponse(
            user=user_summary,
            csrf_token=csrf_secret,
        )
    )


@router.post("/logout", response_model=StandardResponse[MessageResponse])
def logout(
    request: Request,
    response: Response,
    db: Annotated[Session, Depends(get_db)],
) -> StandardResponse[MessageResponse]:
    """Revoke active session and delete session cookies."""
    raw_token = request.cookies.get("session_id")
    if not raw_token:
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            raw_token = auth_header.split(" ", 1)[1].strip()

    if raw_token:
        AuthService.revoke_session(db, raw_token)

    response.delete_cookie(key="session_id", path="/")
    response.delete_cookie(key="csrf_token", path="/")

    return StandardResponse(data=MessageResponse(message="Sesi berhasil diakhiri (logout sukses)."))


@router.get("/me", response_model=StandardResponse[UserSummary])
def get_me(
    current_user: Annotated[User, Depends(get_current_user)],
) -> StandardResponse[UserSummary]:
    """Get current authenticated user profile."""
    return StandardResponse(
        data=UserSummary(
            id=current_user.id,
            username=current_user.username,
            full_name=current_user.full_name,
            role=current_user.role,
            business_id=current_user.business_id,
            phone_e164=current_user.phone_e164,
            is_active=current_user.is_active,
        )
    )


@router.post(
    "/change-password",
    response_model=StandardResponse[MessageResponse],
    dependencies=[Depends(verify_csrf)],
)
def change_password(
    payload: ChangePasswordRequest,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
) -> StandardResponse[MessageResponse]:
    """Change authenticated user password and invalidate previous sessions."""
    AuthService.change_password(
        db,
        user=current_user,
        old_password=payload.old_password,
        new_password=payload.new_password,
    )
    return StandardResponse(
        data=MessageResponse(
            message="Password berhasil diubah. Seluruh sesi sebelumnya telah dicabut."
        )
    )
