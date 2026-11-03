import uuid

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.core.exceptions import ConflictException, ForbiddenException, NotFoundException
from app.core.security import hash_password
from app.modules.audit.service import AuditService
from app.modules.auth.service import AuthService
from app.modules.users.models import User, UserRole
from app.modules.users.schemas import UserCreate, UserUpdate


class UserService:
    @staticmethod
    def list_users(db: Session, business_id: uuid.UUID) -> list[User]:
        stmt = select(User).where(User.business_id == business_id).order_by(User.created_at.desc())
        return list(db.scalars(stmt).all())

    @staticmethod
    def get_user_by_id(db: Session, business_id: uuid.UUID, user_id: uuid.UUID) -> User:
        stmt = select(User).where(User.id == user_id, User.business_id == business_id)
        user = db.scalar(stmt)
        if not user:
            raise NotFoundException("Pengguna tidak ditemukan.")
        return user

    @staticmethod
    def create_user(db: Session, business_id: uuid.UUID, payload: UserCreate) -> User:
        # Check duplicate username within business
        stmt = select(User).where(
            User.business_id == business_id,
            func.lower(User.username) == payload.username.strip().lower(),
        )
        if db.scalar(stmt):
            raise ConflictException(
                code="USERNAME_TAKEN",
                message=f"Username '{payload.username}' sudah digunakan dalam usaha ini.",
            )

        new_user = User(
            business_id=business_id,
            username=payload.username.strip(),
            full_name=payload.full_name.strip(),
            password_hash=hash_password(payload.password),
            role=payload.role.value,
            phone_e164=payload.phone_e164.strip() if payload.phone_e164 else None,
            is_active=True,
        )
        db.add(new_user)
        AuditService.record(
            db=db,
            action="USER_CREATED",
            resource_type="user",
            resource_id=new_user.id,
            after_data={"username": new_user.username, "role": new_user.role},
        )
        db.commit()
        db.refresh(new_user)
        return new_user

    @staticmethod
    def update_user(
        db: Session,
        business_id: uuid.UUID,
        user_id: uuid.UUID,
        payload: UserUpdate,
    ) -> User:
        user = UserService.get_user_by_id(db, business_id, user_id)

        # Invariant: Cannot demote or deactivate the last active owner
        is_demoting = (
            payload.role and payload.role != UserRole.OWNER and user.role == UserRole.OWNER.value
        )
        is_deactivating = payload.is_active is False and user.role == UserRole.OWNER.value
        if is_demoting or is_deactivating:
            active_owners_count = (
                db.scalar(
                    select(func.count(User.id)).where(
                        User.business_id == business_id,
                        User.role == UserRole.OWNER.value,
                        User.is_active.is_(True),
                    )
                )
                or 0
            )
            if active_owners_count <= 1:
                raise ForbiddenException(
                    "Operasi ditolak: tidak dapat mengubah role atau menonaktifkan Owner terakhir."
                )

        if payload.full_name is not None:
            user.full_name = payload.full_name.strip()
        if payload.role is not None:
            user.role = payload.role.value
        if payload.phone_e164 is not None:
            user.phone_e164 = payload.phone_e164.strip() if payload.phone_e164 else None
        if payload.is_active is not None:
            user.is_active = payload.is_active
            if not user.is_active:
                AuthService.revoke_all_user_sessions(db, user.id)

        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def deactivate_user(db: Session, business_id: uuid.UUID, user_id: uuid.UUID) -> User:
        user = UserService.get_user_by_id(db, business_id, user_id)

        if user.role == UserRole.OWNER.value:
            active_owners_count = (
                db.scalar(
                    select(func.count(User.id)).where(
                        User.business_id == business_id,
                        User.role == UserRole.OWNER.value,
                        User.is_active.is_(True),
                    )
                )
                or 0
            )
            if active_owners_count <= 1:
                raise ForbiddenException(
                    "Operasi ditolak: tidak dapat menonaktifkan akun Owner terakhir."
                )

        user.is_active = False
        AuditService.record(
            db=db,
            action="USER_DEACTIVATED",
            resource_type="user",
            resource_id=user.id,
            before_data={"username": user.username, "is_active": True},
            after_data={"username": user.username, "is_active": False},
        )
        db.commit()
        AuthService.revoke_all_user_sessions(db, user.id)
        db.refresh(user)
        return user
