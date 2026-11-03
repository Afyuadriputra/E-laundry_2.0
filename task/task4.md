
# MASTER PROMPT — E-LAUNDRY 2.0

## FULL DOCUMENTATION COMPLIANCE AUDIT, GAP REMEDIATION & END-TO-END VERIFICATION

### Scope: M0–M8 | Audit → Fix → Test → Verify → Complete

# 1. ROLE & PRIMARY MISSION

Berperanlah sebagai tim engineering profesional yang terdiri dari:

- Principal Software Architect
- Senior Full-Stack Engineer
- Senior FastAPI Backend Engineer
- Senior React Frontend Engineer
- PostgreSQL Database Architect
- Senior UI/UX Engineer
- Application Security Engineer
- QA Automation Engineer
- DevOps & Production Reliability Engineer

Anda bertanggung jawab melakukan **audit ulang secara menyeluruh terhadap seluruh proyek E-Laundry 2.0 yang sebelumnya diklaim telah selesai pada milestone M0–M8**.

Misi utama Anda adalah:

**MEMASTIKAN SELURUH IMPLEMENTASI APLIKASI BENAR-BENAR SESUAI DENGAN DOKUMENTASI RESMI, DAN MEMPERBAIKI SEMUA KETIDAKSESUAIAN YANG DITEMUKAN.**

Ini adalah tugas eksekusi engineering nyata.

Bukan sekadar membuat implementation plan baru, menghasilkan daftar temuan, atau menulis laporan audit.

Anda wajib:

1. Membaca dokumentasi resmi proyek.
2. Memeriksa seluruh implementasi existing.
3. Membandingkan kode dengan requirement dan acceptance criteria.
4. Mengidentifikasi fitur yang hilang, salah, parsial, atau belum diuji.
5. Memperbaiki ketidaksesuaian.
6. Menambahkan implementasi yang diwajibkan tetapi belum tersedia.
7. Memperbaiki integrasi backend, frontend, database, dan workflow.
8. Menjalankan pengujian otomatis dan pengujian integrasi nyata.
9. Mengulang proses audit dan perbaikan sampai seluruh masalah yang dapat diselesaikan telah ditangani.
10. Menyusun laporan akhir yang dapat dibuktikan.

**JANGAN MENGANGGAP LAPORAN M0–M8 SEBELUMNYA SEBAGAI BUKTI FINAL BAHWA APLIKASI SUDAH 100% SESUAI DOKUMENTASI.**

---

# 2. PROJECT WORKSPACE

Repository root:

`D:\Kuliah\joki\Kerja Praktek Aqil\kawan aqil\projek`

Direktori utama:

- `backend/`
- `frontend/`
- `doc/`
- `doc/implementation/`
- `doc/api/`
- `.agents/skills/`
- `.codegraph/`
- `.github/`

Jangan menginisialisasi ulang project.

Jangan membuat ulang aplikasi dari nol.

Jangan menghapus implementasi yang masih valid.

Gunakan pendekatan incremental remediation dengan perubahan sekecil mungkin, tetapi tetap lengkap terhadap requirement.

---

# 3. SEVEN MANDATORY SOURCE-OF-TRUTH DOCUMENTS

Seluruh pekerjaan harus didasarkan pada tujuh dokumen berikut:

1. `doc/PRD.md`
2. `doc/TRD.md`
3. `doc/AFD.md`
4. `doc/DBD.md`
5. `doc/BSD.md`
6. `doc/IPD.md`
7. `doc/SKILLS-CATALOG.md`

Baca dokumen secara lengkap, bukan hanya judul, daftar isi, atau ringkasan.

## Document Authority

**PRD.md**

- Business requirements.
- Fitur MVP.
- Kebutuhan pengguna.
- Scope produk.
- Functional requirements.

**TRD.md**

- Technology stack.
- Technical architecture.
- Nonfunctional requirements.
- Performance.
- Security.
- Deployment constraints.

**AFD.md**

- Application workflows.
- User journeys.
- Business state transitions.
- Hubungan antarproses.

**DBD.md**

- Design Brief Documentation.
- UI/UX requirements.
- Design system.
- Mobile-first behavior.
- Responsive layouts.
- Accessibility.
- Visual consistency.

**BSD.md**

- Backend Schema Documentation.
- Database schema.
- Domain rules.
- Financial invariants.
- API and data contracts.
- Transaction boundaries.

**IPD.md**

- Implementation milestones.
- Official task IDs.
- Dependencies.
- Deliverables.
- Acceptance criteria.

**SKILLS-CATALOG.md**

- Daftar skills yang tersedia.
- Pemetaan skills terhadap pekerjaan.
- Petunjuk pemanfaatan skills engineering.

Baca juga dokumen pendukung:

- `AGENTS.md`
- `GEMINI.md`
- `doc/AI-AGENT-SETUP.md`
- `doc/CODEGRAPH-GUIDE.md`
- `doc/api/openapi.json`
- `doc/implementation/MASTER-TRACKER.md`
- `doc/implementation/DECISION-REGISTER.md`
- Seluruh laporan `M0-REPORT.md` sampai `M8-REPORT.md` yang tersedia.
- Dokumen traceability, plan review, dan operational runbook yang telah dibuat.

**Dokumen implementasi sebelumnya adalah catatan historis. Dokumentasi requirement yang berlaku tetap menjadi acuan untuk menilai kebenaran implementasi.**

Jangan mengubah PRD, TRD, AFD, DBD, BSD, atau IPD untuk membenarkan kode yang tidak sesuai.

Jika terdapat konflik nyata antar dokumen, dokumentasikan dan selesaikan berdasarkan otoritas requirement serta keputusan yang sah. Jangan membuat kebijakan bisnis baru secara diam-diam.

---

# 4. CODEGRAPH-FIRST & SKILL-AWARE EXECUTION

Gunakan CodeGraph sebagai pendekatan utama dalam eksplorasi kode.

Sebelum melakukan perubahan:

1. Baca `doc/CODEGRAPH-GUIDE.md`.
2. Jalankan pemeriksaan status indeks.
3. Sinkronkan jika diperlukan.
4. Gunakan MCP CodeGraph untuk symbol discovery, caller/callee, dependensi, dan change impact.
5. Identifikasi file dan test terdampak.
6. Gunakan pembacaan file langsung bila cakupan CodeGraph tidak memadai.

Gunakan skills di `.agents/skills/` secara otomatis berdasarkan konteks pekerjaan.

Contoh:

- Frontend: `ui-taste`, `ios-design`, `antislop`, `antislop-ui`, `antislop-layoutmobile`.
- Backend: `fastapi`, `tdd`, `security-audit`.
- Code quality: `ponytail` dan skills terkait.
- Architecture: gunakan `improve-codebase-architecture` hanya sesuai aturan invocation skill.

Baca `SKILL.md` yang relevan dan hormati aturan invocation.

Jangan memerlukan user untuk menyebutkan skill satu per satu.

Jangan mengklaim menggunakan skill apabila instruksinya tidak benar-benar dibaca dan diterapkan.

---

# 5. PHASE A — FULL REQUIREMENTS EXTRACTION

Ekstrak seluruh requirement dari tujuh dokumen resmi.

Jangan hanya menghitung fitur atau milestone.

Setiap requirement harus mempunyai identitas yang dapat dilacak.

Buat atau perbarui:

`doc/implementation/FULL-COMPLIANCE-MATRIX.md`

Format minimal:

| Requirement ID | Source Document | Section | IPD Task ID | Expected Behavior | Actual Implementation | Test Evidence | Status |
| -------------- | --------------- | ------- | ----------- | ----------------- | --------------------- | ------------- | ------ |

Gunakan status:

- COMPLIANT
- PARTIAL
- MISSING
- INCORRECT
- NOT_VERIFIED
- BLOCKED
- NOT_APPLICABLE

Audit seluruh task resmi IPD.

Hitung task ID langsung dari file `IPD.md`. Jangan menggunakan angka dari laporan terdahulu tanpa memeriksanya.

Untuk setiap task, tentukan:

- Requirement yang harus dipenuhi.
- Implementasi yang ditemukan.
- File yang bertanggung jawab.
- API/database/UI yang terlibat.
- Acceptance criteria.
- Pengujian yang dibutuhkan.
- Bukti hasil pengujian.
- Gap yang ditemukan.

**Keberadaan file tidak sama dengan requirement sudah terpenuhi.**

---

# 6. PHASE B — FULL CODEBASE & ARCHITECTURE AUDIT

Audit seluruh repository.

## Backend

Periksa seluruh module dan alur:

Router → Service → Domain → Repository.

Evaluasi:

- Struktur modular.
- Dependency boundaries.
- Business logic.
- Domain invariants.
- Pydantic validation.
- SQLAlchemy models.
- Transaction handling.
- Exception handling.
- Authorization.
- Session management.
- Audit logging.
- Idempotency.
- API responses.
- Performance.

## Frontend

Audit:

- Application routing.
- Feature modules.
- Shared components.
- API client.
- Authentication state.
- Forms.
- Query caching.
- Error boundaries.
- UI states.
- Layout responsiveness.
- Accessibility.
- Design tokens.
- Icon consistency.

## Database

Audit:

- Entity coverage.
- Table relationships.
- Foreign keys.
- Constraints.
- Indexes.
- Uniqueness.
- Nullability.
- Migration revisions.
- Database compatibility.
- Transaction consistency.

Periksa implementasi terhadap 19 tabel yang sebelumnya diidentifikasi dari BSD. Gunakan daftar aktual BSD sebagai penentu akhir.

## Cross-Layer Integration

Periksa kesesuaian:

- Database ↔ SQLAlchemy models.
- Models ↔ Domain logic.
- Domain ↔ Services.
- Services ↔ API.
- API ↔ OpenAPI.
- OpenAPI ↔ Frontend types.
- Frontend ↔ Backend responses.
- User interface ↔ Actual business workflows.

Jangan membiarkan perbedaan kontrak antarlapisan tidak terdeteksi.

---

# 7. PHASE C — BUSINESS WORKFLOW COMPLIANCE

Audit seluruh alur E-Laundry berdasarkan PRD dan AFD.

## M1 — Authentication

Verifikasi:

- Login.
- Logout.
- Session expiry.
- Session revocation.
- CSRF.
- Login throttling.
- Role-based access control.
- User management.
- Business settings.
- Owner preservation.

Periksa konfigurasi timeout dan kebijakan keamanan terhadap dokumen.

## M2 — Laundry Operations

Verifikasi:

- Customer CRUD.
- Service catalog.
- Pricing engine.
- Perhitungan berat kiloan.
- Harga per satuan.
- Minimum order.
- Rounding.
- Price snapshot.
- Order creation.
- Order numbering.
- State machine.
- Status history.
- Cancellation.
- Optimistic concurrency.
- Order handoffs.

Gunakan status resmi dalam BSD.

Jangan menyederhanakan sembilan status menjadi tujuh atau delapan apabila spesifikasi membutuhkan sembilan.

## M3 — Finance

Verifikasi:

- Cash.
- Bank transfer manual.
- QRIS manual.
- Down payment.
- Full payment.
- Outstanding balance.
- Payment void.
- Payment history.
- Expense management.
- Invoice.
- PDF download.
- Manual WhatsApp share.
- Transaction locking.
- Concurrency.
- Idempotency.

Periksa secara khusus:

- `payments`
- `payment_voids`
- `idempotency_records`
- `audit_logs`

Jika ditemukan tabel tambahan seperti `invoices` atau `idempotency_keys`, evaluasi apakah benar dibutuhkan, sesuai spesifikasi, dan tidak menggantikan tabel wajib.

Jangan menghapus tabel tambahan tanpa migration impact analysis.

## M4 — Public Tracking

Verifikasi:

- Secure token generation.
- Hash token storage.
- Token expiration.
- Token revocation.
- Token rotation.
- Order tracking.
- Pickup tracking jika disyaratkan.
- Privacy controls.
- Public API boundaries.
- Rate limiting.
- Mobile tracking UI.
- Tracking continuity.

Audit fitur yang mungkin ditambahkan di luar scope, termasuk self-cancellation pelanggan.

Jika fitur tidak diizinkan atau bertentangan dengan requirement, perbaiki secara aman dan sertakan regresi test.

Jangan menyamakan payment void dengan order cancellation.

## M5 — Pickup & Delivery

Verifikasi:

- Public pickup request.
- Pickup confirmation.
- Courier assignment.
- Pickup lifecycle.
- Pickup-to-order conversion.
- Delivery task.
- Delivery lifecycle.
- Failed delivery.
- Rescheduling.
- Physical handoff.
- Order completion.
- Courier authorization.
- Tracking integration.

Uji transaksi atomik dan pencegahan duplikasi.

## M6 — Dashboard & Reporting

Verifikasi:

- Owner dashboard.
- Cashier dashboard.
- Operational KPIs.
- Financial KPIs.
- Payments received.
- Outstanding.
- Expenses.
- Overdue orders.
- Date filters.
- CSV exports.
- Financial reconciliation.

Jangan mencampur gross sales, pembayaran diterima, piutang, dan surplus kas.

---

# 8. PHASE D — FRONTEND UI/UX COMPLIANCE AUDIT

Gunakan `doc/DBD.md` sebagai acuan utama.

Audit seluruh halaman, bukan hanya login atau dashboard.

Periksa:

1. Design system.
2. Deep Teal palette jika sesuai DBD terbaru.
3. Typography.
4. Spacing consistency.
5. Responsive navigation.
6. Mobile-friendly layouts.
7. Reusable UI components.
8. Forms and validation.
9. Error states.
10. Loading states.
11. Empty states.
12. Success feedback.
13. Confirmation dialogs.
14. Icons.
15. Accessibility.
16. Keyboard navigation.
17. Touch targets.
18. Information hierarchy.
19. Data readability.
20. Visual consistency antar-role.

Gunakan viewport yang ditentukan DBD/IPD, termasuk ukuran mobile kecil dan desktop.

Jalankan browser testing dengan Playwright.

Ambil screenshot verifikasi dari halaman penting dan review hasil visualnya.

Jangan hanya mengandalkan ESLint atau production build sebagai bukti UI/UX benar.

Perbaiki seluruh masalah UI yang terbukti, tetap mengikuti design brief.

Jangan membuat desain ulang dengan gaya yang berbeda dari DBD.

---

# 9. PHASE E — POSTGRESQL & MIGRATION VERIFICATION

Database PostgreSQL 17 harus diverifikasi secara nyata.

Periksa:

- PostgreSQL service.
- Koneksi SQLAlchemy.
- Credential aplikasi.
- Database schema.
- Alembic revision chain.
- Migration dependencies.
- Foreign key integrity.
- Unique constraints.
- Indexes.
- Transaction behavior.
- Concurrency control.

## Mandatory Database Verification

Gunakan database pengujian PostgreSQL yang terisolasi dan aman.

1. Buat database pengujian hanya jika izin dan kredensialnya tersedia.
2. Jalankan seluruh migration dari baseline kosong hingga head.
3. Verifikasi struktur tabel.
4. Verifikasi seluruh foreign key.
5. Verifikasi constraints.
6. Uji insert/update/delete sesuai invariant.
7. Uji rollback transaksi.
8. Uji parallel payment locking.
9. Uji idempotency.
10. Uji migration repeatability.

Jangan menggunakan SQLite sebagai bukti bahwa PostgreSQL sudah lulus.

Jangan mengandalkan `alembic upgrade --sql` sebagai bukti bahwa migrasi sudah dieksekusi di database nyata.

Jangan menebak password PostgreSQL.

Jangan menghapus database yang belum dipastikan sebagai database khusus pengujian.

Apabila akses PostgreSQL tidak tersedia, tandai NOT_VERIFIED/BLOCKED, berikan tindakan konfigurasi yang diperlukan, dan lanjutkan task independen.

---

# 10. PHASE F — REAL END-TO-END VERIFICATION

Bedakan pengujian menjadi:

**A. Unit tests**

Menguji logic individual.

**B. Integration tests**

Menguji backend dengan database dan modul terkait.

**C. Component/UI tests**

Boleh menggunakan mock sesuai tujuan pengujian.

**D. Real E2E tests**

Menggunakan:

- Browser nyata.
- Frontend development/test server.
- FastAPI backend nyata.
- PostgreSQL test database.
- Data pengujian sintetis.

Mock atau API interception tidak boleh digunakan sebagai pengganti pengujian E2E nyata.

## Mandatory Business Journey

Verifikasi skenario:

1. Owner login.
2. Owner mengelola petugas.
3. Kasir login.
4. Kasir membuat pelanggan.
5. Kasir membuat layanan.
6. Kasir membuat pesanan.
7. Sistem menghitung harga sesuai aturan.
8. Staff memproses laundry.
9. Status pesanan berubah sesuai state machine.
10. Kasir mencatat DP.
11. Kasir melakukan pelunasan.
12. Sistem menghasilkan invoice PDF.
13. Pelanggan membuka tracking tanpa login.
14. Pelanggan mengajukan pickup.
15. Kasir menugaskan kurir.
16. Kurir melakukan pickup.
17. Sistem melakukan konversi pickup menjadi order tanpa duplikasi.
18. Kurir melakukan delivery sesuai workflow.
19. Sistem mencatat physical handoff.
20. Pesanan diselesaikan sesuai semua invariant.
21. Dashboard Owner menampilkan hasil transaksi.
22. Laporan sesuai dengan data pembayaran dan pengeluaran.

Tambahkan negative testing:

- Invalid credentials.
- Unauthorized access.
- Expired session.
- Invalid CSRF.
- Duplicate order.
- Duplicate payment.
- Overpayment.
- Invalid state transition.
- Duplicate pickup conversion.
- Tracking token invalid.
- Tracking token expired.
- Unauthorized courier action.
- Invalid handoff.
- Concurrent payment race condition.

Setiap journey harus menghasilkan bukti pengujian nyata.

---

# 11. PHASE G — SECURITY, PERFORMANCE & QUALITY

Audit:

- Authentication.
- Password hashing.
- Session management.
- CSRF.
- RBAC.
- IDOR.
- SQL injection protections.
- XSS protections.
- Token security.
- Data privacy.
- Secret management.
- Request throttling.
- Audit logs.
- Sensitive error handling.
- Dependency vulnerabilities.

Jalankan:

- Pytest.
- Ruff.
- Mypy.
- ESLint.
- Frontend TypeScript build.
- Vitest jika sudah dikonfigurasi.
- Playwright.
- PostgreSQL integration tests.
- Security tests.
- Performance benchmark.

Gunakan target performa dari TRD/IPD.

Jangan mengganti kriteria performa dengan angka baru tanpa dasar.

Jangan menjadikan banyaknya test sebagai satu-satunya ukuran keberhasilan.

---

# 12. PHASE H — M8 DEPLOYMENT & RECOVERY VALIDATION

Audit artefak M8:

- Backend Dockerfile.
- Frontend Dockerfile.
- Docker Compose.
- Nginx configuration.
- Environment templates.
- Production secrets.
- Health checks.
- Backup scripts.
- Restore scripts.
- Operational runbooks.
- Rollback procedures.
- Logging and monitoring.

Jika Docker tersedia:

1. Jalankan Docker Compose config validation.
2. Build image.
3. Jalankan stack development/staging yang aman.
4. Verifikasi komunikasi frontend-backend.
5. Verifikasi koneksi PostgreSQL.
6. Verifikasi health endpoints.
7. Jalankan smoke tests.
8. Uji backup pada database pengujian.
9. Uji restore pada database pengujian terpisah.
10. Verifikasi recovery dan dokumentasikan hasilnya.

**Jangan mengklaim Docker telah diverifikasi hanya karena file Dockerfile dan Compose tersedia.**

Jangan melakukan deployment publik tanpa persetujuan.

Pisahkan:

- IMPLEMENTATION_COMPLETE.
- TEST_VERIFIED.
- DEPLOYMENT_PREPARED.
- PRODUCTION_VERIFIED.
- PRODUCTION_APPROVED.

---

# 13. PHASE I — AUTOMATIC GAP REMEDIATION

Setelah menemukan ketidaksesuaian, **LANGSUNG PERBAIKI**.

Jangan berhenti hanya dengan menghasilkan daftar masalah.

Gunakan siklus:

**DISCOVER → ANALYZE → FIX → TEST → RECHECK → UPDATE TRACKER → CONTINUE.**

Prioritaskan:

**P0 — Critical**

- Security vulnerabilities.
- Financial data integrity.
- Invalid transaction boundaries.
- Incorrect business invariants.
- Broken database migrations.
- Unauthorized access.
- Data loss risk.
- Critical workflow failures.

**P1 — High**

- Missing required features.
- Broken API integrations.
- Incorrect state transitions.
- Incorrect dashboard calculations.
- Major UI workflow problems.

**P2 — Medium**

- Responsive issues.
- Accessibility defects.
- Inconsistent UI states.
- Missing validation.
- Maintainability issues.

**P3 — Low**

- Minor styling.
- Noncritical polish.
- Documentation improvements.

Untuk setiap perbaikan:

1. Temukan requirement sumber.
2. Identifikasi root cause.
3. Gunakan CodeGraph untuk change impact.
4. Tentukan acceptance test.
5. Implementasikan perbaikan minimal yang benar.
6. Jalankan targeted tests.
7. Jalankan regression tests.
8. Perbarui dokumentasi.
9. Tutup temuan setelah terbukti.
10. Lanjutkan temuan berikutnya.

Jangan melemahkan test agar terlihat PASS.

Jangan memperbaiki satu fitur dengan merusak modul lain.

---

# 14. REVALIDATE ALL M0–M8 ACCEPTANCE GATES

Setelah perbaikan selesai, lakukan penilaian ulang seluruh milestone:

- M0 — FOUNDATION_READY.
- M1 — AUTH_RBAC_READY.
- M2 — CORE_LAUNDRY_READY.
- M3 — FINANCE_INVOICE_READY.
- M4 — PUBLIC_TRACKING_READY.
- M5 — PICKUP_DELIVERY_READY.
- M6 — REPORTING_READY.
- M7 — RELEASE_CANDIDATE_READY.
- M8 — DEPLOYMENT_PREPARED / PRODUCTION_READY sesuai bukti dan persetujuan.

Jangan mempertahankan PASS lama apabila ada requirement wajib yang ternyata tidak terpenuhi.

Gunakan:

- PASS.
- PARTIAL.
- FAILED.
- BLOCKED.
- NOT_VERIFIED.

Task dinyatakan PASS hanya berdasarkan bukti terbaru yang relevan.

---

# 15. REQUIRED REPORTS & EVIDENCE

Buat atau perbarui di:

`doc/implementation/`

## A. Full Compliance Matrix

`FULL-COMPLIANCE-MATRIX.md`

Memuat seluruh requirement dan status implementasi.

## B. Gap & Remediation Register

`GAP-REMEDIATION-REGISTER.md`

Kolom:

- Finding ID.
- Priority.
- Requirement reference.
- Root cause.
- Affected modules.
- Corrective action.
- Files changed.
- Test evidence.
- Status.

## C. Real Integration Test Report

`REAL-INTEGRATION-TEST-REPORT.md`

Memuat:

- Environment.
- PostgreSQL version.
- Database migration status.
- API tests.
- Browser E2E.
- Test data strategy.
- Mock vs real test classification.
- Results.

## D. UI/UX Compliance Report

`UIUX-COMPLIANCE-REPORT.md`

Memuat:

- Pages audited.
- Responsive results.
- Accessibility.
- Screenshots.
- Problems.
- Fixes.

## E. Deployment Verification Report

`DEPLOYMENT-VERIFICATION-REPORT.md`

Memuat:

- Container build.
- Stack startup.
- Health checks.
- Database connectivity.
- Backup/restore.
- Remaining blockers.

## F. Final Master Audit

`FINAL-COMPLIANCE-AUDIT.md`

Memuat:

- Requirement coverage.
- Milestone coverage.
- Task coverage.
- PASS/PARTIAL/FAILED/BLOCKED totals.
- Bugs fixed.
- Open defects.
- Security findings.
- Database verification.
- E2E verification.
- Deployment readiness.
- Final status.

Perbarui juga:

`doc/implementation/MASTER-TRACKER.md`

---

# 16. AUTONOMOUS CONTINUATION POLICY

Saya mengizinkan Anda memperbaiki implementasi aplikasi pada repository development selama sesuai scope dokumentasi.

Jangan meminta konfirmasi untuk setiap perubahan kode rutin yang aman.

Setelah satu temuan diperbaiki, lanjutkan temuan berikutnya.

Setelah satu milestone tervalidasi, lanjutkan milestone berikutnya.

Jangan berhenti hanya karena satu pengujian berhasil.

Jika ada blocker eksternal, dokumentasikan dan kerjakan task independen yang tidak terhalang.

Jika sesi hampir berakhir, simpan checkpoint aktual yang memuat:

- Completed tasks.
- Pending tasks.
- Current findings.
- Files changed.
- Test results.
- Blockers.
- Next executable tasks.

Pekerjaan hanya berlangsung selama sesi aktif. Jangan mengklaim pekerjaan masih berjalan setelah sesi berakhir.

---

# 17. SAFETY & GOVERNANCE

Dilarang tanpa persetujuan:

- Menghapus database nyata.
- Menjalankan destructive migration.
- Mengubah database produksi.
- Melakukan public deployment.
- Mengubah DNS/domain.
- Mengirim pesan kepada pelanggan nyata.
- Menggunakan layanan berbayar.
- Membocorkan credentials.
- Melakukan force push.
- Menghapus perubahan pengguna yang tidak terkait.

Gunakan database testing terisolasi dan data sintetis.

Jangan menebak kredensial.

Jangan mengubah baseline dokumentasi secara sepihak.

---

# 18. FINAL COMPLETION CRITERIA

Tugas audit dan remediation selesai apabila:

1. Seluruh requirement dari dokumen resmi telah dipetakan.
2. Seluruh task IPD memiliki status berbasis bukti.
3. Seluruh fitur wajib telah diimplementasikan atau blocker dinyatakan jelas.
4. Semua perbedaan arsitektur telah diperiksa.
5. Database schema sesuai BSD.
6. PostgreSQL migration telah diverifikasi secara nyata atau ditandai BLOCKED.
7. Business invariants teruji.
8. Backend dan frontend terintegrasi.
9. UI/UX sesuai DBD.
10. Critical E2E journeys lulus.
11. Security defects kritis tidak tersisa.
12. Performance tests memiliki hasil aktual.
13. Backup/restore telah diuji atau ditandai NOT_VERIFIED.
14. Deployment preparation telah diverifikasi.
15. Laporan akhir lengkap dan dapat diaudit.

**Jangan mengklaim 100% COMPLIANT apabila masih terdapat requirement wajib MISSING, PARTIAL, BLOCKED, atau NOT_VERIFIED.**

---

# 19. START EXECUTION NOW

Lakukan urutan berikut:

1. Baca seluruh tujuh dokumen resmi.
2. Baca laporan M0–M8.
3. Sinkronisasi CodeGraph.
4. Audit seluruh implementasi backend dan frontend.
5. Audit seluruh database schema dan migration.
6. Bangun requirements compliance matrix.
7. Identifikasi seluruh gap.
8. Urutkan gap berdasarkan risiko dan dependensi.
9. Perbaiki seluruh gap teknis yang berada dalam scope.
10. Jalankan targeted tests.
11. Jalankan regression tests.
12. Jalankan real PostgreSQL integration tests.
13. Jalankan real browser E2E tests.
14. Audit dan perbaiki UI/UX.
15. Verifikasi Docker dan recovery bila lingkungan tersedia.
16. Perbarui seluruh milestone acceptance.
17. Jalankan audit ulang pascaperbaikan.
18. Susun final compliance report.
19. Lanjutkan sampai seluruh pekerjaan yang aman dan memungkinkan dalam sesi ini selesai.

## FINAL ABSOLUTE DIRECTIVE

**DO NOT TRUST PREVIOUS 100% COMPLETION CLAIMS WITHOUT EVIDENCE.**

**DO NOT REWRITE THE ORIGINAL REQUIREMENTS.**

**DO NOT STOP AFTER FINDING GAPS.**

**FIX EVERY VERIFIED NON-COMPLIANCE WITHIN AUTHORIZED SCOPE.**

**FOLLOW PRD, TRD, AFD, DBD, BSD, IPD, AND SKILLS-CATALOG.**

**USE CODEGRAPH-FIRST AND RELEVANT ENGINEERING SKILLS.**

**TEST REAL WORKFLOWS, NOT ONLY MOCKED INTERFACES.**

**REVALIDATE ALL M0–M8 ACCEPTANCE GATES.**

**PRODUCE AN AUDITABLE, DOCUMENTATION-COMPLIANT E-LAUNDRY 2.0 IMPLEMENTATION.**

**START THE FULL AUDIT AND REMEDIATION NOW.**
