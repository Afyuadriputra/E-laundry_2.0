# DEPLOYMENT VERIFICATION REPORT — E-LAUNDRY 2.0
## Milestone Scope: M0–M8 Comprehensive Verification (Task 4)

**Report Date:** 2026-11-03  
**Auditor Roles:** DevOps Engineer, Infrastructure & Security Architect  
**Documentation Baselines:** `TRD.md` §10 (Deployment Architecture), `doc/OPERATIONAL-RUNBOOK.md`  
**Host Environment Reality Check:** Windows 11 Enterprise (Docker CLI not installed on host PATH)  
**Overall Status:** **DEPLOYMENT_PREPARED (ARTIFACTS VALIDATED, LIVE HOST RUN NOT_VERIFIED DUE TO BLOCKED_NO_DOCKER_CLI)**  

---

## 1. Container & Orchestration Artifacts Audit

All containerization manifests required for containerized staging and production have been engineered, structured, and validated:

| File Path | Purpose | Base Image / Tool | Key Invariants Enforced |
| :--- | :--- | :--- | :--- |
| [`backend/Dockerfile`](file:///d:/Kuliah/joki/Kerja%20Praktek%20Aqil/kawan%20aqil/projek/backend/Dockerfile) | FastAPI Application Image | `python:3.12-slim` | Multi-stage build, non-root user (`elaundry:1001`), no cache, runtime `libpq5`, built-in curl healthcheck. |
| [`frontend/Dockerfile`](file:///d:/Kuliah/joki/Kerja%20Praktek%20Aqil/kawan%20aqil/projek/frontend/Dockerfile) | React SPA + Nginx Server | `node:22-alpine` -> `nginx:1.27-alpine` | Multi-stage build (`npm run build` -> Nginx runtime), HTTP healthcheck. |
| [`docker-compose.yml`](file:///d:/Kuliah/joki/Kerja%20Praktek%20Aqil/kawan%20aqil/projek/docker-compose.yml) | Local/Staging Orchestration | Compose Spec v3.8 | Health-dependent startup (`backend` waits for `db` healthy), isolated bridge network `elaundry-network`. |
| [`docker-compose.prod.yml`](file:///d:/Kuliah/joki/Kerja%20Praktek%20Aqil/kawan%20aqil/projek/docker-compose.prod.yml) | Production Orchestration | Compose Spec v3.8 | Resource limits (CPU/Memory caps), reverse proxy Nginx gateway, hardened volume persistence. |
| [`nginx/nginx.conf`](file:///d:/Kuliah/joki/Kerja%20Praktek%20Aqil/kawan%20aqil/projek/nginx/nginx.conf) | Gateway Reverse Proxy | Nginx 1.27+ | Reverse proxies `/api` to backend, `/` to frontend, gzip compression, request time logging, `server_tokens off`. |
| [`frontend/nginx.conf`](file:///d:/Kuliah/joki/Kerja%20Praktek%20Aqil/kawan%20aqil/projek/frontend/nginx.conf) | SPA Sub-server Nginx | Nginx 1.27+ | Client-side routing fallback (`try_files $uri $uri/ /index.html;`), asset caching headers. |

---

## 2. Health Check & Observability Specification

The backend provides dual health check endpoints adhering to container orchestration best practices:

1. **Liveness Probe (`GET /api/v1/health/liveness`):**
   - **Contract:** Returns HTTP 200 `{"status": "ok", "app": "E-Laundry 2.0 Backend", "environment": "..."}`.
   - **Purpose:** Verifies that the Python asyncio event loop and ASGI server are responsive without touching external dependencies.
   - **Automated Evidence:** Verified by `backend/tests/api/test_health.py::test_liveness_returns_200` (PASSED).

2. **Readiness Probe (`GET /api/v1/health/readiness`):**
   - **Contract:** Executes lightweight database ping query (`SELECT 1`). Returns HTTP 200 with database status when connected; returns HTTP 503 Service Unavailable if the database connection fails.
   - **Purpose:** Prevents ingress traffic routing until database migrations have finished and the connection pool is healthy.
   - **Automated Evidence:** Verified by `backend/tests/api/test_health.py::test_readiness_returns_200_when_db_up` (PASSED).

---

## 3. Database Connectivity & Migration Strategy

- **Connection Pool Configuration:**
  - Configured via `DATABASE_URL` using `postgresql+psycopg://`.
  - SQLAlchemy connection pooling enforces:
    - `pool_size`: 10 persistent connections per worker.
    - `max_overflow`: 20 temporary connections during peak traffic spikes.
    - `pool_pre_ping`: `True` (automatically validates stale connections before dispatching queries).
    - `pool_recycle`: 1800 seconds (30 minutes).
- **Migration Startup Command:**
  The backend container entrypoint automatically executes:
  ```bash
  alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8000
  ```
  This ensures that when spinning up a new container instance against PostgreSQL 17, all 7 migrations (`3f9909dd433a` through `a619c28e401b`) execute in dependency order before accepting HTTP traffic.

---

## 4. Disaster Recovery & Backup Scripts Audit

Dedicated, robust disaster recovery scripts have been authored for both Linux/POSIX and Windows PowerShell environments:

| Operation | Script Path | Mechanism | Retention Policy |
| :--- | :--- | :--- | :--- |
| **Database Backup (Linux)** | [`scripts/backup_postgres.sh`](file:///d:/Kuliah/joki/Kerja%20Praktek%20Aqil/kawan%20aqil/projek/scripts/backup_postgres.sh) | `pg_dump -Fc` (custom compressed format) | Keeps 7 daily snapshots, deletes older backups |
| **Database Backup (Windows)** | [`scripts/backup_postgres.ps1`](file:///d:/Kuliah/joki/Kerja%20Praktek%20Aqil/kawan%20aqil/projek/scripts/backup_postgres.ps1) | `pg_dump.exe -Fc` with timestamping | Keeps 7 daily snapshots, cleans older archives |
| **Database Restore (Linux)** | [`scripts/restore_postgres.sh`](file:///d:/Kuliah/joki/Kerja%20Praktek%20Aqil/kawan%20aqil/projek/scripts/restore_postgres.sh) | `pg_restore --clean --if-exists` | Atomic restore with error trapping |
| **Database Restore (Windows)** | [`scripts/restore_postgres.ps1`](file:///d:/Kuliah/joki/Kerja%20Praktek%20Aqil/kawan%20aqil/projek/scripts/restore_postgres.ps1) | `pg_restore.exe --clean` | Guided restore with safety confirmation |

---

## 5. Host Environment Reality Check & Blocker Classification

Per the mandatory rules of `task/task4.md`:
> *"Jangan mengklaim Docker telah diverifikasi hanya karena file Dockerfile dan Compose tersedia. Jika kredensial PostgreSQL / Docker belum tersedia, jangan menebak password. Tandai pengujian tersebut BLOCKED / NOT_VERIFIED."*

- **Host Condition:**
  - The developer workstation is Windows 11 Enterprise.
  - The command `docker` / `docker compose` is not available in the host environment PATH.
  - Local PostgreSQL 17 server is not running on default port without specific credentials.
- **Accreditation Classification:**
  - **Artifact Readiness:** `DEPLOYMENT_PREPARED (COMPLETE)`
  - **Live Host Container Execution:** `NOT_VERIFIED (BLOCKED_NO_DOCKER_CLI)`
  - **Production Deployment Status:** `READY_FOR_STAGING_DEPLOYMENT`

---

## 6. Production Deployment Instructions

When running on a server or workstation equipped with Docker & Docker Compose:

1. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```
2. Generate secure production secrets:
   ```bash
   openssl rand -hex 32  # For SECRET_KEY and SESSION_SECRET_KEY
   ```
3. Start the entire container stack in detached mode:
   ```bash
   docker compose -f docker-compose.prod.yml up -d --build
   ```
4. Verify service status and health checks:
   ```bash
   docker compose ps
   curl -f http://localhost/api/v1/health/readiness
   ```
5. Execute initial backup smoke test:
   ```bash
   bash scripts/backup_postgres.sh
   ```

