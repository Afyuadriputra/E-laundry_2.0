import uuid
from datetime import UTC, datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.exceptions import NotFoundException
from app.modules.businesses.models import Business, BusinessSettings
from app.modules.businesses.schemas import BusinessSettingsUpdate, BusinessUpdate


class BusinessService:
    @staticmethod
    def get_business(db: Session, business_id: uuid.UUID) -> Business:
        stmt = select(Business).where(Business.id == business_id)
        business = db.scalar(stmt)
        if not business:
            raise NotFoundException("Data bisnis tidak ditemukan.")
        return business

    @staticmethod
    def update_business(
        db: Session,
        business_id: uuid.UUID,
        payload: BusinessUpdate,
    ) -> Business:
        business = BusinessService.get_business(db, business_id)
        if payload.name is not None:
            business.name = payload.name.strip()
        if payload.phone_e164 is not None:
            business.phone_e164 = payload.phone_e164.strip()
        if payload.address is not None:
            business.address = payload.address.strip()
        if payload.logo_path is not None:
            business.logo_path = payload.logo_path.strip() if payload.logo_path else None
        if payload.timezone is not None:
            business.timezone = payload.timezone.strip()

        business.updated_at = datetime.now(UTC)
        db.commit()
        db.refresh(business)
        return business

    @staticmethod
    def get_settings(db: Session, business_id: uuid.UUID) -> BusinessSettings:
        stmt = select(BusinessSettings).where(BusinessSettings.business_id == business_id)
        settings = db.scalar(stmt)
        if not settings:
            # Create default settings if not exists
            settings = BusinessSettings(
                business_id=business_id,
                pickup_enabled=True,
                delivery_enabled=True,
                default_delivery_fee=5000,
                default_completion_hours=48,
                weight_precision=1,
                weight_rounding_mode="HALF_UP",
            )
            db.add(settings)
            db.commit()
            db.refresh(settings)
        return settings

    @staticmethod
    def update_settings(
        db: Session,
        business_id: uuid.UUID,
        user_id: uuid.UUID,
        payload: BusinessSettingsUpdate,
    ) -> BusinessSettings:
        settings = BusinessService.get_settings(db, business_id)

        if payload.pickup_enabled is not None:
            settings.pickup_enabled = payload.pickup_enabled
        if payload.delivery_enabled is not None:
            settings.delivery_enabled = payload.delivery_enabled
        if payload.default_delivery_fee is not None:
            settings.default_delivery_fee = payload.default_delivery_fee
        if payload.default_completion_hours is not None:
            settings.default_completion_hours = payload.default_completion_hours
        if payload.weight_precision is not None:
            settings.weight_precision = payload.weight_precision
        if payload.weight_rounding_mode is not None:
            settings.weight_rounding_mode = payload.weight_rounding_mode
        if payload.operating_hours is not None:
            settings.operating_hours = payload.operating_hours

        settings.updated_by = user_id
        settings.updated_at = datetime.now(UTC)
        db.commit()
        db.refresh(settings)
        return settings
