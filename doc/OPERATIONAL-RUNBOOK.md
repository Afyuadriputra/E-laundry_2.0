# E-Laundry 2.0 — Operational Handover Runbook & Production Guide
**System Version:** 2.0.0-prod  
**Target Architecture:** Multi-Tenant Mobile-First Laundry Operations  
**Document Classification:** Operations, DevOps & System Administration  
**Last Updated:** 2026-11-03  

---

## 1. System Architecture Overview

E-Laundry 2.0 is an enterprise-grade, mobile-first management system designed for laundry micro, small, and medium enterprises (MSMEs). The platform consists of four primary tiers:

```
[ Clients / Mobile Devices / Desktops ]
                   │
                   ▼ (Port 80 / 443)
       ┌───────────────────────┐
       │   Nginx Reverse Proxy │ (SSL/TLS, Gzip, Security Headers, SPA Fallback)
       └───────────┬───────────┘
                   │
         ┌─────────┴─────────┐
         ▼                   ▼
┌─────────────────┐ ┌─────────────────┐
│  Frontend SPA   │ │ FastAPI Backend │ (Python 3.12, Uvicorn, 4 Workers)
│  (React 19+Vite)│ │ (Port 8000)     │
└─────────────────┘ └────────┬────────┘
                             │
                             ▼ (Port 5432 - Private Bridge)
                    ┌─────────────────┐
                    │  PostgreSQL 17  │ (19 Relational Tables, Alembic Migrations)
                    └─────────────────┘
```

### Component Details
| Component | Technology | Role | Port |
| :--- | :--- | :--- | :--- |
| **Frontend** | React 19, TypeScript, Vite, Tailwind CSS v4 | Mobile-first cashier/owner/courier portal and unauthenticated public customer tracking | 80 (Internal container) |
| **Backend** | Python 3.12, FastAPI, SQLAlchemy 2.0, Pydantic v2 | High-performance async API, business logic, state machines, financial invariants | 8000 (Internal container) |
| **Database** | PostgreSQL 17 (Alpine) | Multi-tenant persistent relational store with strict foreign keys and check constraints | 5432 (Internal bridge) |
| **Gateway** | Nginx 1.27 (Alpine) | SSL termination, request routing, rate limiting, and gzip compression | 80 / 443 (Host exposed) |

---

## 2. Environment Variables & Secret Provisioning

### 2.1 Security Guidelines
- **Zero Secrets in VCS:** Never commit `.env` files, API keys, or private tokens to Git.
- **Entropy Requirement:** Use cryptographically secure 256-bit (32-byte) pseudo-random tokens for all secret keys.
- **Secret Generation Commands:**
  ```bash
  # Generate production SECRET_KEY
  openssl rand -hex 32

  # Generate production SESSION_SECRET_KEY
  openssl rand -hex 32
  ```

### 2.2 Environment Configuration File (`.env`)
Create a production `.env` file in the project root:
```ini
# --- Application Environment ---
APP_ENV=production
DEBUG=false
LOG_LEVEL=INFO

# --- Database Credentials (PostgreSQL 17) ---
POSTGRES_DB=elaundry_prod
POSTGRES_USER=elaundry_admin
POSTGRES_PASSWORD=YOUR_HIGH_ENTROPY_POSTGRES_PASSWORD_HERE
DATABASE_URL=postgresql+psycopg://elaundry_admin:YOUR_HIGH_ENTROPY_POSTGRES_PASSWORD_HERE@db:5432/elaundry_prod

# --- Security & Cryptography ---
SECRET_KEY=YOUR_GENERATED_32_BYTE_HEX_SECRET_KEY
SESSION_SECRET_KEY=YOUR_GENERATED_32_BYTE_HEX_SESSION_SECRET_KEY
ALLOWED_ORIGINS=https://laundry.yourdomain.com,https://api.yourdomain.com

# --- Session & Cookie Policies ---
SESSION_LIFETIME_SECONDS=604800
CSRF_COOKIE_NAME=csrf_token
SESSION_COOKIE_NAME=session_id
```

---

## 3. Database Initialization & Migration Runbook

The database schema is managed deterministically via Alembic migrations spanning 5 sequential revisions (`M1` through `M5`).

### 3.1 Fresh Database Setup
1. Verify PostgreSQL server is running and accessible:
   ```bash
   pg_isready -h localhost -p 5432 -U elaundry_admin -d elaundry_prod
   ```
2. Run database migrations to apply the complete schema:
   ```bash
   # From the backend directory
   cd backend
   alembic upgrade head
   ```
3. Verify current revision:
   ```bash
   alembic current
   # Expected head: e528b96f140a (M5: Pickup & Delivery Logistics)
   ```

### 3.2 Verification of Critical Tables
The schema includes 19 tables partitioned across domains:
- **Core Tenant & RBAC:** `businesses`, `business_settings`, `users`, `user_sessions`
- **Core Laundry:** `customers`, `services`, `orders`, `order_items`, `order_status_history`, `order_handoffs`
- **Finance & Invoices:** `payments`, `payment_voids`, `expenses`, `invoices`
- **Tracking & Logistics:** `tracking_tokens`, `pickup_requests`, `delivery_tasks`, `delivery_status_history`, `idempotency_keys`

---

## 4. Production Deployment Procedures

### 4.1 Automated Docker Compose Deployment (Recommended)
This method launches the entire isolated stack with health checks and automated migration execution.

1. Ensure Docker Engine and Docker Compose are installed (`docker --version`).
2. Populate production `.env` file as documented in Section 2.
3. Build and launch services:
   ```bash
   docker compose -f docker-compose.prod.yml up -d --build
   ```
4. Verify container health status:
   ```bash
   docker compose -f docker-compose.prod.yml ps
   ```
   All services (`elaundry-db-prod`, `elaundry-backend-prod`, `elaundry-frontend-prod`, `elaundry-gateway-prod`) must report `healthy` or `running`.

5. Check container logs:
   ```bash
   docker compose -f docker-compose.prod.yml logs -f backend
   ```

### 4.2 Bare-Metal / VPS Systemd Deployment (Alternative)
For environments running directly on a Linux VPS (Ubuntu/Debian) without Docker:

#### 1. Systemd Service: Backend (`/etc/systemd/system/elaundry-backend.service`)
```ini
[Unit]
Description=E-Laundry 2.0 FastAPI Application
After=network.target postgresql.service

[Service]
Type=simple
User=elaundry
WorkingDirectory=/var/www/elaundry/backend
EnvironmentFile=/var/www/elaundry/.env
ExecStart=/var/www/elaundry/backend/.venv/bin/uvicorn app.main:app --host 127.0.0.1 --port 8000 --workers 4 --proxy-headers
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
```

#### 2. Systemd Activation
```bash
sudo systemctl daemon-reload
sudo systemctl enable --now elaundry-backend
sudo systemctl status elaundry-backend
```

---

## 5. Automated Backup & Disaster Recovery (DR)

### 5.1 Automated Daily Backups
E-Laundry 2.0 provides production-ready backup automation scripts supporting automatic compression and rolling 14-day retention.

- **Linux / macOS (Cron):**
  Add daily midnight cron job (`crontab -e`):
  ```bash
  0 2 * * * /var/www/elaundry/scripts/backup_postgres.sh >> /var/log/elaundry_backup.log 2>&1
  ```

- **Windows (Task Scheduler):**
  Schedule execution of `scripts\backup_postgres.ps1` daily.

### 5.2 Manual Backup Execution
```bash
# Linux / macOS
./scripts/backup_postgres.sh

# Windows PowerShell
.\scripts\backup_postgres.ps1
```

### 5.3 Disaster Recovery / Point-In-Time Restore
> [!CAUTION]
> Restoring a database replaces existing tables and data with the contents of the archive. Always verify backup file integrity prior to execution.

```bash
# Linux / macOS
./scripts/restore_postgres.sh ./backups/elaundry_backup_20261103_120000.sql.gz

# Windows PowerShell
.\scripts\restore_postgres.ps1 -BackupFile .\backups\elaundry_backup_20261103_120000.sql.gz
```

---

## 6. Health Checks, Monitoring & Metrics

The platform exposes standardized probe endpoints compliant with container orchestrators and uptime monitoring tools:

| Endpoint | Method | Expected Code | Purpose | Response Payload |
| :--- | :---: | :---: | :--- | :--- |
| `/api/v1/health/live` | GET | `200 OK` | Liveness probe (process is running) | `{"status": "live", "timestamp": "..."}` |
| `/api/v1/health/ready` | GET | `200 OK` | Readiness probe (database connectivity alive) | `{"status": "ready", "database": "connected"}` |

If the database is temporarily unreachable, `/api/v1/health/ready` returns `503 Service Unavailable`, preventing reverse proxies or load balancers from routing traffic to a degraded instance.

---

## 7. Zero-Downtime Rollout & Rollback Procedures

### 7.1 Rolling Application Upgrade
1. Pull new release git tag:
   ```bash
   git fetch --tags
   git checkout tags/v2.x.x
   ```
2. Build new container images:
   ```bash
   docker compose -f docker-compose.prod.yml build
   ```
3. Run non-destructive database migrations:
   ```bash
   docker compose -f docker-compose.prod.yml run --rm backend alembic upgrade head
   ```
4. Restart services with zero-downtime rolling reload:
   ```bash
   docker compose -f docker-compose.prod.yml up -d --no-deps backend frontend
   ```

### 7.2 Emergency Rollback Procedure
If critical runtime errors or regressions are identified post-release:
1. Revert container image to previous release:
   ```bash
   docker compose -f docker-compose.prod.yml rollback  # Or checkout previous stable tag
   ```
2. If database migration needs rollback:
   ```bash
   docker compose -f docker-compose.prod.yml run --rm backend alembic downgrade -1
   ```
3. Restart containers:
   ```bash
   docker compose -f docker-compose.prod.yml up -d
   ```

---

## 8. Incident Response & Troubleshooting Playbook

### Incident 1: User Account Locked Out due to Failed Attempts
- **Symptom:** Cashier or owner sees `"Akun terkunci sementara karena terlalu banyak percobaan gagal. Silakan coba lagi setelah 15 menit."`
- **Cause:** 5 consecutive incorrect passwords triggered in-memory sliding window rate limiter.
- **Resolution:**
  - Standard procedure: Wait 15 minutes for the lockout window to expire.
  - Emergency procedure: Restart backend process/container to reset in-memory sliding tracker, or use an owner account to reset password via `/api/v1/users/{user_id}`.

### Incident 2: HTTP 403 Forbidden with "Token CSRF tidak valid"
- **Symptom:** Cashier encounters 403 on order creation, status change, or payment recording.
- **Cause:** Client session was renewed or cookie expired while form state retained old CSRF token.
- **Resolution:**
  - Refresh the browser tab to re-fetch `/api/v1/auth/csrf`.
  - Re-authenticate to issue synchronized session and CSRF credentials.

### Incident 3: Customer Public Tracking Token 404 Not Found
- **Symptom:** Customer clicks tracking link and sees "Tautan Tidak Ditemukan".
- **Cause:** Malformed token URL, token older than 90 days (auto-expired), or order has been purged.
- **Verification:**
  - Query DB: `SELECT * FROM tracking_tokens WHERE raw_token_hash_or_lookup = '<token>';`
  - Check `expires_at` column. If expired, generate a new token via cashier order view.

---

## 9. Outlet Onboarding & Initial Setup Guide

For newly registered laundry outlets:
1. **Outlet Registration:** Run SQL seed or call `/api/v1/businesses` to initialize the business profile (`name`, `phone_e164`, `address`, `timezone="Asia/Jakarta"`).
2. **Setup Default Catalog:**
   - Add standard Kiloan service (e.g. *Cuci Komplit Reguler*, Rp 7.000 / KG, 48 hours).
   - Add Satuan services (e.g. *Bed Cover Besar*, Rp 25.000 / PCS, 72 hours).
3. **Staff Account Creation:**
   - Owner logs in.
   - Navigates to **Pengaturan Staf** (`/users`).
   - Creates Cashier account for desk operations.
   - Creates Courier account for pickup & delivery dispatch.
4. **Logistics Configuration:**
   - Enable pickup/delivery flags in `business_settings`.
   - Distribute the public pickup request form URL: `https://laundry.yourdomain.com/#pickup`.

