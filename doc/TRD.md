
# TECHNICAL REQUIREMENTS DOCUMENT (TRD)

## WEB APP MANAJEMEN LAUNDRY UMKM

**Versi Dokumen:** 1.0
**Tanggal:** 3 November 2026
**Status:** Draft — Technical Review
**Dokumen Induk:** Product Requirements Document (PRD) v1.0
**Arsitektur:** Modular Monolith — REST API
**Lingkup:** Minimum Viable Product (MVP)
**Target Platform:** Web Desktop, Mobile Browser, dan Progressive Web App (PWA)

---

# 1. PENDAHULUAN

## 1.1 Tujuan Dokumen

Technical Requirements Document (TRD) disusun untuk menerjemahkan kebutuhan bisnis dan fungsional yang telah didefinisikan dalam PRD v1.0 menjadi spesifikasi teknis yang dapat diimplementasikan oleh tim pengembang.

Dokumen ini menjadi acuan dalam:

1. Menentukan arsitektur perangkat lunak.
2. Menentukan teknologi frontend, backend, dan database.
3. Merancang struktur modular aplikasi.
4. Menentukan kontrak komunikasi API.
5. Mengatur autentikasi, otorisasi, dan keamanan.
6. Mendefinisikan aturan validasi data dan transaksi.
7. Menetapkan persyaratan performa dan keandalan.
8. Menentukan kebutuhan deployment dan infrastruktur.
9. Menyusun strategi pengujian.
10. Menetapkan standar implementasi dan penerimaan teknis.

TRD tidak menggantikan PRD, tetapi menjadi dokumen teknis turunan yang harus konsisten dengan kebutuhan produk.

## 1.2 Referensi Dokumen

| ID     | Dokumen             | Fungsi                                            |
| ------ | ------------------- | ------------------------------------------------- |
| DOC-01 | PRD v1.0            | Sumber kebutuhan bisnis dan fungsional.           |
| DOC-02 | TRD v1.0            | Spesifikasi teknis implementasi.                  |
| DOC-03 | AFD                 | Desain arsitektur dan alur sistem terperinci.     |
| DOC-04 | DBD                 | Desain database, relasi, indeks, dan constraint.  |
| DOC-05 | API Contract        | Kontrak OpenAPI dan skema request/response final. |
| DOC-06 | UI/UX Specification | Perincian halaman dan komponen antarmuka.         |
| DOC-07 | Test Plan           | Rencana pengujian dan acceptance matrix.          |

## 1.3 Ringkasan Produk

Web App Manajemen Laundry UMKM merupakan aplikasi untuk mengelola operasional laundry melalui smartphone atau laptop.

Sistem mendukung:

- Penerimaan dan pencatatan pesanan.
- Manajemen pelanggan.
- Proses pencucian dan status pekerjaan.
- Pembayaran manual.
- Nota digital.
- Penjemputan dan pengantaran cucian.
- Tracking pelanggan tanpa login.
- Dashboard dan laporan usaha.
- Manajemen petugas dan konfigurasi usaha.

Aplikasi tidak mewajibkan penggunaan mesin kasir fisik, printer thermal, scanner barcode, payment gateway, WhatsApp API berbayar, maupun GPS tracking.

## 1.4 Prinsip Arsitektur

Pengembangan menggunakan prinsip:

**Modular Monolith**

Seluruh domain bisnis dijalankan melalui satu aplikasi backend yang dipisahkan secara logis berdasarkan modul.

**Separation of Concerns**

Presentasi, pemrosesan request, logika bisnis, dan penyimpanan data dipisahkan.

**SOLID**

Komponen dibangun dengan tanggung jawab yang jelas serta dependensi yang dapat diuji.

**KISS (Keep It Simple, Stupid)**

Menghindari kompleksitas yang belum diperlukan oleh skala usaha.

**DRY dengan Pertimbangan Domain**

Mengurangi duplikasi logika tanpa memaksakan abstraksi yang memperumit kode.

**Security by Design**

Keamanan, otorisasi, validasi, dan audit diterapkan sejak awal.

**API-First**

Komunikasi frontend dan backend mengikuti kontrak API yang terdokumentasi.

---

# 2. ARSITEKTUR SISTEM

## 2.1 Model Arsitektur

Sistem menggunakan arsitektur client-server dengan REST API.

Komponen utama:

1. Frontend Internal.
2. Frontend Publik Pelanggan.
3. Reverse Proxy / HTTPS.
4. Backend FastAPI.
5. Business Logic Layer.
6. Data Access Layer.
7. Database PostgreSQL.
8. Layanan pendukung untuk PDF, logging, dan backup.

### Alur Komunikasi

**Pengguna Internal / Pelanggan**

↓ HTTPS

**Web Frontend React**

↓ REST API

**Backend FastAPI**

↓ Application Services

**Repository / Data Access**

↓ SQL

**PostgreSQL Database**

Frontend internal dan portal publik merupakan dua kelompok route dalam satu aplikasi web, dengan pembatasan akses yang berbeda.

## 2.2 Pemilihan Modular Monolith

Arsitektur microservices tidak digunakan pada MVP.

Alasan:

- Jumlah pengguna dan transaksi relatif kecil.
- Biaya infrastruktur lebih rendah.
- Deployment lebih sederhana.
- Pengujian integrasi lebih mudah.
- Tidak memerlukan message broker.
- Tidak memerlukan service discovery.
- Tidak memerlukan API gateway terpisah.
- Seluruh transaksi bisnis dapat menggunakan satu database.

Modular Monolith tetap memungkinkan pemisahan modul menjadi layanan tersendiri pada masa depan apabila dibutuhkan.

## 2.3 Pola Deployment

Untuk produksi, frontend dan API direkomendasikan disajikan pada satu origin melalui reverse proxy.

Contoh konseptual:

- `/` → Frontend React.
- `/app/*` → Dashboard internal.
- `/track/*` → Portal tracking.
- `/pickup` → Formulir penjemputan.
- `/api/v1/*` → Backend FastAPI.

Pendekatan satu origin mempermudah pengelolaan cookie sesi, CORS, dan keamanan browser.

Domain final belum ditentukan dan tidak menjadi persyaratan pengembangan lokal.

## 2.4 Batasan Lingkup Arsitektur

MVP menggunakan satu usaha laundry dan satu lokasi operasional.

Database dapat menyimpan identitas usaha melalui `business_id`, tetapi tidak mengimplementasikan SaaS multi-tenant.

Sistem tidak memerlukan:

- Kubernetes.
- Redis sebagai dependency wajib.
- Kafka atau RabbitMQ.
- Elasticsearch.
- Microservices.
- Cloud Functions untuk setiap modul.
- Integrasi IoT.

Teknologi tambahan hanya boleh dimasukkan berdasarkan kebutuhan teknis yang terukur.

---

# 3. TECHNOLOGY STACK

## 3.1 Frontend

| Komponen              | Pilihan                                    |
| --------------------- | ------------------------------------------ |
| Framework             | React 19                                   |
| Bahasa                | TypeScript                                 |
| Build Tool            | Vite                                       |
| Styling               | Tailwind CSS 4                             |
| UI Components         | shadcn/ui dan Radix UI                     |
| Routing               | React Router                               |
| Server State          | TanStack Query                             |
| Form Management       | React Hook Form                            |
| Schema Validation     | Zod                                        |
| Icons                 | Lucide React                               |
| Animation             | Motion, hanya bila diperlukan              |
| HTTP Client           | Fetch API dengan wrapper terpusat          |
| PWA                   | Web App Manifest dan konfigurasi instalasi |
| Unit / Component Test | Vitest + React Testing Library             |
| E2E Test              | Playwright                                 |

### Persyaratan

1. TypeScript menggunakan strict mode.
2. Seluruh request API melewati lapisan service/client terpusat.
3. Token sesi autentikasi tidak disimpan dalam localStorage.
4. Komponen UI menggunakan design tokens.
5. Validasi frontend meningkatkan pengalaman pengguna, tetapi bukan sumber kebenaran keamanan.
6. Halaman publik tidak memuat modul dashboard internal yang tidak diperlukan.
7. Route-based code splitting diterapkan untuk mengurangi beban awal.
8. Loading, empty, success, dan error state wajib ditangani.

## 3.2 Backend

| Komponen           | Pilihan                      |
| ------------------ | ---------------------------- |
| Framework          | FastAPI                      |
| Bahasa             | Python 3.12                  |
| Data Validation    | Pydantic v2                  |
| ORM                | SQLAlchemy 2.x               |
| Database Migration | Alembic                      |
| PostgreSQL Driver  | Psycopg 3                    |
| Server             | Uvicorn                      |
| Password Hashing   | Argon2id                     |
| Authentication     | Stateful Server-Side Session |
| Authorization      | RBAC                         |
| API Documentation  | OpenAPI                      |
| Testing            | Pytest + HTTPX               |
| Lint / Formatting  | Ruff                         |
| Type Checking      | Pyright atau Mypy            |
| Logging            | Structured JSON Logging      |

### Keputusan Implementasi

Untuk MVP, backend menggunakan SQLAlchemy synchronous Session dengan driver PostgreSQL yang sesuai.

Pendekatan ini dipilih untuk menyederhanakan transaksi database dan logika bisnis.

Endpoint database yang bersifat synchronous menggunakan route atau dependency yang dijalankan dengan pola threadpool FastAPI yang benar, sehingga tidak memblokir event loop secara tidak sengaja.

Penggunaan async SQLAlchemy dapat dievaluasi kembali jika pengujian menunjukkan kebutuhan nyata.

Seluruh dependensi harus menggunakan versi kompatibel yang dikunci dalam lockfile setelah pengujian.

## 3.3 Database

**Pilihan:** PostgreSQL 17.

Alasan:

- Mendukung transaksi ACID.
- Memiliki constraint relasional.
- Mendukung indexing.
- Mendukung row-level locking.
- Mendukung pengolahan data numerik secara presisi.
- Memiliki ekosistem ORM dan migration yang matang.
- Cocok untuk transaksi pesanan dan keuangan.

SQLite boleh digunakan untuk pengujian utilitas yang tidak bergantung pada database, tetapi pengujian integrasi utama wajib menggunakan PostgreSQL agar perilaku transaksi mendekati produksi.

## 3.4 Manajemen Versi

Ketentuan:

1. Node.js menggunakan versi LTS aktif yang kompatibel.
2. Python ditetapkan pada seri 3.12 untuk baseline awal.
3. PostgreSQL menggunakan major version 17.
4. Dependensi frontend dikunci menggunakan lockfile.
5. Dependensi backend dikunci dengan versi yang telah diuji.
6. Pembaruan mayor harus melalui compatibility test.
7. Versi paket diperiksa kembali pada M0 sebelum instalasi.

---

# 4. STRUKTUR PROJECT

## 4.1 Repository

Direkomendasikan menggunakan monorepo sederhana.

Struktur:

**laundry-umkm/**

- `apps/web/` — Aplikasi frontend.
- `apps/api/` — Aplikasi backend.
- `docs/` — Dokumentasi proyek.
- `infra/` — Docker dan deployment.
- `scripts/` — Skrip pengembangan dan operasi.
- `.github/workflows/` — CI/CD jika menggunakan GitHub Actions.
- `README.md` — Petunjuk proyek.

## 4.2 Struktur Frontend

Struktur konseptual `apps/web/src/`:

- `app/` — Bootstrap aplikasi, routing, provider.
- `features/auth/`
- `features/dashboard/`
- `features/orders/`
- `features/customers/`
- `features/payments/`
- `features/expenses/`
- `features/pickup-delivery/`
- `features/invoices/`
- `features/public-tracking/`
- `features/settings/`
- `components/ui/`
- `components/shared/`
- `lib/api/`
- `lib/utils/`
- `hooks/`
- `styles/`
- `types/`
- `tests/`

Setiap fitur dapat memiliki:

- `components/`
- `pages/`
- `hooks/`
- `services/`
- `schemas/`
- `types/`
- `tests/`

### Aturan

1. Komponen UI tidak mengakses database.
2. Komponen tidak menulis endpoint API secara langsung di banyak tempat.
3. Query dan mutation didefinisikan per fitur.
4. Model respons API dikonversi ke model presentasi jika diperlukan.
5. Utility bersama tidak boleh berisi logika bisnis khusus satu modul.
6. Dependency antarfitur harus dijaga agar tidak membentuk circular dependency.

## 4.3 Struktur Backend

Struktur konseptual `apps/api/app/`:

- `main.py`
- `core/`
- `db/`
- `modules/`
- `shared/`
- `middleware/`
- `tests/`

Modul backend:

- `auth/`
- `users/`
- `businesses/`
- `services/`
- `customers/`
- `orders/`
- `payments/`
- `expenses/`
- `pickup_delivery/`
- `invoices/`
- `tracking/`
- `dashboard/`
- `audit/`

## 4.4 Arsitektur Internal Backend

Setiap modul minimal menggunakan pemisahan berikut.

**Layer 1 — Router / Presentation**

Menangani HTTP request, dependency autentikasi, parsing, dan response.

**Layer 2 — Application Service**

Mengatur use case dan orkestrasi transaksi.

**Layer 3 — Domain / Business Rules**

Mengelola validasi bisnis, perhitungan, dan state transition.

**Layer 4 — Repository / Persistence**

Mengakses database melalui ORM.

Ketentuan:

- Router tidak menyimpan business logic kompleks.
- Repository tidak mengembalikan HTTP response.
- Domain tidak bergantung pada framework frontend.
- Service mengatur transaction boundary.
- Dependency dapat diganti untuk kebutuhan testing.
- Tidak membuat abstraksi generik berlebihan hanya untuk memenuhi jumlah layer.

---

# 5. AUTENTIKASI DAN OTORISASI

## 5.1 Model Autentikasi

Pengguna internal wajib login.

Pelanggan tidak menggunakan autentikasi akun.

Sistem menggunakan **stateful server-side session**.

### Alur Login

1. Pengguna membuka halaman login.
2. Pengguna memasukkan username dan password.
3. Backend memvalidasi kredensial.
4. Backend memeriksa status akun.
5. Backend membuat session identifier acak.
6. Session disimpan secara aman pada server/database.
7. Browser menerima session cookie.
8. Frontend mengambil informasi pengguna melalui endpoint `/auth/me`.
9. Pengguna diarahkan ke dashboard sesuai peran.

## 5.2 Penyimpanan Session

Cookie sesi memiliki karakteristik:

- HttpOnly.
- Secure pada produksi.
- SameSite=Lax.
- Path=/.
- Host-only.
- Identifier acak yang kuat.

Nama cookie produksi direkomendasikan menggunakan prefix `__Host-`.

Session identifier tidak boleh disimpan dalam localStorage.

Token session yang disimpan di database sebaiknya berupa hash.

## 5.3 Session Lifetime

Konfigurasi awal yang diusulkan:

| Parameter                 | Nilai Awal                                        |
| ------------------------- | ------------------------------------------------- |
| Inactivity timeout        | 60 menit                                          |
| Absolute session lifetime | 12 jam                                            |
| Logout                    | Mencabut sesi server                              |
| Akun dinonaktifkan        | Seluruh sesi aktif dicabut                        |
| Pergantian password       | Sesi lama dicabut                                 |
| Concurrent session        | Maksimal 3 sesi per akun sebagai konfigurasi awal |

Nilai tersebut merupakan keputusan teknis awal yang dapat disesuaikan berdasarkan uji penggunaan dan analisis risiko.

## 5.4 Perlindungan CSRF

Karena autentikasi menggunakan cookie, endpoint yang mengubah data wajib memiliki perlindungan CSRF.

Pendekatan:

1. Backend menyediakan token CSRF yang terikat pada konteks sesi.
2. Frontend mengirim token melalui header `X-CSRF-Token`.
3. Backend memvalidasi token pada operasi mutasi.
4. Backend memeriksa Origin untuk request sensitif.
5. CORS tidak dibuka secara permisif.

Autentikasi login juga wajib dilindungi terhadap login CSRF.

## 5.5 Role-Based Access Control

Role internal:

- OWNER
- CASHIER
- STAFF
- COURIER

Permission ditentukan berdasarkan aksi.

Contoh permission:

- `orders:create`
- `orders:read`
- `orders:update`
- `orders:cancel`
- `orders:status:update`
- `payments:create`
- `payments:void`
- `financial_reports:read`
- `services:manage`
- `users:manage`
- `delivery:update`

### Ketentuan

1. Permission diperiksa di backend.
2. Frontend hanya mencerminkan hak akses.
3. Owner memiliki hak administrasi usaha.
4. Kasir tidak otomatis mendapat hak mengelola akun.
5. Staf tidak dapat mengubah harga atau pembayaran.
6. Kurir hanya mengakses tugas yang diberikan kepadanya.
7. Pelanggan tidak boleh mengakses endpoint internal.

---

# 6. SPESIFIKASI DATABASE

## 6.1 Konvensi Umum

Database menggunakan PostgreSQL.

Aturan:

- Primary key menggunakan UUID.
- Foreign key menggunakan tipe konsisten.
- Tanggal dan waktu menggunakan `TIMESTAMPTZ`.
- Penyimpanan waktu menggunakan UTC.
- Tampilan waktu mengikuti konfigurasi zona waktu usaha.
- Default zona waktu bisnis untuk implementasi awal: `Asia/Jakarta`.
- Nilai uang Rupiah disimpan sebagai integer.
- Berat disimpan menggunakan tipe numerik presisi.
- Referential integrity menggunakan foreign key.
- Index dibuat berdasarkan kebutuhan query.
- Tidak menggunakan floating-point untuk menghitung uang.

## 6.2 Tabel Inti

| Tabel                       | Tanggung Jawab                                       |
| --------------------------- | ---------------------------------------------------- |
| `businesses`              | Identitas laundry.                                   |
| `business_settings`       | Konfigurasi usaha.                                   |
| `users`                   | Pengguna internal.                                   |
| `user_sessions`           | Sesi autentikasi.                                    |
| `customers`               | Informasi pelanggan.                                 |
| `services`                | Layanan dan tarif.                                   |
| `orders`                  | Header pesanan.                                      |
| `order_items`             | Rincian layanan.                                     |
| `order_status_history`    | Riwayat pekerjaan.                                   |
| `payments`                | Transaksi pembayaran.                                |
| `payment_voids`           | Pembatalan atau pembalikan pembayaran terverifikasi. |
| `expenses`                | Pengeluaran operasional.                             |
| `pickup_requests`         | Permintaan penjemputan.                              |
| `delivery_tasks`          | Penugasan kurir.                                     |
| `delivery_status_history` | Riwayat tugas.                                       |
| `tracking_tokens`         | Akses tracking publik.                               |
| `idempotency_records`     | Pencegahan transaksi ganda.                          |
| `audit_logs`              | Riwayat tindakan sensitif.                           |

Skema lengkap akan dijabarkan dalam Database Design Document.

## 6.3 Tipe Data Utama

| Jenis Informasi          | Tipe                             |
| ------------------------ | -------------------------------- |
| Identifier               | UUID                             |
| Nomor pesanan            | VARCHAR dengan unique constraint |
| Nama                     | VARCHAR                          |
| WhatsApp                 | VARCHAR                          |
| Harga Rupiah             | BIGINT                           |
| Berat cucian             | NUMERIC(10,3)                    |
| Jumlah satuan            | NUMERIC sesuai aturan layanan    |
| Tanggal transaksi        | TIMESTAMPTZ                      |
| Status                   | VARCHAR + validasi nilai         |
| Catatan                  | TEXT                             |
| Pengaturan terbatas      | JSONB bila diperlukan            |
| Token tracking tersimpan | Hash kriptografis                |

## 6.4 Pengelolaan Harga

Tabel `services` berisi tarif aktif.

Tabel `order_items` menyimpan:

- Identitas layanan.
- Nama layanan saat transaksi.
- Jenis tarif saat transaksi.
- Satuan.
- Kuantitas.
- Harga satuan saat transaksi.
- Subtotal.

Tujuannya adalah menjaga histori transaksi.

Jika Owner mengubah tarif cuci setrika dari Rp7.000 menjadi Rp8.000, pesanan lama tetap memakai tarif Rp7.000.

## 6.5 Indeks Database

Indeks prioritas:

1. Unique index nomor pesanan.
2. Index tanggal pesanan.
3. Index status operasional.
4. Index pelanggan pada pesanan.
5. Index nomor WhatsApp yang dinormalisasi.
6. Index pembayaran berdasarkan pesanan.
7. Index pengeluaran berdasarkan tanggal.
8. Unique index hash token tracking.
9. Index tugas kurir berdasarkan petugas dan status.
10. Index permintaan pickup berdasarkan status dan tanggal.

Indeks gabungan ditentukan setelah pola query dan hasil analisis performa tersedia.

## 6.6 Database Migration

Alembic menjadi mekanisme resmi migrasi skema.

Ketentuan:

1. Setiap perubahan skema dibuat sebagai migration.
2. File migration masuk version control.
3. Migration yang dihasilkan otomatis harus direview.
4. Migration tidak boleh dijalankan secara bersamaan oleh beberapa worker.
5. Migration produksi didahului backup.
6. Migration berisiko harus memiliki prosedur rollback atau recovery.
7. Perubahan destruktif membutuhkan persetujuan teknis.
8. Database tidak diubah langsung secara manual tanpa dokumentasi.

## 6.7 Transaksi Database

Operasi berikut harus menggunakan transaksi atomik:

- Pembuatan pesanan beserta item.
- Pencatatan pembayaran.
- Koreksi atau void pembayaran.
- Pembatalan pesanan.
- Perubahan status dengan audit history.
- Pembuatan permintaan pickup dan token tracking.
- Konversi permintaan pickup menjadi pesanan.

Jika salah satu operasi gagal, perubahan terkait harus di-rollback agar data tetap konsisten.

---

# 7. PERHITUNGAN BISNIS DAN KONSISTENSI TRANSAKSI

## 7.1 Mesin Perhitungan Harga

Sistem harus menyediakan satu komponen perhitungan harga di backend.

### Rumus

Subtotal item = Kuantitas × Harga satuan.

Subtotal pesanan = Total seluruh subtotal item.

Total tagihan = Subtotal pesanan + Biaya tambahan + Biaya antar-jemput − Diskon yang sah.

Karena diskon belum masuk MVP, nilainya dianggap nol sampai fitur tersebut dikembangkan.

### Ketentuan Pembulatan

1. Berat menggunakan Decimal.
2. Tarif disimpan dalam Rupiah.
3. Aturan minimum berat dan pembulatan ditentukan oleh konfigurasi usaha.
4. Hasil uang harus berupa Rupiah bulat.
5. Kebijakan pembulatan harus konsisten antara backend, nota, dan laporan.
6. Frontend boleh menghitung pratinjau, tetapi backend menjadi sumber kebenaran total harga.

## 7.2 Pencatatan Pembayaran

Pembayaran tidak disimpan sebagai satu angka yang bisa diubah bebas.

Setiap pembayaran memiliki record tersendiri.

Contoh:

| Transaksi          |  Nominal | Status        |
| ------------------ | -------: | ------------- |
| Tagihan pesanan    | Rp50.000 | Aktif         |
| Pembayaran pertama | Rp20.000 | Terverifikasi |
| Pembayaran kedua   | Rp30.000 | Terverifikasi |
| Sisa tagihan       |      Rp0 | Lunas         |

### Aturan Teknis

1. Backend memvalidasi jumlah pembayaran.
2. Pembayaran yang sah dihitung dari pembayaran terverifikasi yang tidak dibatalkan.
3. Record pembayaran tidak dapat dihapus langsung.
4. Koreksi pembayaran menggunakan prosedur void dengan alasan dan audit.
5. Sistem menghitung ulang sisa tagihan setelah koreksi.
6. Pembayaran lebih dari sisa tagihan ditolak pada MVP.
7. Pembatalan pesanan yang sudah dibayar harus mengikuti SOP refund yang disetujui.

## 7.3 Concurrency Control

Kasus yang harus ditangani:

- Dua kasir menyimpan pembayaran pesanan yang sama.
- Dua staf mengubah status secara bersamaan.
- Owner mengubah pesanan ketika kasir sedang membukanya.
- Pengguna menekan tombol simpan beberapa kali.

### Solusi

**Pessimistic Locking**

Digunakan untuk transaksi keuangan dan perubahan total yang membutuhkan konsistensi kuat.

Contohnya, backend mengunci record pesanan menggunakan row-level locking selama pemeriksaan dan pencatatan pembayaran.

**Optimistic Locking**

Digunakan pada pembaruan data pesanan dan status melalui field versi.

Contoh:

- Versi awal pesanan: 4.
- Petugas A dan B membaca versi 4.
- Petugas A berhasil memperbarui menjadi versi 5.
- Petugas B mengirim versi 4.
- Backend mengembalikan konflik dan meminta pemuatan ulang data.

## 7.4 Idempotency

Operasi pembuatan data penting harus mendukung `Idempotency-Key`.

Operasi prioritas:

- Pembuatan pesanan.
- Pencatatan pembayaran.
- Pengajuan penjemputan bila sesuai mekanisme token.
- Pembatalan pembayaran.
- Konversi pickup menjadi order.

Jika request yang sama dikirim ulang menggunakan kunci yang sama, sistem tidak boleh membuat transaksi kedua.

Backend menyimpan informasi kunci, scope operasi, hash request, status, dan hasil transaksi.

Penggunaan kunci yang sama dengan payload berbeda harus ditolak.

---

# 8. DESAIN REST API

## 8.1 Konvensi API

Base path:

`/api/v1`

Format data:

- Request: JSON.
- Response: JSON.
- Encoding: UTF-8.
- Waktu: ISO 8601 UTC.
- Identifier: UUID.
- Nilai uang: integer Rupiah.
- Pagination: diterapkan pada daftar.
- Authentication: session cookie untuk endpoint internal.

## 8.2 Format Response

Response sukses direkomendasikan menggunakan pola konsisten:

- `data`: hasil utama.
- `meta`: metadata opsional.
- `request_id`: identitas permintaan untuk pelacakan.

Response error menggunakan:

- `error.code`: kode error stabil.
- `error.message`: penjelasan yang aman.
- `error.details`: rincian validasi opsional.
- `request_id`: identitas permintaan.

Backend tidak boleh mengembalikan stack trace atau informasi rahasia kepada pengguna.

## 8.3 Standar HTTP Status

| Status | Penggunaan                                             |
| ------ | ------------------------------------------------------ |
| 200    | Request berhasil.                                      |
| 201    | Resource berhasil dibuat.                              |
| 204    | Operasi berhasil tanpa isi response.                   |
| 400    | Request tidak valid.                                   |
| 401    | Pengguna belum terautentikasi.                         |
| 403    | Tidak memiliki izin.                                   |
| 404    | Resource tidak ditemukan atau tidak boleh diungkapkan. |
| 409    | Konflik data, versi, atau state transition.            |
| 422    | Validasi request gagal.                                |
| 429    | Batas request terlampaui.                              |
| 500    | Kesalahan internal.                                    |
| 503    | Layanan sementara tidak tersedia.                      |

## 8.4 Authentication API

| Method | Endpoint                  | Fungsi                                |
| ------ | ------------------------- | ------------------------------------- |
| GET    | `/auth/csrf`            | Menginisialisasi proteksi CSRF.       |
| POST   | `/auth/login`           | Login petugas.                        |
| POST   | `/auth/logout`          | Mengakhiri sesi.                      |
| GET    | `/auth/me`              | Mendapatkan identitas dan permission. |
| POST   | `/auth/change-password` | Mengubah password sendiri.            |

Seluruh endpoint tersebut berada di bawah `/api/v1`.

## 8.5 Dashboard API

| Method | Endpoint                       | Fungsi                            |
| ------ | ------------------------------ | --------------------------------- |
| GET    | `/dashboard/summary`         | Ringkasan operasional.            |
| GET    | `/dashboard/recent-orders`   | Pesanan terbaru.                  |
| GET    | `/dashboard/overdue-orders`  | Pesanan terlambat.                |
| GET    | `/dashboard/payment-summary` | Ringkasan pembayaran sesuai izin. |

## 8.6 Orders API

| Method | Endpoint                            | Fungsi                      |
| ------ | ----------------------------------- | --------------------------- |
| GET    | `/orders`                         | Daftar pesanan.             |
| POST   | `/orders`                         | Membuat pesanan.            |
| GET    | `/orders/{id}`                    | Detail pesanan.             |
| PATCH  | `/orders/{id}`                    | Memperbarui pesanan.        |
| POST   | `/orders/{id}/status-transitions` | Mengubah status pengerjaan. |
| POST   | `/orders/{id}/cancel`             | Membatalkan pesanan.        |
| GET    | `/orders/{id}/history`            | Riwayat perubahan.          |

### Request Membuat Pesanan

Field minimum:

- `customer_id`
- `items`
- `estimated_completion_at`
- `fulfillment_method`
- `customer_notes` opsional
- `internal_notes` opsional

Setiap item:

- `service_id`
- `quantity`

Harga dihitung ulang di backend berdasarkan tarif layanan yang aktif.

Frontend tidak boleh menentukan total pembayaran yang dianggap final oleh server.

### Response Membuat Pesanan

Field utama:

- `id`
- `order_number`
- `customer`
- `items`
- `subtotal_amount`
- `delivery_fee_amount`
- `total_amount`
- `paid_amount`
- `remaining_amount`
- `payment_status`
- `operational_status`
- `estimated_completion_at`
- `version`
- `created_at`

## 8.7 Customers API

| Method | Endpoint                   | Fungsi              |
| ------ | -------------------------- | ------------------- |
| GET    | `/customers`             | Daftar pelanggan.   |
| POST   | `/customers`             | Tambah pelanggan.   |
| GET    | `/customers/{id}`        | Detail pelanggan.   |
| PATCH  | `/customers/{id}`        | Perbarui pelanggan. |
| GET    | `/customers/{id}/orders` | Riwayat pesanan.    |

## 8.8 Services API

| Method | Endpoint                      | Fungsi               |
| ------ | ----------------------------- | -------------------- |
| GET    | `/services`                 | Daftar layanan.      |
| POST   | `/services`                 | Tambah layanan.      |
| GET    | `/services/{id}`            | Detail layanan.      |
| PATCH  | `/services/{id}`            | Perbarui layanan.    |
| POST   | `/services/{id}/deactivate` | Nonaktifkan layanan. |

Hanya Owner yang dapat melakukan perubahan tarif dan konfigurasi layanan.

## 8.9 Payments API

| Method | Endpoint                  | Fungsi                                             |
| ------ | ------------------------- | -------------------------------------------------- |
| GET    | `/orders/{id}/payments` | Riwayat pembayaran.                                |
| POST   | `/orders/{id}/payments` | Catat pembayaran terverifikasi.                    |
| POST   | `/payments/{id}/void`   | Membatalkan catatan pembayaran dengan izin khusus. |
| GET    | `/payments/{id}`        | Detail transaksi.                                  |

### Request Pembayaran

- `amount`
- `payment_method`
- `payment_time`
- `reference_note` opsional

Metode:

- CASH
- BANK_TRANSFER
- QRIS_MANUAL

Petugas yang memverifikasi diambil dari sesi autentikasi, bukan dari input frontend.

Backend wajib menghitung sisa tagihan di dalam transaksi database.

## 8.10 Expenses API

| Method | Endpoint           | Fungsi                |
| ------ | ------------------ | --------------------- |
| GET    | `/expenses`      | Daftar pengeluaran.   |
| POST   | `/expenses`      | Mencatat pengeluaran. |
| GET    | `/expenses/{id}` | Detail pengeluaran.   |
| PATCH  | `/expenses/{id}` | Koreksi dengan audit. |

## 8.11 Pickup & Delivery API

| Method | Endpoint                                    | Fungsi                                          |
| ------ | ------------------------------------------- | ----------------------------------------------- |
| GET    | `/pickup-requests`                        | Daftar permintaan.                              |
| GET    | `/pickup-requests/{id}`                   | Detail permintaan.                              |
| POST   | `/pickup-requests/{id}/confirm`           | Konfirmasi jadwal.                              |
| POST   | `/pickup-requests/{id}/reject`            | Tolak permintaan.                               |
| POST   | `/pickup-requests/{id}/convert-to-order`  | Membuat pesanan dari pickup.                    |
| GET    | `/delivery-tasks`                         | Daftar tugas kurir.                             |
| POST   | `/delivery-tasks`                         | Membuat tugas pengantaran/penjemputan internal. |
| PATCH  | `/delivery-tasks/{id}`                    | Perbarui jadwal/penugasan.                      |
| POST   | `/delivery-tasks/{id}/status-transitions` | Perbarui progres tugas.                         |
| GET    | `/delivery-tasks/{id}/history`            | Riwayat tugas.                                  |

## 8.12 Invoice API

| Method | Endpoint                          | Fungsi                            |
| ------ | --------------------------------- | --------------------------------- |
| GET    | `/orders/{id}/invoice`          | Data nota internal.               |
| GET    | `/orders/{id}/invoice.pdf`      | Menghasilkan PDF nota.            |
| GET    | `/orders/{id}/whatsapp-preview` | Membuat pratinjau pesan WhatsApp. |

Nota menggunakan data transaksi yang telah tersimpan.

## 8.13 Public API

Endpoint publik tidak menggunakan session petugas.

| Method | Endpoint                              | Fungsi                      |
| ------ | ------------------------------------- | --------------------------- |
| POST   | `/public/pickup-requests`           | Pengajuan pickup pelanggan. |
| GET    | `/public/track/{token}`             | Tracking berdasarkan token. |
| GET    | `/public/track/{token}/invoice`     | Nota yang dibatasi token.   |
| GET    | `/public/track/{token}/invoice.pdf` | PDF nota publik.            |
| GET    | `/public/business-info`             | Informasi publik usaha.     |

### Ketentuan Public API

1. Tidak mengembalikan data pelanggan lain.
2. Tidak menerima identitas internal yang tidak diperlukan.
3. Token diverifikasi menggunakan hash yang disimpan.
4. Semua response tracking menggunakan `Cache-Control: no-store`.
5. Request memiliki rate limiting.
6. Tidak ada mutation status pesanan oleh pelanggan.
7. Field response publik menggunakan allowlist eksplisit.
8. Nomor telepon dan alamat lengkap tidak dikembalikan.
9. Request pickup harus mendapat perlindungan terhadap spam dan penyalahgunaan.

## 8.14 Settings dan User API

| Method | Endpoint                   | Fungsi                  |
| ------ | -------------------------- | ----------------------- |
| GET    | `/business`              | Profil usaha.           |
| PATCH  | `/business`              | Ubah profil usaha.      |
| GET    | `/settings`              | Pengaturan operasional. |
| PATCH  | `/settings`              | Ubah pengaturan.        |
| GET    | `/users`                 | Daftar pegawai.         |
| POST   | `/users`                 | Buat akun pegawai.      |
| PATCH  | `/users/{id}`            | Perbarui akun.          |
| POST   | `/users/{id}/deactivate` | Nonaktifkan akun.       |

## 8.15 Reporting API

| Method | Endpoint                 | Fungsi                       |
| ------ | ------------------------ | ---------------------------- |
| GET    | `/reports/orders`      | Laporan pesanan.             |
| GET    | `/reports/payments`    | Laporan pembayaran.          |
| GET    | `/reports/outstanding` | Daftar piutang.              |
| GET    | `/reports/expenses`    | Laporan pengeluaran.         |
| GET    | `/reports/export.csv`  | Ekspor laporan yang dipilih. |

Endpoint laporan harus memeriksa permission sesuai jenis informasi.

---

# 9. STATE MANAGEMENT DAN WORKFLOW

## 9.1 Status Cucian

Representasi internal:

1. `RECEIVED`
2. `QUEUED`
3. `WASHING`
4. `DRYING`
5. `IRONING`
6. `QC_PACKING`
7. `READY`
8. `COMPLETED`
9. `CANCELLED`

Label antarmuka tetap menggunakan Bahasa Indonesia.

### Aturan

- Tahapan dapat dilewati jika tidak relevan dengan layanan.
- Transisi harus diperiksa berdasarkan state machine.
- Perubahan mundur memerlukan alasan dan permission.
- `COMPLETED` memerlukan catatan serah terima.
- `CANCELLED` adalah status terminal untuk alur normal.
- Setiap transisi menyimpan `from_status`, `to_status`, waktu, petugas, dan alasan jika diperlukan.

## 9.2 Status Penjemputan

Representasi internal:

- `REQUESTED`
- `CONFIRMED`
- `ASSIGNED`
- `EN_ROUTE`
- `PICKED_UP`
- `AT_LAUNDRY`
- `REJECTED`
- `FAILED`
- `CANCELLED`

Antarmuka pelanggan dapat menyederhanakan status internal menjadi status yang mudah dipahami.

## 9.3 Status Pengantaran

Representasi internal:

- `PENDING`
- `SCHEDULED`
- `EN_ROUTE`
- `IN_DELIVERY`
- `DELIVERED`
- `FAILED`
- `CANCELLED`

Kegagalan pengantaran dapat dibuatkan penjadwalan ulang tanpa menghapus riwayat sebelumnya.

## 9.4 Status Pembayaran

Status pembayaran merupakan hasil perhitungan:

- `UNPAID`
- `PARTIALLY_PAID`
- `PAID`

Status tidak boleh ditentukan hanya dengan mengubah field secara manual.

## 9.5 Hubungan Antarstatus

Status pencucian, penjemputan, pengantaran, dan pembayaran merupakan empat state yang berbeda.

Contoh:

- Cucian: `READY`
- Pickup: `AT_LAUNDRY`
- Delivery: `SCHEDULED`
- Payment: `PARTIALLY_PAID`

Sistem wajib dapat menyimpan keadaan tersebut tanpa konflik.

---

# 10. TEKNIS TRACKING TANPA LOGIN

## 10.1 Mekanisme Token

Sistem menggunakan bearer token khusus tracking.

Token dihasilkan dengan cryptographically secure random generator.

Persyaratan:

- Entropi minimal 128 bit.
- Direkomendasikan 256 bit.
- Encoding URL-safe.
- Tidak menggunakan nomor urut.
- Tidak mengandung informasi pelanggan.
- Token mentah tidak disimpan dalam log.
- Database menyimpan hash token.

## 10.2 Validasi Token

Saat pelanggan membuka tautan:

1. Backend menerima token.
2. Backend menghitung hash token.
3. Backend mencari record token yang sesuai.
4. Backend memastikan token masih aktif.
5. Backend memeriksa waktu kedaluwarsa.
6. Backend memeriksa resource yang diotorisasi.
7. Backend membentuk response publik dari allowlist data.
8. Frontend menampilkan informasi tracking.

## 10.3 Masa Berlaku Token

Kebijakan awal yang diusulkan:

- Token pickup tetap berlaku saat permintaan diproses.
- Token dapat tetap mengakses pesanan setelah pickup dikonversi.
- Token berlaku sampai 90 hari setelah pesanan selesai.
- Owner/Admin dapat mencabut dan membuat token baru.
- Masa berlaku dapat disesuaikan setelah kebijakan retensi disetujui.

Masa berlaku ini merupakan rancangan, bukan keputusan bisnis final.

## 10.4 Pencegahan Kebocoran Token

Persyaratan keamanan:

1. Gunakan HTTPS.
2. Gunakan `Referrer-Policy: no-referrer`.
3. Gunakan `X-Robots-Tag: noindex, nofollow`.
4. Gunakan `Cache-Control: no-store`.
5. Jangan memuat skrip analitik pihak ketiga pada halaman tracking.
6. Hindari resource eksternal yang dapat menerima informasi URL sensitif.
7. Jangan mencatat path bertoken secara mentah dalam access log.
8. Jangan menampilkan token pada pesan error.
9. Jangan mengekspos token melalui API daftar pesanan.
10. Gunakan mekanisme rotasi jika tautan bocor.

## 10.5 Penyelarasan Tracking Pickup dan Order

Pada tahap awal pelanggan menerima token untuk permintaan penjemputan.

Setelah permintaan dikonversi menjadi order:

1. `pickup_request` dihubungkan dengan `order`.
2. Token tetap mengarah ke konteks tracking yang sama.
3. Response publik dapat menampilkan status pesanan terkait.
4. Tidak perlu memaksa pelanggan menerima tautan baru.
5. Akses tidak diperluas ke pesanan lain milik pelanggan.

## 10.6 Peremajaan Data

MVP menggunakan polling sederhana.

Rekomendasi:

- Saat halaman dibuka, data diambil dari API.
- Tombol Muat Ulang tersedia.
- Polling otomatis opsional setiap 60 detik ketika halaman aktif.
- Polling dihentikan ketika halaman tidak aktif.
- Sistem menampilkan waktu pembaruan terakhir.

WebSocket tidak diperlukan pada MVP.

---

# 11. TEKNIS WHATSAPP MANUAL

## 11.1 Konsep

WhatsApp digunakan sebagai kanal komunikasi manual.

Sistem tidak memerlukan WhatsApp Business API.

Backend hanya menyiapkan pesan berdasarkan data transaksi.

## 11.2 Template Pesan

Template mencakup:

- Konfirmasi pesanan.
- Pengiriman nota.
- Cucian selesai.
- Pengingat pengambilan.
- Konfirmasi penjemputan.
- Konfirmasi pengantaran.

## 11.3 Mekanisme Teknis

1. Admin memilih tindakan komunikasi.
2. Sistem membentuk pesan.
3. Nomor telepon dinormalisasi ke format internasional.
4. Sistem membentuk tautan WhatsApp.
5. Browser membuka WhatsApp atau WhatsApp Web.
6. Admin meninjau dan mengirim pesan.

Format dasar:

`https://wa.me/{nomor}?text={pesan_terenkripsi_url}`

## 11.4 Batasan

Sistem tidak boleh mengklaim:

- Pesan pasti terkirim.
- Pesan sudah dibaca.
- Nomor WhatsApp aktif.
- Pelanggan menerima notifikasi otomatis.

Tanpa integrasi resmi, aplikasi tidak mempunyai bukti pengiriman pesan.

---

# 12. TEKNIS NOTA DIGITAL DAN PDF

## 12.1 Sumber Data Nota

Nota dibuat dari data pesanan yang tersimpan di server.

Frontend tidak boleh menjadi sumber tunggal perhitungan nota.

## 12.2 Konten Nota

- Identitas usaha.
- Nomor pesanan.
- Tanggal.
- Nama pelanggan.
- Rincian layanan.
- Berat atau jumlah.
- Tarif.
- Total tagihan.
- Pembayaran diterima.
- Sisa tagihan.
- Estimasi selesai.
- Informasi tracking.
- Ketentuan layanan.

## 12.3 Rendering PDF

Backend menghasilkan PDF dari template nota yang dikontrol aplikasi.

Persyaratan:

1. Tidak memerlukan printer.
2. Mendukung unduhan melalui browser mobile.
3. Layout dapat dibaca pada kertas A4 jika suatu saat dicetak.
4. Nominal dan tanggal menggunakan format Indonesia.
5. PDF tidak mengungkap data internal.
6. Nama file tidak mengandung data pribadi yang tidak diperlukan.
7. Pembuatan PDF tidak boleh mengubah data keuangan.
8. PDF dihasilkan dari data terverifikasi dan terbaru.

## 12.4 Keamanan PDF

- Escape konten dinamis.
- Batasi sumber gambar/logo.
- Hindari pengambilan URL arbitrer oleh server.
- Validasi input template.
- Gunakan header keamanan sesuai jenis response.
- PDF publik hanya tersedia jika token valid.

---

# 13. KEAMANAN APLIKASI

## 13.1 Security Baseline

Standar acuan:

**OWASP Application Security Verification Standard (ASVS) 5.0**, dengan kontrol yang relevan terhadap autentikasi, sesi, kontrol akses, validasi input, perlindungan data, dan API.

## 13.2 Password Security

Ketentuan:

1. Password tidak disimpan dalam plaintext.
2. Gunakan Argon2id.
3. Parameter hashing mengikuti rekomendasi yang relevan dan kemampuan server.
4. Password tidak muncul di log.
5. Login menerapkan throttling.
6. Pesan kesalahan login tidak membocorkan keberadaan akun.
7. Akun dapat dinonaktifkan.
8. Penggantian password mencabut sesi sesuai kebijakan.

## 13.3 API Security

Persyaratan:

- Validasi menggunakan Pydantic.
- Otorisasi pada setiap endpoint internal.
- Pemeriksaan kepemilikan atau assignment resource.
- Rate limiting pada endpoint publik.
- Pembatasan ukuran request.
- Parameterized query melalui ORM.
- Penanganan kesalahan terpusat.
- Security headers.
- CORS dengan origin terbatas.
- CSRF protection.
- Tidak ada hardcoded secret.

## 13.4 Pencegahan IDOR

Penggunaan UUID tidak dianggap cukup sebagai kontrol akses.

Untuk setiap endpoint:

1. Backend memeriksa autentikasi bila diperlukan.
2. Backend memeriksa permission.
3. Backend memeriksa konteks resource.
4. Kurir hanya melihat tugas yang sah.
5. Portal publik hanya melihat resource yang diotorisasi token.

## 13.5 Audit Log

Tindakan yang wajib diaudit:

- Login gagal berulang.
- Perubahan akun dan role.
- Perubahan tarif.
- Perubahan nilai pesanan.
- Pembatalan pesanan.
- Perubahan pembayaran.
- Void pembayaran.
- Perubahan pengaturan penting.
- Pencabutan token tracking.
- Koreksi status operasional.

Informasi audit:

- Actor ID.
- Action.
- Resource type.
- Resource ID.
- Timestamp.
- Request ID.
- Metadata perubahan yang tidak sensitif.
- Alasan jika diwajibkan.

Audit log tidak boleh mengandung password, session token, atau token tracking mentah.

## 13.6 File Upload

MVP tidak mewajibkan upload foto cucian maupun bukti pembayaran.

Jika logo usaha diunggah:

1. Validasi tipe file.
2. Validasi ukuran maksimum.
3. Batasi format gambar yang diperbolehkan.
4. Jangan mempercayai ekstensi file.
5. Gunakan nama file acak.
6. Simpan di lokasi terkontrol.
7. Jangan mengizinkan eksekusi file upload.

---

# 14. FRONTEND UI/UX TECHNICAL REQUIREMENTS

## 14.1 Responsive Breakpoints

Rancangan perlu diuji minimal pada viewport:

- 320 px.
- 360 px.
- 375 px.
- 390 px.
- 430 px.
- 768 px.
- 1024 px.
- 1440 px.

Penggunaan breakpoint CSS dapat menyesuaikan framework, tetapi hasil akhir harus diuji pada ukuran tersebut.

## 14.2 Navigation

### Mobile

Menggunakan navigasi yang ringkas, dengan akses cepat ke:

- Dashboard.
- Pesanan.
- Buat Pesanan.
- Antar-Jemput.
- Menu lainnya.

### Desktop

Menggunakan sidebar navigasi dan area konten yang lebih luas.

## 14.3 Design System

Token utama:

- Primary.
- Secondary.
- Surface.
- Text Primary.
- Text Secondary.
- Border.
- Success.
- Warning.
- Error.
- Info.

Warna final ditetapkan pada dokumen UI/UX, bukan dikunci dalam TRD.

## 14.4 Form Requirements

Setiap formulir harus:

1. Memiliki label.
2. Menandai field wajib.
3. Memberi pesan validasi di dekat input.
4. Mencegah submit ganda.
5. Menampilkan feedback penyimpanan.
6. Mempertahankan input saat validasi gagal.
7. Menangani kesalahan jaringan.
8. Mendukung keyboard mobile sesuai jenis data.
9. Memberikan konfirmasi pada aksi berisiko.
10. Tidak menghilangkan data input tanpa pemberitahuan.

## 14.5 Accessibility

Target awal mengikuti WCAG 2.2 Level AA untuk komponen dan alur yang relevan.

Persyaratan:

- Kontras yang memadai.
- Label pada input.
- Navigasi keyboard.
- Focus indicator.
- Ukuran target sentuh yang memadai.
- Tidak mengandalkan warna saja.
- Error message yang jelas.
- Dukungan prefers-reduced-motion.
- Struktur heading semantik.
- Screen reader label pada kontrol ikon.

## 14.6 PWA

PWA dapat diinstal melalui browser yang mendukung.

Persyaratan:

- Manifest.
- Ikon aplikasi.
- Nama dan deskripsi.
- Mode tampilan standalone bila didukung.
- HTTPS pada produksi.

**Batasan:** MVP tetap membutuhkan internet. Service worker tidak boleh menyimpan halaman tracking, informasi pembayaran, atau respons privat dalam cache publik.

---

# 15. PERFORMANCE REQUIREMENTS

## 15.1 Target API

Target awal pengujian:

| Operasi               | Target          |
| --------------------- | --------------- |
| GET daftar standar    | p95 ≤ 1.000 ms |
| GET detail pesanan    | p95 ≤ 800 ms   |
| POST pesanan          | p95 ≤ 2.000 ms |
| POST pembayaran       | p95 ≤ 1.500 ms |
| GET tracking publik   | p95 ≤ 1.000 ms |
| GET dashboard summary | p95 ≤ 1.500 ms |

Target diukur pada lingkungan pengujian yang ditentukan, tidak termasuk latensi jaringan eksternal pengguna.

## 15.2 Skenario Beban

Baseline pengujian awal:

- 5.000 pelanggan.
- 20.000 pesanan historis.
- 50.000 item layanan.
- 30.000 riwayat status.
- 10.000 transaksi pembayaran.
- Hingga 25 pengguna internal aktif bersamaan.
- Hingga 100 sesi pembacaan tracking publik pada skenario beban uji.

Angka tersebut merupakan dataset dan target pengujian, bukan klaim kapasitas produksi.

## 15.3 Frontend Performance

Target:

1. Halaman inti dapat digunakan dalam waktu yang wajar pada koneksi mobile representatif.
2. Loading tidak menghalangi navigasi utama secara tidak perlu.
3. Daftar panjang menggunakan pagination.
4. Aset frontend dioptimalkan.
5. Bundle dipecah berdasarkan route.
6. Komponen berat dimuat hanya saat diperlukan.
7. Gambar dikompresi.
8. Interaksi utama tidak menyebabkan freeze yang berulang.

Pengukuran dilakukan menggunakan Lighthouse dan pengujian perangkat nyata bila tersedia.

---

# 16. ERROR HANDLING DAN OBSERVABILITY

## 16.1 Error Handling

Backend menggunakan exception handler terpusat.

Contoh kode error domain:

- `ORDER_NOT_FOUND`
- `INVALID_ORDER_STATE`
- `PAYMENT_EXCEEDS_BALANCE`
- `PAYMENT_ALREADY_VOIDED`
- `STALE_ORDER_VERSION`
- `UNAUTHORIZED_ACTION`
- `TRACKING_TOKEN_INVALID`
- `TRACKING_TOKEN_EXPIRED`
- `PICKUP_REQUEST_NOT_FOUND`
- `VALIDATION_ERROR`
- `IDEMPOTENCY_CONFLICT`

Pesan frontend menggunakan Bahasa Indonesia yang mudah dipahami.

## 16.2 Structured Logging

Log minimal mencatat:

- Timestamp.
- Log level.
- Request ID.
- Method.
- Route template.
- Status code.
- Duration.
- Actor ID jika tersedia.
- Error code jika ada.

Log tidak boleh mengandung:

- Password.
- Session identifier.
- Token tracking mentah.
- Nomor rekening lengkap.
- Data pembayaran sensitif.
- URL publik bertoken dalam bentuk mentah.

## 16.3 Health Check

Endpoint:

- `/health/live`
- `/health/ready`

`live` memastikan proses aplikasi hidup.

`ready` memastikan dependency kritis, terutama database, tersedia sesuai kebutuhan.

Health endpoint tidak boleh memaparkan konfigurasi internal secara publik.

## 16.4 Monitoring

Monitoring minimal:

- Uptime aplikasi.
- Error rate.
- Latensi API.
- Database connection failures.
- Kegagalan login berulang.
- Penyimpanan database.
- Keberhasilan backup.
- Kegagalan operasi transaksi.

Untuk MVP, monitoring sederhana dan log terstruktur lebih diprioritaskan daripada platform observability kompleks.

---

# 17. INFRASTRUKTUR DAN DEPLOYMENT

## 17.1 Environment

Tiga environment direkomendasikan:

| Environment | Fungsi                          |
| ----------- | ------------------------------- |
| Development | Pengembangan lokal.             |
| Staging     | Pengujian terintegrasi dan UAT. |
| Production  | Penggunaan operasional nyata.   |

Database, secret, dan data antar-environment harus dipisahkan.

## 17.2 Development Lokal

Lingkungan pengembangan menggunakan:

- Node.js.
- Python 3.12.
- PostgreSQL.
- Docker Compose opsional untuk database.
- Vite development server.
- FastAPI development server.

Konfigurasi sensitif disimpan dalam `.env` yang tidak masuk version control.

## 17.3 Production Architecture

Arsitektur produksi minimal:

1. HTTPS reverse proxy atau hosting yang mengelola TLS.
2. Frontend static assets.
3. FastAPI application server.
4. PostgreSQL database.
5. Persistent storage untuk data yang diperlukan.
6. Backup database.
7. Logging.
8. Health monitoring.

Tidak perlu cluster Kubernetes.

## 17.4 Perkiraan Infrastruktur Awal

Kapasitas awal yang dapat diuji:

- API: 1–2 vCPU.
- RAM API: sekitar 1–2 GB.
- PostgreSQL: layanan database kecil yang didukung.
- Storage database: mulai dari kebutuhan rendah dan dapat ditingkatkan.
- HTTPS aktif.
- Backup harian.

Spesifikasi tersebut merupakan kandidat awal, bukan hasil benchmark dan bukan jaminan kecukupan.

Sizing final dilakukan setelah load test dan pengukuran penggunaan memori.

## 17.5 Deployment Procedure

Urutan deployment:

1. Jalankan CI.
2. Jalankan test.
3. Build frontend.
4. Build backend/container.
5. Verifikasi konfigurasi.
6. Lakukan backup bila ada perubahan database.
7. Jalankan migration satu kali.
8. Deploy aplikasi.
9. Jalankan health check.
10. Jalankan smoke test.
11. Aktifkan traffic produksi.
12. Pantau error setelah deployment.

## 17.6 Rollback

Rollback aplikasi harus menggunakan versi artefak yang telah diketahui stabil.

Untuk perubahan database:

- Migration harus direview.
- Perubahan destruktif tidak boleh diasumsikan dapat di-rollback otomatis.
- Gunakan pendekatan expand-and-contract jika perlu.
- Recovery database menggunakan backup teruji apabila diperlukan.

---

# 18. BACKUP DAN DISASTER RECOVERY

## 18.1 Kebijakan Backup

Rekomendasi awal:

- Backup database otomatis setiap hari.
- Retensi backup harian minimal 7 hari sebagai baseline awal.
- Backup sebelum migration berisiko.
- Penyimpanan backup terpisah dari database utama.
- Enkripsi backup ketika memuat data pelanggan.
- Pembatasan akses backup.

## 18.2 Target Recovery

Target awal:

| Indikator        | Sasaran                     |
| ---------------- | --------------------------- |
| RPO              | Maksimal 24 jam             |
| RTO              | Maksimal 4 jam              |
| Backup Frequency | Harian                      |
| Restore Test     | Sebelum go-live dan berkala |

RPO merupakan batas kehilangan data yang ditargetkan, sedangkan RTO adalah target pemulihan layanan.

Target harus disesuaikan dengan kemampuan hosting dan anggaran.

## 18.3 Pengujian Restore

Prosedur:

1. Ambil backup.
2. Pulihkan ke lingkungan terisolasi.
3. Validasi struktur database.
4. Verifikasi jumlah data.
5. Verifikasi beberapa pesanan dan pembayaran.
6. Jalankan smoke test.
7. Dokumentasikan hasil.

Backup tidak dianggap valid hanya karena file backup berhasil dibuat.

---

# 19. TESTING STRATEGY

## 19.1 Unit Testing

Fokus:

- Perhitungan harga.
- Pembulatan berat.
- Sisa tagihan.
- Status pembayaran.
- State transition.
- Validasi bisnis.
- Normalisasi nomor WhatsApp.
- Token hashing.
- Perhitungan keterlambatan.

## 19.2 Integration Testing

Menggunakan PostgreSQL pengujian.

Skenario:

- Create order dan items secara atomik.
- Simpan pembayaran.
- Void pembayaran.
- Pembatalan pesanan.
- Konversi pickup menjadi order.
- Permission check.
- Migration.
- Concurrency.
- Idempotency.

## 19.3 API Contract Testing

Setiap endpoint diperiksa terhadap OpenAPI.

Pengujian:

- Request valid.
- Request invalid.
- Response schema.
- Error schema.
- Permission.
- Pagination.
- Status code.
- Batas ukuran input.
- Field yang tidak boleh bocor.

## 19.4 Frontend Testing

Lingkup:

- Rendering komponen.
- Validasi formulir.
- Loading state.
- Error state.
- Permission-based navigation.
- Perhitungan pratinjau harga.
- Interaksi pembayaran.
- Tracking publik.

## 19.5 End-to-End Testing

Skenario wajib:

**E2E-01 — Pesanan Langsung**

Login → Pilih pelanggan → Buat pesanan → Simpan → Nota → Update status → Selesai.

**E2E-02 — Pembayaran DP**

Buat pesanan → Catat DP → Periksa sisa → Pelunasan → Verifikasi lunas.

**E2E-03 — Pickup**

Form publik → Permintaan masuk → Konfirmasi → Penugasan → Penjemputan → Konversi menjadi order.

**E2E-04 — Delivery**

Pesanan siap → Jadwalkan → Kurir mengantar → Konfirmasi penerimaan → Selesai.

**E2E-05 — Tracking Publik**

Terima token → Buka halaman → Lihat status → Staf mengubah status → Refresh → Status terbaru terlihat.

## 19.6 Security Testing

Wajib menguji:

1. Brute-force login.
2. Session expiry.
3. Logout invalidation.
4. CSRF.
5. XSS.
6. SQL injection.
7. IDOR.
8. Broken access control.
9. Token guessing.
10. Token revocation.
11. Data leakage.
12. Rate limiting.
13. Abuse terhadap formulir publik.
14. Unauthorized payment mutation.
15. Unauthorized price modification.

## 19.7 Concurrency Testing

Minimal menguji:

- Dua kasir membayar pesanan yang sama.
- Dua petugas mengubah status.
- Pesanan disimpan dua kali.
- Void pembayaran bersamaan dengan pelunasan.
- Permintaan pickup dikonversi dua kali.

Hasil yang diharapkan adalah tidak terjadi duplikasi, kehilangan pembaruan, atau perhitungan keuangan tidak konsisten.

## 19.8 Data Testing

Dataset uji mencakup:

- Pelanggan baru.
- Pelanggan berulang.
- Pesanan kiloan.
- Pesanan satuan.
- Pesanan multi-layanan.
- Pembayaran belum lunas.
- DP.
- Pelunasan.
- Pembayaran dibatalkan.
- Pickup.
- Delivery.
- Pesanan terlambat.
- Pesanan dibatalkan.
- Token kedaluwarsa.
- Token tidak valid.

---

# 20. CODE QUALITY DAN CI/CD

## 20.1 Coding Standard Backend

- Python menggunakan type hints.
- Ruff dijalankan secara konsisten.
- Business logic tidak ditulis langsung dalam router.
- SQLAlchemy session dikelola dengan jelas.
- Exception menggunakan domain error terstruktur.
- Query database harus terukur.
- Migration direview.
- Tidak menggunakan secret hardcoded.
- Tidak menggunakan wildcard import tanpa alasan kuat.

## 20.2 Coding Standard Frontend

- TypeScript strict.
- ESLint aktif.
- Komponen menggunakan tanggung jawab jelas.
- API client terpusat.
- Form schema terdefinisi.
- Tidak menggunakan `any` tanpa alasan terdokumentasi.
- Design tokens digunakan konsisten.
- Loading dan error state tersedia.
- Tidak menyimpan session token dalam localStorage.

## 20.3 Pipeline CI

Tahapan CI:

1. Install dependencies.
2. Dependency integrity check.
3. Lint frontend.
4. Typecheck frontend.
5. Test frontend.
6. Lint backend.
7. Typecheck backend.
8. Unit test backend.
9. Integration test PostgreSQL.
10. Migration check.
11. Build frontend.
12. Build backend.
13. Security/dependency scan.
14. Ringkasan hasil CI.

## 20.4 Branching Strategy

Rekomendasi sederhana:

- `main` — kode stabil.
- `develop` — integrasi bila diperlukan.
- `feature/*` — pengembangan fitur.
- `fix/*` — perbaikan bug.
- `release/*` — persiapan release bila diperlukan.

Untuk tim sangat kecil, trunk-based development dengan pull request singkat juga diperbolehkan.

## 20.5 Pull Request Requirements

Setiap PR harus:

- Menjelaskan perubahan.
- Memiliki referensi task.
- Menyebutkan dampak.
- Menambahkan atau memperbarui test.
- Lulus CI.
- Tidak menambah secret.
- Tidak membuat breaking change tanpa dokumentasi.
- Diperiksa sebelum merge.

---

# 21. TRACEABILITY PRD KE TRD

| PRD                  | Implementasi Teknis                       | Verifikasi               |
| -------------------- | ----------------------------------------- | ------------------------ |
| Dashboard            | Dashboard service dan reporting query     | API dan UI test          |
| Pesanan              | Orders module, order items, state machine | Unit, integration, E2E   |
| Pelanggan            | Customers module                          | API dan authorization    |
| Antar-Jemput         | Pickup requests dan delivery tasks        | E2E                      |
| Pembayaran Manual    | Payments service dan database transaction | Financial invariant test |
| Nota Digital         | Invoice service dan PDF generator         | PDF test                 |
| Tracking Tanpa Login | Tracking token service dan public API     | Security dan E2E         |
| Pengaturan           | Business, service, dan user settings      | Permission test          |
| Login Petugas        | Session auth dan RBAC                     | Authentication test      |
| Audit                | Audit logging module                      | Integration test         |
| Backup               | Deployment dan backup procedure           | Restore test             |

Setiap fitur P0 pada PRD wajib memiliki implementasi, acceptance criteria, dan hasil pengujian yang dapat ditelusuri.

---

# 22. MILESTONE IMPLEMENTASI TEKNIS

## M0 — Architecture & Repository Foundation

Deliverable:

- Repository.
- Struktur frontend/backend.
- Environment configuration.
- Database lokal.
- Dokumen arsitektur.
- Baseline OpenAPI.
- CI awal.

**Gate:** Infrastruktur development dapat dijalankan dan diverifikasi.

## M1 — Authentication & Business Configuration

Deliverable:

- Login.
- Session.
- CSRF.
- RBAC.
- Profil usaha.
- User management.
- Dashboard shell.

**Gate:** Hak akses backend dan session diuji.

## M2 — Core Laundry Operations

Deliverable:

- Services.
- Customers.
- Orders.
- Order items.
- Pricing.
- Status history.

**Gate:** Transaksi pesanan berjalan end-to-end.

## M3 — Finance & Digital Invoice

Deliverable:

- Payments.
- DP.
- Payment void.
- Expenses.
- Invoice.
- PDF.
- WhatsApp link.

**Gate:** Perhitungan dan konsistensi keuangan lulus.

## M4 — Public Tracking

Deliverable:

- Tracking token.
- Public tracking API.
- Tracking UI.
- Token revocation.
- Public security controls.

**Gate:** Tidak ada akses lintas pesanan atau kebocoran informasi.

## M5 — Pickup & Delivery

Deliverable:

- Pickup request.
- Pickup confirmation.
- Courier assignment.
- Delivery status.
- Pickup-to-order conversion.

**Gate:** Alur antar-jemput lulus E2E.

## M6 — Dashboard & Reporting

Deliverable:

- Dashboard metrics.
- Payments report.
- Expenses report.
- Outstanding balances.
- CSV export.

**Gate:** Rekonsiliasi dengan data transaksi lulus.

## M7 — Quality & Security Hardening

Deliverable:

- Full integration tests.
- E2E tests.
- Security tests.
- Load test.
- Responsive audit.
- Backup restore test.

**Gate:** Tidak terdapat critical blocker.

## M8 — Production Deployment

Deliverable:

- Production infrastructure.
- HTTPS.
- Database migration.
- Monitoring.
- Backup.
- Documentation.
- UAT sign-off.

**Gate:** Production readiness disetujui.

---

# 23. TECHNICAL ACCEPTANCE CRITERIA

## 23.1 Backend

Backend dinyatakan siap apabila:

1. Seluruh endpoint P0 tersedia.
2. Seluruh endpoint memiliki validasi input.
3. Seluruh endpoint internal dilindungi RBAC.
4. Kontrak OpenAPI sesuai implementasi.
5. Database migration lulus.
6. Perhitungan keuangan konsisten.
7. Operasi kritis atomik.
8. Concurrency ditangani.
9. Idempotency pada operasi penting berfungsi.
10. Tidak ada critical security finding yang terbuka.

## 23.2 Frontend

Frontend dinyatakan siap apabila:

1. Seluruh halaman P0 tersedia.
2. Tampilan mobile responsif.
3. Tidak ada overflow horizontal pada viewport target.
4. Form validasi berjalan.
5. Loading dan error ditangani.
6. Navigasi mengikuti permission.
7. Integrasi API berhasil.
8. Tracking publik dapat digunakan tanpa login.
9. Nota digital dapat dibuka dan disimpan.
10. Tidak ada runtime error kritis pada skenario utama.

## 23.3 Database

Database dinyatakan siap apabila:

1. Skema sesuai DBD.
2. Foreign key konsisten.
3. Constraint penting tersedia.
4. Migration dapat dijalankan dari database kosong.
5. Query utama memenuhi target pengujian.
6. Financial invariants terjaga.
7. Backup berhasil.
8. Restore berhasil.
9. Tidak terdapat data yatim yang tidak sah.
10. Tidak ada penggunaan floating-point untuk uang.

## 23.4 Production

Production dapat disetujui apabila:

- HTTPS aktif.
- Secret dikelola aman.
- Database tidak terbuka secara tidak perlu.
- Backup aktif.
- Monitoring tersedia.
- Health check lulus.
- Smoke test lulus.
- UAT disetujui.
- SOP operasional tersedia.
- Rencana rollback dan recovery terdokumentasi.

---

# 24. TECHNICAL RISKS

| Risiko                               | Dampak                      | Mitigasi                                   |
| ------------------------------------ | --------------------------- | ------------------------------------------ |
| Kesalahan perhitungan pembayaran     | Kerugian keuangan           | Decimal, transaksi atomik, invariant tests |
| Race condition                       | Data tidak konsisten        | Locking dan optimistic concurrency         |
| Session hijacking                    | Akses tidak sah             | Cookie aman, rotasi, expiry                |
| Token tracking bocor                 | Data pelanggan terbuka      | Token acak, data minimum, revocation       |
| API publik disalahgunakan            | Spam dan beban server       | Rate limiting dan abuse controls           |
| Koneksi tidak stabil                 | Transaksi gagal             | Retry aman dan idempotency                 |
| Migration bermasalah                 | Gangguan aplikasi           | Review, backup, rollback plan              |
| Perbedaan perhitungan FE/BE          | Tagihan tidak sinkron       | Backend sebagai sumber kebenaran           |
| Query lambat                         | Pengalaman pengguna menurun | Index, pagination, profiling               |
| Infrastruktur terlalu kompleks       | Biaya meningkat             | Modular monolith dan dependency minimal    |
| Backup tidak dapat dipulihkan        | Kehilangan data             | Restore testing                            |
| Perubahan requirements tanpa kontrol | Rework                      | Versioning dokumen dan change request      |

---

# 25. KEPUTUSAN TEKNIS YANG PERLU DIFINALISASI

| ID       | Keputusan        | Rekomendasi Awal                                |
| -------- | ---------------- | ----------------------------------------------- |
| T-DEC-01 | Topologi hosting | Satu origin dengan reverse proxy                |
| T-DEC-02 | Database         | PostgreSQL 17                                   |
| T-DEC-03 | ORM              | SQLAlchemy 2.x                                  |
| T-DEC-04 | Session          | Server-side session cookie                      |
| T-DEC-05 | CSRF             | Token + Origin validation                       |
| T-DEC-06 | Berat cucian     | Decimal dengan presisi bisnis terkonfigurasi    |
| T-DEC-07 | Money storage    | BIGINT Rupiah                                   |
| T-DEC-08 | Tracking token   | Random 256-bit, hashed storage                  |
| T-DEC-09 | Token expiry     | Usulan 90 hari setelah penyelesaian             |
| T-DEC-10 | Polling tracking | Maksimal sekali per 60 detik pada halaman aktif |
| T-DEC-11 | WhatsApp         | Manual via deep link                            |
| T-DEC-12 | PDF              | Server-generated                                |
| T-DEC-13 | Offline mode     | Tidak termasuk MVP                              |
| T-DEC-14 | Refund workflow  | Menunggu keputusan SOP bisnis                   |
| T-DEC-15 | Hosting provider | Belum ditetapkan                                |
| T-DEC-16 | RPO/RTO          | Usulan RPO 24 jam, RTO 4 jam                    |
| T-DEC-17 | Multi-tenancy    | Tidak termasuk MVP                              |
| T-DEC-18 | Domain final     | Belum ditetapkan                                |

Keputusan yang masih berupa usulan tidak boleh dianggap final sebelum review dan persetujuan.

---

# 26. REFERENSI TEKNIS

Dokumentasi resmi yang menjadi acuan:

1. React — https://react.dev/
2. TypeScript — https://www.typescriptlang.org/docs/
3. Vite — https://vite.dev/
4. Tailwind CSS — https://tailwindcss.com/docs
5. FastAPI — https://fastapi.tiangolo.com/
6. Pydantic — https://docs.pydantic.dev/
7. SQLAlchemy — https://docs.sqlalchemy.org/
8. Alembic — https://alembic.sqlalchemy.org/
9. PostgreSQL — https://www.postgresql.org/docs/
10. OWASP ASVS — https://asvs.owasp.org/
11. OWASP Cheat Sheet Series — https://cheatsheetseries.owasp.org/
12. WCAG 2.2 — https://www.w3.org/TR/WCAG22/
13. Playwright — https://playwright.dev/
14. Pytest — https://docs.pytest.org/
15. OpenAPI Specification — https://spec.openapis.org/oas/latest.html

Versi library dan standar dikunci berdasarkan compatibility review pada milestone M0.

---

# 27. KESIMPULAN

Technical Requirements Document v1.0 menetapkan rancangan teknis awal untuk implementasi Web App Manajemen Laundry UMKM berdasarkan PRD v1.0.

Sistem menggunakan arsitektur Modular Monolith dengan frontend React dan TypeScript, backend FastAPI, serta database PostgreSQL.

Rancangan ini memprioritaskan:

1. Kesederhanaan pengembangan dan operasional.
2. Efisiensi biaya.
3. Penggunaan melalui smartphone.
4. Konsistensi transaksi dan keuangan.
5. Keamanan autentikasi dan hak akses.
6. Tracking pelanggan tanpa login.
7. Pembayaran dan WhatsApp secara manual.
8. Pengujian yang terukur.
9. Deployment serta backup yang dapat dipelihara.
10. Kemampuan pengembangan bertahap.

Dokumen TRD ini menjadi pedoman teknis utama untuk penyusunan Architecture & Flow Design, Database Design Document, kontrak OpenAPI, UI/UX Specification, dan implementasi sistem.

**Status akhir: TRD v1.0 — DRAFT FOR TECHNICAL REVIEW.**

Dokumen belum menyatakan bahwa sistem sudah dikembangkan atau seluruh pilihan teknologi telah diuji. Persetujuan teknis dilakukan setelah keputusan terbuka, keselarasan dengan PRD, dan rancangan database diperiksa.

---

**AKHIR DOKUMEN — TECHNICAL REQUIREMENTS DOCUMENT v1.0**
