# Requirements Traceability Matrix (M0–M8) — E-Laundry 2.0

Dokumen ini memetakan seluruh kebutuhan sistem dari dokumen spesifikasi resmi (`PRD.md`, `TRD.md`, `AFD.md`, `DBD.md`, `BSD.md`, `IPD.md`) ke implementasi nyata, pengujian, dan bukti akseptansi pada setiap task ID.

---

## 1. Milestone 0: Project Foundation (M0)

| Requirement ID | Source Section | IPD Task ID | Implementation Deliverable | Required Test | Acceptance Evidence |
| :--- | :--- | :---: | :--- | :--- | :--- |
| **REQ-M0-01** | `TRD.md §1.2`, `IPD.md §9.2` | **M0-01** | Laporan audit konsistensi: `M0-01-CONSISTENCY-REPORT.md` | Manual cross-doc check | Konsistensi antardokumen tervalidasi |
| **REQ-M0-02** | `PRD.md §4`, `BSD.md §5` | **M0-02** | Decision Register: `DECISION-REGISTER.md` | Audit klasifikasi status | 9 Keputusan berstatus DOCUMENTED_REQUIREMENT |
| **REQ-M0-03** | `TRD.md §2.1`, `IPD.md §9.2` | **M0-03** | Struktur monorepo `backend/` & `frontend/` | Directory inspection | Struktur folder bersih tanpa artifak rusak |
| **REQ-M0-04** | `TRD.md §2.2`, `BSD.md §4` | **M0-04** | FastAPI Skeleton: `backend/app/main.py` | FastAPI startup check | Server booting & OpenAPI endpoint 200 |
| **REQ-M0-05** | `DBD.md §6-8`, `IPD.md §9.2` | **M0-05** | Vite + React + Tailwind 4: `frontend/src/` | Build & Lint | `npm run build` sukses dalam 1.07s |
| **REQ-M0-06** | `TRD.md §2.3`, `BSD.md §5` | **M0-06** | PostgreSQL + SQLAlchemy 2.x + Alembic | Engine connection test | `setup_postgres.sql` & Alembic initialized |
| **REQ-M0-07** | `TRD.md §2.2`, `IPD.md §9.2` | **M0-07** | Config parser: `backend/app/core/config.py` | Settings validator test | Resilient boolean validation pass |
| **REQ-M0-08** | `TRD.md §4`, `BSD.md §35` | **M0-08** | Logging, RequestID & Security Headers Middleware | ASGI middleware test | X-Request-ID propagation & nosniff verified |
| **REQ-M0-09** | `TRD.md §4.2`, `IPD.md §9.2` | **M0-09** | Health APIs: `/health/live` & `/health/ready` | API Test: `test_health.py` | 6 tests passed (200 OK liveness & readiness) |
| **REQ-M0-10** | `TRD.md §7`, `IPD.md §9.2` | **M0-10** | CI Workflow: `.github/workflows/ci.yml` | Workflow syntax validation | Pipeline backend & frontend siap |
| **REQ-M0-11** | `TRD.md §4.1`, `BSD.md §29` | **M0-11** | OpenAPI Baseline: `doc/api/openapi.json` | JSON Schema export test | Export OpenAPI schema berhasil |
| **REQ-M0-12** | `TRD.md §6`, `IPD.md §9.2` | **M0-12** | Threat Model STRIDE: `M0-12-THREAT-MODEL.md` | Security threat review | Gate `FOUNDATION_REVALIDATED_PASS` |

---

## 2. Milestone 1: Authentication & Business Configuration (M1)

| Requirement ID | Source Section | IPD Task ID | Implementation Deliverable | Required Test | Acceptance Evidence |
| :--- | :--- | :---: | :--- | :--- | :--- |
| **REQ-M1-01** | `BSD.md §7-8`, `IPD.md §10.2` | **M1-01** | Migration `businesses` & `business_settings` | Alembic autogenerate | `ec501d8d2522_m1_auth_and_business.py` |
| **REQ-M1-02** | `BSD.md §9-10`, `IPD.md §10.2` | **M1-02** | Migration `users` & `user_sessions` | Model registration check | Registered in `models_registry.py` |
| **REQ-M1-03** | `TRD.md §6.1`, `BSD.md §9.5` | **M1-03** | Argon2id hasher: `backend/app/core/security.py` | Security test: `test_argon2.py` | RFC 9106 params verified, salt uniqueness pass |
| **REQ-M1-04** | `BSD.md §10`, `IPD.md §10.2` | **M1-04** | Session service: `backend/app/modules/auth/service.py` | Session test: `test_session_and_csrf.py`| Sliding & absolute expiry pass, token hash valid |
| **REQ-M1-05** | `TRD.md §6.2`, `BSD.md §10.3` | **M1-05** | CSRF header check & Login rate-limiting | Throttling test: `test_login_throttling.py` | 429 blocked on 6th failed attempt |
| **REQ-M1-06** | `BSD.md §30`, `IPD.md §10.2` | **M1-06** | RBAC dependencies: `backend/app/core/permissions.py` | RBAC test: `test_rbac_and_users.py` | Role hierarchy enforced, 403 on unauthorized |
| **REQ-M1-07** | `BSD.md §29.3`, `IPD.md §10.2` | **M1-07** | Endpoints `/auth`, `/users`, `/business`, `/settings` | API test: `test_auth_api.py` | Endpoints return `StandardResponse[T]` |
| **REQ-M1-08** | `DBD.md §11`, `IPD.md §10.2` | **M1-08** | Login UI & AppShell: `LoginPage.tsx`, `AppShell.tsx` | Component & responsive test | Mobile-first 44px tap targets, role navigation |
| **REQ-M1-09** | `TRD.md §3.2`, `IPD.md §10.2` | **M1-09** | Frontend Auth context: `auth-provider.tsx`, `use-auth.ts` | Frontend build & lint | Cookie HttpOnly integration & state management pass |
| **REQ-M1-10** | `TRD.md §7.1`, `IPD.md §10.2` | **M1-10** | Automated security & auth test suite | Pytest execution | 15/15 tests passing cleanly |
| **REQ-M1-11** | `BSD.md §9.5`, `IPD.md §10.2` | **M1-11** | Staff Account Management UI: `UsersPage.tsx` | Role-gating test | Owner can create staff; last owner non-deactivable |
| **REQ-M1-12** | `IPD.md §10.6` | **M1-12** | E2E Auth verification report: `doc/implementation/M1-REPORT.md` | Full regression run | Gate `AUTH_RBAC_READY (PASS)` |

---

## 3. Milestone 2: Core Laundry Operations (M2)

| Requirement ID | Source Section | IPD Task ID | Implementation Deliverable | Required Test | Acceptance Evidence |
| :--- | :--- | :---: | :--- | :--- | :--- |
| **REQ-M2-01** | `BSD.md §11-12`, `IPD.md §11.2` | **M2-01** | Migration `customers` & `services` | Alembic migration check | Tabel dan indeks unik terverifikasi |
| **REQ-M2-02** | `BSD.md §13-14`, `IPD.md §11.2` | **M2-02** | Migration `orders` & `order_items` (`pickup_request_id` nullable UUID, FK ditangguhkan ke M5) | Database constraint test | FK restrict pada customer, subtotal BIGINT $\ge 0$ |
| **REQ-M2-03** | `BSD.md §15-16`, `IPD.md §11.2` | **M2-03** | Migration `order_status_history` & `order_handoffs` (`delivery_task_id` nullable UUID, FK ditangguhkan ke M5) | Foreign key integrity check | Relasi cascade dan unique constraint 1:1 handoff |
| **REQ-M2-04** | `BSD.md §11.3`, `IPD.md §11.2` | **M2-04** | Customer Service & E.164 phone normalizer | Unit test normalizer | Nomor WhatsApp dinormalisasi & cek duplikasi |
| **REQ-M2-05** | `BSD.md §12`, `IPD.md §11.2` | **M2-05** | Service catalog & price snapshot logic | Service price snapshot test | Snapshot harga item tidak terpengaruh update katalog |
| **REQ-M2-06** | `BSD.md §5.5`, `DEC-01`, `DEC-02`| **M2-06** | Pricing Engine Python `Decimal`: `pricing.py` | Pricing unit test suite | Pembulatan 0.1 kg HALF_UP & batas minimal 3.0 kg |
| **REQ-M2-07** | `BSD.md §13.6`, `DEC-03` | **M2-07** | Order creation transaction & daily code generator | Atomic transaction test | `ORD-YYYYMMDD-XXXX` berurutan & rollback on error |
| **REQ-M2-08** | `BSD.md §29.4`, `IPD.md §11.2` | **M2-08** | Order APIs: List, Detail, Update, Cancel | API test suite | Filter status, pagination, authorization pass |
| **REQ-M2-09** | `BSD.md §27.1-27.3`, `AFD.md §4` | **M2-09** | Laundry State Machine (9 status resmi BSD); validasi negatif COMPLETED | State transition unit test | Transisi ilegal ditolak; transisi ke COMPLETED tanpa lunas/handoff menghasilkan 422 |
| **REQ-M2-10** | `DBD.md §13`, `IPD.md §11.2` | **M2-10** | UI Pelanggan & Layanan: `customers-page.tsx`, `services-page.tsx` | Component & form test | Input validasi, mobile layout responsif |
| **REQ-M2-11** | `DBD.md §12.2`, `IPD.md §11.2` | **M2-11** | Form Buat Pesanan: `create-order-page.tsx` | Form validation & math test | Kalkulasi berat desimal instan, tanpa float error |
| **REQ-M2-12** | `DBD.md §12.3`, `IPD.md §11.2` | **M2-12** | Order Detail & Status Transition UI | UI interaction test | Action button transisi status sesuai permission |
| **REQ-M2-13** | `BSD.md §31.4`, `IPD.md §11.2` | **M2-13** | Optimistic locking via `orders.version` | Concurrency collision test | Mutasi konkuren versi lama ditolak dengan 409 Conflict |
| **REQ-M2-14** | `IPD.md §11.7` | **M2-14** | Regression test suite & M2 Report (termasuk verifikasi negatif COMPLETED) | Automated test run | Gate `CORE_LAUNDRY_READY (PASS)` |

---

## 4. Milestone 3: Finance & Digital Invoices (M3)

| Requirement ID | Source Section | IPD Task ID | Implementation Deliverable | Required Test | Acceptance Evidence |
| :--- | :--- | :---: | :--- | :--- | :--- |
| **REQ-M3-01** | `BSD.md §17-19`, `IPD.md §12.2` | **M3-01** | Migration `payments`, `payment_voids`, `expenses` | Alembic migration check | Skema tabel keuangan, amount BIGINT > 0 |
| **REQ-M3-02** | `BSD.md §18.4`, `IPD.md §12.2` | **M3-02** | Payment domain & balance derivation service (`UNPAID`, `PARTIALLY_PAID`, `PAID`) | Balance derivation test | `remaining_amount` & status turunan kanonikal akurat |
| **REQ-M3-03** | `BSD.md §17.3-17.5` | **M3-03** | Manual Payment API (Cash, Transfer, QRIS Manual) | Payment API test | Verifikasi pembayaran manual, tolak amount $\le 0$ |
| **REQ-M3-04** | `BSD.md §18`, `DEC-06` | **M3-04** | Payment Void service & audit log | Void logic & audit test | Void 1x saja, saldo dihitung ulang tanpa hard delete |
| **REQ-M3-05** | `BSD.md §31.2-31.3` | **M3-05** | Pessimistic Row Locking (`SELECT ... FOR UPDATE`) | Concurrent payment test | Bebas overpayment saat transaksi simultan |
| **REQ-M3-06** | `BSD.md §19`, `IPD.md §12.2` | **M3-06** | Expense CRUD Module & categorization | Expense API test | Pencatatan beban operasional valid |
| **REQ-M3-07** | `BSD.md §29.7`, `DBD.md §16` | **M3-07** | Invoice Data Mapper & Read Model | Invoice mapper test | Data nota terisi lengkap tanpa informasi rahasia |
| **REQ-M3-08** | `PRD.md §5.3`, `IPD.md §12.2` | **M3-08** | PDF Invoice Generator (Thermal 58mm/80mm / A4) | PDF generation test | File PDF terbentuk valid dengan barcode/link |
| **REQ-M3-09** | `PRD.md §5.3`, `AFD.md §5` | **M3-09** | WhatsApp manual share deep link generator | Deep link formatter test | Link `https://wa.me/...` terisi pesan rapi |
| **REQ-M3-10** | `DBD.md §15.3-15.4` | **M3-10** | Payment modal, ledger & void UI: `payments-page.tsx` | Finance UI test | Input nominal, kembalian tunai instan, daftar void |
| **REQ-M3-11** | `DBD.md §16`, `IPD.md §12.2` | **M3-11** | Nota digital modal & print preview | UI Print test | Pratinjau nota thermal & tombol share WhatsApp |
| **REQ-M3-12** | `IPD.md §12.8` | **M3-12** | Financial integration test suite & M3 Report | Full financial test run | Gate `FINANCE_INVOICE_READY (PASS)` |

---

## 5. Milestone 4: Public Tracking (M4)

| Requirement ID | Source Section | IPD Task ID | Implementation Deliverable | Required Test | Acceptance Evidence |
| :--- | :--- | :---: | :--- | :--- | :--- |
| **REQ-M4-01** | `BSD.md §23`, `IPD.md §13.2` | **M4-01** | Migration `tracking_tokens` (FK `orders.id`, kolom `pickup_request_id` nullable, constraint FK ditangguhkan ke M5) | Check constraint test | Token terhubung ke order; migrasi terisolasi dari tabel M5 |
| **REQ-M4-02** | `BSD.md §23.4`, `TRD.md §6.4` | **M4-02** | 256-bit URL-safe token generator & SHA-256 hasher | Token security test | Token unguessable, raw token tidak masuk DB |
| **REQ-M4-03** | `BSD.md §28.8`, `BSD.md §34.3` | **M4-03** | Public Tracking Read Model (PII Redacted) | PII Sanitization test | Nama & HP disamarkan; no internal notes leakage |
| **REQ-M4-04** | `BSD.md §34.2`, `IPD.md §13.2` | **M4-04** | Public Tracking API (`/public/track/{token}`) | Zero-login access test | Akses publik tanpa sesi berhasil; invalid 404 |
| **REQ-M4-05** | `BSD.md §23.4`, `DEC-07` | **M4-05** | Token expiration (30 days post-completion) & rotation | Expiry & rotation test | Token kedaluwarsa/dicabut menolak akses |
| **REQ-M4-06** | `DBD.md §17`, `IPD.md §13.2` | **M4-06** | Halaman Tracking Publik: `public-tracking-page.tsx` | Mobile-first UI test | Timeline vertikal cucian bersih & responsif |
| **REQ-M4-07** | `DBD.md §17.6`, `IPD.md §13.2` | **M4-07** | Live status polling / manual refresh button | Client refresh test | Data status teranyar dimuat tanpa reload halaman |
| **REQ-M4-08** | `BSD.md §34.4`, `TRD.md §6.4` | **M4-08** | Security Headers (no-store, no-referrer) & Rate-limit | Abuse test: 30 req/min | Header keamanan aktif, IP berlebih diblokir 429 |
| **REQ-M4-09** | `IPD.md §13.6` | **M4-09** | Security & privacy audit suite & M4 Report | Security test suite | Gate `PUBLIC_TRACKING_READY (PASS)` |

---

## 6. Milestone 5: Pickup & Delivery Logistics (M5)

| Requirement ID | Source Section | IPD Task ID | Implementation Deliverable | Required Test | Acceptance Evidence |
| :--- | :--- | :---: | :--- | :--- | :--- |
| **REQ-M5-01** | `BSD.md §20`, `IPD.md §14.2` | **M5-01** | Migration `pickup_requests` & penambahan deferred FK (`orders.pickup_request_id`, `tracking_tokens.pickup_request_id`, check constraint `num_nonnulls = 1`) | Alembic migration check | Tabel pickup terdaftar, FK lintas tabel & constraint dual-scope aktif |
| **REQ-M5-02** | `BSD.md §21-22`, `IPD.md §14.2` | **M5-02** | Migration `delivery_tasks`, `delivery_status_history` & deferred FK (`order_handoffs.delivery_task_id`)| Check constraint test | Mutual exclusivity task_type PICKUP vs DELIVERY & relasi handoff aktif |
| **REQ-M5-03** | `BSD.md §20.4`, `AFD.md §6` | **M5-03** | Public Pickup Request API (`/public/pickup`) | Public submission test | Pengajuan penjemputan tanpa login berhasil |
| **REQ-M5-04** | `AFD.md §6`, `IPD.md §14.2` | **M5-04** | Pickup Confirmation & Rejection Service | Admin confirmation test | Konfirmasi jadwal dan pencatatan alasan tolak |
| **REQ-M5-05** | `BSD.md §21.5`, `AFD.md §6` | **M5-05** | Courier Assignment & Scope Isolation | Courier authorization test | Kurir hanya melihat dan mengedit tugas miliknya |
| **REQ-M5-06** | `BSD.md §20.3`, `AFD.md §6` | **M5-06** | Pickup State Machine (`ASSIGNED` $\rightarrow$ `EN_ROUTE` $\rightarrow$ `PICKED_UP`) | State machine test | Transisi kurir pickup sinkron dengan pickup request |
| **REQ-M5-07** | `BSD.md §32`, `IPD.md §14.2` | **M5-07** | Atomic Pickup-to-Order Conversion Service | Idempotent conversion test | Transaksi atomik; zero duplicate order creation |
| **REQ-M5-08** | `BSD.md §21`, `AFD.md §8` | **M5-08** | Delivery State Machine (`ASSIGNED` $\rightarrow$ `EN_ROUTE` $\rightarrow$ `DELIVERED`)| Delivery workflow test | Status pengantaran terisolasi dari status pesanan |
| **REQ-M5-09** | `BSD.md §33`, `DEC-05` | **M5-09** | Physical Handoff & Order Completion Enforcement (Positive E2E COMPLETED transition) | Handoff invariant test | Transisi COMPLETED sukses bila handoff ada dan pembayaran PAID |
| **REQ-M5-10** | `DBD.md §18`, `IPD.md §14.2` | **M5-10** | Form Pickup Publik UI: `public-pickup-page.tsx` | Mobile form usability test | Input jadwal & alamat mudah diisi pelanggan |
| **REQ-M5-11** | `DBD.md §14`, `IPD.md §14.2` | **M5-11** | Dispatch Board & Courier UI: `courier-tasks-page.tsx` | Courier tap target test | 1-klik navigasi status, direct call WhatsApp kurir |
| **REQ-M5-12** | `AFD.md §6-8`, `BSD.md §23.5`| **M5-12** | Integrated Workflow: Pickup $\rightarrow$ Order $\rightarrow$ Tracking $\rightarrow$ Delivery | End-to-end integration test | Token pickup otomatis menampilkan progres order cucian |
| **REQ-M5-13** | `IPD.md §14.7` | **M5-13** | Logistics E2E & Concurrency Suite & M5 Report | Comprehensive test run | Gate `PICKUP_DELIVERY_READY (PASS)` |

---

## 7. Milestone 6: Dashboard & Reporting (M6)

| Requirement ID | Source Section | IPD Task ID | Implementation Deliverable | Required Test | Acceptance Evidence |
| :--- | :--- | :---: | :--- | :--- | :--- |
| **REQ-M6-01** | `BSD.md §29.10`, `IPD.md §15.2`| **M6-01** | Dashboard Aggregation Service (Owner vs Kasir) | Aggregation unit test | Metrik kasir terbatas; metrik Owner komprehensif |
| **REQ-M6-02** | `PRD.md §5.5`, `IPD.md §15.2` | **M6-02** | Overdue Orders Calculation Service | Overdue timing test | Pesanan melewati `estimated_completion_at` terdeteksi |
| **REQ-M6-03** | `PRD.md §5.5`, `DBD.md §15.6` | **M6-03** | Orders Status & Volume Reporting | Orders report test | Filter tanggal & ringkasan kiloan/satuan akurat |
| **REQ-M6-04** | `BSD.md §31.1`, `DBD.md §15` | **M6-04** | Payments & Accounts Receivable (Piutang) Report | Financial reconciliation test | Omzet kotor vs Uang diterima vs Piutang terpisah jelas |
| **REQ-M6-05** | `BSD.md §19`, `IPD.md §15.2` | **M6-05** | Expenses Report & Net Operating Margin | Expense summary test | Total pengeluaran teragregasi per kategori |
| **REQ-M6-06** | `TRD.md §4.1`, `IPD.md §15.2` | **M6-06** | CSV Streaming Export Service (Orders, Payments, Expenses) | RFC 4180 CSV export test | File CSV ter-generate rapi & aman dari CSV injection |
| **REQ-M6-07** | `DBD.md §11.1`, `IPD.md §15.2`| **M6-07** | Dashboard Owner UI: `owner-dashboard.tsx` | Chart & KPI render test | Recharts visualisasi tren omzet & piutang operasional |
| **REQ-M6-08** | `DBD.md §11.2`, `IPD.md §15.2`| **M6-08** | Dashboard Kasir UI: `cashier-dashboard.tsx` | Operational queue test | Antrean cucian hari ini & pesanan siap serah terima |
| **REQ-M6-09** | `DBD.md §15.6`, `IPD.md §15.2`| **M6-09** | Filter Tanggal & Export UI: `reports-page.tsx` | Date picker filter test | Filter dinamis & tombol download CSV berfungsi |
| **REQ-M6-10** | `IPD.md §15.6` | **M6-10** | Financial reconciliation & performance suite & M6 Report| Data audit test run | Gate `REPORTING_READY (PASS)` |

---

## 8. Milestone 7: Quality, Security & Hardening (M7)

| Requirement ID | Source Section | IPD Task ID | Implementation Deliverable | Required Test | Acceptance Evidence |
| :--- | :--- | :---: | :--- | :--- | :--- |
| **REQ-M7-01** | `TRD.md §7.1`, `IPD.md §16.2` | **M7-01** | Full Unit Test Regression Suite (All modules) | Automated pytest suite | Seluruh unit test lulus 100% |
| **REQ-M7-02** | `TRD.md §5.1`, `BSD.md §31.3` | **M7-02** | PostgreSQL Transaction & Concurrency Test Suite | PostgreSQL lock test | Pessimistic locking terbukti mencegah overpayment simultan |
| **REQ-M7-03** | `TRD.md §7.3`, `IPD.md §16.2` | **M7-03** | End-to-End Critical Journey Tests | E2E journey test run | Alur lengkap order $\rightarrow$ bayar $\rightarrow$ tracking $\rightarrow$ handoff lulus |
| **REQ-M7-04** | `TRD.md §6.1`, `IPD.md §16.2` | **M7-04** | Authentication & Session Security Audit | Security penetration test | Anti-brute force, sliding session, hash integrity pass |
| **REQ-M7-05** | `BSD.md §30`, `TRD.md §6.3` | **M7-05** | RBAC & IDOR Vulnerability Audit | Privilege escalation test | Zero IDOR: akses resource lintas bisnis/role diblokir |
| **REQ-M7-06** | `BSD.md §34`, `IPD.md §16.2` | **M7-06** | Public Tracking Security & Enumeration Audit | Token abuse & leakage test | Zero PII leaks, rate limiting aktif, no-store headers |
| **REQ-M7-07** | `BSD.md §31.1`, `IPD.md §16.2`| **M7-07** | Financial Invariant Integrity Stress Test | Math assertion stress test | Zero negative balances, void consistency verified |
| **REQ-M7-08** | `DBD.md §8`, `IPD.md §16.2` | **M7-08** | Responsive Viewport Audit (320px–1440px) | Playwright viewport test | 0 horizontal overflow, minimum 44px tap targets |
| **REQ-M7-09** | `DBD.md §23`, `IPD.md §16.2` | **M7-09** | Accessibility Audit (WCAG 2.2 AA) | Axe / Lighthouse audit | Contrast ratio $\ge 4.5:1$, keyboard navigability pass |
| **REQ-M7-10** | `TRD.md §3.1`, `IPD.md §16.2` | **M7-10** | API Performance & Latency Benchmark (p95) | Load test benchmark | p95 latency $\le 200\text{ms}$ pada workload standar |
| **REQ-M7-11** | `TRD.md §5.3`, `IPD.md §16.2` | **M7-11** | Backup & Disaster Recovery Drill Test | Script test: `backup_db` & `restore_db`| Dump PostgreSQL berhasil direstore tanpa kehilangan data |
| **REQ-M7-12** | `PRD.md §7`, `IPD.md §16.2` | **M7-12** | User Acceptance Testing (UAT) Scenario Document | UAT scenario verification | Skenario operasional UMKM terdokumentasi rapi |
| **REQ-M7-13** | `IPD.md §16.2` | **M7-13** | Critical Bug Fixes & Code Polishing | Code quality audit | Zero high/critical bugs remaining |
| **REQ-M7-14** | `IPD.md §16.7` | **M7-14** | Final Traceability Verification & M7 Report | Matrix audit | Gate `RELEASE_CANDIDATE_READY (PASS)` |

---

## 9. Milestone 8: Production Deployment Readiness (M8)

| Requirement ID | Source Section | IPD Task ID | Implementation Deliverable | Required Test | Acceptance Evidence |
| :--- | :--- | :---: | :--- | :--- | :--- |
| **REQ-M8-01** | `TRD.md §8`, `IPD.md §17.2` | **M8-01** | Production Multi-stage Dockerfiles (`backend`, `frontend`)| Docker build test | Container image ter-build optimal & non-root user |
| **REQ-M8-02** | `TRD.md §6.4`, `IPD.md §17.2` | **M8-02** | Reverse Proxy Config (Nginx / Caddy SSL HTTPS) | Config lint & syntax test | Security headers (HSTS, CSP, X-Frame-Options) pass |
| **REQ-M8-03** | `TRD.md §5.1`, `IPD.md §17.2` | **M8-03** | PostgreSQL Production Setup Guide & Tuning | Database config check | Connection pooling, WAL archiving, UTF-8 verified |
| **REQ-M8-04** | `TRD.md §6.5`, `IPD.md §17.2` | **M8-04** | Production Secrets Management Template (`.env.production`)| Secret hygiene check | Zero hardcoded secrets, `.gitignore` dipatuhi |
| **REQ-M8-05** | `BSD.md §38`, `IPD.md §17.2` | **M8-05** | Production Migration Runbook (`MIGRATION-RUNBOOK.md`) | Migration dry-run | Upgrade & downgrade prosedur terdokumentasi aman |
| **REQ-M8-06** | `TRD.md §5.3`, `IPD.md §17.2` | **M8-06** | Automated Backup Cron Setup Script | Automated backup run | Cron script siap merotasi arsip backup berkala |
| **REQ-M8-07** | `TRD.md §4.2`, `IPD.md §17.2` | **M8-07** | Production Observability & Health Probes Config | Container healthcheck | Probes `/health/live` & `/health/ready` terpasang |
| **REQ-M8-08** | `TRD.md §8`, `IPD.md §17.2` | **M8-08** | Docker Compose Production Stack (`docker-compose.yml`) | Stack validation | Orchestration stack siap jalan |
| **REQ-M8-09** | `TRD.md §7.4`, `IPD.md §17.2` | **M8-09** | Production Smoke Test Automated Script | Smoke test execution | Verifikasi endpoint utama pasca deployment |
| **REQ-M8-10** | `IPD.md §17.6` | **M8-10** | Go-Live Approval & Deployment Guide Document | Procedural sign-off | Prosedur persetujuan rilis resmi tercatat |
| **REQ-M8-11** | `TRD.md §8.3`, `IPD.md §17.2` | **M8-11** | Rollback & Emergency Recovery Runbook | Rollback drill test | Langkah rollback versi & pemulihan DB jelas |
| **REQ-M8-12** | `IPD.md §17.6` | **M8-12** | Final Project Report: `FINAL-PROJECT-REPORT.md` | Final audit checklist | Status `DEPLOYMENT_PREPARED (READY)` |

---

## 10. Task Accounting & Reconciliation Summary

Berdasarkan ekstraksi tuntas terhadap seluruh task ID di `doc/IPD.md`, total task resmi terhitung tepat **108 task**, dengan cakupan keterlacakan (*traceability coverage*) sebesar **100%**:

| Milestone ID | Nama Milestone | Rentang Task ID Asli | Jumlah Task | Status Keterlacakan |
| :---: | :--- | :---: | :---: | :---: |
| **M0** | Project Foundation | `M0-01` s/d `M0-12` | 12 | 100% (Verified & PASS) |
| **M1** | Authentication & Business Configuration | `M1-01` s/d `M1-12` | 12 | 100% (Verified & PASS) |
| **M2** | Core Laundry Operations | `M2-01` s/d `M2-14` | 14 | 100% (Approved Baseline) |
| **M3** | Finance & Digital Invoices | `M3-01` s/d `M3-12` | 12 | 100% (Approved Baseline) |
| **M4** | Public Tracking | `M4-01` s/d `M4-09` | 9 | 100% (Approved Baseline) |
| **M5** | Pickup & Delivery Logistics | `M5-01` s/d `M5-13` | 13 | 100% (Approved Baseline) |
| **M6** | Dashboard & Reporting | `M6-01` s/d `M6-10` | 10 | 100% (Approved Baseline) |
| **M7** | Quality, Security & Hardening | `M7-01` s/d `M7-14` | 14 | 100% (Approved Baseline) |
| **M8** | Production Deployment Readiness | `M8-01` s/d `M8-12` | 12 | 100% (Approved Baseline) |
| **TOTAL** | **Seluruh Milestone (M0–M8)** | **108 Task ID Unik** | **108** | **100% Traceability Covered** |

---

## 11. Cross-Milestone Relational & Lifecycle Architecture

1. **Database Migration Decoupling**:
   - Kolom `orders.pickup_request_id` dan `order_handoffs.delivery_task_id` dibuat di M2 sebagai nullable UUID tanpa foreign key.
   - Kolom `tracking_tokens.pickup_request_id` dibuat di M4 sebagai nullable UUID tanpa foreign key.
   - Seluruh foreign key (`fk_orders_pickup_request_id`, `fk_order_handoffs_delivery_task_id`, `fk_tracking_tokens_pickup_request_id`) dan constraint mutual exclusivity `ck_tracking_tokens_resource_scope` diaktifkan di M5 setelah tabel `pickup_requests` dan `delivery_tasks` dibuat.
   - Menjamin migrasi PostgreSQL sekuensial berjalan bersih dari database kosong (*fresh migration*).
2. **Order Completion Staging**:
   - M2 menguji state machine cucian hingga `READY` dan memverifikasi kegagalan transisi ilegal ke `COMPLETED` (HTTP 422).
   - M3 menghitung status pembayaran (`UNPAID`, `PARTIALLY_PAID`, `PAID`) secara dinamis.
   - M5 mengintegrasikan bukti fisik handoff dan memverifikasi *happy path* transisi `READY` $\rightarrow$ `COMPLETED`.
3. **Kanonikalitas Status Keuangan**:
   - Seluruh modul mengadopsi enum kanonikal: `UNPAID`, `PARTIALLY_PAID`, `PAID` sesuai `doc/BSD.md §18.4 & §27.4`.

---

## 12. Final Traceability Verdict

- **Total Requirements Covered:** 108 / 108 (100%)
- **Unmapped Task IDs:** 0
- **Architectural Gaps:** 0 (P0 & P1 Resolved)
- **Status Validasi:** **`PLAN_APPROVED_FOR_EXECUTION`**


