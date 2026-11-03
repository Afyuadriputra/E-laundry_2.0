import uuid
from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.permissions import require_owner
from app.db.session import get_db
from app.modules.auth.dependencies import verify_csrf
from app.modules.users.models import User
from app.modules.users.schemas import UserCreate, UserRead, UserUpdate
from app.modules.users.service import UserService
from app.shared.schemas.responses import StandardResponse

router = APIRouter(prefix="/users", tags=["Users Management"])


@router.get("", response_model=StandardResponse[list[UserRead]])
def list_users(
    current_user: Annotated[User, Depends(require_owner)],
    db: Annotated[Session, Depends(get_db)],
) -> StandardResponse[list[UserRead]]:
    """List all user accounts for the current business (Owner only)."""
    users = UserService.list_users(db, current_user.business_id)
    return StandardResponse(
        data=[
            UserRead(
                id=u.id,
                business_id=u.business_id,
                username=u.username,
                full_name=u.full_name,
                role=u.role,
                phone_e164=u.phone_e164,
                is_active=u.is_active,
                created_at=u.created_at,
                last_login_at=u.last_login_at,
            )
            for u in users
        ]
    )


@router.post(
    "",
    response_model=StandardResponse[UserRead],
    dependencies=[Depends(verify_csrf)],
)
def create_user(
    payload: UserCreate,
    current_user: Annotated[User, Depends(require_owner)],
    db: Annotated[Session, Depends(get_db)],
) -> StandardResponse[UserRead]:
    """Create a new staff user account (Owner only)."""
    user = UserService.create_user(db, current_user.business_id, payload)
    return StandardResponse(
        data=UserRead(
            id=user.id,
            business_id=user.business_id,
            username=user.username,
            full_name=user.full_name,
            role=user.role,
            phone_e164=user.phone_e164,
            is_active=user.is_active,
            created_at=user.created_at,
            last_login_at=user.last_login_at,
        )
    )


@router.patch(
    "/{user_id}",
    response_model=StandardResponse[UserRead],
    dependencies=[Depends(verify_csrf)],
)
def update_user(
    user_id: uuid.UUID,
    payload: UserUpdate,
    current_user: Annotated[User, Depends(require_owner)],
    db: Annotated[Session, Depends(get_db)],
) -> StandardResponse[UserRead]:
    """Update a staff user account (Owner only)."""
    user = UserService.update_user(db, current_user.business_id, user_id, payload)
    return StandardResponse(
        data=UserRead(
            id=user.id,
            business_id=user.business_id,
            username=user.username,
            full_name=user.full_name,
            role=user.role,
            phone_e164=user.phone_e164,
            is_active=user.is_active,
            created_at=user.created_at,
            last_login_at=user.last_login_at,
        )
    )


@router.post(
    "/{user_id}/deactivate",
    response_model=StandardResponse[UserRead],
    dependencies=[Depends(verify_csrf)],
)
def deactivate_user(
    user_id: uuid.UUID,
    current_user: Annotated[User, Depends(require_owner)],
    db: Annotated[Session, Depends(get_db)],
) -> StandardResponse[UserRead]:
    """Deactivate a staff user account and revoke all active sessions (Owner only)."""
    user = UserService.deactivate_user(db, current_user.business_id, user_id)
    return StandardResponse(
        data=UserRead(
            id=user.id,
            business_id=user.business_id,
            username=user.username,
            full_name=user.full_name,
            role=user.role,
            phone_e164=user.phone_e164,
            is_active=user.is_active,
            created_at=user.created_at,
            last_login_at=user.last_login_at,
        )
    )
