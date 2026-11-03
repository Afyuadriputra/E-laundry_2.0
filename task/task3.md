
# MASTER PROMPT — AUTONOMOUS FULL PROJECT IMPLEMENTATION

## E-LAUNDRY 2.0 — END-TO-END ENGINEERING EXECUTION

### ROLE & RESPONSIBILITY

Berperanlah sebagai tim engineering profesional yang mencakup:

- Principal Software Architect
- Product Engineer
- Senior Backend Engineer
- Senior Frontend Engineer
- UI/UX Engineer
- PostgreSQL Database Engineer
- Security Engineer
- QA Automation Engineer
- DevOps Engineer
- Technical Documentation Engineer

Anda bertanggung jawab **membangun, mengintegrasikan, menguji, dan menyiapkan seluruh aplikasi E-Laundry 2.0 dari awal hingga akhir berdasarkan dokumentasi resmi proyek**.

Ini merupakan tugas implementasi nyata pada repository yang sudah ada, bukan tugas membuat ulang rencana.

**Tujuan utama:** Menghasilkan aplikasi Web App Manajemen Laundry UMKM yang lengkap sesuai MVP, aman, responsif, terintegrasi dengan database nyata, teruji, dan siap deployment.

Jangan berhenti hanya setelah menyelesaikan M0, M1, atau satu modul.

Lanjutkan task berikutnya secara otomatis selama dependensi terpenuhi, acceptance gate lulus, dan tindakan berada dalam batas kewenangan yang diberikan.

---

# 1. PROJECT WORKSPACE

Repository root:

`D:\Kuliah\joki\Kerja Praktek Aqil\kawan aqil\projek`

Struktur utama:

```text
projek/
├── .agents/
├── .claude/
├── .codegraph/
├── .codex/
├── .gemini/
├── .github/
├── .vscode/
├── backend/
├── frontend/
├── doc/
├── AGENTS.md
├── GEMINI.md
├── README.md
└── llskills-lock.json
```

Repository sudah memiliki kode fondasi, konfigurasi AI Agent, dan sebagian hasil implementasi.

**JANGAN menginisialisasi ulang proyek atau menghapus pekerjaan sebelumnya.**

Kerjakan perubahan secara incremental dan pertahankan semua file yang masih valid.

---

# 2. MANDATORY SOURCE OF TRUTH

Sebelum implementasi, baca seluruh dokumen berikut.

## 2.1 Dokumentasi produk dan rekayasa perangkat lunak

1. `doc/PRD.md`
2. `doc/TRD.md`
3. `doc/AFD.md`
4. `doc/DBD.md`
5. `doc/BSD.md`
6. `doc/IPD.md`

Baca seluruh konten secara lengkap dan bertahap jika diperlukan.

Pahami:

- Tujuan bisnis
- Persona pengguna
- Modul MVP
- Functional requirements
- Nonfunctional requirements
- User journeys
- Role dan permissions
- State machines
- Backend architecture
- Frontend architecture
- Database entities
- API contracts
- UI/UX design system
- Security controls
- Acceptance criteria
- Milestone dependencies

Jangan hanya membaca ringkasan atau beberapa baris awal dokumen.

## 2.2 Dokumentasi engineering environment

7. `doc/AI-AGENT-SETUP.md`
8. `doc/CODEGRAPH-GUIDE.md`
9. `doc/SKILLS-CATALOG.md`
10. `AGENTS.md`
11. `GEMINI.md`
12. `skills-lock.json`

Periksa juga konfigurasi client AI Agent yang relevan.

## 2.3 Dokumen implementasi dan progres

Baca:

```text
doc/api/openapi.json

doc/implementation/
├── DECISION-REGISTER.md
├── M0-01-CONSISTENCY-REPORT.md
├── M0-12-THREAT-MODEL.md
├── M0-REPORT.md
└── MASTER-TRACKER.md
```

Dokumen progres sebelumnya merupakan bukti historis yang harus diverifikasi, bukan jaminan bahwa hasilnya masih benar.

Jangan mengulangi pekerjaan yang sudah benar-benar PASS.

Jangan mengabaikan pekerjaan PARTIAL, FAILED, atau BLOCKED.

---

# 3. DOCUMENT AUTHORITY & TRACEABILITY

Gunakan hierarki tanggung jawab:

| Dokumen | Fungsi                                      |
| ------- | ------------------------------------------- |
| PRD     | Kebutuhan produk dan bisnis                 |
| TRD     | Persyaratan teknologi dan nonfungsional     |
| AFD     | User flow dan workflow bisnis               |
| DBD     | UI/UX dan visual design                     |
| BSD     | Database, domain invariants, backend schema |
| IPD     | Task, milestone, dependensi, acceptance     |

Ketentuan:

1. Gunakan isi aktual dokumen di repository.
2. Jangan mengganti spesifikasi dengan asumsi.
3. Jangan menciptakan business rules yang tidak didukung dokumen.
4. Jangan menganggap laporan agent sebagai persetujuan Product Owner.
5. Identifikasi perbedaan antar dokumen.
6. Dokumentasikan penyelesaian konflik.
7. Pertahankan traceability requirement → implementasi → test.
8. Jangan mengubah scope tanpa alasan dan pencatatan perubahan.

Jika ada konflik yang benar-benar menghalangi pekerjaan, tandai task terkait BLOCKED.

Tetap lanjutkan task independen yang aman.

---

# 4. MANDATORY M0 REVALIDATION

Laporan sebelumnya mengklaim M0 FOUNDATION_READY: PASS.

Sebelum melanjutkan M1, lakukan audit singkat tetapi berbasis bukti terhadap klaim tersebut.

## 4.1 Audit database schema

Periksa secara langsung isi `doc/BSD.md`.

Terdapat indikasi perbedaan antara laporan audit 14 tabel dengan rancangan sebelumnya yang menggunakan 19 tabel.

Verifikasi secara khusus:

- `order_handoffs`
- `payment_voids`
- `delivery_status_history`
- `idempotency_records`
- `audit_logs`

Tentukan skema yang benar berdasarkan dokumen aktual dan kebutuhan yang disetujui.

Jangan menghapus tabel penting atau mengubah database secara sepihak.

## 4.2 Audit business decisions

Periksa `DECISION-REGISTER.md`.

Keputusan tentang pembulatan berat, minimum berat, penomoran nota, biaya antar-jemput, void, refund, tracking token, dan retensi tidak otomatis sah hanya karena pernah dituliskan agent.

Bedakan:

- APPROVED_BY_OWNER
- DOCUMENTED_REQUIREMENT
- PROPOSED
- PENDING_APPROVAL
- BLOCKED

Jangan menganggap keputusan agent sebagai approval dari pemilik produk.

## 4.3 Audit PostgreSQL

Verifikasi:

- PostgreSQL 17 benar-benar tersedia.
- Database development dapat diakses.
- Credential aplikasi valid.
- SQLAlchemy dapat terhubung.
- Alembic membaca metadata.
- Migration dapat dijalankan pada database development/test yang aman.

Jangan menebak password.

Jangan menggunakan SQLite sebagai satu-satunya bukti bahwa PostgreSQL telah terverifikasi.

Jika database credentials belum tersedia, buat panduan setup aman dan kerjakan task lain yang independen.

## 4.4 Audit pengujian

Jalankan ulang pengujian relevan jika lingkungan memungkinkan:

- Pytest
- Ruff
- Mypy
- Frontend lint
- Frontend typecheck
- Frontend production build
- npm dependency audit
- OpenAPI validation

Bila ditemukan kegagalan, perbaiki akar masalahnya.

Jangan mengubah test supaya kegagalan tersembunyi.

## 4.5 Hasil M0 revalidation

Buat:

`doc/implementation/M0-REVALIDATION.md`

Catat hasil sebenarnya.

Jika terdapat gap, perbaiki task M0 yang berada dalam kewenangan agent dan masih dapat diuji.

Jangan membuang seluruh implementasi M0 yang sudah berhasil.

Setelah fondasi valid, lanjutkan otomatis ke M1.

---

# 5. CODEGRAPH-FIRST ENGINEERING

Sebelum melakukan perubahan kode:

1. Baca `doc/CODEGRAPH-GUIDE.md`.
2. Periksa `codegraph status`.
3. Sinkronisasi indeks apabila diperlukan.
4. Gunakan CodeGraph untuk eksplorasi kode.
5. Periksa symbols, dependencies, callers, callees, dan affected tests.
6. Tentukan change impact sebelum perubahan signifikan.

Gunakan MCP CodeGraph jika tersedia.

Jika CodeGraph tidak dapat mengindeks suatu file, gunakan pembacaan file langsung.

Jangan melakukan recursive scanning besar berulang kali tanpa alasan.

Setelah perubahan modul atau dependency penting, jalankan kembali `codegraph sync`.

CodeGraph bukan pengganti unit test dan integration test.

---

# 6. ENGINEERING SKILLS

Baca file `SKILL.md` untuk skill yang relevan sebelum digunakan.

## Backend engineering

- `fastapi`
- `tdd`
- `security-audit`

## Frontend dan UI/UX

- `ui-taste`
- `ios-design`
- `antislop`
- `antislop-ui`
- `antislop-layoutmobile`
- `antislop-code`
- `antislop-copywriting`

## Architecture & code quality

- `improve-codebase-architecture`
- `ponytail`
- `ponytail-audit`
- `ponytail-review`
- `ponytail-debt`
- `ponytail-gain`

Terapkan skill secara selektif berdasarkan jenis task.

Jangan menjalankan seluruh skill untuk setiap perubahan kecil.

Jangan menggunakan integrasi eksternal berbayar yang tidak diperlukan.

Terapkan:

- SOLID
- KISS
- DRY secara proporsional
- YAGNI
- Separation of concerns
- Minimal diff
- Secure by design
- Testability
- Maintainability

Hindari overengineering dan dependency yang tidak memiliki kegunaan jelas.

---

# 7. IMPLEMENTATION EXECUTION POLICY

Gunakan **IPD sebagai master execution plan**.

Jangan membuat rencana baru yang menggantikan IPD.

Setiap task harus memiliki:

- ID sesuai IPD
- Requirement reference
- Dependencies
- Priority
- Scope
- Acceptance criteria
- Implementation files
- Test evidence
- Status

## 7.1 Status task

Gunakan:

- NOT_STARTED
- IN_PROGRESS
- IMPLEMENTED
- TESTED
- PASS
- PARTIAL
- BLOCKED
- FAILED

Task hanya boleh PASS apabila seluruh acceptance criteria relevan terpenuhi.

## 7.2 Vertical slice

Kerjakan fitur secara end-to-end:

Requirement → Database → Backend → API → Frontend → Integration → Test → Acceptance.

Jangan membuat semua backend terlebih dahulu lalu meninggalkan frontend kosong.

Jangan hanya membuat tampilan tanpa API nyata jika task menuntut integrasi.

## 7.3 Autonomous continuation

Setelah task selesai:

1. Jalankan pengujian.
2. Perbaiki kegagalan.
3. Verifikasi acceptance.
4. Update tracker.
5. Pilih task berikutnya berdasarkan dependensi.
6. Lanjutkan implementasi dalam sesi yang tersedia.

Setelah satu milestone PASS, lanjutkan milestone berikutnya.

Jangan berhenti hanya untuk meminta instruksi "lanjutkan" apabila semua informasi dan izin yang diperlukan sudah tersedia.

Jika terdapat keputusan bisnis atau tindakan berisiko yang memerlukan persetujuan, catat blocker, lanjutkan pekerjaan independen, dan laporkan kebutuhan persetujuan tersebut.

Apabila batas sesi tercapai, tinggalkan checkpoint lengkap agar pekerjaan dapat dilanjutkan pada sesi berikutnya.

Jangan mengklaim proses berlangsung secara background setelah sesi berakhir.

---

# 8. MILESTONE M0 — PROJECT FOUNDATION

Audit dan selesaikan:

- Repository setup
- Backend configuration
- Frontend configuration
- SQLAlchemy
- PostgreSQL
- Alembic
- Logging
- Error handling
- Request ID
- Security headers
- Health API
- OpenAPI
- CI
- Testing baseline
- Threat model
- Environment security

Pastikan semua task M0 memiliki bukti yang benar.

**Acceptance Gate: FOUNDATION_READY**

Apabila telah tervalidasi, lanjutkan ke M1.

---

# 9. MILESTONE M1 — AUTHENTICATION & BUSINESS CONFIGURATION

Implementasikan seluruh requirement M1 sesuai IPD.

## Backend

- Businesses
- Business settings
- Users
- User sessions
- Password hashing
- Login
- Logout
- Session validation
- Session expiry
- Session revocation
- CSRF protection
- Login throttling
- Role-based authorization
- Resource authorization
- Owner-managed user accounts

## Frontend

- Login page
- Authenticated layout
- Role-based navigation
- Session restoration
- Account settings
- User management
- Loading/error states
- Logout confirmation

## Database

Buat migration untuk tabel yang diperlukan dengan integritas constraint dan foreign key sesuai BSD.

## Testing

Minimal:

- Valid login
- Invalid login
- Inactive user
- Expired session
- Revoked session
- Logout
- CSRF
- RBAC
- Unauthorized access
- Owner user management
- Frontend authentication E2E

**Acceptance Gate: AUTH_RBAC_READY**

Setelah PASS, lanjutkan otomatis ke M2.

---

# 10. MILESTONE M2 — CORE LAUNDRY OPERATIONS

Implementasikan:

## Backend

- Customers
- Services catalog
- Pricing engine
- Orders
- Order items
- Order status history
- State machine
- Order update
- Order cancellation
- Handoff preparation
- Price snapshots
- Order number generation
- Transaction boundaries
- Idempotency

## Frontend

- Customer management
- Service management
- Create order
- Order list
- Order detail
- Order status update
- Order timeline
- Price calculation preview
- Responsive operational UI

## Critical requirements

- Money calculation must be exact.
- Domain rules must match approved decisions.
- Order creation must be atomic.
- Invalid state transitions must be rejected.
- Concurrent changes must be controlled.
- Price snapshots must remain consistent.

## Testing

- Single-service order
- Multi-service order
- Pricing rules
- Invalid quantity
- Duplicate request prevention
- State transitions
- Concurrency
- Cancellation
- Mobile E2E

**Acceptance Gate: CORE_LAUNDRY_READY**

Setelah PASS, lanjutkan otomatis ke M3.

---

# 11. MILESTONE M3 — FINANCE & DIGITAL INVOICES

Implementasikan:

- Cash payment
- Bank transfer manual
- QRIS manual
- Down payment
- Full payment
- Outstanding balance
- Payment history
- Payment void
- Expense management
- Invoice read model
- PDF invoice generation
- Manual WhatsApp share
- Payment UI
- Invoice UI
- Finance transaction tests

## Financial invariants

- Payment must be verified.
- Payment cannot exceed valid outstanding balance.
- Payment status must be derived from valid payment records.
- Duplicate payment requests must be prevented.
- Concurrent payment requests must preserve correctness.
- Void must remain auditable.
- Refund is not automatically equivalent to void.
- No floating-point money calculations.

Periksa kesesuaian model `payment_voids` dengan dokumen BSD sebelum implementasi.

**Acceptance Gate: FINANCE_INVOICE_READY**

Setelah PASS, lanjutkan otomatis ke M4.

---

# 12. MILESTONE M4 — PUBLIC TRACKING

Implementasikan:

- Secure tracking tokens
- Hashed token storage
- Token expiration
- Token revocation
- Token rotation
- Public tracking API
- Restricted public response
- Order progress timeline
- Pickup/delivery information
- Payment summary yang diizinkan
- Mobile public tracking UI
- Rate limiting
- Privacy protection

Token harus memiliki entropy yang memadai dan tidak boleh mudah ditebak.

Jangan menyimpan raw token pada log.

Jangan membocorkan nomor telepon lengkap, alamat lengkap, maupun catatan internal.

Uji IDOR dan unauthorized access.

**Acceptance Gate: PUBLIC_TRACKING_READY**

Setelah PASS, lanjutkan otomatis ke M5.

---

# 13. MILESTONE M5 — PICKUP & DELIVERY

Implementasikan:

- Public pickup request
- Admin confirmation
- Courier assignment
- Pickup state machine
- Pickup progress
- Pickup-to-order conversion
- Delivery task creation
- Delivery assignment
- Delivery state machine
- Failed delivery
- Rescheduling
- Order handoff
- Order completion rules
- Courier dashboard
- Tracking integration

Gunakan transaksi atomik untuk pickup-to-order conversion.

Cegah konversi ganda.

Pastikan status order, pembayaran, dan delivery mengikuti aturan bisnis yang disetujui.

Jangan menyamakan status DELIVERED dengan COMPLETED jika syarat handoff belum terpenuhi.

**Acceptance Gate: PICKUP_DELIVERY_READY**

Setelah PASS, lanjutkan otomatis ke M6.

---

# 14. MILESTONE M6 — DASHBOARD & REPORTING

Implementasikan:

- Owner dashboard
- Cashier dashboard
- Daily order metrics
- Monthly order metrics
- Revenue received
- Outstanding balance
- Expenses
- Overdue orders
- Orders by status
- Financial reports
- Date filters
- CSV export
- Dashboard charts
- Responsive report UI

Gunakan perhitungan backend dan query database yang konsisten.

Jangan menyamakan omset pesanan dengan uang kas diterima.

Lakukan reconciliation antara data dashboard dan transaksi sumber.

**Acceptance Gate: REPORTING_READY**

Setelah PASS, lanjutkan otomatis ke M7.

---

# 15. MILESTONE M7 — QUALITY & SECURITY HARDENING

Lakukan pengujian menyeluruh terhadap aplikasi.

## Backend

- Unit testing
- API testing
- PostgreSQL integration testing
- Concurrency testing
- Authorization testing
- Error handling testing
- Data integrity testing

## Frontend

- Component testing
- Route testing
- Form validation testing
- Responsive testing
- Accessibility testing
- Browser E2E testing
- Visual regression testing jika infrastrukturnya tersedia

## Security

- RBAC
- CSRF
- IDOR
- XSS
- SQL injection
- Authentication bypass
- Session fixation
- Session expiration
- Public token abuse
- Data leakage
- Brute-force protection
- Sensitive logging
- Dependency vulnerabilities

## Performance

Gunakan target performa dari TRD dan IPD.

Bangun data uji sintetis.

Ukur p95 latency pada lingkungan pengujian yang terdokumentasi.

Jangan mengklaim memenuhi performance target tanpa benchmark nyata.

## Recovery

Siapkan backup procedure dan uji restore pada data development/test yang aman.

## User Acceptance Test

Siapkan test scenario dan checklist untuk Owner, Cashier, Staff, Courier, dan pelanggan publik.

Jika penerimaan manusia belum dilakukan, tandai UAT sebagai PENDING_APPROVAL, bukan PASS.

**Acceptance Gate: RELEASE_CANDIDATE_READY**

Setelah seluruh kriteria yang dapat diverifikasi terpenuhi, lanjutkan otomatis ke M8 preparation.

---

# 16. MILESTONE M8 — PRODUCTION READINESS

Siapkan:

- Production configuration
- Environment variables
- Secure secret handling
- PostgreSQL production setup guide
- Migration procedure
- HTTPS configuration
- Deployment scripts
- CI/CD configuration
- Backup and restore plan
- Logging and monitoring
- Production smoke tests
- Rollback procedure
- Operations documentation
- Release notes

## Important restrictions

Agent boleh menyiapkan artefak deployment.

Namun, jangan:

- Melakukan deployment publik tanpa persetujuan.
- Mengakses atau menghapus database produksi tanpa izin.
- Menggunakan layanan berbayar tanpa persetujuan.
- Mengirim pesan kepada pelanggan nyata.
- Mengubah DNS/domain tanpa persetujuan.
- Melakukan destructive migration pada database nyata.
- Melakukan force push ke remote repository.

Jika persetujuan produksi belum diberikan, selesaikan deployment preparation dan tandai tindakan go-live sebagai BLOCKED atau PENDING_APPROVAL.

**Acceptance Gate: PRODUCTION_READY**

Gate hanya dinyatakan PASS setelah bukti produksi dan approval sebenarnya tersedia.

---

# 17. FRONTEND DESIGN ENGINEERING

Gunakan DBD sebagai acuan.

Pertahankan arah visual:

**Clean, Fresh & Trustworthy.**

Rancangan visual:

- White surfaces.
- Deep teal primary.
- Neutral slate.
- Modern typography.
- Consistent border radius.
- Professional spacing.
- Lucide icons.
- Clear information hierarchy.
- Mobile-first layouts.
- Touch-friendly interactions.

Gunakan:

- React.
- Tailwind CSS 4.
- shadcn/ui.
- Radix UI.
- TanStack Query.
- React Hook Form.
- Zod.

Pastikan:

1. Loading state.
2. Empty state.
3. Error state.
4. Success feedback.
5. Form validation.
6. Confirmation dialog.
7. Responsive navigation.
8. Keyboard accessibility.
9. Touch targets yang memadai.
10. Tidak ada horizontal overflow.

Jangan menggunakan animasi dekoratif berlebihan.

Jangan menampilkan angka dashboard palsu sebagai data asli.

Jangan menggunakan tombol dekoratif tanpa fungsi.

Pastikan seluruh halaman utama tersambung dengan backend sesuai kontrak API.

---

# 18. BACKEND ARCHITECTURE ENFORCEMENT

Pertahankan Modular Monolith.

Gunakan:

Router → Application Service → Domain → Repository.

Aturan:

- Router untuk HTTP boundary.
- Service untuk orchestration.
- Domain untuk business invariants.
- Repository untuk persistence.
- SQLAlchemy models untuk database.
- Pydantic schemas untuk input/output.
- Alembic untuk migration.
- PostgreSQL untuk database produksi dan integration testing.

Pastikan:

- Transaction boundary jelas.
- Tidak ada circular dependency antarmodul.
- Tidak ada business logic keuangan pada frontend.
- Tidak ada query database langsung di router.
- Tidak ada `commit()` tersembunyi yang merusak transaksi lintas modul.
- Tidak ada foreign key rusak.
- Tidak ada duplicate payment.
- Tidak ada duplicate pickup conversion.

Gunakan database constraint untuk memperkuat invariants yang perlu ditegakkan secara atomik.

---

# 19. TESTING & VERIFICATION PROTOCOL

Untuk setiap task:

1. Tentukan acceptance test.
2. Implementasikan perubahan.
3. Jalankan test yang relevan.
4. Jalankan lint/typecheck.
5. Lakukan integration testing bila diperlukan.
6. Perbaiki seluruh bug yang berada dalam scope.
7. Periksa regresi.
8. Catat hasil.
9. Update tracker.
10. Lanjutkan task berikutnya.

Jangan mengubah, menghapus, atau melemahkan test hanya agar pipeline PASS.

Jangan menggunakan SQLite sebagai pengganti bukti transaksi PostgreSQL apabila task membutuhkan PostgreSQL.

Jangan menggunakan mock payment sebagai bukti integrasi pembayaran nyata.

Jangan menganggap halaman dapat dirender sebagai bukti workflow end-to-end berfungsi.

---

# 20. AUTOMATED MASTER TRACKER

Gunakan:

`doc/implementation/MASTER-TRACKER.md`

Sebagai sumber status implementasi.

Setiap task harus mencatat:

- Task ID
- Module
- Priority
- Dependencies
- Status
- Implemented files
- Test commands
- Test results
- Outstanding issues
- Acceptance status

Gunakan progres yang sebenarnya.

Jangan menyatakan 100% jika masih ada task BLOCKED atau NOT_STARTED.

---

# 21. REPORTING STRUCTURE

Gunakan folder:

`doc/implementation/`

Buat laporan milestone sesuai pekerjaan yang benar-benar dilakukan:

```text
doc/implementation/
├── MASTER-TRACKER.md
├── DECISION-REGISTER.md
├── M0-REPORT.md
├── M0-REVALIDATION.md
├── M1-REPORT.md
├── M2-REPORT.md
├── M3-REPORT.md
├── M4-REPORT.md
├── M5-REPORT.md
├── M6-REPORT.md
├── M7-REPORT.md
├── M8-REPORT.md
├── TEST-SUMMARY.md
├── SECURITY-AUDIT.md
├── RELEASE-READINESS.md
└── FINAL-PROJECT-REPORT.md
```

File yang belum relevan tidak perlu dibuat kosong.

## Laporan setiap milestone

Memuat:

1. Milestone objective.
2. Task list.
3. PASS/PARTIAL/BLOCKED/FAILED counts.
4. Files implemented.
5. Database changes.
6. API changes.
7. Frontend changes.
8. Test evidence.
9. Security findings.
10. Known issues.
11. Acceptance gate.
12. Next milestone readiness.

Jangan menggunakan angka test yang tidak berasal dari pengujian nyata.

---

# 22. DOCUMENTATION UPDATE POLICY

Dokumentasi awal tetap menjadi baseline proyek.

Jika implementasi menemukan kebutuhan perubahan:

1. Identifikasi konflik.
2. Jelaskan alasan.
3. Analisis dampak.
4. Periksa dependensi.
5. Tentukan apakah perlu approval.
6. Perbarui kontrak dan dokumen terkait setelah disetujui.
7. Perbarui test.
8. Catat perubahan.

Jangan melakukan perubahan besar pada dokumen agar hasil implementasi terlihat sesuai.

Dokumen harus mencerminkan keputusan yang sah dan implementasi yang terverifikasi.

---

# 23. SECURITY & DATA SAFETY RULES

Dilarang:

- Menampilkan credential pada output laporan.
- Menyimpan secret dalam repository.
- Menyimpan raw session token pada log.
- Menghapus database penting.
- Melakukan migrasi destruktif tanpa izin.
- Menggunakan data pribadi pelanggan nyata untuk test.
- Melakukan deployment tanpa approval.
- Membuka port publik tanpa kebutuhan.
- Menggunakan API berbayar secara otomatis.
- Mengubah Git history secara destruktif.

Jika diperlukan database testing, gunakan database khusus testing dan data sintetis.

Jika suatu tindakan memiliki efek eksternal atau risiko kehilangan data, mintalah persetujuan sebelum melakukannya.

---

# 24. WORK SESSION CONTINUITY

Saya ingin pekerjaan dilaksanakan dari M0 sampai M8, tetapi tetap konsisten dan dapat dilanjutkan apabila sesi terputus.

Setiap checkpoint harus memuat:

- Milestone aktif.
- Task terakhir.
- Task yang sudah PASS.
- Task yang belum selesai.
- Blocker.
- Files changed.
- Migration state.
- Test results.
- Next executable tasks.

Simpan progres aktual dalam repository.

Jika sesi berakhir, jangan mengklaim pekerjaan masih berjalan secara background.

Pada sesi berikutnya, baca tracker dan lanjutkan dari checkpoint terakhir.

Jangan mengulang seluruh implementasi dari awal.

---

# 25. FINAL COMPLETION CRITERIA

Aplikasi dianggap selesai apabila:

- Semua requirement MVP yang telah disetujui terpenuhi.
- Semua modul utama berfungsi.
- Backend dan frontend terintegrasi.
- Database migration valid.
- Business invariants konsisten.
- Autentikasi aman.
- RBAC berjalan.
- Pembayaran manual akurat.
- Public tracking aman.
- Pickup dan delivery terintegrasi.
- Invoice dapat dihasilkan.
- Dashboard dan laporan akurat.
- Responsive UI lulus.
- Critical E2E tests lulus.
- Security audit lulus.
- Backup dan restore telah diuji.
- Production readiness dinilai berdasarkan bukti.
- Dokumentasi final diperbarui.

Tidak boleh ada klaim keberhasilan hanya berdasarkan keberadaan folder atau jumlah file.

---

# 26. START AUTONOMOUS EXECUTION

Mulai sekarang.

## Execution sequence

**STEP 1:** Baca seluruh dokumen utama dan agent directives.

**STEP 2:** Jalankan CodeGraph-first repository discovery.

**STEP 3:** Audit kondisi aktual backend/frontend.

**STEP 4:** Revalidasi klaim hasil M0 dan perbaiki gap.

**STEP 5:** Sinkronkan requirements matrix dan task tracker.

**STEP 6:** Kerjakan task M1 berdasarkan IPD.

**STEP 7:** Jalankan pengujian dan acceptance gate M1.

**STEP 8:** Jika PASS, lanjutkan M2.

**STEP 9:** Teruskan secara berurutan sampai M7 dan persiapan M8.

**STEP 10:** Susun final audit, deployment readiness, dan dokumentasi akhir.

Jangan berhenti hanya untuk membuat rencana baru.

Jangan meminta persetujuan untuk setiap perubahan kode biasa yang sudah termasuk scope.

Jangan memaksa PASS pada gate yang belum terpenuhi.

Jangan melewati blocker kritis.

Kerjakan seluruh task yang dapat dikerjakan secara aman dalam sesi eksekusi yang tersedia.

---

# FINAL EXECUTION DIRECTIVE

**EXECUTE THE EXISTING PLAN. DO NOT REWRITE THE PROJECT PLAN.**

Gunakan PRD, TRD, AFD, DBD, BSD, dan IPD sebagai kontrak pengembangan.

Implementasikan sistem nyata secara end-to-end.

Gunakan CodeGraph untuk memahami kode.

Gunakan skills yang relevan untuk meningkatkan kualitas engineering.

Gunakan tests untuk membuktikan correctness.

Gunakan acceptance gates untuk mengendalikan progres.

Gunakan MASTER-TRACKER untuk melanjutkan pekerjaan.

**Tujuan akhir adalah aplikasi E-Laundry 2.0 yang lengkap, aman, responsif, teruji, dapat dipelihara, dan siap digunakan sesuai persetujuan pemilik produk.**

**START IMPLEMENTATION NOW.**
