
# TASK 5 — FINAL COMPLIANCE RECONCILIATION & REAL SYSTEM VERIFICATION

## Project: E-Laundry 2.0

Lanjutkan proyek E-Laundry 2.0 dari hasil Task 4. Jangan membuat ulang aplikasi atau perencanaan M0–M8.

Tujuan: menutup ketidaksesuaian yang tersisa pada dokumentasi audit, requirements traceability, database, dan pengujian sistem nyata.

Gunakan PRD.md, TRD.md, AFD.md, DBD.md, BSD.md, IPD.md, SKILLS-CATALOG.md, AGENTS.md, serta CodeGraph-first.

## P0 — Requirements and Task Reconciliation

1. Ekstrak semua task ID resmi dari IPD.md secara programatis.
2. Bandingkan dengan MASTER-TRACKER.md dan FULL-COMPLIANCE-MATRIX.md.
3. Periksa mengapa implementation plan sebelumnya menyatakan 108 task, Master Tracker memuat 96 task, dan Compliance Matrix memiliki 39 baris tetapi mengklaim 38 requirement.
4. Perbaiki seluruh task ID mapping yang tidak sesuai.
5. Pastikan setiap task IPD memiliki requirement, deliverable, actual implementation, acceptance criteria, dan evidence.
6. Jangan mengubah ID asli IPD untuk menyamakan angka.

## P0 — Real PostgreSQL Verification

1. Periksa PostgreSQL 17 dan kredensial yang tersedia secara aman.
2. Verifikasi rantai migrasi Alembic aktual menggunakan revision/down_revision.
3. Gunakan database testing yang terisolasi.
4. Jalankan migration dari database kosong sampai head jika akses tersedia.
5. Verifikasi 19 tabel BSD, foreign key, check constraint, unique constraint, dan index.
6. Jalankan integration tests serta concurrent payment tests pada PostgreSQL nyata.
7. Jangan menganggap SQLite tests sebagai pengganti PostgreSQL verification.
8. Jika environment tidak tersedia, tandai BLOCKED dengan bukti spesifik. Jangan mengklaim PASS.

## P0 — True Browser-to-Database E2E

Buat suite terpisah untuk real E2E, tanpa page.route/API mock terhadap endpoint bisnis.

Jalankan browser Chromium → React → FastAPI → PostgreSQL test database.

Uji alur penting:

- Login dan RBAC.
- Customer & Service CRUD.
- Order intake dan pricing.
- Laundry status transitions.
- Partial dan full payment.
- Invoice PDF.
- Public tracking.
- Pickup dan assignment kurir.
- Pickup-to-order conversion.
- Delivery dan physical handoff.
- Order completion.
- Dashboard dan financial reporting.

Pertahankan mocked Playwright tests sebagai UI/component regression tests dan klasifikasikan dengan benar.

## P1 — Documentation Consistency

1. Perbarui Master Tracker yang masih menyebut public self-cancellation dan cancellation modal sebagai PASS.
2. Pastikan GAP-02 benar-benar menonaktifkan perubahan status melalui public tracking.
3. Samakan nama dan ID migrasi di seluruh laporan.
4. Samakan angka requirement, task, migrasi, dan status milestone.
5. Verifikasi bahwa penambahan audit_logs tidak merusak migrasi, financial invariants, dan transaksi bisnis.
6. Jangan mengubah source-of-truth agar cocok dengan implementasi.

## P1 — Deployment and Recovery

1. Validasi konfigurasi Docker jika CLI tersedia.
2. Uji build, startup, healthcheck, dan backup/restore pada staging/test environment.
3. Jika Docker tidak tersedia, pertahankan BLOCKED_NO_DOCKER_CLI.
4. Jangan mengklaim PRODUCTION_READY hanya berdasarkan keberadaan Dockerfile, Compose, atau runbook.
5. Jangan melakukan public deployment atau destructive database operation.

## P1 — UI/UX Acceptance

Audit ulang klaim minimum 44px touch targets. Laporan sebelumnya masih menyebut sebagian target berukuran 36–44px.

Periksa setiap pengecualian berdasarkan DBD dan kriteria aksesibilitas yang sebenarnya berlaku. Perbaiki jika tidak memenuhi requirement.

## Required Final Evidence

Perbarui:

- FULL-COMPLIANCE-MATRIX.md
- GAP-REMEDIATION-REGISTER.md
- REAL-INTEGRATION-TEST-REPORT.md
- MASTER-TRACKER.md
- FINAL-COMPLIANCE-AUDIT.md

Tambahkan:

- POSTGRESQL-VERIFICATION-REPORT.md
- REAL-BROWSER-E2E-REPORT.md
- TASK-ID-RECONCILIATION.md

Untuk setiap status PASS, wajib sertakan perintah pengujian, hasil nyata, file/test pendukung, dan batasan lingkungan.

Lakukan perbaikan kode yang diperlukan secara langsung dan aman. Jangan berhenti pada daftar temuan.

Jangan melemahkan test untuk memperoleh PASS.

**Final verdict harus membedakan:**

- IMPLEMENTATION_COMPLETE
- UNIT_AND_MOCK_TESTS_PASS
- POSTGRESQL_INTEGRATION_VERIFIED
- REAL_E2E_VERIFIED
- DEPLOYMENT_PREPARED
- PRODUCTION_VERIFIED
- PRODUCTION_APPROVED

Jangan mengklaim full compliance jika masih ada mandatory requirement yang belum dibuktikan.

START TASK 5 NOW.
