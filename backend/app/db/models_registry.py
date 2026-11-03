"""Central registry for all SQLAlchemy models to ensure Alembic and Base metadata see them."""

from app.db.base import Base
from app.modules.audit.models import AuditLog
from app.modules.auth.models import UserSession
from app.modules.businesses.models import Business, BusinessSettings
from app.modules.customers.models import Customer
from app.modules.expenses.models import Expense
from app.modules.idempotency.models import IdempotencyRecord
from app.modules.orders.models import Order, OrderHandoff, OrderItem, OrderStatusHistory
from app.modules.payments.models import Payment, PaymentVoid
from app.modules.pickup_delivery.models import (
    DeliveryStatusHistory,
    DeliveryTask,
    PickupRequest,
)
from app.modules.services.models import Service
from app.modules.tracking.models import TrackingToken
from app.modules.users.models import User

__all__ = [
    "AuditLog",
    "Base",
    "Business",
    "BusinessSettings",
    "Customer",
    "DeliveryStatusHistory",
    "DeliveryTask",
    "Expense",
    "IdempotencyRecord",
    "Order",
    "OrderHandoff",
    "OrderItem",
    "OrderStatusHistory",
    "Payment",
    "PaymentVoid",
    "PickupRequest",
    "Service",
    "TrackingToken",
    "User",
    "UserSession",
]
