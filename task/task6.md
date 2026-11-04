# TASK — E-LAUNDRY 2.0 DOCUMENTATION SYNCHRONIZATION & IMPLEMENTATION CHECKLIST

## MODE: DOCUMENTATION-ONLY EXECUTION

### Scope: PRD, TRD, AFD, DBD, BSD, IPD

### Objective: Update Documentation Based on Actual Existing Codebase

### Strict Rule: DO NOT MODIFY APPLICATION SOURCE CODE

# 1. ROLE & MISSION

Berperanlah sebagai:

- Principal Software Architect
- Senior Technical Documentation Engineer
- Software Requirements Analyst
- Full-Stack Codebase Auditor
- Database Documentation Specialist
- QA & Requirements Traceability Engineer

Tugas Anda adalah membaca seluruh source code E-Laundry 2.0 yang telah dikembangkan pada milestone M0–M8, kemudian **memperbarui enam dokumen utama dengan status implementasi, checklist progres, referensi kode, dan bukti pengujian yang tersedia**.

Tujuan:

**MENYINKRONKAN DOKUMENTASI DENGAN KONDISI IMPLEMENTASI AKTUAL TANPA MENGUBAH SOURCE CODE ATAU MENGHAPUS KEBUTUHAN ASLI.**

Ini merupakan pekerjaan DOCUMENTATION-ONLY.

Jangan menjalankan task pengembangan fitur.

Jangan melakukan bug fixing.

Jangan mengubah struktur aplikasi.

Jangan melakukan refactoring.

Jangan mengubah database.

Jangan membuat migration.

Jangan mengubah tests.

---

# 2. PROJECT WORKSPACE

Repository root:

`D:\Kuliah\joki\Kerja Praktek Aqil\kawan aqil\projek`

Enam dokumen yang diizinkan untuk diperbarui:

1. `doc/PRD.md`
2. `doc/TRD.md`
3. `doc/AFD.md`
4. `doc/DBD.md`
5. `doc/BSD.md`
6. `doc/IPD.md`

Seluruh file selain keenam dokumen tersebut bersifat READ-ONLY.

File pendukung yang boleh dibaca:

- `AGENTS.md`
- `doc/SKILLS-CATALOG.md`
- `doc/CODEGRAPH-GUIDE.md`
- `doc/api/openapi.json`
- `doc/implementation/MASTER-TRACKER.md`
- Seluruh laporan M0–M8
- Seluruh audit dan test reports
- Backend source code
- Frontend source code
- SQLAlchemy models
- Alembic migrations
- Test suites
- Docker configuration

Jangan memperbarui laporan lama untuk menyembunyikan ketidaksesuaian.

---

# 3. ABSOLUTE NO-CODE-CHANGE POLICY

**Hanya file Markdown berikut yang boleh diubah:**

- `doc/PRD.md`
- `doc/TRD.md`
- `doc/AFD.md`
- `doc/DBD.md`
- `doc/BSD.md`
- `doc/IPD.md`

Dilarang mengubah:

- `backend/**`
- `frontend/**`
- `scripts/**`
- `docker-compose*.yml`
- `nginx/**`
- `.env`
- `.env.example`
- Alembic migration files
- Test files
- Dependency manifests
- Lock files
- OpenAPI JSON
- `.codegraph/**`
- Git configuration

Gunakan CodeGraph dalam mode READ-ONLY jika tersedia.

Jangan menjalankan CodeGraph sync atau perintah lain yang mengubah file indeks.

Jangan menginstal dependency atau menjalankan formatter yang berpotensi menulis ke source code.

Jika perintah pemeriksaan menghasilkan cache atau artifact baru, hindari perintah tersebut pada task ini.

Sebelum dan sesudah pekerjaan, catat `git status` dan `git diff` untuk membuktikan bahwa hanya keenam dokumen yang berubah akibat task ini.

Jangan melakukan commit, reset, checkout destruktif, atau menghapus perubahan pengguna.

---

# 4. DOCUMENTATION AUTHORITY & PRESERVATION RULES

Enam dokumen ini merupakan baseline spesifikasi proyek.

**PENTING: Dokumentasi requirement tidak boleh diubah menjadi sekadar deskripsi perilaku kode yang ada.**

Bedakan dua konsep:

1. **REQUIRED BEHAVIOR:** Perilaku yang seharusnya ada berdasarkan dokumentasi dan keputusan bisnis yang sah.
2. **IMPLEMENTED BEHAVIOR:** Perilaku yang saat ini benar-benar dilakukan kode aplikasi.

Jika keduanya berbeda:

- Pertahankan requirement asli.
- Dokumentasikan perbedaannya.
- Tandai sebagai MISMATCH.
- Cantumkan file yang terdampak.
- Cantumkan bukti.
- Jangan mengubah requirement untuk membenarkan bug.

Jangan menganggap keputusan yang masih berstatus Draft atau Pending sebagai keputusan yang telah disetujui.

Jangan menaikkan status PRD menjadi Approved tanpa persetujuan pengguna.

Jangan mengubah scope MVP secara sepihak.

Gunakan pendekatan additive documentation updates: tambahkan status, checklist, dan referensi implementasi di lokasi yang relevan dengan perubahan editorial seminimal mungkin.

---

# 5. PHASE A — FULL CODEBASE INVENTORY

Lakukan audit READ-ONLY terhadap seluruh aplikasi.

## Backend

Periksa:

- FastAPI routers.
- Application services.
- Domain services.
- Business invariants.
- Authentication.
- RBAC.
- Customer management.
- Service catalog.
- Order management.
- Finance and payment.
- Invoice and PDF.
- Public tracking.
- Pickup and delivery.
- Dashboard and reports.
- Audit logging.
- Idempotency.
- Error handling.
- Database models.
- Alembic migrations.

## Frontend

Periksa:

- React routes.
- Pages and layouts.
- Forms.
- Tables.
- Modals.
- Dashboard.
- Customer management.
- Order management.
- Payment screens.
- Invoice interfaces.
- Public tracking.
- Pickup request.
- Courier views.
- Settings.
- Role-specific navigation.
- Responsive behavior.

## Database

Periksa:

- Tables.
- Columns.
- Relationships.
- Constraints.
- Indexes.
- Registered SQLAlchemy models.
- Migration revision chain.
- Foreign keys across milestones.

## Testing and Evidence

Periksa:

- Existing pytest tests.
- Playwright tests.
- Integration reports.
- Audit reports.
- Test results.
- Previous milestone acceptance reports.

Bedakan keberadaan test dari keberhasilan test yang benar-benar dijalankan.

Bedakan SQLite, mocked API, PostgreSQL integration, dan real E2E.

Jangan menyatakan real PostgreSQL verification PASS jika bukti yang tersedia hanya SQLite atau Alembic offline SQL generation.

---

# 6. PHASE B — CHECKLIST STATUS STANDARD

Gunakan format checklist Markdown standar.

## Implemented & Verified

- [x] **PASS** — Fitur telah diimplementasikan, sesuai requirement, dan memiliki bukti pengujian relevan yang berhasil.

## Implemented but Unverified

- [ ] **NOT_VERIFIED** — Kode ditemukan tetapi pengujian yang diperlukan belum terbukti berhasil.

## Partially Implemented

- [ ] **PARTIAL** — Sebagian kebutuhan tersedia, tetapi ada komponen atau perilaku yang belum lengkap.

## Missing

- [ ] **MISSING** — Requirement belum ditemukan implementasinya.

## Specification Mismatch

- [ ] **MISMATCH** — Implementasi berbeda atau bertentangan dengan spesifikasi.

## External Blocker

- [ ] **BLOCKED** — Verifikasi tidak dapat diselesaikan karena kendala lingkungan atau dependency eksternal.

## Out of Scope

- [ ] **OUT_OF_SCOPE** — Fitur tidak diwajibkan pada MVP yang berlaku.

## Decision Required

- [ ] **DECISION_REQUIRED** — Terdapat konflik atau keputusan bisnis yang belum disahkan.

Aturan penting:

**Checklist `[x]` hanya boleh diberikan jika implementasi dan bukti pengujian relevan mendukung status PASS.**

Jangan menandai PASS hanya karena file source code tersedia.

Jangan menganggap test berbasis mock membuktikan integrasi produksi.

Jangan mengubah semua checklist menjadi `[x]` untuk mengejar angka 100%.

---

# 7. PHASE C — UPDATE PRD.md

Perbarui `doc/PRD.md` dengan checklist implementasi berdasarkan fitur resmi.

PRD tetap menjadi dokumen kebutuhan produk.

Jangan mengubah deskripsi bisnis, prioritas, aturan, atau acceptance criteria asli.

## A. Feature Implementation Checklist

Gunakan seluruh Feature ID yang sudah didefinisikan.

### Dashboard

`DASH-01` sampai `DASH-10`

### Orders

`ORD-01` sampai `ORD-18`

### Customers

`CUS-01` sampai `CUS-09`

### Pickup & Delivery

`PUD-01` sampai `PUD-14`

### Finance

`FIN-01` sampai `FIN-15`

### Digital Invoice

`INV-01` sampai `INV-10`

### Public Tracking

`TRK-01` sampai `TRK-12`

### Settings

`SET-01` sampai `SET-13`

Periksa jumlah dan prioritas langsung dari PRD aktual.

Untuk tiap fitur, tambahkan checklist di lokasi yang relevan dengan ID dan judul asli, status, serta referensi kode atau pengujian.

Contoh:

- [x] **ORD-01 — Membuat pesanan baru** | PASSImplementasi: `backend/app/modules/orders/service.py`Evidence: `backend/tests/api/test_orders_api.py`
- [ ] **PUD-12 — Reschedule dan pembatalan tugas** | PARTIALImplementasi: [lokasi kode aktual]Gap: [perilaku yang belum tersedia]
- [ ] **TRK-10 — Pencabutan atau penggantian token** | NOT_VERIFIED
      Implementasi: [lokasi kode aktual]
      Missing evidence: [pengujian yang belum ditemukan]

Contoh hanyalah format, bukan penetapan status sebenarnya.

## B. Acceptance Test Checklist

Tambahkan atau perbarui status:

`AT-01` sampai `AT-30`.

Setiap AT harus memiliki:

- Status.
- Test yang tersedia.
- Bukti eksekusi bila ada.
- Missing evidence bila belum lulus.
- Catatan dependency.

## C. PRD Implementation Summary

Tambahkan bagian singkat:

`Implementation Status — As-Built Assessment`

Memuat:

- Total fitur P0/P1/P2.
- Fitur PASS.
- Fitur PARTIAL.
- Fitur MISSING.
- Fitur NOT_VERIFIED.
- Fitur MISMATCH.
- Fitur OUT_OF_SCOPE.
- Acceptance tests PASS/FAIL/BLOCKED.

Jangan mengubah requirement yang belum dipenuhi menjadi opsional hanya karena belum diimplementasikan.

---

# 8. PHASE D — UPDATE TRD.md

Perbarui `doc/TRD.md` dengan checklist kepatuhan teknis aktual.

Audit dan beri status pada:

- Technology stack.
- Backend architecture.
- Frontend architecture.
- Database integration.
- API contracts.
- Authentication.
- Authorization.
- CSRF protection.
- Session management.
- Security headers.
- Data validation.
- Error handling.
- Logging.
- Database migrations.
- Transaction consistency.
- Concurrency protection.
- Performance requirements.
- Backup and recovery.
- Docker and containerization.
- Deployment configuration.
- Monitoring.
- Testing infrastructure.
- CI/CD if required.

Gunakan checklist di bawah bagian teknis yang sesuai atau status matrix yang mereferensikan section aslinya.

Contoh:

- [x] **Backend Framework** — FastAPIEvidence: `backend/app/main.py`
- [ ] **PostgreSQL Transaction Integration** — NOT_VERIFIEDReason: Belum ada bukti pengujian transaksi dengan PostgreSQL nyata.
- [ ] **Docker Runtime Verification** — BLOCKED
      Reason: Docker CLI belum tersedia pada lingkungan yang diperiksa.

Sesuaikan seluruh status dengan fakta repository dan bukti yang ditemukan.

Jangan menggunakan klaim deployment report sebagai pengganti eksekusi container aktual.

---

# 9. PHASE E — UPDATE AFD.md

Perbarui `doc/AFD.md` dengan status implementasi workflow dan state machine.

Audit seluruh alur:

1. Authentication.
2. Owner management.
3. Customer management.
4. Order intake.
5. Service selection.
6. Pricing calculation.
7. Laundry processing.
8. Order cancellation.
9. Payment and DP.
10. Payment correction.
11. Invoice generation.
12. Public tracking.
13. Pickup request.
14. Pickup confirmation.
15. Courier assignment.
16. Pickup-to-order conversion.
17. Delivery workflow.
18. Physical handoff.
19. Order completion.
20. Dashboard and reporting.

Untuk setiap workflow:

- Cantumkan workflow ID/section asli.
- Checklist implementasi.
- Backend implementation reference.
- Frontend implementation reference jika relevan.
- Test reference.
- Status.
- Gap atau mismatch.

Jangan mengganti diagram atau aturan status hanya untuk menyamakan implementasi.

Jika state machine kode tidak sesuai AFD, dokumentasikan perbedaannya.

Perhatikan secara khusus:

- Perubahan status yang tidak sah.
- Handoff order.
- Order yang masih memiliki piutang.
- Konversi pickup menjadi order.
- Delivery failure dan rescheduling.
- Tracking continuity.

---

# 10. PHASE F — UPDATE DBD.md

`DBD.md` adalah Design Brief Documentation untuk UI/UX.

Jangan menganggapnya sebagai Database Design Document.

Perbarui status implementasi UI/UX berdasarkan frontend aktual.

Audit:

- Design tokens.
- Typography.
- Color palette.
- Layout.
- Navigation.
- Dashboard.
- Forms.
- Tables.
- Dialogs.
- Error states.
- Loading states.
- Empty states.
- Success feedback.
- Accessibility.
- Mobile responsiveness.
- Touch targets.
- Consistency across roles.

Untuk setiap halaman atau komponen yang diwajibkan DBD, tambahkan:

- Checklist status.
- Route aktual.
- Component/page file.
- Screenshot/test reference bila tersedia.
- Gap atau catatan validasi.

Jangan menyatakan seluruh UI memenuhi accessibility hanya karena aplikasi berhasil di-build.

Jika audit visual manual belum tersedia, gunakan NOT_VERIFIED.

Pertahankan seluruh desain dan visual requirement asli.

---

# 11. PHASE G — UPDATE BSD.md

Perbarui `doc/BSD.md` dengan checklist implementasi backend dan database.

Audit:

- Entity catalog.
- 19 core tables jika masih sesuai BSD aktual.
- SQLAlchemy models.
- Alembic migrations.
- Foreign keys.
- Constraints.
- Indexes.
- API data contracts.
- Financial invariants.
- Business domain invariants.
- Audit logs.
- Idempotency.
- Token tracking.
- Access controls.
- Transaction boundaries.
- Concurrency controls.

Untuk setiap entity:

- Checklist model implementation.
- Checklist migration availability.
- Checklist PostgreSQL migration verification.
- Checklist constraints verification.
- References ke model/migration.
- Gap jika ada.

Contoh:

**Entity: audit_logs**

- [x] Model tersedia.
- [x] Alembic migration tersedia.
- [ ] PostgreSQL migration execution — NOT_VERIFIED.

Contoh hanya menjelaskan format; status final harus berasal dari repository aktual.

Catat seluruh tabel tambahan yang ditemukan tanpa langsung menganggapnya pelanggaran.

Periksa apakah tabel tambahan mempunyai justifikasi dan tidak menghilangkan entitas wajib.

Jangan mengubah definisi schema canonical agar cocok dengan bug.

---

# 12. PHASE H — UPDATE IPD.md

IPD menjadi dokumen utama untuk melihat progres seluruh milestone.

Audit seluruh task ID resmi IPD dari M0 sampai M8.

Jangan mengandalkan angka 98, 108, atau jumlah lain dari laporan sebelumnya.

Ekstrak task IDs dari IPD asli dan hitung secara aktual.

Untuk setiap task ID:

- Status checklist.
- Requirement reference.
- Actual implementation reference.
- Test/evidence reference.
- Gap.
- Dependency/blocker.

Contoh:

- [x] **M2-06 — Pricing Engine** | PASSCode: `backend/app/modules/orders/domain/pricing.py`Test: `backend/tests/unit/test_pricing.py`
- [ ] **M7-XX — PostgreSQL Concurrency Verification** | NOT_VERIFIED
      Reason: Belum ditemukan bukti real PostgreSQL concurrency test.

Jangan memakai contoh ID sebagai sumber penomoran jika IPD aktual berbeda.

## Milestone Overview

Tambahkan ringkasan status per milestone:

| Milestone | Total Tasks | PASS | PARTIAL | MISSING | NOT_VERIFIED | BLOCKED |
| --------- | ----------: | ---: | ------: | ------: | -----------: | ------: |

## Progress Calculation

Hitung progres berdasarkan total task resmi.

Jika suatu task mempunyai beberapa acceptance criteria, jangan tandai PASS sebelum seluruh kriteria wajib terpenuhi.

Jangan menyatakan milestone 100% selesai hanya karena seluruh source files ditemukan.

Cantumkan:

- Total official tasks.
- Completed & verified.
- Incomplete.
- Unverified.
- Blocked.
- Remaining work.

Jangan mengubah definisi task IPD asli.

---

# 13. CROSS-DOCUMENT CONSISTENCY VALIDATION

Setelah memperbarui keenam dokumen, lakukan audit konsistensi.

Periksa:

1. Semua Feature IDs PRD tetap utuh.
2. Semua AT-01 sampai AT-30 tetap utuh.
3. Seluruh task IDs IPD tetap utuh.
4. Tidak ada perubahan prioritas tanpa persetujuan.
5. Requirement PRD tidak berubah makna.
6. Business rules AFD tidak berubah makna.
7. Technical requirements TRD tidak dilonggarkan.
8. UI/UX design requirements DBD dipertahankan.
9. BSD canonical schema tetap dipertahankan.
10. Tidak ada klaim PASS tanpa evidence.
11. Tidak ada status yang bertentangan antar dokumen.
12. Semua referensi kode menunjuk path yang benar-benar ada.
13. Semua referensi test menunjuk file test nyata.
14. Semua angka summary dihitung ulang.
15. Seluruh blocker dicantumkan dengan jelas.

Jika ditemukan konflik antar dokumen lama, catat sebagai DECISION_REQUIRED tanpa memaksakan perubahan requirement.

---

# 14. DOCUMENT FORMATTING

Pertahankan struktur asli setiap dokumen.

Jangan mengganti keseluruhan isi dokumen dengan laporan ringkas baru.

Jangan menghapus:

- Judul.
- Section.
- Diagram.
- Tabel requirement.
- User stories.
- Acceptance criteria.
- Business rules.
- Architecture decisions.
- Existing documentation references.

Gunakan:

- Markdown checklists `[x]` dan `[ ]`.
- Heading yang konsisten.
- Relative file path.
- Tabel ringkas jika dibutuhkan.
- Status yang jelas.
- Referensi source code.
- Referensi pengujian.

Usahakan checklist ditempatkan dekat requirement atau task yang bersangkutan.

Untuk section dengan banyak requirement, boleh gunakan status matrix setelah tabel requirement asli agar tidak menimbulkan duplikasi berlebihan.

Cantumkan metadata:

- Last Implementation Review Date.
- Baseline Commit SHA jika tersedia.
- Audit Scope: READ-ONLY CODEBASE ASSESSMENT.
- Evidence Limitations.

Jangan menggunakan simbol centang sebagai satu-satunya penyampai status; sertakan teks PASS, PARTIAL, atau NOT_VERIFIED.

---

# 15. REQUIRED VERIFICATION

Setelah dokumentasi diperbarui:

1. Periksa `git diff -- doc/`.
2. Pastikan hanya keenam dokumen yang diubah akibat task ini.
3. Validasi syntax Markdown secara read-only jika tersedia.
4. Periksa semua checklist.
5. Hitung ulang total status.
6. Verifikasi internal links dan relative code paths.
7. Periksa apakah ada requirement yang hilang.
8. Periksa apakah ada perubahan tidak sengaja pada dokumen.
9. Tampilkan ringkasan perubahan.
10. Jangan menjalankan application build atau migration hanya untuk task documentation sync.

Jika terdapat perubahan source code yang sudah ada sebelum task dimulai, jangan menyentuhnya. Bandingkan status sebelum dan sesudah untuk membedakan perubahan milik task ini.

---

# 16. REQUIRED FINAL OUTPUT

Setelah selesai, tampilkan:

## A. Documentation Update Summary

| Document | Sections Updated | Checklist Total | PASS | PARTIAL | NOT_VERIFIED | MISSING |
| -------- | ---------------: | --------------: | ---: | ------: | -----------: | ------: |

## B. PRD Feature Coverage

Tampilkan status fitur berdasarkan delapan modul:

- Dashboard.
- Orders.
- Customers.
- Pickup & Delivery.
- Finance.
- Digital Invoice.
- Public Tracking.
- Settings.

## C. Milestone Coverage

Tampilkan status M0 sampai M8 berdasarkan IPD.

## D. Outstanding Gaps

Tampilkan seluruh:

- MISSING.
- PARTIAL.
- MISMATCH.
- BLOCKED.
- NOT_VERIFIED.
- DECISION_REQUIRED.

Sertakan referensi section, source code, dan test.

## E. Change Integrity

Buktikan:

- 6 Markdown documents updated.
- 0 application source files modified.
- 0 test files modified.
- 0 migrations modified.
- 0 configuration files modified.
- 0 database operations performed.
- 0 deployment actions performed.

Jika salah satu dokumen memang tidak memerlukan perubahan, jelaskan alasannya dan jangan membuat perubahan semu.

---

# 17. FINAL DIRECTIVE

**READ THE REAL CODEBASE.**

**READ ALL SIX DOCUMENTS.**

**UPDATE DOCUMENTATION ONLY.**

**ADD CHECKLISTS FOR IMPLEMENTED, PARTIAL, MISSING, MISMATCHED, AND UNVERIFIED REQUIREMENTS.**

**MARK `[x]` ONLY WHEN EVIDENCE SUPPORTS PASS.**

**DO NOT CHANGE ORIGINAL REQUIREMENTS TO MATCH EXISTING BUGS.**

**DO NOT MODIFY SOURCE CODE, TESTS, DATABASE, OR CONFIGURATION.**

**DO NOT CLAIM 100% COMPLETION WITHOUT EVIDENCE.**

**PRESERVE THE ORIGINAL DOCUMENT STRUCTURE.**

**PRODUCE SIX ACCURATE, TRACEABLE, IMPLEMENTATION-AWARE DOCUMENTS.**

## START NOW

Mulai dengan membaca keenam dokumen, melakukan read-only codebase inventory, menemukan seluruh implementasi dan bukti pengujian, lalu langsung memperbarui checklist status pada dokumen yang relevan.

Selesaikan sinkronisasi seluruh enam dokumen dalam sesi aktif dan tampilkan ringkasan perubahan beserta hasil `git diff`.
