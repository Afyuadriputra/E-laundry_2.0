
# IMPLEMENTATION PLAN DOCUMENTATION (IPD)

## WEB APP MANAJEMEN LAUNDRY UMKM

**Versi:** 1.0
**Tanggal:** 3 November 2026
**Status:** DRAFT — IMPLEMENTATION PLANNING
**Dokumen Acuan:** PRD v1.0, TRD v1.0, AFD v1.0, DBD v1.0, BSD v1.0
**Metode:** Milestone-Based Incremental Development
**Arsitektur:** Modular Monolith — REST API
**Lingkup:** Minimum Viable Product (MVP)
**Platform:** Mobile-First Web Application / PWA
**Target Implementasi:** Satu usaha laundry, satu lokasi operasional

---

# 1. PENDAHULUAN

## 1.1 Latar Belakang

Web App Manajemen Laundry UMKM dirancang sebagai solusi digitalisasi usaha laundry skala kecil dan menengah.

Aplikasi mendukung pengelolaan pesanan, pelanggan, proses pencucian, pembayaran manual, nota digital, penjemputan, pengantaran, laporan usaha, dan tracking cucian tanpa login pelanggan.

Lima dokumen sebelumnya telah memberikan dasar pengembangan:

1. PRD menentukan kebutuhan bisnis.
2. TRD menentukan persyaratan teknis.
3. AFD menentukan alur dan proses aplikasi.
4. DBD menentukan arah desain UI/UX.
5. BSD menentukan struktur backend, skema data, dan kontrak API.

Implementation Plan Documentation (IPD) menjadi dokumen yang menerjemahkan seluruh rancangan tersebut menjadi pekerjaan implementasi yang terukur.

## 1.2 Tujuan IPD

IPD bertujuan:

1. Menentukan urutan pengembangan.
2. Membagi pekerjaan berdasarkan milestone.
3. Mendefinisikan tugas frontend, backend, database, integrasi, dan QA.
4. Menentukan dependensi antartugas.
5. Menentukan deliverable setiap milestone.
6. Menetapkan kriteria keberhasilan.
7. Mencegah implementasi fitur yang belum dirancang.
8. Memastikan konsistensi antar dokumen.
9. Menentukan proses pengujian dan audit.
10. Menentukan kesiapan deployment produksi.

## 1.3 Hasil Akhir yang Diharapkan

Hasil akhir berupa aplikasi laundry yang dapat digunakan melalui HP maupun laptop untuk:

- Membuat dan mengelola pesanan.
- Mengelola data pelanggan.
- Mengatur layanan dan harga.
- Mengubah status pengerjaan.
- Mencatat pembayaran manual.
- Membuat nota digital.
- Membagikan informasi melalui WhatsApp manual.
- Menerima permintaan penjemputan tanpa login.
- Mengelola tugas kurir.
- Menampilkan tracking tanpa login.
- Memantau pendapatan, pengeluaran, dan tagihan.
- Mengatur akun serta hak akses petugas.

Aplikasi harus dapat dijalankan tanpa perangkat kasir fisik, printer nota, scanner barcode, payment gateway, atau GPS khusus.

---

# 2. BASELINE DAN BATASAN PROYEK

## 2.1 Dokumen Sumber

| Dokumen                    | Versi | Status         |
| -------------------------- | ----- | -------------- |
| PRD                        | 1.0   | Draft tersedia |
| TRD                        | 1.0   | Draft tersedia |
| AFD                        | 1.0   | Draft tersedia |
| DBD — Design Brief        | 1.0   | Draft tersedia |
| BSD — Backend Schema      | 1.0   | Draft tersedia |
| IPD — Implementation Plan | 1.0   | Dokumen ini    |

Semua dokumen masih memerlukan review sebelum ditetapkan sebagai baseline yang disetujui.

## 2.2 Keputusan Produk yang Dipertahankan

1. Sistem berbasis web.
2. Mobile-first.
3. Mendukung desktop.
4. Pelanggan tidak perlu login.
5. Pembayaran dilakukan manual.
6. Tidak menggunakan payment gateway.
7. WhatsApp melalui tautan pesan siap kirim.
8. Tidak menggunakan GPS real-time.
9. Tidak mewajibkan printer nota.
10. Tidak mewajibkan perangkat POS.
11. MVP untuk satu usaha.
12. Fitur dikembangkan bertahap.
13. Status cucian dan pembayaran disimpan terpisah.
14. Backend menjadi sumber kebenaran transaksi.
15. Data pelanggan dilindungi dengan pembatasan hak akses.

## 2.3 Out of Scope

Tidak termasuk MVP:

- SaaS multi-tenant.
- Multi-cabang.
- Membership.
- Loyalty points.
- Payment gateway.
- WhatsApp bot otomatis.
- GPS kurir.
- Sistem akuntansi penuh.
- AI prediction.
- Integrasi IoT.
- Offline transaction synchronization.
- Aplikasi mobile native.

Penambahan fitur di luar lingkup harus melalui proses perubahan kebutuhan.

---

# 3. STRATEGI IMPLEMENTASI

## 3.1 Pendekatan Pengembangan

Menggunakan pendekatan:

**Incremental Development**

Sistem dikembangkan secara bertahap sehingga hasil setiap milestone dapat diuji.

**Vertical Slice Development**

Satu fitur dikerjakan sampai mencakup backend, database, frontend, dan pengujian, bukan sekadar membuat tampilan terlebih dahulu.

**Contract-First API**

Frontend dan backend mengikuti skema request/response yang disepakati.

**Test-Driven Risk Management**

Komponen berisiko tinggi seperti pembayaran, autentikasi, tracking publik, dan concurrency mendapatkan pengujian lebih mendalam.

**Milestone Acceptance Gate**

Milestone berikutnya dimulai setelah dependensi dan kriteria penerimaan yang relevan terpenuhi.

## 3.2 Prinsip Pengembangan

1. Correctness before optimization.
2. Security by design.
3. Single source of truth.
4. Separation of concerns.
5. SOLID.
6. KISS.
7. Reusable components.
8. Transactional consistency.
9. Explicit validation.
10. Auditability.
11. Automated testing.
12. Documentation-driven implementation.

## 3.3 Aturan Pelaksanaan

- Tidak mengimplementasikan aturan bisnis berdasarkan asumsi yang belum disetujui.
- Tidak menyatakan fitur PASS hanya karena tampilannya sudah selesai.
- Tidak membuat endpoint tanpa validasi dan authorization.
- Tidak menyimpan uang menggunakan floating-point.
- Tidak menganggap pembayaran berhasil tanpa verifikasi petugas.
- Tidak menganggap pesan WhatsApp terkirim secara otomatis.
- Tidak membuka data pelanggan tanpa autentikasi atau token yang sah.
- Tidak melakukan deployment produksi sebelum pengujian kritis lulus.

---

# 4. TECHNOLOGY IMPLEMENTATION BASELINE

## 4.1 Frontend

| Komponen   | Teknologi                                 |
| ---------- | ----------------------------------------- |
| Framework  | React 19                                  |
| Language   | TypeScript                                |
| Build Tool | Vite                                      |
| Styling    | Tailwind CSS 4                            |
| UI Library | shadcn/ui + Radix UI                      |
| Routing    | React Router                              |
| Form       | React Hook Form                           |
| Validation | Zod                                       |
| API State  | TanStack Query                            |
| Icons      | Lucide React                              |
| Animation  | Motion bila diperlukan                    |
| Testing    | Vitest, React Testing Library, Playwright |

## 4.2 Backend

| Komponen   | Teknologi         |
| ---------- | ----------------- |
| Language   | Python 3.12       |
| Framework  | FastAPI           |
| Schema     | Pydantic v2       |
| ORM        | SQLAlchemy 2.x    |
| Migration  | Alembic           |
| Driver     | Psycopg 3         |
| Database   | PostgreSQL 17     |
| Server     | Uvicorn           |
| Test       | Pytest + HTTPX    |
| Lint       | Ruff              |
| Type Check | Pyright atau Mypy |

## 4.3 Infrastructure

Rekomendasi:

- Monorepo.
- Docker untuk environment yang membutuhkan konsistensi.
- PostgreSQL.
- HTTPS reverse proxy.
- Production database terpisah.
- Automated backup.
- Structured logging.
- CI/CD.

Redis, Kubernetes, message broker, dan microservices tidak menjadi persyaratan MVP.

## 4.4 Version Locking

Versi paket yang kompatibel harus diverifikasi pada M0.

Ketentuan:

- Lockfile frontend wajib tersedia.
- Dependensi backend dipin.
- Build harus reproducible.
- Pembaruan dependency harus melewati test.
- Tidak menggunakan versi `latest` tanpa kontrol pada produksi.

---

# 5. STRUKTUR REPOSITORY

## 5.1 Monorepo

Struktur target:

**laundry-umkm/**

- `apps/web/`
- `apps/api/`
- `docs/`
- `infra/`
- `scripts/`
- `.github/workflows/`
- `README.md`
- `.gitignore`
- `.editorconfig`

## 5.2 Frontend Structure

**apps/web/src/**

- `app/`
- `features/auth/`
- `features/dashboard/`
- `features/orders/`
- `features/customers/`
- `features/payments/`
- `features/expenses/`
- `features/pickup-delivery/`
- `features/invoices/`
- `features/tracking/`
- `features/settings/`
- `components/ui/`
- `components/shared/`
- `lib/api/`
- `lib/utils/`
- `hooks/`
- `styles/`
- `types/`
- `tests/`

## 5.3 Backend Structure

**apps/api/app/**

- `main.py`
- `core/`
- `db/`
- `middleware/`
- `shared/`
- `modules/auth/`
- `modules/users/`
- `modules/businesses/`
- `modules/services/`
- `modules/customers/`
- `modules/orders/`
- `modules/payments/`
- `modules/expenses/`
- `modules/pickup_delivery/`
- `modules/invoices/`
- `modules/tracking/`
- `modules/dashboard/`
- `modules/reports/`
- `modules/audit/`

## 5.4 Backend Module Files

Setiap modul dapat berisi:

- `router.py`
- `schemas.py`
- `models.py`
- `repository.py`
- `service.py`
- `domain.py`
- `permissions.py`
- `constants.py`

Struktur di atas adalah target rancangan, bukan daftar file yang sudah dibuat.

---

# 6. WORKSTREAM DAN TANGGUNG JAWAB

## 6.1 Workstream

| Kode | Workstream         | Tanggung Jawab                            |
| ---- | ------------------ | ----------------------------------------- |
| PM   | Project Management | Scope, backlog, keputusan, dan acceptance |
| DOC  | Documentation      | Spesifikasi dan traceability              |
| UX   | UI/UX              | Wireframe, design system, prototype       |
| FE   | Frontend           | React, routing, form, dan UI              |
| BE   | Backend            | FastAPI, service, API, dan domain         |
| DB   | Database           | Schema, migration, integrity              |
| INT  | Integration        | Kontrak dan integrasi frontend-backend    |
| QA   | Quality Assurance  | Testing dan audit                         |
| SEC  | Security           | Authentication, authorization, privacy    |
| OPS  | DevOps             | CI/CD, hosting, backup, monitoring        |

Pada tim kecil, satu orang dapat mengerjakan beberapa workstream. Pemisahan ini merupakan pemisahan tanggung jawab, bukan kewajiban mempekerjakan banyak orang.

## 6.2 Ownership

Setiap task harus mempunyai:

- Task ID.
- Judul.
- Workstream.
- Prioritas.
- Dependensi.
- Acceptance Criteria.
- Status.
- Bukti hasil.
- Reviewer.

Task tanpa acceptance criteria dianggap belum siap dikerjakan.

---

# 7. SISTEM PRIORITAS DAN STATUS

## 7.1 Prioritas

**P0 — Critical MVP**

Wajib untuk operasional dan keamanan.

**P1 — Enhancement**

Penting, tetapi dapat ditunda setelah MVP.

**P2 — Future**

Fitur lanjutan.

## 7.2 Status Task

| Status      | Makna                                               |
| ----------- | --------------------------------------------------- |
| NOT_STARTED | Belum dikerjakan                                    |
| IN_PROGRESS | Sedang dikerjakan                                   |
| IMPLEMENTED | Kode selesai, belum seluruh pengujian               |
| TESTED      | Pengujian telah dijalankan                          |
| PASS        | Seluruh acceptance criteria terpenuhi               |
| PARTIAL     | Sebagian kriteria terpenuhi                         |
| BLOCKED     | Tidak dapat dilanjutkan karena dependensi/keputusan |
| FAILED      | Pengujian atau acceptance tidak lulus               |

## 7.3 Aturan Status PASS

Task hanya PASS apabila:

1. Implementasi tersedia.
2. Validasi berjalan.
3. Test relevan dijalankan.
4. Tidak ada bug kritis terkait.
5. Acceptance criteria dipenuhi.
6. Bukti hasil tersedia.

Hasil dokumentasi atau mockup tidak boleh diklaim sebagai implementasi produksi.

---

# 8. MASTER MILESTONE PLAN

| Milestone | Nama                           | Fokus                                   |
| --------- | ------------------------------ | --------------------------------------- |
| M0        | Project Foundation             | Repository, arsitektur, dokumentasi, CI |
| M1        | Authentication & Configuration | Login, RBAC, business settings          |
| M2        | Core Laundry Operations        | Pelanggan, layanan, pesanan, status     |
| M3        | Finance & Invoices             | Pembayaran, pengeluaran, nota           |
| M4        | Public Tracking                | Tracking tanpa login                    |
| M5        | Pickup & Delivery              | Penjemputan dan pengantaran             |
| M6        | Dashboard & Reporting          | Monitoring dan laporan                  |
| M7        | Quality & Security Hardening   | Full testing, security, performance     |
| M8        | Production Deployment          | Go-live dan verifikasi                  |

Urutan ini menjadi baseline utama.

Desain UI/UX berjalan paralel sesuai kesiapan fitur.

Durasi setiap milestone ditetapkan setelah kapasitas pengembang dan kompleksitas teknis diverifikasi. IPD tidak menetapkan tanggal penyelesaian yang belum memiliki dasar estimasi.

---

# 9. M0 — PROJECT FOUNDATION

## 9.1 Objective

Membangun fondasi teknis dan organisasi proyek sebelum implementasi domain bisnis.

## 9.2 Task Breakdown

| Task ID | Workstream | Task                                            | Deliverable                     |
| ------- | ---------- | ----------------------------------------------- | ------------------------------- |
| M0-01   | PM/DOC     | Audit konsistensi PRD, TRD, AFD, DBD, BSD       | Requirements consistency report |
| M0-02   | PM         | Finalisasi keputusan P0 yang memengaruhi coding | Decision register               |
| M0-03   | BE/FE      | Inisialisasi monorepo                           | Repository structure            |
| M0-04   | BE         | Setup FastAPI                                   | API skeleton                    |
| M0-05   | FE         | Setup React + TypeScript + Vite                 | Frontend skeleton               |
| M0-06   | DB         | Setup PostgreSQL dan Alembic                    | Database foundation             |
| M0-07   | BE/OPS     | Konfigurasi environment dan secrets             | Config module dan .env.example  |
| M0-08   | BE         | Structured logging dan error response           | Core middleware                 |
| M0-09   | BE         | Health endpoints                                | Health API                      |
| M0-10   | QA/OPS     | CI baseline dan smoke tests                     | Pipeline awal                   |
| M0-11   | DOC/BE     | Baseline OpenAPI dan error convention           | API contract draft              |
| M0-12   | SEC        | Security threat review awal                     | Threat model ringkas            |

## 9.3 Detail Implementasi

### M0-01 — Dokumentasi dan Konsistensi

Lakukan pemeriksaan terhadap:

- Requirement ID.
- Modul.
- Role.
- Business rules.
- Alur status.
- API.
- Entity database.
- Acceptance criteria.

Hasil berupa matriks keterlacakan dan daftar konflik atau keputusan yang belum final.

### M0-02 — Decision Register

Keputusan yang perlu ditetapkan sebelum kode terkait dibuat:

1. Pembulatan berat.
2. Berat minimum.
3. Penomoran pesanan.
4. Kebijakan harga pickup dan delivery.
5. Aturan pembayaran saat serah terima.
6. Refund dan pembatalan setelah pembayaran.
7. Masa berlaku token tracking.
8. Retensi data.
9. Zona waktu usaha.

Keputusan yang belum final harus mempunyai owner, status, serta milestone batas penyelesaiannya.

### M0-03 sampai M0-06 — Initial Setup

Implementasikan:

- Struktur monorepo.
- Frontend yang dapat dijalankan.
- Backend yang dapat dijalankan.
- Database lokal.
- Alembic.
- Environment configuration.
- Database connection test.

### M0-07 sampai M0-10 — Engineering Foundation

Implementasikan:

- Config loading.
- Error schema.
- Request ID.
- Logging.
- Health checks.
- Lint.
- Typecheck.
- Unit test baseline.
- CI.

## 9.4 Acceptance Gate M0

M0 dinyatakan PASS jika:

1. Repository dapat dijalankan dari clean checkout.
2. Frontend development server berjalan.
3. Backend development server berjalan.
4. PostgreSQL terkoneksi.
5. Migration awal dapat dijalankan.
6. Health endpoint berhasil.
7. Lint dan typecheck baseline lulus.
8. CI berhasil.
9. Tidak ada secret dalam repository.
10. Keputusan kritis yang menghalangi M1 telah diselesaikan.
11. OpenAPI baseline tersedia.
12. Dokumentasi setup tersedia.

**Output:** FOUNDATION_READY.

---

# 10. M1 — AUTHENTICATION & BUSINESS CONFIGURATION

## 10.1 Objective

Menyediakan autentikasi dan konfigurasi usaha yang aman.

## 10.2 Task Breakdown

| Task ID | Workstream | Task                                       | Deliverable          |
| ------- | ---------- | ------------------------------------------ | -------------------- |
| M1-01   | DB         | Migration businesses dan business_settings | Core business schema |
| M1-02   | DB         | Migration users dan user_sessions          | Auth schema          |
| M1-03   | BE         | Password hashing Argon2id                  | Credential service   |
| M1-04   | BE/SEC     | Session creation, validation, revocation   | Auth service         |
| M1-05   | BE/SEC     | CSRF dan login throttling                  | Security controls    |
| M1-06   | BE         | RBAC dan permission dependencies           | Authorization module |
| M1-07   | BE         | Auth, users, business, settings API        | Protected endpoints  |
| M1-08   | FE/UX      | Login dan authenticated app shell          | Login UI, navigation |
| M1-09   | FE/INT     | Integrasi login, session, role             | Auth frontend        |
| M1-10   | QA/SEC     | Auth, CSRF, RBAC, session tests            | Security test report |
| M1-11   | BE/FE      | Owner-managed staff accounts               | User management      |
| M1-12   | QA         | End-to-end login dan logout                | E2E evidence         |

## 10.3 Backend Deliverables

Endpoint utama:

- GET `/auth/csrf`
- POST `/auth/login`
- POST `/auth/logout`
- GET `/auth/me`
- POST `/auth/change-password`
- GET `/users`
- POST `/users`
- PATCH `/users/{id}`
- POST `/users/{id}/deactivate`
- GET/PATCH `/business`
- GET/PATCH `/settings`

Seluruh path berada di bawah `/api/v1`.

## 10.4 Security Requirements

- Password menggunakan Argon2id.
- Session menggunakan cookie HttpOnly dan Secure pada produksi.
- CSRF protection untuk operasi relevan.
- Rate limiting login.
- Session expiration.
- Session revocation.
- Account deactivation.
- Backend permission enforcement.

## 10.5 Frontend Deliverables

- Login page.
- Protected routes.
- Auth state.
- Role-based navigation.
- Loading auth state.
- Unauthorized page.
- Session expired handling.
- Logout.

## 10.6 Acceptance Gate M1

1. Login valid berhasil.
2. Login invalid ditolak.
3. Akun nonaktif ditolak.
4. Session expiry bekerja.
5. Logout mencabut sesi.
6. CSRF test lulus.
7. Backend menolak akses tanpa permission.
8. Owner dapat membuat akun petugas.
9. Menu menyesuaikan role.
10. Test otomatis lulus.

**Output:** AUTH_RBAC_READY.

---

# 11. M2 — CORE LAUNDRY OPERATIONS

## 11.1 Objective

Membuat sistem inti pencatatan dan pemrosesan cucian.

## 11.2 Task Breakdown

| Task ID | Workstream | Task                                  | Deliverable             |
| ------- | ---------- | ------------------------------------- | ----------------------- |
| M2-01   | DB         | Migration customers dan services      | Customer/service schema |
| M2-02   | DB         | Migration orders dan order_items      | Order schema            |
| M2-03   | DB         | Migration status history dan handoffs | Lifecycle schema        |
| M2-04   | BE         | Customer CRUD dan normalisasi nomor   | Customer service        |
| M2-05   | BE         | Service catalog dan snapshot harga    | Service module          |
| M2-06   | BE         | Pricing Engine menggunakan Decimal    | Pricing domain          |
| M2-07   | BE         | Order creation transaction            | Order service           |
| M2-08   | BE         | Order list, detail, update, cancel    | Order APIs              |
| M2-09   | BE         | Laundry state machine dan histori     | Workflow service        |
| M2-10   | FE/UX      | Halaman pelanggan dan layanan         | Customer/service UI     |
| M2-11   | FE/UX      | Form buat pesanan dan detail          | Order UI                |
| M2-12   | FE/INT     | Integrasi order dan perubahan status  | Functional flow         |
| M2-13   | BE/QA      | Optimistic locking dan idempotency    | Concurrency safety      |
| M2-14   | QA         | Unit, integration, E2E tests          | M2 test report          |

## 11.3 Pricing Implementation

Backend menghitung harga menggunakan:

- Harga layanan aktif.
- Kuantitas valid.
- Aturan satuan.
- Aturan pembulatan.
- Biaya tambahan.
- Biaya antar-jemput jika berlaku.

Harga dan nama layanan disimpan sebagai snapshot pada `order_items`.

Frontend hanya menampilkan pratinjau.

Server tetap menghitung ulang sebelum transaksi disimpan.

## 11.4 Order Transaction

Operasi create order meliputi:

1. Validasi pelanggan.
2. Validasi layanan.
3. Perhitungan harga.
4. Pembuatan nomor pesanan.
5. Penyimpanan order.
6. Penyimpanan item.
7. Penyimpanan status awal.
8. Pencatatan audit jika relevan.
9. Commit transaksi.

Jika gagal, transaksi harus rollback.

## 11.5 State Machine

Status minimum:

RECEIVED → QUEUED → WASHING → DRYING → IRONING/QC_PACKING → READY → COMPLETED.

Transisi tidak relevan dapat dilewati sesuai aturan layanan.

Status CANCELLED memerlukan alur pembatalan yang sah.

## 11.6 Frontend Deliverables

- Daftar pelanggan.
- Form pelanggan.
- Daftar layanan.
- Buat pesanan.
- Pencarian pelanggan.
- Input layanan multi-item.
- Ringkasan harga.
- Detail pesanan.
- Status timeline.
- Update status.
- Riwayat perubahan.
- Error dan conflict handling.

## 11.7 Acceptance Gate M2

1. Pelanggan dapat dibuat.
2. Duplikasi kontak diberi peringatan.
3. Layanan dapat dikonfigurasi Owner.
4. Pesanan single-service berhasil.
5. Pesanan multi-service berhasil.
6. Perhitungan Rupiah benar.
7. Snapshot harga tidak berubah.
8. Order creation atomik.
9. Nomor pesanan unik.
10. Retry tidak membuat pesanan ganda.
11. State transition valid berhasil.
12. Transisi invalid ditolak.
13. Status history tersedia.
14. Konflik versi ditangani.
15. Alur mobile lulus E2E.

**Output:** CORE_LAUNDRY_READY.

---

# 12. M3 — FINANCE & DIGITAL INVOICES

## 12.1 Objective

Membuat pencatatan pembayaran manual yang aman dan nota digital.

## 12.2 Task Breakdown

| Task ID | Workstream | Task                                        | Deliverable              |
| ------- | ---------- | ------------------------------------------- | ------------------------ |
| M3-01   | DB         | Migration payments, payment_voids, expenses | Finance schema           |
| M3-02   | BE         | Payment domain dan balance calculation      | Payment service          |
| M3-03   | BE         | Manual payment API                          | Record payment           |
| M3-04   | BE         | Payment void dan audit                      | Correction service       |
| M3-05   | BE/DB      | Row locking dan idempotency                 | Transaction safety       |
| M3-06   | BE         | Expense CRUD                                | Expense module           |
| M3-07   | BE         | Invoice data mapper                         | Invoice read model       |
| M3-08   | BE         | PDF generator                               | PDF invoice              |
| M3-09   | BE/FE      | WhatsApp message preview                    | Manual share integration |
| M3-10   | FE         | Payment form, history, outstanding          | Finance UI               |
| M3-11   | FE         | Invoice preview dan download                | Nota UI                  |
| M3-12   | QA         | Financial, concurrency, PDF, E2E tests      | M3 evidence              |

## 12.3 Payment Implementation

Metode:

- CASH.
- BANK_TRANSFER.
- QRIS_MANUAL.

Pembayaran dianggap terverifikasi hanya setelah petugas memeriksa penerimaan dana.

## 12.4 Financial Invariants

1. Total tagihan tidak negatif.
2. Nominal pembayaran lebih besar dari nol.
3. Total pembayaran sah tidak melebihi tagihan.
4. Sisa tagihan tidak negatif.
5. Void tidak menghapus pembayaran asli.
6. Payment status berasal dari transaksi yang sah.
7. Retry pembayaran tidak membuat duplikasi.
8. Koreksi total pesanan mengikuti aturan finansial.

## 12.5 Concurrency

Pengujian wajib:

- Dua kasir mencatat pembayaran bersamaan.
- Pembayaran bersamaan dengan void.
- Perubahan total bersamaan dengan pembayaran.
- Request pembayaran dikirim ulang.
- Dua permintaan void untuk transaksi sama.

## 12.6 Invoice

Nota wajib menampilkan:

- Profil laundry.
- Nomor pesanan.
- Pelanggan.
- Layanan.
- Harga.
- Total.
- Pembayaran.
- Sisa tagihan.
- Estimasi selesai.
- Tracking link.

Nota dapat dibuka dalam halaman web atau disimpan sebagai PDF.

## 12.7 WhatsApp Manual

Implementasi:

- Normalisasi nomor.
- Template pesan.
- URL encoding.
- Tombol buka WhatsApp.
- Fallback salin pesan.

Tidak menggunakan WhatsApp API.

## 12.8 Acceptance Gate M3

1. Tunai berhasil dicatat.
2. Transfer manual berhasil dicatat.
3. QRIS manual berhasil dicatat.
4. DP dihitung benar.
5. Pelunasan dihitung benar.
6. Payment void berhasil dan memiliki audit.
7. Tidak ada overpayment.
8. Tidak ada duplicate payment.
9. Riwayat keuangan konsisten.
10. Pengeluaran tercatat.
11. Nota PDF dapat diunduh.
12. WhatsApp preview benar.
13. Sistem tidak mengklaim WhatsApp terkirim otomatis.
14. Semua financial critical tests lulus.

**Output:** FINANCE_INVOICE_READY.

---

# 13. M4 — PUBLIC TRACKING

## 13.1 Objective

Menyediakan halaman tracking pelanggan yang aman tanpa login.

## 13.2 Task Breakdown

| Task ID | Workstream | Task                                        | Deliverable            |
| ------- | ---------- | ------------------------------------------- | ---------------------- |
| M4-01   | DB         | Migration tracking_tokens                   | Tracking schema        |
| M4-02   | BE/SEC     | Secure token generation dan hashing         | Token service          |
| M4-03   | BE         | Public tracking read models                 | Restricted schema      |
| M4-04   | BE         | Token validation dan resource authorization | Public API             |
| M4-05   | BE/SEC     | Token rotation/revocation                   | Token lifecycle        |
| M4-06   | FE/UX      | Tracking page dan status timeline           | Public UI              |
| M4-07   | FE/INT     | Integrasi live status via polling/refresh   | Tracking functionality |
| M4-08   | SEC        | Headers, log redaction, rate limits         | Public protection      |
| M4-09   | QA         | Token, privacy, E2E, abuse tests            | M4 test report         |

## 13.3 Tracking Token Rules

- Dibuat menggunakan random generator kriptografis.
- Direkomendasikan 256-bit.
- URL-safe.
- Disimpan sebagai hash di database.
- Memiliki expiry.
- Dapat dicabut.
- Tidak dicatat pada log.
- Tidak boleh memperlihatkan pesanan lain.

## 13.4 Public Data Scope

Yang boleh tampil:

- Nomor pesanan.
- Layanan.
- Berat/jumlah.
- Timeline.
- Estimasi selesai.
- Status antar-jemput.
- Ringkasan tagihan.
- Kontak usaha.

Yang tidak boleh tampil:

- Alamat pelanggan lengkap.
- Nomor WhatsApp pelanggan lengkap.
- Catatan internal.
- Data karyawan.
- Audit internal.
- Data pesanan lain.
- Informasi kredensial.

## 13.5 Frontend Deliverables

- Public tracking layout.
- Laundry timeline.
- Pickup status.
- Delivery status.
- Payment summary.
- Invoice access.
- Last updated indicator.
- Refresh button.
- Expired/invalid link state.
- WhatsApp contact.

## 13.6 Acceptance Gate M4

1. Token valid membuka resource yang benar.
2. Tidak memerlukan login.
3. Token invalid ditolak.
4. Token dicabut tidak berfungsi.
5. Token kedaluwarsa ditolak.
6. Data pelanggan lain tidak bocor.
7. Status terbaru dapat dibaca.
8. Invoice publik dibatasi.
9. Rate limiting bekerja.
10. Token tidak muncul pada log sensitif.
11. Halaman mobile responsif.
12. Security tests lulus.

**Output:** PUBLIC_TRACKING_READY.

---

# 14. M5 — PICKUP & DELIVERY

## 14.1 Objective

Mengimplementasikan alur antar-jemput cucian tanpa GPS dan tanpa login pelanggan.

## 14.2 Task Breakdown

| Task ID | Workstream | Task                                        | Deliverable             |
| ------- | ---------- | ------------------------------------------- | ----------------------- |
| M5-01   | DB         | Migration pickup_requests                   | Pickup schema           |
| M5-02   | DB         | Migration delivery_tasks dan history        | Courier schema          |
| M5-03   | BE         | Public pickup submission                    | Pickup API              |
| M5-04   | BE         | Pickup confirmation dan rejection           | Admin service           |
| M5-05   | BE         | Courier assignment                          | Task management         |
| M5-06   | BE         | Pickup state machine                        | Pickup workflow         |
| M5-07   | BE         | Pickup-to-order conversion                  | Atomic business service |
| M5-08   | BE         | Delivery task dan status transitions        | Delivery workflow       |
| M5-09   | BE         | Handoff/completion integration              | Order completion        |
| M5-10   | FE/UX      | Form pickup publik dan konfirmasi           | Public pickup UI        |
| M5-11   | FE/UX      | Admin pickup dan dashboard kurir            | Internal logistics UI   |
| M5-12   | INT        | Hubungkan pickup, order, tracking, delivery | Integrated workflow     |
| M5-13   | QA         | E2E, concurrency, authorization tests       | M5 evidence             |

## 14.3 Pickup Flow

1. Pelanggan membuka formulir.
2. Pelanggan mengisi data.
3. Backend menyimpan pickup request.
4. Pelanggan menerima tautan tracking melalui hasil pengajuan yang aman.
5. Admin mengonfirmasi jadwal.
6. Admin menugaskan kurir.
7. Kurir menjemput.
8. Cucian tiba di laundry.
9. Kasir menimbang.
10. Kasir membuat order dari permintaan.
11. Tracking tetap berfungsi.

## 14.4 Pickup-to-Order Requirements

Operasi harus atomik.

Persyaratan:

- Pickup memiliki status yang sah.
- Belum pernah dikonversi.
- Berat dan layanan valid.
- Nomor order unik.
- Relasi pickup-order disimpan.
- Token tracking tetap memiliki cakupan yang benar.
- Retry tidak menghasilkan order kedua.

## 14.5 Delivery Flow

1. Order READY.
2. Admin menjadwalkan pengantaran.
3. Kurir menerima tugas.
4. Kurir menuju pelanggan.
5. Kurir menyerahkan cucian.
6. Kurir mengonfirmasi penerimaan.
7. Backend mencatat handoff.
8. Order menjadi COMPLETED jika syarat terpenuhi.

## 14.6 Failed Delivery

Jika gagal:

- Task diberi status FAILED.
- Alasan wajib.
- Order tidak menjadi COMPLETED.
- Admin dapat menjadwalkan ulang.
- Histori tetap tersedia.

## 14.7 Acceptance Gate M5

1. Form pickup tanpa login berhasil.
2. Request tersimpan.
3. Jadwal tidak otomatis dianggap dikonfirmasi.
4. Admin dapat konfirmasi/tolak.
5. Kurir menerima tugas yang ditugaskan.
6. Kurir dapat memperbarui status.
7. Pickup tiba dapat dikonversi.
8. Konversi tidak duplikat.
9. Tracking menampilkan status terkait.
10. Delivery berhasil dicatat.
11. Handoff final tersedia.
12. Delivery gagal dapat dijadwalkan ulang.
13. Completed tidak terjadi tanpa handoff.
14. Pembayaran tetap independen.
15. Semua tes kritis lulus.

**Output:** PICKUP_DELIVERY_READY.

---

# 15. M6 — DASHBOARD & REPORTING

## 15.1 Objective

Menyediakan ringkasan operasional dan keuangan yang konsisten dengan data transaksi.

## 15.2 Task Breakdown

| Task ID | Workstream | Task                                 | Deliverable    |
| ------- | ---------- | ------------------------------------ | -------------- |
| M6-01   | BE         | Dashboard aggregation service        | Summary API    |
| M6-02   | BE         | Overdue calculation                  | Overdue API    |
| M6-03   | BE         | Orders reporting                     | Orders report  |
| M6-04   | BE         | Payments dan outstanding report      | Finance report |
| M6-05   | BE         | Expenses report                      | Expense report |
| M6-06   | BE         | CSV export                           | Export API     |
| M6-07   | FE         | Owner dashboard                      | Dashboard UI   |
| M6-08   | FE         | Kasir dashboard                      | Operational UI |
| M6-09   | FE/INT     | Laporan dan filter                   | Report UI      |
| M6-10   | QA         | Reconciliation dan performance tests | M6 evidence    |

## 15.3 Dashboard Metrics

- Pesanan hari ini.
- Nilai pesanan.
- Uang diterima.
- Cucian sedang diproses.
- Cucian siap.
- Pesanan terlambat.
- Tagihan belum lunas.
- Pengeluaran.

## 15.4 Financial Definitions

**Order Value**

Nilai pesanan sah berdasarkan periode yang didefinisikan.

**Cash Received**

Pembayaran terverifikasi yang berlaku dan diterima dalam periode terkait.

**Outstanding**

Sisa tagihan order yang belum dibayar.

**Expenses**

Pengeluaran yang dicatat dalam periode.

**Simple Cash Difference**

Uang masuk dikurangi pengeluaran yang tercatat.

Tidak menggunakan istilah laba bersih untuk laporan kas sederhana.

## 15.5 Data Reconciliation

Pengujian:

- Dashboard vs database.
- Payment report vs payments.
- Outstanding vs order balances.
- Expenses vs expenses table.
- Cancelled orders exclusion.
- Payment void treatment.
- Date filter dan timezone.

## 15.6 Acceptance Gate M6

1. Dashboard memuat data benar.
2. Kasir hanya melihat metrik yang diizinkan.
3. Nilai order berbeda jelas dari uang diterima.
4. Pesanan terlambat dihitung benar.
5. Tagihan belum lunas dihitung benar.
6. Payment void tidak dihitung sebagai penerimaan sah.
7. Filter tanggal konsisten.
8. CSV berfungsi dan aman.
9. Responsive UI lulus.
10. Reconciliation tests lulus.

**Output:** REPORTING_READY.

---

# 16. M7 — QUALITY, SECURITY & PERFORMANCE HARDENING

## 16.1 Objective

Memastikan seluruh sistem aman dan cukup stabil untuk operasional nyata.

## 16.2 Task Breakdown

| Task ID | Workstream | Task                                  | Deliverable             |
| ------- | ---------- | ------------------------------------- | ----------------------- |
| M7-01   | QA         | Full unit test regression             | Unit test report        |
| M7-02   | QA         | PostgreSQL integration tests          | Integration report      |
| M7-03   | QA         | End-to-end journey tests              | E2E report              |
| M7-04   | SEC        | Authentication/session audit          | Auth security report    |
| M7-05   | SEC        | RBAC/IDOR security audit              | Authorization report    |
| M7-06   | SEC        | Public tracking security audit        | Public API report       |
| M7-07   | QA/BE      | Financial invariant/concurrency tests | Financial safety report |
| M7-08   | QA/FE      | Responsive audit                      | Viewport report         |
| M7-09   | QA/UX      | Accessibility audit                   | Accessibility report    |
| M7-10   | QA/OPS     | Load/performance tests                | Performance baseline    |
| M7-11   | OPS        | Backup and restore test               | Recovery evidence       |
| M7-12   | PM/QA      | User Acceptance Test                  | UAT report              |
| M7-13   | BE/FE      | Critical bug resolution               | Release candidate       |
| M7-14   | QA         | Final traceability verification       | Requirement coverage    |

## 16.3 Critical E2E Journeys

**Journey 1 — Walk-In Order**

Login → Customer → Create Order → Process Laundry → Invoice → Handoff → Complete.

**Journey 2 — Partial Payment**

Order → DP → Remaining Balance → Final Payment → PAID.

**Journey 3 — Pickup**

Public Form → Admin Confirmation → Courier Pickup → Arrive → Convert to Order.

**Journey 4 — Delivery**

READY → Schedule → Courier → DELIVERED → Handoff → COMPLETED.

**Journey 5 — Tracking**

Token → Public Page → Status Update → Refresh → Correct Status.

**Journey 6 — Cancellation/Error**

Invalid state → Rejected Mutation → Data Consistency Preserved.

## 16.4 Security Coverage

Pengujian wajib:

1. Brute force.
2. Session expiry.
3. Session revocation.
4. CSRF.
5. XSS.
6. SQL injection.
7. Unauthorized access.
8. IDOR.
9. Token guessing.
10. Token rotation.
11. Token expiration.
12. Public data leakage.
13. Rate limiting.
14. Concurrent payment.
15. Duplicate request.
16. File/PDF security.
17. Sensitive logging.
18. Misconfiguration.

## 16.5 Responsive Viewports

Minimal:

- 320 px.
- 360 px.
- 375 px.
- 390 px.
- 430 px.
- 768 px.
- 1024 px.
- 1440 px.

Seluruh flow P0 wajib diuji pada mobile.

## 16.6 Performance Baseline

Target API mengikuti TRD:

- GET Orders p95 ≤ 1.000 ms.
- GET Order Detail p95 ≤ 800 ms.
- POST Order p95 ≤ 2.000 ms.
- POST Payment p95 ≤ 1.500 ms.
- GET Tracking p95 ≤ 1.000 ms.
- GET Dashboard p95 ≤ 1.500 ms.

Target berlaku pada lingkungan dan kondisi beban uji yang terdokumentasi.

## 16.7 Acceptance Gate M7

1. Semua P0 selesai.
2. Semua critical E2E lulus.
3. Tidak ada critical security issue.
4. Tidak ada financial consistency issue.
5. Concurrency tests lulus.
6. Responsive tests lulus.
7. Accessibility issue kritis diselesaikan.
8. Backup restore lulus.
9. Performance dievaluasi dan memenuhi batas yang disetujui.
10. UAT disetujui.
11. Release candidate stabil.
12. Traceability lengkap.

**Output:** RELEASE_CANDIDATE_READY.

---

# 17. M8 — PRODUCTION DEPLOYMENT

## 17.1 Objective

Meluncurkan aplikasi ke lingkungan produksi dengan kontrol keamanan, backup, dan monitoring.

## 17.2 Task Breakdown

| Task ID | Workstream | Task                                      | Deliverable               |
| ------- | ---------- | ----------------------------------------- | ------------------------- |
| M8-01   | OPS        | Menentukan dan menyiapkan hosting         | Production infrastructure |
| M8-02   | OPS/SEC    | HTTPS, domain, security config            | Secure production         |
| M8-03   | DB/OPS     | PostgreSQL production setup               | Production DB             |
| M8-04   | OPS        | Secrets management                        | Secure config             |
| M8-05   | DB         | Production migration                      | Production schema         |
| M8-06   | OPS        | Automated backup dan restore procedure    | Recovery setup            |
| M8-07   | OPS        | Logging, monitoring, health checks        | Observability             |
| M8-08   | OPS        | Deploy frontend/backend                   | Production release        |
| M8-09   | QA         | Production smoke tests                    | Smoke report              |
| M8-10   | PM/QA      | Go-live approval dan dokumentasi          | Release sign-off          |
| M8-11   | OPS        | Rollback/recovery runbook                 | Incident readiness        |
| M8-12   | PM         | Operasional pilot dan pencatatan feedback | Pilot evaluation          |

## 17.3 Production Checklist

- HTTPS aktif.
- Domain valid.
- Environment terpisah.
- Secret aman.
- Database terlindungi.
- Migration berhasil.
- Backup aktif.
- Restore telah diuji.
- Health checks lulus.
- Logging aktif.
- RBAC aktif.
- CSRF aktif.
- Rate limiting aktif.
- Tidak ada debug mode.
- Smoke test lulus.
- Dokumentasi admin tersedia.

## 17.4 Go-Live Gate

Produksi hanya dapat dinyatakan siap setelah:

1. M7 PASS.
2. Tidak ada critical blocker.
3. Production security checklist lulus.
4. Database backup terverifikasi.
5. Migration aman.
6. Monitoring berjalan.
7. Recovery procedure tersedia.
8. Owner atau penanggung jawab menyetujui go-live.
9. Alur transaksi utama berhasil pada smoke test produksi.
10. Penggunaan pilot tidak mengungkap masalah kritis yang belum ditangani.

**Output:** PRODUCTION_READY.

---

# 18. DEPENDENCY MANAGEMENT

## 18.1 Dependency Antar-Milestone

Urutan utama:

M0 → M1 → M2 → M3 → M4 → M5 → M6 → M7 → M8.

Urutan tersebut merupakan urutan integrasi dan acceptance baseline.

Sebagian pekerjaan dapat berjalan paralel:

- UI/UX dan backend.
- Customer UI dan customer API.
- Invoice UI dan invoice service.
- Tracking UI dan token service.
- Dashboard layout dan reporting service.

Namun pengujian akhir tiap fitur tetap bergantung pada seluruh komponen terkait.

## 18.2 Critical Dependencies

| Task                | Bergantung pada                       |
| ------------------- | ------------------------------------- |
| Orders              | Auth, Customers, Services             |
| Payments            | Orders, Transactions, Authorization   |
| Invoice             | Orders, Payments                      |
| Tracking            | Orders, Token Schema, Public Security |
| Pickup Conversion   | Pickup, Orders, Tracking              |
| Delivery Completion | Orders, Delivery Tasks, Handoff       |
| Dashboard Finance   | Orders, Payments, Expenses            |
| Production          | Security, Testing, Backup, UAT        |

## 18.3 Parallel Development Rules

1. Frontend dapat menggunakan mock API yang mengikuti OpenAPI.
2. Mock data harus ditandai sebagai simulasi.
3. Backend tidak boleh mengubah response schema tanpa pembaruan kontrak.
4. Integrasi harus diuji kembali setelah perubahan API.
5. Modul berisiko tinggi tidak dianggap selesai sebelum integrasi nyata.
6. Test harus menggunakan database PostgreSQL pada integration stage.

---

# 19. DATABASE MIGRATION PLAN

## 19.1 Migration Sequence

Urutan migrasi yang diusulkan:

| Migration | Cakupan                                           |
| --------- | ------------------------------------------------- |
| 0001      | Businesses, Settings                              |
| 0002      | Users, Sessions                                   |
| 0003      | Customers, Services                               |
| 0004      | Orders, Order Items, Status History, Handoffs     |
| 0005      | Payments, Payment Voids, Expenses                 |
| 0006      | Tracking Tokens                                   |
| 0007      | Pickup Requests, Delivery Tasks, Delivery History |
| 0008      | Idempotency Records, Audit Logs                   |
| 0009      | Indexes, Constraints, Performance Refinement      |

Urutan tersebut perlu disesuaikan dengan dependensi foreign key.

## 19.2 Ketentuan Integritas Migrasi

Karena `orders` memiliki relasi opsional terhadap `pickup_requests`, migrasi harus menghindari referensi tabel yang belum dibuat.

Pendekatan yang diperbolehkan:

- Membuat tabel parent terlebih dahulu; atau
- Menambahkan foreign key lintas modul melalui migration berikutnya.

Constraint harus dipastikan telah lengkap sebelum milestone yang memerlukannya dinyatakan PASS.

## 19.3 Migration Acceptance

- Migration berhasil dari database kosong.
- Upgrade path berhasil.
- Foreign key valid.
- Unique constraint aktif.
- Check constraint aktif.
- Indeks sesuai kebutuhan.
- Tidak ada orphaned records.
- Rollback/recovery strategy tersedia untuk perubahan berisiko.

---

# 20. API CONTRACT IMPLEMENTATION PLAN

## 20.1 Kontrak API

Kontrak API harus memuat:

1. Endpoint.
2. HTTP method.
3. Request schema.
4. Response schema.
5. Error schema.
6. Permission.
7. Authentication requirement.
8. Validation.
9. Pagination.
10. Idempotency requirement.
11. Example payload.
12. Acceptance test reference.

## 20.2 API Contract Ownership

Backend menjadi pemilik implementasi endpoint.

Kontrak harus direview bersama frontend sebelum implementasi integrasi.

## 20.3 Contract Change Process

Perubahan breaking harus:

1. Dicatat dalam change log.
2. Diperiksa dampaknya terhadap frontend.
3. Memperbarui OpenAPI.
4. Memperbarui test.
5. Memperbarui dokumentasi.
6. Dikoordinasikan sebelum merge.

## 20.4 API Review Gate

Endpoint belum PASS apabila:

- Response schema belum stabil.
- Error handling belum ditentukan.
- Permission belum diuji.
- Validasi belum lengkap.
- Contract tests belum lulus.

---

# 21. UI/UX IMPLEMENTATION PLAN

## 21.1 Design Milestones

| Tahap | Fokus                       |
| ----- | --------------------------- |
| D0    | Design discovery            |
| D1    | Information architecture    |
| D2    | Wireframe                   |
| D3    | Design system               |
| D4    | High-fidelity design        |
| D5    | Interactive prototype       |
| D6    | Usability testing           |
| D7    | Developer handoff           |
| D8    | Visual dan accessibility QA |

## 21.2 Prioritas Halaman

Urutan utama:

1. Login.
2. Dashboard shell.
3. Daftar pesanan.
4. Buat pesanan.
5. Detail pesanan.
6. Pelanggan.
7. Pembayaran.
8. Nota.
9. Tracking publik.
10. Pickup publik.
11. Admin pickup.
12. Dashboard kurir.
13. Delivery.
14. Laporan.
15. Pengaturan.

## 21.3 Component Design

Komponen dasar:

- Button.
- Input.
- Select.
- Date Picker.
- Dialog.
- Card.
- Badge.
- Table.
- Skeleton.
- Toast.
- Alert.
- Pagination.

Komponen domain:

- Order Summary.
- Payment Summary.
- Laundry Timeline.
- Pickup Timeline.
- Delivery Timeline.
- Courier Task Card.
- Invoice Preview.
- Pricing Preview.

## 21.4 Frontend Acceptance

1. Design tokens konsisten.
2. Halaman mobile responsif.
3. Tidak ada overflow horizontal pada flow utama.
4. Validasi formulir jelas.
5. Loading tersedia.
6. Error state tersedia.
7. Role-based navigation sesuai.
8. Tidak ada klaim keberhasilan sebelum respons backend.
9. Accessibility checklist lulus.
10. Flow utama diuji pada mobile.

---

# 22. SECURITY IMPLEMENTATION PLAN

## 22.1 Authentication

- Password hashing Argon2id.
- Session server-side.
- Cookie aman.
- Session expiry.
- Session revocation.
- Login throttling.
- CSRF protection.

## 22.2 Authorization

- Permission backend.
- Resource authorization.
- Courier assignment checks.
- Public token scope.
- Owner-only sensitive actions.
- No IDOR.

## 22.3 Tracking Security

- Strong random token.
- Hashed token storage.
- Token expiry.
- Token rotation.
- Rate limiting.
- No-store.
- Noindex.
- Referrer protection.
- Sensitive log redaction.
- Public response allowlist.

## 22.4 Payment Security

- Atomic transaction.
- Row locking.
- Idempotency.
- Audit.
- Payment invariants.
- Controlled void.
- No direct payment status mutation.

## 22.5 Security Gate

Seluruh kontrol kritis wajib memiliki automated test atau bukti audit yang memadai.

Penemuan vulnerability kritis menyebabkan production gate BLOCKED sampai ditangani.

---

# 23. TESTING PLAN

## 23.1 Test Layers

| Layer              | Tujuan                               |
| ------------------ | ------------------------------------ |
| Unit               | Business rules dan fungsi kecil      |
| Integration        | Database, service, dan transaksi     |
| API Contract       | Request/response consistency         |
| Frontend Component | Rendering dan interaksi              |
| E2E                | User journey                         |
| Security           | Authentication, authorization, abuse |
| Concurrency        | Race condition dan duplication       |
| Performance        | Latency dan kapasitas                |
| UAT                | Penerimaan pengguna                  |

## 23.2 Critical Test Matrix

| Test ID | Skenario                        | Prioritas |
| ------- | ------------------------------- | --------- |
| CT-01   | Login dan RBAC                  | Critical  |
| CT-02   | Order creation                  | Critical  |
| CT-03   | Multi-service pricing           | Critical  |
| CT-04   | Price snapshot                  | Critical  |
| CT-05   | Duplicate order retry           | Critical  |
| CT-06   | Payment DP                      | Critical  |
| CT-07   | Payment full                    | Critical  |
| CT-08   | Concurrent payment              | Critical  |
| CT-09   | Payment void                    | Critical  |
| CT-10   | Payment balance invariant       | Critical  |
| CT-11   | Pickup submission               | Critical  |
| CT-12   | Pickup conversion               | Critical  |
| CT-13   | Duplicate conversion prevention | Critical  |
| CT-14   | Delivery state machine          | Critical  |
| CT-15   | Handoff requirement             | Critical  |
| CT-16   | Public token validation         | Critical  |
| CT-17   | Public data isolation           | Critical  |
| CT-18   | Token rotation                  | Critical  |
| CT-19   | CSRF                            | Critical  |
| CT-20   | Unauthorized mutation           | Critical  |
| CT-21   | Backup restore                  | Critical  |
| CT-22   | Full mobile journey             | Critical  |

## 23.3 Test Data

Gunakan data sintetis:

- Pelanggan baru.
- Pelanggan lama.
- Pesanan kiloan.
- Pesanan satuan.
- Pesanan multi-layanan.
- DP.
- Pelunasan.
- Void.
- Pickup.
- Delivery.
- Failed delivery.
- Order cancelled.
- Expired tracking token.
- Concurrent user operations.

Data pribadi pelanggan nyata tidak boleh dimasukkan ke repository.

---

# 24. QUALITY GATES DAN DEFINITION OF DONE

## 24.1 Definition of Ready

Sebuah task siap dikerjakan jika:

1. Requirement jelas.
2. Task ID tersedia.
3. Dependensi diketahui.
4. Acceptance criteria tersedia.
5. API contract tersedia bila relevan.
6. Database schema tersedia bila relevan.
7. UI design tersedia bila relevan.
8. Keputusan bisnis yang dibutuhkan sudah final.

## 24.2 Definition of Done

Sebuah task selesai jika:

1. Kode tersedia.
2. Fitur sesuai spesifikasi.
3. Validasi tersedia.
4. Error handling tersedia.
5. Permission diterapkan.
6. Unit tests lulus.
7. Integration tests lulus bila relevan.
8. E2E tests lulus bila relevan.
9. Tidak ada regresi kritis.
10. Dokumentasi diperbarui.
11. CI lulus.
12. Acceptance evidence tersedia.

## 24.3 Acceptance Evidence

Bukti dapat berupa:

- Test report.
- CI log.
- API response.
- Screenshot UI.
- E2E trace.
- Migration result.
- Security report.
- Load test report.
- UAT sign-off.

Screenshot saja tidak cukup untuk membuktikan keamanan, konsistensi transaksi, atau integritas database.

---

# 25. RISK MANAGEMENT

| Risiko                         | Dampak                    | Mitigasi                          |
| ------------------------------ | ------------------------- | --------------------------------- |
| Scope terlalu luas             | Pengembangan tidak fokus  | P0 dahulu                         |
| API berubah tanpa kontrol      | Integrasi rusak           | Contract-first                    |
| Pembayaran salah hitung        | Kerugian usaha            | Financial invariants              |
| Duplicate transaction          | Data tidak akurat         | Idempotency                       |
| Race condition                 | Saldo tidak konsisten     | Locking/versioning                |
| Token bocor                    | Privasi pelanggan         | Token lifecycle                   |
| RBAC tidak konsisten           | Akses tidak sah           | Backend permission tests          |
| Pickup duplikat                | Operasional membingungkan | Unique constraint dan transaction |
| UI terlalu kompleks            | Sulit digunakan UMKM      | Mobile-first usability testing    |
| Hosting terlalu mahal          | Tidak cocok UMKM          | Infrastruktur sederhana           |
| Backup gagal                   | Risiko kehilangan data    | Restore testing                   |
| Perubahan bisnis tanpa dokumen | Rework                    | Change management                 |

## 25.1 Risk Review

Risiko ditinjau:

- Saat M0.
- Sebelum milestone berisiko.
- Setelah bug kritis.
- Sebelum production deployment.

---

# 26. CHANGE MANAGEMENT

## 26.1 Jenis Perubahan

**Minor Change**

Perubahan UI kecil atau perbaikan tanpa mengubah kontrak dan business rules.

**Major Change**

Perubahan:

- API.
- Database schema.
- Business logic.
- Authentication.
- Authorization.
- Payment.
- Tracking.
- Workflow.

## 26.2 Change Request

Setiap major change harus mencatat:

1. Alasan perubahan.
2. Dokumen yang terdampak.
3. Modul terdampak.
4. Risiko.
5. Migration impact.
6. API impact.
7. Test impact.
8. Keputusan.
9. Reviewer.

## 26.3 Dokumentasi

Perubahan harus memperbarui dokumen sumber yang relevan agar implementasi dan spesifikasi tidak berbeda.

---

# 27. OPEN DECISION REGISTER

## 27.1 Keputusan Wajib Sebelum Modul Terkait

| ID     | Keputusan                           | Batas Gate                                |
| ------ | ----------------------------------- | ----------------------------------------- |
| DEC-01 | Pembulatan berat                    | Sebelum M2                                |
| DEC-02 | Berat minimum layanan               | Sebelum M2                                |
| DEC-03 | Format nomor pesanan                | Sebelum M2                                |
| DEC-04 | Ongkir dan biaya tambahan           | Sebelum implementasi harga final M2/M5    |
| DEC-05 | Aturan pembayaran saat serah terima | Sebelum M3/M5                             |
| DEC-06 | SOP refund                          | Sebelum pembatalan order berbayar dirilis |
| DEC-07 | Masa berlaku token tracking         | Sebelum M4                                |
| DEC-08 | Retensi data pelanggan dan audit    | Sebelum M8                                |
| DEC-09 | Hosting production                  | Sebelum M8                                |
| DEC-10 | Backup retention                    | Sebelum M8                                |
| DEC-11 | Session timeout final               | Sebelum M1 gate                           |
| DEC-12 | Identitas visual final              | Sebelum D4 approval                       |

## 27.2 Aturan

Keputusan yang belum disetujui tidak boleh diam-diam dikunci menjadi perilaku produk.

Task yang benar-benar bergantung pada keputusan tersebut diberi status BLOCKED sampai keputusan selesai.

Task independen tetap dapat dilanjutkan.

---

# 28. RESOURCE DAN KAPASITAS

## 28.1 Model Tim Minimum

Pengembangan dapat dijalankan dengan:

- Satu pengembang full-stack.
- Bantuan AI coding tools bila digunakan.
- Owner/stakeholder sebagai reviewer bisnis.
- Pengujian pengguna dari calon operator laundry.

Jika pengembang bekerja sendiri, workstream tetap dipisahkan secara logis.

## 28.2 Kapasitas

Estimasi pengerjaan harus mempertimbangkan:

- Kompleksitas.
- Dependensi.
- Risiko.
- Kemampuan pengembang.
- Waktu review.
- Waktu pengujian.
- Waktu perbaikan.

Tanggal rilis tidak boleh ditetapkan hanya berdasarkan jumlah task.

## 28.3 Task Sizing

Gunakan:

- S — Kecil.
- M — Sedang.
- L — Besar.
- XL — Perlu dipecah.

Task XL harus dipecah sebelum dikerjakan.

---

# 29. PROJECT TRACKING FORMAT

## 29.1 Format Task

Setiap task memiliki:

- ID.
- Milestone.
- Title.
- Workstream.
- Priority.
- Size.
- Status.
- Dependencies.
- Acceptance Criteria.
- Deliverables.
- Evidence.
- Reviewer.

## 29.2 Contoh Task

**Task ID:** M3-03
**Title:** Implement Manual Payment API
**Workstream:** Backend
**Priority:** P0
**Size:** M
**Dependencies:** M3-01, M3-02, M1-06, M2-07

**Deliverables:**

- Payment endpoint.
- Pydantic schema.
- Payment service.
- Repository operation.
- Transaction handling.
- Error response.
- Tests.

**Acceptance Criteria:**

1. Cash payment berhasil.
2. Transfer manual berhasil.
3. QRIS manual berhasil.
4. Overpayment ditolak.
5. Saldo dihitung ulang.
6. Permission diterapkan.
7. Idempotency bekerja.
8. Concurrent payment test lulus.

**Status Awal:** NOT_STARTED.

---

# 30. RELEASE MANAGEMENT

## 30.1 Release Types

**Development Build**

Untuk pengembangan lokal.

**Staging Release**

Untuk integrasi dan UAT.

**Release Candidate**

Untuk pengujian akhir sebelum produksi.

**Production Release**

Untuk penggunaan nyata.

## 30.2 Versioning

Rekomendasi:

- `0.x.x` selama pengembangan.
- `1.0.0` untuk MVP produksi yang disetujui.

## 30.3 Release Notes

Memuat:

- Fitur baru.
- Perbaikan bug.
- Perubahan API.
- Perubahan database.
- Known issues.
- Migration requirement.
- Rollback notes.

## 30.4 Rollback

Rollback aplikasi dan recovery database harus direncanakan secara terpisah.

Database migration yang destruktif tidak boleh diasumsikan bisa dibalik secara otomatis.

---

# 31. OPERATIONS DAN MAINTENANCE

## 31.1 Monitoring

Pantau:

- Uptime.
- HTTP error rate.
- API latency.
- Database connection.
- Backup.
- Failed authentication.
- Transaction errors.
- Storage growth.

## 31.2 Backup

Baseline:

- Backup harian.
- Penyimpanan aman.
- Restore test.
- Retensi sesuai kebijakan.
- Backup sebelum migration berisiko.

## 31.3 Incident Categories

**Critical**

Transaksi keuangan rusak, data bocor, atau aplikasi tidak dapat digunakan.

**High**

Fitur inti gagal tetapi masih ada workaround yang aman.

**Medium**

Gangguan terbatas pada fungsi nonkritis.

**Low**

Masalah kosmetik atau minor.

## 31.4 Maintenance

- Dependency updates.
- Security patches.
- Backup checks.
- Log review.
- Performance review.
- User feedback.
- Bug fixes.

---

# 32. MASTER ACCEPTANCE MATRIX

| Area           | Gate                           |
| -------------- | ------------------------------ |
| Foundation     | Clean setup dan CI PASS        |
| Authentication | Login, session, RBAC PASS      |
| Orders         | Order dan pricing PASS         |
| Payments       | Financial invariants PASS      |
| Tracking       | Public security PASS           |
| Pickup         | Pickup-to-order PASS           |
| Delivery       | Handoff dan completion PASS    |
| Reporting      | Reconciliation PASS            |
| Frontend       | Mobile E2E dan responsive PASS |
| Security       | Critical security tests PASS   |
| Database       | Migration dan integrity PASS   |
| Backup         | Restore PASS                   |
| Production     | Smoke test dan approval PASS   |

Semua gate kritis wajib dipenuhi.

---

# 33. TRACEABILITY MATRIX

| PRD Requirement | TRD Component      | AFD Flow   | BSD Component       | Milestone |
| --------------- | ------------------ | ---------- | ------------------- | --------- |
| Authentication  | Session Auth       | FLOW-AUTH  | Users/Sessions      | M1        |
| Dashboard       | Reporting API      | FLOW-DASH  | Dashboard Service   | M6        |
| Customers       | Customer API       | FLOW-CUS   | Customers           | M2        |
| Services        | Service API        | FLOW-SET   | Services            | M2        |
| Orders          | Orders API         | FLOW-ORD   | Orders/Items        | M2        |
| Laundry Status  | State Machine      | FLOW-WRK   | Order History       | M2        |
| Payments        | Payment Service    | FLOW-PAY   | Payments/Voids      | M3        |
| Expenses        | Expenses API       | FLOW-FIN   | Expenses            | M3/M6     |
| Invoice         | PDF Service        | FLOW-INV   | Invoice Mapper      | M3        |
| Tracking        | Public API         | FLOW-TRK   | Tracking Tokens     | M4        |
| Pickup          | Pickup API         | FLOW-PUP   | Pickup Requests     | M5        |
| Delivery        | Delivery API       | FLOW-DLV   | Delivery Tasks      | M5        |
| Handoff         | Completion Service | FLOW-DLV   | Order Handoffs      | M5        |
| Reports         | Report Service     | FLOW-FIN   | Aggregation Queries | M6        |
| Audit           | Audit Service      | Cross-Flow | Audit Logs          | M1–M7    |
| Error Handling  | Exception Handler  | FLOW-ERR   | Error Schema        | M0–M7    |

---

# 34. FINAL IMPLEMENTATION CHECKLIST

## 34.1 Sebelum Coding

- [ ] PRD direview.
- [ ] TRD direview.
- [ ] AFD direview.
- [ ] DBD direview.
- [ ] BSD direview.
- [ ] IPD direview.
- [ ] Keputusan P0 ditetapkan.
- [ ] Repository disiapkan.
- [ ] Environment disiapkan.
- [ ] API contract baseline disiapkan.
- [ ] Database migration strategy disetujui.
- [ ] Design direction disetujui.

## 34.2 Selama Coding

- [ ] Mengikuti task ID.
- [ ] Mengikuti dependency.
- [ ] Menggunakan migration.
- [ ] Menggunakan validation.
- [ ] Menggunakan authorization.
- [ ] Menggunakan transaction boundaries.
- [ ] Menulis unit tests.
- [ ] Menulis integration tests.
- [ ] Memperbarui API contract.
- [ ] Memperbarui dokumentasi.
- [ ] Menjaga CI.
- [ ] Melakukan review sebelum merge.

## 34.3 Sebelum Produksi

- [ ] Seluruh fitur P0 tersedia.
- [ ] Semua critical tests lulus.
- [ ] Tidak ada critical security issue.
- [ ] Database integrity lulus.
- [ ] Backup restore lulus.
- [ ] Responsive audit lulus.
- [ ] E2E mobile lulus.
- [ ] UAT disetujui.
- [ ] HTTPS aktif.
- [ ] Monitoring aktif.
- [ ] Production configuration aman.
- [ ] Rollback tersedia.
- [ ] Go-live approval tersedia.

---

# 35. RENCANA EKSEKUSI PERTAMA

## 35.1 Prioritas Awal

Pekerjaan pertama adalah M0.

Urutan yang disarankan:

1. Audit dokumen.
2. Finalisasi keputusan yang menghalangi M0/M1.
3. Inisialisasi repository.
4. Setup frontend.
5. Setup backend.
6. Setup PostgreSQL.
7. Setup Alembic.
8. Setup environment.
9. Setup logging dan health checks.
10. Setup CI.
11. Verifikasi clean installation.
12. Audit acceptance gate M0.

## 35.2 Hasil yang Harus Didapat

Pada akhir M0 tersedia:

- Frontend yang dapat dijalankan.
- Backend yang dapat dijalankan.
- Database yang terkoneksi.
- Migration awal.
- OpenAPI awal.
- CI yang berjalan.
- Struktur modular.
- Dokumentasi setup.
- Test baseline.

M0 tidak mencakup pengembangan lengkap modul pesanan atau pembayaran.

## 35.3 Audit M0

Hasil audit wajib melaporkan:

- Task ID.
- Implemented files.
- Test commands.
- Test results.
- Known issues.
- Dependencies.
- Gate status.
- Next milestone readiness.

---

# 36. KEBIJAKAN PENGGUNAAN AI CODING TOOLS

## 36.1 Tujuan

AI coding tools dapat membantu implementasi, analisis kode, penulisan test, dan review.

Namun setiap hasil harus diverifikasi.

## 36.2 Aturan untuk Coding Agent

Setiap tugas kepada coding agent harus menyertakan:

1. Task ID.
2. Tujuan.
3. Dokumen acuan.
4. Lingkup perubahan.
5. File atau modul relevan.
6. Batasan.
7. Acceptance criteria.
8. Test requirements.
9. Output report.

## 36.3 Codebase Exploration

Sebelum perubahan:

- Periksa struktur repository.
- Pelajari modul terkait.
- Periksa kontrak API.
- Periksa migration yang ada.
- Periksa test yang relevan.
- Identifikasi dependensi.
- Evaluasi dampak perubahan.

Jika repository telah memiliki CodeGraph atau alat analisis kode sejenis yang tervalidasi, alat tersebut dapat digunakan untuk memahami hubungan simbol dan dampak perubahan.

Tidak perlu menambah dependency code intelligence hanya untuk memenuhi proses formal.

## 36.4 Aturan AI Implementation

1. Jangan langsung mengubah seluruh sistem.
2. Kerjakan task yang teridentifikasi.
3. Jangan membuat fitur di luar scope.
4. Jangan menghapus test agar pipeline lulus.
5. Jangan mengubah business rules tanpa persetujuan.
6. Jangan menyatakan PASS tanpa menjalankan pengujian.
7. Jangan membuat mock yang diklaim sebagai integrasi nyata.
8. Jangan mengekspos credential.
9. Laporkan blocker.
10. Berikan ringkasan file yang berubah dan hasil test.

## 36.5 Output Laporan Coding Agent

Format:

**Task:** [ID]

**Status:** PASS / PARTIAL / BLOCKED / FAILED

**Implemented:**

- Perubahan utama.

**Files Changed:**

- File terkait.

**Tests Executed:**

- Command.
- Result.

**Acceptance Criteria:**

- Hasil tiap kriteria.

**Issues:**

- Masalah tersisa.

**Next Dependency:**

- Task berikutnya yang dapat dikerjakan.

---

# 37. APPROVAL DAN BASELINE CONTROL

## 37.1 Approval Gate

IPD dinyatakan approved setelah:

1. Konsisten dengan PRD.
2. Konsisten dengan TRD.
3. Konsisten dengan AFD.
4. Konsisten dengan DBD.
5. Konsisten dengan BSD.
6. Keputusan kritis teridentifikasi.
7. Milestone dapat diuji.
8. Dependensi dapat ditelusuri.
9. Risiko utama memiliki mitigasi.
10. Stakeholder menyetujui lingkup MVP.

## 37.2 Version Control

Perubahan dokumen harus mencatat:

- Versi.
- Tanggal.
- Perubahan.
- Alasan.
- Dampak.
- Persetujuan.

## 37.3 Status Baseline

**IPD v1.0 — DRAFT FOR IMPLEMENTATION REVIEW.**

Belum ada klaim bahwa milestone atau task telah dikerjakan.

---

# 38. KESIMPULAN

Implementation Plan Documentation v1.0 menetapkan roadmap implementasi Web App Manajemen Laundry UMKM secara bertahap dari fondasi sistem hingga deployment produksi.

Pengembangan dibagi menjadi sembilan milestone:

1. M0 — Project Foundation.
2. M1 — Authentication & Business Configuration.
3. M2 — Core Laundry Operations.
4. M3 — Finance & Digital Invoices.
5. M4 — Public Tracking.
6. M5 — Pickup & Delivery.
7. M6 — Dashboard & Reporting.
8. M7 — Quality, Security & Performance Hardening.
9. M8 — Production Deployment.

Setiap milestone memiliki tugas, deliverable, dependensi, pengujian, dan acceptance gate.

Prioritas utama proyek adalah:

- Menjaga kesederhanaan aplikasi bagi UMKM.
- Menjamin kebenaran pencatatan pesanan dan pembayaran.
- Memisahkan status operasional dan keuangan.
- Menjamin keamanan tracking tanpa login.
- Mendukung proses antar-jemput manual.
- Menyediakan UI mobile-first.
- Menghindari infrastruktur dan integrasi berbiaya tinggi.
- Mengembangkan sistem yang dapat diuji, diaudit, dan dipelihara.

**IPD ini menjadi baseline rencana pelaksanaan proyek setelah review dan persetujuan, serta dapat digunakan sebagai acuan pembagian task kepada developer maupun AI coding agent.**

**Status Akhir: IPD v1.0 — DRAFT FOR IMPLEMENTATION REVIEW.**

---

**AKHIR DOKUMEN — IMPLEMENTATION PLAN DOCUMENTATION v1.0**
