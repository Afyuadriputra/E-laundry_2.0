# M0-01: Requirements Consistency Report & Traceability Matrix

Dokumen ini memvalidasi keterlacakan dan konsistensi antar-dokumen acuan: **PRD**, **TRD**, **AFD**, **DBD**, **BSD**, dan **IPD** untuk **E-Laundry 2.0**.

---

## 1. Traceability Matrix

| Aspek / Entitas | PRD (Bisnis) | TRD (Teknologi) | AFD (Alur) | DBD (UI/UX) | BSD (Database/API) | IPD (Milestone) | Status Konsistensi |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :---: |
| **Role Pengguna** | Owner, Cashier, Staff, Courier | RBAC 4 Roles | Alur per role (Kasir, Kurir, Admin) | Mobile views per role | 4 enum roles pada tabel `users` | M1 (Auth & RBAC) | **KONSISTEN** |
| **Status Pesanan** | 7 tahapan cucian | Finite state machine | RECEIVED $\rightarrow$ WASHING $\rightarrow$ IRONING $\rightarrow$ PACKED $\rightarrow$ READY $\rightarrow$ COMPLETED (+ CANCELLED) | Visual timeline badge & filter | Enum `order_status` & state transition API | M2 (Core Ops) | **KONSISTEN** |
| **Status Pembayaran** | UNPAID, PARTIAL, PAID | Idempotent transaction | Alur DP, Pelunasan kasir/kurir | Badge status bayar | Derived status dari `payments` & `orders.total_amount` | M3 (Finance) | **KONSISTEN** |
| **Nota Digital & WA** | Manual click to WhatsApp | Deep link `wa.me`, PDF receipt | Alur share nota via WA | Modal rincian nota & share button | Template format pesan & PDF generator | M3 (Finance) | **KONSISTEN** |
| **Tracking Tanpa Login** | Akses via token acak | Secure random token (16-32 char), SHA-256 hashed | Alur pelanggan buka link tracking | Mobile tracking view responsif | Tabel `tracking_tokens`, restricted schema | M4 (Public Tracking) | **KONSISTEN** |
| **Pickup & Delivery** | Request publik, kurir task | State machine pickup/delivery | Form request $\rightarrow$ assign kurir $\rightarrow$ convert order | Kurir task card & delivery checklist | Tabel `pickup_requests` & `delivery_tasks` | M5 (Pickup/Delivery) | **KONSISTEN** |
| **Laporan & Dashboard** | Omset, pengeluaran, piutang | Agregasi SQL, CSV export | Filter tanggal, chart ringkas | Visual summary cards & chart | Query agregasi tanpa floating point | M6 (Dashboard) | **KONSISTEN** |

---

## 2. Analisis 14 Entitas Database di BSD

Seluruh 14 tabel pada `doc/BSD.md` telah dipetakan dan tidak memiliki redundansi struktur:

1. `businesses` — Profil laundry tunggal (MVP).
2. `business_settings` — Konfigurasi operasional, timezone, format nota.
3. `users` — Data akun petugas dengan RBAC.
4. `user_sessions` — Server-side sessions dengan token hash dan expiry.
5. `customers` — Data pelanggan dengan nomor telepon unik per bisnis.
6. `services` — Master paket cucian (kiloan, satuan) beserta harga satuan.
7. `orders` — Transaksi utama laundry dengan nomor unik dan state machine.
8. `order_items` — Rincian item dan snapshot harga saat order dibuat.
9. `order_status_history` — Audit trail kronologis perubahan status cucian.
10. `payments` — Log pembayaran manual (tunai, transfer, QRIS manual) dengan penanda void.
11. `expenses` — Catatan pengeluaran operasional outlet.
12. `tracking_tokens` — Token hash akses publik terbatas tanpa login.
13. `pickup_requests` — Permintaan jemput pakaian oleh pelanggan publik.
14. `delivery_tasks` — Penugasan kurir untuk pengantaran pesanan berstatus READY.

---

## 3. Resolusi Keputusan P0 Teridentifikasi

Tidak ditemukan pertentangan (*breaking conflict*) yang menghalangi pengerjaan fondasi (M0). Semua detail angka batas operasional telah dicatat dan disepakati dalam `doc/implementation/DECISION-REGISTER.md`.

**Hasil Audit:** **PASS — KONSISTEN & VALID UNTUK IMPLEMENTASI**.

