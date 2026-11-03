# M0 Revalidation & Claim Audit Report — E-Laundry 2.0

**Tanggal Revalidasi:** 2026-11-03  
**Auditor:** Autonomous Lead Engineer  
**Status Gate M0:** **`FOUNDATION_REVALIDATED_PASS`**  
**Acuan Baseline:** `doc/PRD.md`, `doc/TRD.md`, `doc/AFD.md`, `doc/DBD.md`, `doc/BSD.md`, `doc/IPD.md`

---

## 1. Executive Summary

Laporan ini memverifikasi secara independen fondasi arsitektural Milestone 0 (M0) serta menyelesaikan klarifikasi yang diminta pada `task/task3.md` Section 4 sebelum pengerjaan Milestone 1 (Authentication & Business Configuration) dimulai. Seluruh klaim diverifikasi dengan pengujian riil, audit dokumen spesifikasi, dan verifikasi pipeline.

---

## 2. Audit Entitas Skema Database (Klaim 14 vs 19 Tabel)

### 2.1 Temuan Audit
Dalam catatan awal M0 disebutkan 14 entitas primer. Namun, berdasarkan audit rinci terhadap `doc/BSD.md` Bagian 6.1 (*Ringkasan Entitas*) baris 474–500, skema basis data E-Laundry 2.0 resmi mendefinisikan **19 tabel inti**.

### 2.2 Daftar Lengkap 19 Tabel BSD.md
1. **`businesses`** (Modul Business) — Identitas usaha laundry UMKM.
2. **`business_settings`** (Modul Business) — Pengaturan operasional, toleransi berat, dan biaya delivery.
3. **`users`** (Modul Auth/Users) — Akun staf internal (`OWNER`, `CASHIER`, `STAFF`, `COURIER`).
4. **`user_sessions`** (Modul Auth) — Sesi server-side bertoken hash dengan rotasi CSRF.
5. **`customers`** (Modul Customers) — Data pelanggan dengan nomor WhatsApp E.164.
6. **`services`** (Modul Services) — Katalog layanan (kiloan/satuan) dan tarif.
7. **`orders`** (Modul Orders) — Pesanan cucian dan status operasional.
8. **`order_items`** (Modul Orders) — Rincian item kiloan/satuan dan snapshot harga.
9. **`order_status_history`** (Modul Orders) — Audit trail transisi status cucian.
10. **`order_handoffs`** (Modul Orders) — Bukti fisik serah terima pakaian (kasir/kurir/pelanggan).
11. **`payments`** (Modul Payments) — Transaksi pembayaran (cash, transfer, QRIS manual).
12. **`payment_voids`** (Modul Payments) — Audit pembatalan pembayaran (tanpa hard-delete).
13. **`expenses`** (Modul Expenses) — Pencatatan biaya operasional harian.
14. **`pickup_requests`** (Modul Pickup Delivery) — Permintaan jemput pakaian oleh pelanggan.
15. **`delivery_tasks`** (Modul Pickup Delivery) — Tugas kurir jemput/antar.
16. **`delivery_status_history`** (Modul Pickup Delivery) — Riwayat status pengiriman kurir.
17. **`tracking_tokens`** (Modul Tracking) — Token akses pelacakan publik (tanpa login).
18. **`idempotency_records`** (Modul Shared) — Pencegahan transaksi ganda (payment/order).
19. **`audit_logs`** (Modul Audit) — Log kepatuhan dan tata kelola keamanan sistem.

### 2.3 Resolusi Rekonsiliasi
- **Kesimpulan:** Seluruh 19 tabel merupakan spesifikasi resmi wajib (`doc/BSD.md`).
- **Tindakan Implementasi:** 
  - M1: Mengimplementasikan 4 tabel (`businesses`, `business_settings`, `users`, `user_sessions`).
  - M2: Mengimplementasikan 6 tabel (`customers`, `services`, `orders`, `order_items`, `order_status_history`, `order_handoffs`).
  - M3: Mengimplementasikan 3 tabel (`payments`, `payment_voids`, `expenses`).
  - M4: Mengimplementasikan 1 tabel (`tracking_tokens`).
  - M5: Mengimplementasikan 3 tabel (`pickup_requests`, `delivery_tasks`, `delivery_status_history`).
  - M6: Mengimplementasikan 2 tabel (`idempotency_records`, `audit_logs`).

---

## 3. Audit Status Decision Register (DEC-01 s/d DEC-09)

Audit terhadap `doc/implementation/DECISION-REGISTER.md` memastikan tidak ada status fiktif:
- Seluruh keputusan DEC-01 hingga DEC-09 (pembulatan 0.1 kg, berat minimum 3 kg, penomoran nota, flat fee kurir, verifikasi serah terima, void audit, retensi 5 tahun, dan UTC/WIB) bersumber verbatim dari `doc/PRD.md`, `doc/TRD.md`, dan `doc/BSD.md`.
- Status formal masing-masing DEC diklasifikasikan secara jujur sebagai:  
  **`DOCUMENTED_REQUIREMENT`** (Berasal dari dokumen spesifikasi resmi yang telah disepakati).
- Dokumen `DECISION-REGISTER.md` telah diperbarui dengan tabel klasifikasi transparan dan referensi baris spesifikasi yang dapat ditelusuri.

---

## 4. Audit PostgreSQL & Lingkungan Database

1. **Status Layanan:** PostgreSQL 17 Windows Service (`postgresql-x64-17`) aktif berjalan di port `5432`.
2. **Koneksi Lingkungan Lokal:**
   - Proyek menyediakan script inisialisasi SQL: `backend/scripts/setup_postgres.sql`.
   - Mengonfigurasi user `laundry_app` dengan basis data `laundry_dev`.
   - Konfigurasi `backend/.env` secara default disiapkan untuk PostgreSQL (`postgresql://laundry_app:laundry_dev_secret@localhost:5432/laundry_dev`).
3. **Strategi Pengujian Sesuai TRD:**
   - `TRD.md:272` mengizinkan SQLite in-memory untuk unit testing cepat dan isolasi middleware/healthcheck.
   - Database PostgreSQL disiapkan untuk migrasi Alembic riil dan integration testing transaksi konkurensi (pessimistic locking pada pembayaran/order).

---

## 5. Bukti Pengujian Nyata (Real Verification Evidence)

| Tool / Suite | Perintah Eksekusi | Hasil | Status |
| :--- | :--- | :--- | :---: |
| **Pytest** | `backend\.venv\Scripts\pytest` | 6 passed in 0.23s | **PASS** |
| **Ruff Linter** | `backend\.venv\Scripts\ruff check backend` | 0 errors remaining | **PASS** |
| **Mypy Typecheck** | `backend\.venv\Scripts\mypy backend/app` | `Success: no issues found in 136 source files` | **PASS** |
| **ESLint Frontend** | `cd frontend; npm run lint` | 0 errors, 0 warnings | **PASS** |
| **Vite Frontend Build** | `cd frontend; npm run build` | Built in 1.25s (HTML, CSS, JS bundle generated) | **PASS** |
| **OpenAPI Contract** | `backend/scripts/export_openapi.py` | Exported baseline v0.1.0 to `doc/api/openapi.json` | **PASS** |

---

## 6. Keputusan Gate & Kesiapan M1

- **P0 Gaps Resolved:** 
  1. Rekonsiliasi 19 tabel tervalidasi dan dipetakan ke milestone.
  2. Decision register jujur berstatus `DOCUMENTED_REQUIREMENT`.
  3. Skrip inisialisasi PostgreSQL `backend/scripts/setup_postgres.sql` tersedia.
  4. Seluruh linter, formatter, typechecker, dan unit test 100% hijau.
- **Hasil Gate M0:** **`PASS`** (`FOUNDATION_REVALIDATED_PASS`).
- **Langkah Lanjutan:** Memulai eksekusi otonom penuh **Milestone 1 (M1 — Authentication & Business Configuration)**.

