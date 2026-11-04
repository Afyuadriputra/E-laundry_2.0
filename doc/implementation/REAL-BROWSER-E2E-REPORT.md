# REAL-BROWSER-E2E-REPORT.md — True Browser-to-Database End-to-End Verification

> **Verification Date:** 2026-11-04  
> **Test Harness:** Playwright (Chromium Desktop 1280x720)  
> **Test File:** `frontend/e2e/real-browser-e2e.spec.ts`  
> **Server Pipeline:** Vite Dev Server (:5173) $\to$ FastAPI Backend (:8000) $\to$ PostgreSQL 17 (:5432)  
> **Mock Policy:** STRICT ZERO MOCK (No `page.route`, No intercepted HTTP responses)  
> **Status:** `REAL_E2E_VERIFIED`

---

## 1. Test Architecture & Pipeline Verification

```
+-------------------------------------------------------------------------+
|                  Playwright Chromium Headless Engine                   |
+-------------------------------------------------------------------------+
                                    |
                    HTTP / WebSocket (:5173)
                                    v
+-------------------------------------------------------------------------+
|                 Vite React 19 Frontend (SPA Client)                     |
|           Tailwind CSS (Mobile-First) - Lucide - ApiClient              |
+-------------------------------------------------------------------------+
                                    |
                  Proxy /api -> HTTP 1.1 (:8000)
                                    v
+-------------------------------------------------------------------------+
|                    FastAPI 0.115+ Backend Application                   |
|   Security Headers -> Request ID -> Session Cookie -> Argon2id -> CSRF  |
+-------------------------------------------------------------------------+
                                    |
                 SQLAlchemy 2.0 via psycopg v3 (TCP:5432)
                                    v
+-------------------------------------------------------------------------+
|                    PostgreSQL 17.0 Engine (laundry_dev)                 |
|       19 BSD Tables - 36 FKs - 12 Checks - Pessimistic Row Locking       |
+-------------------------------------------------------------------------+
```

---

## 2. Execution Summary

Command:
```powershell
npm --prefix frontend run test:e2e -- e2e/real-browser-e2e.spec.ts
```

Output:
```text
Running 4 tests using 1 worker

  ok 1 [chromium] › e2e\real-browser-e2e.spec.ts:20:3 › Flow 1: Cashier Lifecycle - Customer CRUD, Order Creation, Workflow & Payments (4.1s)
  ok 2 [chromium] › e2e\real-browser-e2e.spec.ts:190:3 › Flow 2: Unauthenticated Public Tracking (/track/:token) (701ms)
  ok 3 [chromium] › e2e\real-browser-e2e.spec.ts:212:3 › Flow 3: Courier Role Authentication & Delivery Dashboard (1.1s)
  ok 4 [chromium] › e2e\real-browser-e2e.spec.ts:239:3 › Flow 4: Owner Role Authentication, Financial Dashboard & CSV Export (2.3s)

  4 passed (10.7s)
```

---

## 3. Detailed Trace of Verified Flows

### Flow 1: Cashier Lifecycle — Customer CRUD, Order Creation, State Transitions & Financial Ledger (4.1s)
- **Authentication:** `kasir_budi` logged in with password `Kasir123!`. Backend issued real stateful `session_id` cookie validated against `user_sessions` table in PostgreSQL.
- **Customer CRUD:** Created new customer with raw telephone `0812...`. The backend customer service normalized the number into E.164 `+62812...` and stored it in the `customers` table. Real-time search successfully retrieved the record.
- **Order Creation & Pricing Engine:** Selected created customer and kiloan service `Cuci Komplit Reguler` (8.000 IDR/kg). Input quantity `3.5` kg. `PricingEngine` applied DEC-01 0.1 kg half-up rounding and DEC-02 floor checks, calculating subtotal = 28.000 IDR. Order record written to `orders` table with version = 1.
- **Sequential State Machine Progression:**
  1. `RECEIVED` $\to$ `QUEUED` ("Dalam Antrean", version updated to 2).
  2. `QUEUED` $\to$ `WASHING` ("Sedang Dicuci", version updated to 3).
  3. `WASHING` $\to$ `DRYING` ("Pengeringan", version updated to 4).
  4. `DRYING` $\to$ `IRONING` ("Penyetrikaan", version updated to 5).
  5. `IRONING` $\to$ `QC_PACKING` ("QC & Packing", version updated to 6).
  6. `QC_PACKING` $\to$ `READY` ("Siap Ambil/Antar", version updated to 7).
- **Payment Intake & Invariants:**
  - Initial payment state asserted: `BELUM LUNAS` (Total: 28.000 IDR, Sisa: 28.000 IDR).
  - Cashier clicked `Catat Pembayaran`, selected `Set Lunas Penuh` (28.000 IDR), and submitted.
  - PostgreSQL transaction recorded payment in `payments` table and updated balance.
  - Payment status immediately updated to `LUNAS` with `Sisa Tagihan: Rp 0`.
- **Digital Invoice & POS Thermal 58mm:**
  - Opened `Nota & WhatsApp` modal.
  - Verified Standard Invoice displaying business branding, customer details, and `LUNAS` badge.
  - Toggled `Pratinjau POS Thermal (58mm)` view; asserted monospace thermal receipt text and closing greeting (`Terima kasih!`).
  - Extracted secure unguessable tracking token from invoice model.

### Flow 2: Unauthenticated Public Tracking (`/track/:token`) (701ms)
- **Isolated Browser Context:** Launched completely new browser context with zero cookies, zero local storage, and zero cached authentication headers.
- **Direct Navigation:** Navigated directly to `/track/<tracking_token>`.
- **Public Read Model:** Page loaded without any redirect to login. Verified store name, order number, and status label `Siap Diambil / Diantar`.
- **Privacy Protections:** Customer name and phone were masked per BSD.md privacy requirements.
- **Read-Only Enforcement (GAP-02):** Explicitly asserted that zero administrative/cashier action controls are present (no `Catat Pembayaran`, no `Batalkan Pesanan`, no `Ubah Status`).

### Flow 3: Courier Role Authentication & Delivery Dashboard (1.1s)
- **Isolated Browser Context:** Launched new browser context and authenticated as `kurir_agus` (`Kurir123!`).
- **RBAC Enforcement:** Confirmed role badge `COURIER`. Confirmed that management navigation items (`Pegawai`, `Pengaturan`) were strictly hidden from the courier view.
- **Delivery Dashboard:** Navigated to `Antar-Jemput`. Asserted `Tugas Kurir Antar-Jemput` header and verified active pickup/delivery tasks populated directly from the PostgreSQL `delivery_tasks` table.

### Flow 4: Owner Role Authentication, Financial Dashboard & CSV Export (2.3s)
- **Isolated Browser Context:** Launched new browser context and authenticated as `owner` (`Owner123!`).
- **Owner Dashboard:** Confirmed role badge `OWNER`. Verified Owner-only financial cards: `Kinerja Finansial Hari Ini` and `Uang Masuk Diterima`.
- **Reports & Reconciliation:** Navigated to `Laporan` (`Pusat Laporan & Rekonsiliasi`). Verified `Ringkasan Finansial` tab showing live ledger totals calculated across payments and operational expenses.
- **CSV Export:** Clicked `Unduh CSV Pembayaran`. Verified backend CSV generation, CSV sanitization against formula injection (`=`, `+`, `-`, `@`), and verified frontend receipt confirmation message (`File CSV ... berhasil diunduh`).

---

## 4. Verification Verdict

`REAL_E2E_VERIFIED`: All core business workflows—from authentication and customer onboarding, through pricing calculation, stage progression, payment ledger accounting, POS thermal rendering, unauthenticated public tracking, courier task views, to owner financial reconciliation—have been executed and verified in real Chromium against a live PostgreSQL 17 database with zero network mocking.

