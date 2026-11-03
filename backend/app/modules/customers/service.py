import re
import uuid

from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session

from app.core.exceptions import NotFoundException
from app.modules.customers.models import Customer
from app.modules.customers.schemas import CustomerCreate, CustomerUpdate
from app.modules.orders.models import Order


class CustomerService:
    @staticmethod
    def list_customers(
        db: Session,
        business_id: uuid.UUID,
        search: str | None = None,
        is_active: bool | None = None,
        limit: int = 50,
        offset: int = 0,
    ) -> tuple[list[Customer], int]:
        query = select(Customer).where(Customer.business_id == business_id)

        if is_active is not None:
            query = query.where(Customer.is_active == is_active)

        if search:
            search_trimmed = search.strip()
            name_pattern = f"%{search_trimmed}%"
            phone_conditions = [Customer.phone_e164.ilike(name_pattern)]

            cleaned_digits = re.sub(r"\D", "", search_trimmed)
            if cleaned_digits:
                if cleaned_digits.startswith("0"):
                    phone_conditions.append(Customer.phone_e164.ilike(f"%+62{cleaned_digits[1:]}%"))
                    phone_conditions.append(Customer.phone_e164.ilike(f"%{cleaned_digits[1:]}%"))
                elif cleaned_digits.startswith("62"):
                    phone_conditions.append(Customer.phone_e164.ilike(f"%+{cleaned_digits}%"))
                else:
                    phone_conditions.append(Customer.phone_e164.ilike(f"%{cleaned_digits}%"))

            query = query.where(
                or_(
                    Customer.full_name.ilike(name_pattern),
                    *phone_conditions,
                )
            )

        total_query = select(func.count()).select_from(query.subquery())
        total = db.scalar(total_query) or 0

        customers = db.scalars(
            query.order_by(Customer.full_name.asc()).offset(offset).limit(limit)
        ).all()
        return list(customers), total

    @staticmethod
    def get_by_id(db: Session, business_id: uuid.UUID, customer_id: uuid.UUID) -> Customer:
        customer = db.scalar(
            select(Customer).where(
                Customer.id == customer_id,
                Customer.business_id == business_id,
            )
        )
        if not customer:
            raise NotFoundException(f"Pelanggan dengan ID '{customer_id}' tidak ditemukan.")
        return customer

    @staticmethod
    def find_by_phone(db: Session, business_id: uuid.UUID, phone_e164: str) -> Customer | None:
        return db.scalar(
            select(Customer).where(
                Customer.business_id == business_id,
                Customer.phone_e164 == phone_e164,
            )
        )

    @staticmethod
    def create_customer(db: Session, business_id: uuid.UUID, data: CustomerCreate) -> Customer:
        customer = Customer(
            business_id=business_id,
            full_name=data.full_name.strip(),
            phone_e164=data.phone_e164,
            address=data.address.strip() if data.address else None,
            notes=data.notes.strip() if data.notes else None,
            is_active=True,
        )
        db.add(customer)
        db.commit()
        db.refresh(customer)
        return customer

    @staticmethod
    def update_customer(
        db: Session,
        business_id: uuid.UUID,
        customer_id: uuid.UUID,
        data: CustomerUpdate,
    ) -> Customer:
        customer = CustomerService.get_by_id(db, business_id, customer_id)

        if data.full_name is not None:
            customer.full_name = data.full_name.strip()
        if data.phone_e164 is not None:
            customer.phone_e164 = data.phone_e164
        if data.address is not None:
            customer.address = data.address.strip() if data.address else None
        if data.notes is not None:
            customer.notes = data.notes.strip() if data.notes else None
        if data.is_active is not None:
            customer.is_active = data.is_active

        db.commit()
        db.refresh(customer)
        return customer

    @staticmethod
    def get_order_count(db: Session, customer_id: uuid.UUID) -> int:
        return db.scalar(select(func.count(Order.id)).where(Order.customer_id == customer_id)) or 0
