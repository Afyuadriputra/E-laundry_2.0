# Multi-stage Dockerfile for E-Laundry 2.0 Backend (FastAPI + Python 3.12)

# --- Stage 1: Build Dependencies ---
FROM python:3.12-slim AS builder

WORKDIR /build

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml ./

# Install python dependencies to wheels
RUN pip install --upgrade pip && \
    pip wheel --no-cache-dir --no-deps --wheel-dir /build/wheels -e .

# --- Stage 2: Production Runtime ---
FROM python:3.12-slim AS runtime

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    APP_ENV=production \
    PORT=8000

# Install runtime libpq for PostgreSQL
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN groupadd -g 1001 elaundry && \
    useradd -u 1001 -g elaundry -s /bin/bash -m elaundry

# Copy wheels and install
COPY --from=builder /build/wheels /wheels
COPY pyproject.toml ./
RUN pip install --no-cache-dir /wheels/* && rm -rf /wheels

# Copy application source and migrations
COPY --chown=elaundry:elaundry alembic.ini ./
COPY --chown=elaundry:elaundry alembic ./alembic
COPY --chown=elaundry:elaundry app ./app

USER elaundry

EXPOSE 8000

# Healthcheck probe using built-in liveness endpoint
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:8000/api/v1/health/live || exit 1

# Production startup command using Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "2", "--proxy-headers", "--forwarded-allow-ips", "*"]

