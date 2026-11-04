from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import app.db.models_registry  # noqa: F401
from app.api.v1.router import api_v1_router
from app.core.config import settings
from app.core.exception_handlers import register_exception_handlers
from app.core.logging import setup_logging
from app.middleware.request_id import RequestIdMiddleware
from app.middleware.security_headers import SecurityHeadersMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logging()
    yield


app = FastAPI(
    title=settings.APP_NAME,
    version="0.1.0",
    description="API Backend E-Laundry 2.0 untuk Manajemen Laundry UMKM",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# Register Middlewares (Order of execution: Security -> RequestId -> CORS)
app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(RequestIdMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register Exception Handlers
register_exception_handlers(app)

# Include API Routers
app.include_router(api_v1_router, prefix="/api/v1")


@app.get("/", tags=["root"], summary="Root API Info")
def root_info() -> dict[str, str]:
    return {
        "app": settings.APP_NAME,
        "version": "0.1.0",
        "docs": "/docs",
        "health": "/api/v1/health/live",
    }
