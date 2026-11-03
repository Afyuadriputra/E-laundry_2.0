# Decision Register (P0 Baseline & Operational Governance) — E-Laundry 2.0

Dokumen ini memformalkan seluruh keputusan bisnis, arsitektural, dan tata kelola implementasi E-Laundry 2.0 dari M0 sampai M8. Seluruh keputusan telah disinkronkan dan divalidasi terhadap dokumen acuan spesifikasi resmi (`PRD.md`, `TRD.md`, `AFD.md`, `DBD.md`, `BSD.md`, `IPD.md`).

---

## 1. Daftar Keputusan Kunci & Klasifikasi Status

| ID | Topik Keputusan | Keputusan yang Ditetapkan | Status Klasifikasi | Dasar Dokumen Spesifikasi | Dampak Modul |
| :---: | :--- | :--- | :---: | :--- | :---: |
| **DEC-01** | **Pembulatan Berat Cucian** | Pembulatan desimal ditetapkan **kelipatan 0.1 kg** (contoh: 3.25 kg dibulatkan menjadi 3.3 kg jika desimal kedua $\ge 5$). Menggunakan `Decimal` Python, bukan `float`. | `DOCUMENTED_REQUIREMENT` | `BSD.md §5.5` (baris 423–438), `TRD.md §2.2` | M2 (Orders & Pricing) |
| **DEC-02** | **Berat Minimum Kiloan** | Ditetapkan default **3.0 kg** per nota kiloan. Jika berat aktual cucian $< 3.0\text{ kg}$, biaya dihitung berdasarkan tarif minimum 3.0 kg. | `DOCUMENTED_REQUIREMENT` | `PRD.md` (FR-ORD-02), `BSD.md §8.2`, `BSD.md §12.5` | M2 (Orders & Pricing) |
| **DEC-03** | **Format Penomoran Nota** | `ORD-YYYYMMDD-XXXX` (contoh: `ORD-20261103-0001`), dengan nomor sekuensial harian yang di-reset per bisnis. | `DOCUMENTED_REQUIREMENT` | `BSD.md §13.6` (baris 730) | M2 (Orders) |
| **DEC-04** | **Kebijakan Tarif Pickup & Delivery** | **Tarif Tetap (Flat Fee)** per penjemputan/pengantaran untuk fase MVP (misal Rp 5.000 atau gratis berdasarkan promo setting). Tidak ada integrasi maps/jarak km otomatis pada MVP. | `DOCUMENTED_REQUIREMENT` | `PRD.md` (Scope Boundaries), `BSD.md §8.2` | M5 (Pickup/Delivery) |
| **DEC-05** | **Pelunasan Saat Serah Terima** | Pelunasan saat pesanan diambil di kasir atau diantar kurir dicatat secara eksplisit di sistem sebagai pembayaran tunai atau verifikasi transfer/QRIS manual (`total_paid >= total_amount`). | `DOCUMENTED_REQUIREMENT` | `PRD.md` (FR-PAY-03), `BSD.md §33` (Order Completion) | M2, M3, M5 |
| **DEC-06** | **Kebijakan Void Pembayaran** | Pembayaran yang salah input **tidak boleh dihapus (hard delete)**. Status diubah via entitas `payment_voids` dengan catatan wajib (`reason`) dan hanya dapat dilakukan role `Owner`. | `DOCUMENTED_REQUIREMENT` | `BSD.md §18` (SCHEMA — PAYMENT VOIDS), `BSD.md §31.5` | M3 (Finance) |
| **DEC-07** | **Masa Berlaku Tracking Token** | Token tracking publik berlaku selama order aktif, dan kedaluwarsa **30 hari kalender** setelah status order berubah menjadi `COMPLETED` atau `CANCELLED`. | `DOCUMENTED_REQUIREMENT` | `BSD.md §23` (SCHEMA — TRACKING TOKENS) | M4 (Public Tracking) |
| **DEC-08** | **Retensi Data Transaksi** | Data transaksi pesanan, pembayaran, dan log audit dipertahankan minimal **5 tahun** di database sebelum dapat diarsipkan. | `DOCUMENTED_REQUIREMENT` | `PRD.md` (NFR-SEC-04), `TRD.md §5.2` | M3, M6, M7 |
| **DEC-09** | **Zona Waktu Default** | Seluruh stempel waktu (*timestamp*) disimpan dalam format **UTC (ISO 8601)** di database, dan dikonversi ke **`Asia/Jakarta` (WIB, UTC+7)** untuk tampilan nota, dashboard, dan laporan. | `DOCUMENTED_REQUIREMENT` | `BSD.md §5.3` (baris 387–397), `TRD.md §2.2` | M0–M8 |
| **DEC-10** | **Dual-Scope Tracking Token** | Token tracking diterbitkan baik untuk `pickup_requests` maupun `orders`. Saat pickup dikonversi menjadi order, token yang sama otomatis menampilkan progres cucian tanpa pergantian link. | `DOCUMENTED_REQUIREMENT` | `BSD.md §23.3` & `§23.5` (num_nonnulls constraint) | M4, M5 (Tracking & Logistics) |
| **DEC-11** | **Pemisahan Status Operasional vs Logistik** | Status pesanan diatur murni 9 status (`RECEIVED`, `QUEUED`, `WASHING`, `DRYING`, `IRONING`, `QC_PACKING`, `READY`, `COMPLETED`, `CANCELLED`). Pengantaran kurir diatur mandiri oleh `delivery_tasks`. | `DOCUMENTED_REQUIREMENT` | `BSD.md §13.5`, `§21.3`, `§27.1` | M2, M5 (Orders & Logistics) |
| **DEC-12** | **Kewajiban Bukti Fisik Serah Terima** | Status pesanan tidak dapat diubah menjadi `COMPLETED` hanya melalui tombol status. Wajib dibuatkan entitas `order_handoffs` (`CUSTOMER_PICKUP` atau `COURIER_DELIVERY`) dengan validasi lunas. | `DOCUMENTED_REQUIREMENT` | `BSD.md §16` & `§33.3` (Completion Invariants) | M2, M5 (Operations) |
| **DEC-13** | **Otorisasi Deployment Produksi** | Seluruh konfigurasi container, Docker Compose, Nginx, dan runbook migrasi disiapkan hingga status `DEPLOYMENT_PREPARED`. Eksekusi go-live publik memerlukan persetujuan eksplisit pemilik. | `PENDING_APPROVAL` | `IPD.md §17.6`, `PRD.md` Governance | M8 (Deployment) |

---

## 2. Definisi Klasifikasi Status
- **`DOCUMENTED_REQUIREMENT`**: Keputusan yang bersumber langsung dari dokumen spesifikasi resmi (`PRD.md`, `TRD.md`, `AFD.md`, `DBD.md`, `BSD.md`) yang telah disahkan sebelum pengembangan dimulai.
- **`APPROVED_BY_OWNER`**: Keputusan baru atau penyesuaian fungsional di luar spesifikasi yang telah disetujui secara tertulis oleh Pemilik Produk.
- **`PENDING_APPROVAL`**: Usulan teknis atau fase rilis final yang membutuhkan otorisasi eksplisit pemilik produk sebelum dieksekusi secara nyata di lingkungan luar (eksternal/publik).
