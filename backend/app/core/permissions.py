from collections.abc import Callable
from enum import StrEnum
from typing import Annotated

from fastapi import Depends

from app.core.exceptions import ForbiddenException
from app.modules.auth.dependencies import get_current_user
from app.modules.users.models import User


class Role(StrEnum):
    OWNER = "OWNER"
    CASHIER = "CASHIER"
    STAFF = "STAFF"
    COURIER = "COURIER"


def require_roles(*allowed_roles: str) -> Callable[[User], User]:
    def dependency(
        current_user: Annotated[User, Depends(get_current_user)],
    ) -> User:
        if current_user.role not in allowed_roles:
            raise ForbiddenException(
                f"Akses ditolak: role '{current_user.role}' tidak memiliki izin untuk aksi ini."
            )
        return current_user

    return dependency


# Standard permission dependencies
require_owner = require_roles(Role.OWNER.value)
require_owner_or_cashier = require_roles(Role.OWNER.value, Role.CASHIER.value)
require_staff_or_above = require_roles(Role.OWNER.value, Role.CASHIER.value, Role.STAFF.value)
require_any_authenticated = require_roles(
    Role.OWNER.value,
    Role.CASHIER.value,
    Role.STAFF.value,
    Role.COURIER.value,
)
