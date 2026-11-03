import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.exceptions import NotFoundException
from app.modules.audit.service import AuditService
from app.modules.services.models import Service
from app.modules.services.schemas import ServiceCreate, ServiceUpdate


class ServiceCatalogService:
    @staticmethod
    def list_services(
        db: Session,
        business_id: uuid.UUID,
        is_active: bool | None = None,
    ) -> list[Service]:
        query = select(Service).where(Service.business_id == business_id)
        if is_active is not None:
            query = query.where(Service.is_active == is_active)
        return list(db.scalars(query.order_by(Service.name.asc())).all())

    @staticmethod
    def get_by_id(db: Session, business_id: uuid.UUID, service_id: uuid.UUID) -> Service:
        service = db.scalar(
            select(Service).where(
                Service.id == service_id,
                Service.business_id == business_id,
            )
        )
        if not service:
            raise NotFoundException(f"Layanan dengan ID '{service_id}' tidak ditemukan.")
        return service

    @staticmethod
    def create_service(db: Session, business_id: uuid.UUID, data: ServiceCreate) -> Service:
        service = Service(
            business_id=business_id,
            name=data.name.strip(),
            pricing_type=data.pricing_type.value,
            unit=data.unit.value,
            unit_price=data.unit_price,
            estimated_hours=data.estimated_hours,
            requires_ironing=data.requires_ironing,
            is_active=True,
            version=1,
        )
        db.add(service)
        AuditService.record(
            db=db,
            action="SERVICE_CREATED",
            resource_type="service",
            resource_id=service.id,
            after_data={"name": service.name, "unit_price": service.unit_price, "unit": service.unit},
        )
        db.commit()
        db.refresh(service)
        return service

    @staticmethod
    def update_service(
        db: Session,
        business_id: uuid.UUID,
        service_id: uuid.UUID,
        data: ServiceUpdate,
    ) -> Service:
        service = ServiceCatalogService.get_by_id(db, business_id, service_id)

        old_price = service.unit_price
        increment_version = False
        if data.name is not None and data.name.strip() != service.name:
            service.name = data.name.strip()
            increment_version = True
        if data.pricing_type is not None and data.pricing_type.value != service.pricing_type:
            service.pricing_type = data.pricing_type.value
            increment_version = True
        if data.unit is not None and data.unit.value != service.unit:
            service.unit = data.unit.value
            increment_version = True
        if data.unit_price is not None and data.unit_price != service.unit_price:
            service.unit_price = data.unit_price
            increment_version = True
        if data.requires_ironing is not None and data.requires_ironing != service.requires_ironing:
            service.requires_ironing = data.requires_ironing
            increment_version = True
        if data.estimated_hours is not None:
            service.estimated_hours = data.estimated_hours
        if data.is_active is not None:
            service.is_active = data.is_active

        if increment_version:
            service.version += 1

        AuditService.record(
            db=db,
            action="SERVICE_UPDATED",
            resource_type="service",
            resource_id=service.id,
            before_data={"unit_price": old_price},
            after_data={"unit_price": service.unit_price, "is_active": service.is_active},
        )

        db.commit()
        db.refresh(service)
        return service

