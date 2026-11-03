from fastapi import APIRouter

from app.api.v1.health import router as health_router
from app.modules.auth.router import router as auth_router
from app.modules.businesses.router import (
    business_router,
    settings_router,
)
from app.modules.customers.router import router as customers_router
from app.modules.expenses.router import router as expenses_router
from app.modules.invoices.router import router as invoices_router
from app.modules.orders.router import router as orders_router
from app.modules.payments.router import router as payments_router
from app.modules.pickup_delivery.router import router as pickup_delivery_router
from app.modules.reports.router import router as reports_router
from app.modules.services.router import router as services_router
from app.modules.tracking.router import router as tracking_router
from app.modules.users.router import router as users_router

api_v1_router = APIRouter()

api_v1_router.include_router(health_router)
api_v1_router.include_router(auth_router)
api_v1_router.include_router(users_router)
api_v1_router.include_router(business_router)
api_v1_router.include_router(settings_router)
api_v1_router.include_router(customers_router)
api_v1_router.include_router(services_router)
api_v1_router.include_router(orders_router)
api_v1_router.include_router(payments_router)
api_v1_router.include_router(expenses_router)
api_v1_router.include_router(invoices_router)
api_v1_router.include_router(tracking_router)
api_v1_router.include_router(pickup_delivery_router)
api_v1_router.include_router(reports_router)
