# Master Implementation Tracker — E-Laundry 2.0

Dokumen ini memantau seluruh status pekerjaan bertahap (*milestone-based*) E-Laundry 2.0 berdasarkan `doc/IPD.md` dan `task/task3.md`.

---

## 1. Status Milestone Overview

| Milestone | Nama Milestone | Status | Gate Status | Tanggal Mulai | Tanggal Selesai |
| :--- | :--- | :---: | :---: | :---: | :---: |
| **M0** | **Project Foundation** | **PASS** | **FOUNDATION_REVALIDATED_PASS** | 2026-11-03 | 2026-11-03 |
| **M1** | **Authentication & Business Configuration** | **PASS** | **AUTH_RBAC_READY (PASS)** | 2026-11-03 | 2026-11-03 |
| **M2** | **Core Laundry Operations** | **PASS** | **CORE_LAUNDRY_READY (PASS)** | 2026-11-03 | 2026-11-03 |
| **M3** | **Finance & Digital Invoices** | **PASS** | **FINANCE_INVOICE_READY (PASS)** | 2026-11-03 | 2026-11-03 |
| **M4** | **Public Tracking** | **PASS** | **PUBLIC_TRACKING_READY (PASS)** | 2026-11-03 | 2026-11-03 |
| **M5** | **Pickup & Delivery** | **PASS** | **PICKUP_DELIVERY_READY (PASS)** | 2026-11-03 | 2026-11-03 |
| **M6** | **Dashboard & Reporting** | **PASS** | **REPORTING_READY (PASS)** | 2026-11-03 | 2026-11-03 |
| **M7** | **Security, Testing & Hardening** | **PASS** | **RELEASE_CANDIDATE_READY (PASS)** | 2026-11-03 | 2026-11-03 |
| **M8** | **Production Deployment** | **PASS** | **PRODUCTION_READY (PASS)** | 2026-11-03 | 2026-11-03 |

---

## 2. Milestone 0: Project Foundation — Task Breakdown

| Task ID | Workstream | Deskripsi Task | Dependensi | Deliverable | Status |
| :---: | :--- | :--- | :---: | :--- | :---: |
| **M0-01** | PM/DOC | Audit konsistensi PRD, TRD, AFD, DBD, BSD | - | `M0-01-CONSISTENCY-REPORT.md` | **PASS** |
| **M0-02** | PM | Finalisasi keputusan P0 yang memengaruhi coding | M0-01 | `DECISION-REGISTER.md` (DOCUMENTED_REQUIREMENT) | **PASS** |
| **M0-03** | BE/FE | Inisialisasi struktur monorepo & script root | M0-02 | Monorepo structure alignment | **PASS** |
| **M0-04** | BE | Setup FastAPI application skeleton & CORS | M0-03 | `backend/app/main.py` | **PASS** |
| **M0-05** | FE | Setup React + TypeScript + Vite & design tokens | M0-03 | Clean frontend shell & tokens | **PASS** |
| **M0-06** | DB | Setup PostgreSQL, SQLAlchemy 2.x & Alembic | M0-04 | DB session & `setup_postgres.sql` | **PASS** |
| **M0-07** | BE/OPS | Konfigurasi environment & pydantic-settings | M0-04 | `config.py` & `.env.example` | **PASS** |
| **M0-08** | BE | Structured logging, Request ID & Error Schema | M0-04, M0-07 | Core middlewares & error handlers | **PASS** |
| **M0-09** | BE | Health endpoints (`/health/live`, `/health/ready`) | M0-06, M0-08 | Health check APIs | **PASS** |
| **M0-10** | QA/OPS | CI baseline, test fixtures & smoke tests | M0-09 | Pytest/Vitest baseline & CI workflow | **PASS** |
| **M0-11** | DOC/BE | Baseline OpenAPI v1.0 & kontrak API | M0-09 | `doc/api/openapi.json` | **PASS** |
| **M0-12** | SEC | Security threat review awal (STRIDE) | M0-08, M0-09 | `M0-12-THREAT-MODEL.md` & Gate | **PASS** |
| **M0-REV**| QA/AUDIT | Revalidasi M0: Rekonsiliasi 19 tabel BSD & status register | M0-12 | `doc/implementation/M0-REVALIDATION.md` | **PASS** |

---

## 3. Milestone 1: Authentication & Business Configuration — Task Breakdown

| Task ID | Workstream | Deskripsi Task | Dependensi | Deliverable | Status |
| :---: | :--- | :--- | :---: | :--- | :---: |
| **M1-01** | DB | Migration `businesses` dan `business_settings` | M0 | `alembic/versions/ec501d8d2522_m1_auth_and_business.py` | **PASS** |
| **M1-02** | DB | Migration `users` dan `user_sessions` | M1-01 | Registered models in `models_registry.py` | **PASS** |
| **M1-03** | BE | Password hashing Argon2id (RFC 9106) | M0 | `backend/app/core/security.py` | **PASS** |
| **M1-04** | BE/SEC | Sesi server-side token hash, sliding & absolute expiry | M1-02, M1-03 | `backend/app/modules/auth/service.py` | **PASS** |
| **M1-05** | BE/SEC | Proteksi CSRF & login throttling (5x failed max) | M1-04 | `verify_csrf` & in-memory sliding tracker | **PASS** |
| **M1-06** | BE | RBAC dependencies (`require_owner`, `require_roles`) | M1-02 | `backend/app/core/permissions.py` | **PASS** |
| **M1-07** | BE | API endpoints `/auth`, `/users`, `/business`, `/settings` | M1-04, M1-06 | `auth/router.py`, `users/router.py`, `businesses/router.py` | **PASS** |
| **M1-08** | FE/UX | Login page & mobile-first responsive AppShell | M1-07 | `LoginPage.tsx`, `AppShell.tsx` (Deep Teal `#0F766E`) | **PASS** |
| **M1-09** | FE/INT | Integrasi session, cookie HttpOnly, CSRF header | M1-08 | `api-client.ts`, `AuthProvider`, `useAuth` | **PASS** |
| **M1-10** | QA/SEC | Automated tests (Argon2, CSRF, RBAC, session expiry) | M1-07 | `tests/security/` (15 passing tests) | **PASS** |
| **M1-11** | BE/FE | Owner-managed staff accounts (tambah, list, nonaktifkan) | M1-07, M1-09 | `UsersPage.tsx` & `/users` endpoints | **PASS** |
| **M1-12** | QA | E2E auth flow & Acceptance Gate sign-off | M1-01–M1-11 | `doc/implementation/M1-REPORT.md` | **PASS** |

---

## 4. Milestone 2: Core Laundry Operations — Task Breakdown

| Task ID | Workstream | Deskripsi Task | Dependensi | Deliverable | Status |
| :---: | :--- | :--- | :---: | :--- | :---: |
| **M2-01** | DB | Migration `customers` dan `services` | M1 | `alembic/versions/7a89e41b2c10_m2_core_laundry_operations.py` | **PASS** |
| **M2-02** | DB | Migration `orders` dan `order_items` (`pickup_request_id` nullable UUID) | M2-01 | Schema tables with BIGINT $\ge 0$ constraints | **PASS** |
| **M2-03** | DB | Migration `order_status_history` dan `order_handoffs` (`delivery_task_id` nullable UUID) | M2-02 | Schema tables with 1:1 cascade and indexes | **PASS** |
| **M2-04** | BE | Customer CRUD & E.164 phone normalizer | M2-01 | `customers/` service, router, normalizer | **PASS** |
| **M2-05** | BE | Service catalog & price snapshotting | M2-01 | `services/` service, router, versioning | **PASS** |
| **M2-06** | BE | Pricing Engine Python `Decimal` (DEC-01 & DEC-02) | M2-05 | `orders/domain/pricing.py` (0.1 kg HALF_UP, 3.0 kg floor) | **PASS** |
| **M2-07** | BE | Atomic order creation & daily code `ORD-YYYYMMDD-XXXX` | M2-02, M2-06 | `OrderService:create_order` sequential numbering | **PASS** |
| **M2-08** | BE | Order APIs (List, Detail, Update, Cancel) | M2-07 | `orders/router.py` | **PASS** |
| **M2-09** | BE | 9-State Laundry Machine & completion invariant | M2-08 | `orders/domain/state_machine.py` (422 rejection test) | **PASS** |
| **M2-10** | FE/UX | Customer management UI & Services catalog UI | M2-04, M2-05 | `customers-page.tsx`, `services-page.tsx` | **PASS** |
| **M2-11** | FE/UX | Order intake form UI dengan kalkulasi desimal instan | M2-06, M2-07 | `create-order-page.tsx` with live rounding/floor | **PASS** |
| **M2-12** | FE/INT | Order detail view & status transition control | M2-08, M2-09 | `order-detail-page.tsx`, `orders-page.tsx` | **PASS** |
| **M2-13** | BE/QA | Optimistic locking via `orders.version` (409 Conflict) | M2-08 | Version check in transition_status | **PASS** |
| **M2-14** | QA | Regression test suite & M2 Acceptance Report | M2-01–M2-13 | 29 passing tests & `doc/implementation/M2-REPORT.md` | **PASS** |

---

## 5. Milestone 3: Finance & Digital Invoices — Task Breakdown

| Task ID | Workstream | Deskripsi Task | Dependensi | Deliverable | Status |
| :---: | :--- | :--- | :---: | :--- | :---: |
| **M3-01** | DB | Migration `payments`, `payment_voids`, `expenses`, `idempotency_records` | M2 | `alembic/versions/d912a784c4e1_m3_finance_and_digital_invoices.py` | **PASS** |
| **M3-02** | BE | Domain calculation logic & invariants (`balance.py`, `invariants.py`) | M2 | `app/modules/payments/domain/` | **PASS** |
| **M3-03** | BE | Multi-payment intake API (`POST /orders/{id}/payments`, `GET`) | M3-01, M3-02 | `payments/router.py`, `service.py`, `models.py` | **PASS** |
| **M3-04** | BE | Payment void API with mandatory reason & recalculation | M3-03 | `payments/router.py`, `service.py` | **PASS** |
| **M3-05** | BE | Pessimistic row locking & Idempotency service | M3-01, M3-03 | `app/modules/idempotency/`, `payments/service.py` | **PASS** |
| **M3-06** | BE | Operational expenses management API (`/expenses`) | M3-01 | `app/modules/expenses/` | **PASS** |
| **M3-07** | BE | Digital invoice payload generator | M3-03 | `app/modules/invoices/service.py`, `router.py` | **PASS** |
| **M3-08** | BE | POS thermal 58mm text generator & HTML print view | M3-07 | `app/modules/invoices/pdf_renderer.py` | **PASS** |
| **M3-09** | BE | WhatsApp deep link and nota slip formatter | M3-07 | `app/modules/invoices/whatsapp_message.py` | **PASS** |
| **M3-10** | FE/UX | Frontend expenses management UI (`ExpensesPage`) | M3-06 | `frontend/src/pages/expenses/expenses-page.tsx`, `services/expenses.ts` | **PASS** |
| **M3-11** | FE/INT | Frontend payment ledger & invoice modals | M3-03, M3-07 | `frontend/src/pages/payments/`, `invoices/invoice-modal.tsx`, `order-detail-page.tsx` | **PASS** |
| **M3-12** | QA | Test verification, linting, typechecking & M3 Report | M3-01–M3-11 | 36 Pytest tests, Playwright E2E, `doc/implementation/M3-REPORT.md` | **PASS** |

---

## 6. Milestone 4: Customer Public Tracking & Notifications — Task Breakdown

| Task ID | Workstream | Deskripsi Task | Dependensi | Deliverable | Status |
| :---: | :--- | :--- | :---: | :--- | :---: |
| **M4-01** | DB | Migration `tracking_tokens` (FK order_id; nullable pickup_request_id deferred to M5) | M3 | `c018a74e512b_m4_customer_public_tracking.py` | **PASS** |
| **M4-02** | BE | Cryptographically secure token generator & SHA-256 hash storage | M4-01 | `tracking/service.py` | **PASS** |
| **M4-03** | BE | Public tracking API (`GET /api/v1/tracking/{token}`) with strict allowlist & PII masking | M4-02 | `tracking/router.py`, `schemas.py` | **PASS** |
| **M4-04** | BE | Public order cancellation endpoint with operational state constraints | M4-03 | `tracking/router.py`, `service.py` | **PASS** |
| **M4-05** | BE | Automatic token generation hook on order intake | M4-02 | Hook in `orders/service.py` & invoices | **PASS** |
| **M4-06** | FE/UX | Mobile-first public tracking page (`/track/:token`) | M4-03 | `frontend/src/pages/tracking/public-tracking-page.tsx` | **PASS** |
| **M4-07** | FE/UX | Order timeline stepper, payment status card, WhatsApp customer action | M4-06 | Timeline & Status Stepper components | **PASS** |
| **M4-08** | FE/INT | Customer cancellation modal with confirmation | M4-04, M4-06 | Cancellation UI component | **PASS** |
| **M4-09** | QA | Unit & API tests for tracking, token revocation, PII masking | M4-01–M4-05 | `tests/api/test_tracking_api.py` (38 passed) | **PASS** |
| **M4-10** | QA | E2E Playwright test & M4 Acceptance Report | M4-01–M4-09 | `frontend/e2e/m4-tracking.spec.ts` & `doc/implementation/M4-REPORT.md` | **PASS** |

---

## 7. Milestone 5: Pickup & Delivery Logistics — Task Breakdown

| Task ID | Workstream | Deskripsi Task | Dependensi | Deliverable | Status |
| :---: | :--- | :--- | :---: | :--- | :---: |
| **M5-01** | DB | Migration `pickup_requests`, `delivery_tasks`, `delivery_status_history` & FK resolution (`orders.pickup_request_id`, `tracking_tokens.pickup_request_id`, `order_handoffs.delivery_task_id`) | M4 | `alembic/versions/e528b96f140a_m5_pickup_and_delivery_logistics.py` | **PASS** |
| **M5-02** | BE | Pickup request lifecycle & domain states (`REQUESTED` -> `ASSIGNED` -> `PICKED_UP` -> `CONVERTED`) | M5-01 | `pickup_delivery/service.py`, `models.py` | **PASS** |
| **M5-03** | BE | Cashier pickup confirmation, scheduling & courier dispatch | M5-01, M5-02 | `pickup_delivery/service.py`, `schemas.py` | **PASS** |
| **M5-04** | BE | Delivery task dispatching & courier lifecycle (`ASSIGNED` -> `EN_ROUTE` -> `ARRIVED` -> `COMPLETED`/`FAILED`) | M5-01 | `pickup_delivery/service.py` | **PASS** |
| **M5-05** | BE | Courier role-based APIs (courier task listing, proof photo path, status transitions) | M5-02, M5-04 | `pickup_delivery/router.py`, `schemas.py` | **PASS** |
| **M5-06** | BE | Atomic Pickup-to-Order conversion service (DEC-10: exactly 1 order per request, anti-duplicate) | M5-02, M2 | `pickup_delivery/service.py` | **PASS** |
| **M5-07** | FE/UX | Mobile courier task dashboard & status progression UI | M5-05 | `frontend/src/pages/delivery/delivery-page.tsx` | **PASS** |
| **M5-08** | FE/UX | Cashier pickup request intake & conversion modal | M5-03, M5-06 | `frontend/src/pages/delivery/delivery-page.tsx` | **PASS** |
| **M5-09** | QA | Backend test suite for pickup lifecycle, atomic conversion & delivery tasks | M5-01–M5-06 | `tests/api/test_pickup_delivery_api.py` (39 passed) | **PASS** |
| **M5-10** | QA | Playwright E2E browser test & Milestone 5 Report | M5-01–M5-09 | `frontend/e2e/m5-delivery.spec.ts` & `doc/implementation/M5-REPORT.md` | **PASS** |

---

## 8. Milestone 6: Dashboard & Reporting — Task Breakdown

| Task ID | Workstream | Deskripsi Task | Dependensi | Deliverable | Status |
| :---: | :--- | :--- | :---: | :--- | :---: |
| **M6-01** | BE | Dashboard aggregation service & summary metrics | M3, M5 | `backend/app/modules/reports/service.py`, `schemas.py` | **PASS** |
| **M6-02** | BE | Overdue orders tracking & operational aging logic | M2, M6-01 | `backend/app/modules/reports/service.py` | **PASS** |
| **M6-03** | BE | Orders detailed reporting with status, customer & date range filters | M2, M6-01 | `backend/app/modules/reports/router.py` | **PASS** |
| **M6-04** | BE | Payments and outstanding balance reconciliation report | M3, M6-01 | `backend/app/modules/reports/router.py` | **PASS** |
| **M6-05** | BE | Expenses summary and category-based financial report | M3, M6-01 | `backend/app/modules/reports/router.py` | **PASS** |
| **M6-06** | BE | Sanitized CSV export endpoints (orders, payments, expenses) with formula injection protection | M6-03–M6-05 | `backend/app/modules/reports/csv_export.py` | **PASS** |
| **M6-07** | FE/UX | Owner dashboard view (KPIs, Cash Received vs Order Value, Simple Cash Difference) | M6-01, M6-02 | `frontend/src/App.tsx` (`DashboardView`) | **PASS** |
| **M6-08** | FE/UX | Cashier operational dashboard (active orders, overdue alerts, ready for pickup) | M6-01, M6-02 | `frontend/src/App.tsx` (`DashboardView`) | **PASS** |
| **M6-09** | FE/INT | Interactive reporting screens with date filters & CSV download | M6-03–M6-06 | `frontend/src/pages/reports/reports-page.tsx`, `AppShell.tsx` | **PASS** |
| **M6-10** | QA | Reconciliation unit/API tests, Playwright E2E & M6 Report | M6-01–M6-09 | 40 Pytest + 8 Playwright passing, `doc/implementation/M6-REPORT.md` | **PASS** |

---

## 9. Milestone 7: Security, Testing & Hardening — Task Breakdown

| Task ID | Workstream | Deskripsi Task | Dependensi | Deliverable | Status |
| :---: | :--- | :--- | :---: | :--- | :---: |
| **M7-01** | SEC | Security vulnerability audit (OWASP Top 10, CWE-1236, CSRF, Session, SQLi, IDOR) | M0–M6 | `test_security_hardening.py` (Tenant isolation, CSRF) | **PASS** |
| **M7-02** | BE/SEC | Rate limiting, brute-force protection & privacy headers (`Cache-Control: no-store`) | M1, M7-01 | SecurityHeadersMiddleware & login throttling | **PASS** |
| **M7-03** | QA/INT | Multi-role end-to-end integration test suite (Owner, Cashier, Courier, Customer) | M1–M6 | 43 Pytest + 15 Playwright E2E passing | **PASS** |
| **M7-04** | QA/PERF | Database indexing, foreign key integrity & performance validation | M0–M6 | Alembic migrations, PostgreSQL schema integrity | **PASS** |
| **M7-05** | FE/UX | Cross-device responsive layout audit & WCAG AA contrast verification | M1–M6 | `m7-responsive-a11y.spec.ts` (320px–1440px) | **PASS** |
| **M7-06** | QA/DOC | Release Candidate audit, automated CI verification & M7 Report | M7-01–M7-05 | `doc/implementation/M7-REPORT.md` | **PASS** |

---

## 10. Milestone 8: Production Deployment & Operations — Task Breakdown

| Task ID | Workstream | Deskripsi Task | Dependensi | Deliverable | Status |
| :---: | :--- | :--- | :---: | :--- | :---: |
| **M8-01** | DEVOPS | Production Dockerfile and multi-stage container build | M0–M7 | `backend/Dockerfile`, `frontend/Dockerfile` | **PASS** |
| **M8-02** | DEVOPS | Production Docker Compose orchestration (PostgreSQL 17, Uvicorn, Nginx) | M8-01 | `docker-compose.yml`, `docker-compose.prod.yml` | **PASS** |
| **M8-03** | DEVOPS | Nginx reverse proxy configuration, SSL/TLS, gzip & security headers | M8-02 | `nginx/nginx.conf`, `frontend/nginx.conf` | **PASS** |
| **M8-04** | OPS/DB | PostgreSQL automated backup & point-in-time recovery scripts | M8-02 | `scripts/backup_postgres.sh`, `.ps1`, `restore_postgres.sh`, `.ps1` | **PASS** |
| **M8-05** | OPS | Zero-downtime deployment & rollback procedure documentation | M8-02 | `doc/OPERATIONAL-RUNBOOK.md` §7 | **PASS** |
| **M8-06** | SEC/OPS | Secret provisioning & production environment checklist | M8-02 | `doc/OPERATIONAL-RUNBOOK.md` §2 | **PASS** |
| **M8-07** | DOC/OPS | Operational handover runbook & disaster recovery guide | M8-04–M8-06 | `doc/OPERATIONAL-RUNBOOK.md` | **PASS** |
| **M8-08** | QA/OPS | Full end-to-end verification of production build & smoke test | M8-01–M8-03 | Clean build across frontend and backend | **PASS** |
| **M8-09** | DOC | Final API documentation (OpenAPI v1.0 complete spec) export | M8-08 | `doc/api/openapi.json` (48 paths) | **PASS** |
| **M8-10** | ARCH | Final autonomous implementation sign-off & M8 Report | M8-01–M8-09 | `doc/implementation/M8-REPORT.md` | **PASS** |

---

## 11. Task 4: Full Documentation Compliance Audit & Gap Remediation

**Audit Execution Date:** 2026-11-03  
**Status:** **AUDIT_AND_REMEDIATION_COMPLETE (100% EVIDENCE-VERIFIED)**  

### A. Closed Gap Log
1. **GAP-01 (P0):** Added Table 19 `audit_logs` model, `AuditService.record()` with credential redaction, Alembic migration `a619c28e401b`, and integrated state transition audit hooks. Verified by `test_audit_logs.py`.
2. **GAP-02 (P0):** Enforced strict read-only boundary on public tracking links (PRD §5.7 #9). Removed public self-cancellation mutation endpoint and UI button; replaced with cashier WhatsApp assistance button. Verified by `test_tracking_api.py` and `m4-tracking.spec.ts`.
3. **GAP-03 (P1):** Corrected attribute reference `payment.method` in payment void audit hook in `payments/service.py`. Verified by `test_payments_api.py`.
4. **GAP-04 (P2):** Cleaned unused imports and organized Alembic migration imports. Verified with `ruff check backend` (0 errors).

### B. Automated Verification Metrics
- **Pytest Backend Suite:** 45 tests passed, 0 failed (12.08s runtime).
- **Playwright E2E Suite:** 15 tests passed, 0 failed (22.7s runtime).
- **Static Code Analysis:** Ruff 0 errors, ESLint 0 errors, TypeScript Vite build succeeded (1.51s).

### C. Master Compliance Artifacts
1. [`FULL-COMPLIANCE-MATRIX.md`](file:///d:/Kuliah/joki/Kerja%20Praktek%20Aqil/kawan%20aqil/projek/doc/implementation/FULL-COMPLIANCE-MATRIX.md)
2. [`GAP-REMEDIATION-REGISTER.md`](file:///d:/Kuliah/joki/Kerja%20Praktek%20Aqil/kawan%20aqil/projek/doc/implementation/GAP-REMEDIATION-REGISTER.md)
3. [`REAL-INTEGRATION-TEST-REPORT.md`](file:///d:/Kuliah/joki/Kerja%20Praktek%20Aqil/kawan%20aqil/projek/doc/implementation/REAL-INTEGRATION-TEST-REPORT.md)
4. [`UIUX-COMPLIANCE-REPORT.md`](file:///d:/Kuliah/joki/Kerja%20Praktek%20Aqil/kawan%20aqil/projek/doc/implementation/UIUX-COMPLIANCE-REPORT.md)
5. [`DEPLOYMENT-VERIFICATION-REPORT.md`](file:///d:/Kuliah/joki/Kerja%20Praktek%20Aqil/kawan%20aqil/projek/doc/implementation/DEPLOYMENT-VERIFICATION-REPORT.md)
6. [`FINAL-COMPLIANCE-AUDIT.md`](file:///d:/Kuliah/joki/Kerja%20Praktek%20Aqil/kawan%20aqil/projek/doc/implementation/FINAL-COMPLIANCE-AUDIT.md)




