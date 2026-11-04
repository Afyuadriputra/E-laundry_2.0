# TASK 8 — FINAL FULL-STACK TEST VERIFICATION & AUTOMATED REMEDIATION

## E-Laundry 2.0 — Evidence-Based Quality Assurance

### EXECUTION MODE | CONTINUATION OF TASK 7

### Test → Audit → Fix Code → Retest → Verify → Final Acceptance

---

# 1. ROLE & OBJECTIVE

Berperan sebagai:

- Principal Software Architect
- Principal SDET / QA Automation Engineer
- Senior FastAPI Engineer
- Senior React & TypeScript Engineer
- PostgreSQL Database Engineer
- Application Security Engineer
- Performance & Reliability Engineer
- UI/UX Accessibility Engineer

Lanjutkan pengembangan E-Laundry 2.0 berdasarkan hasil Task 7.

Task 7 sebelumnya melaporkan:

- 90 backend tests PASS.
- 22 frontend Vitest tests PASS.
- 19 Playwright tests PASS.
- Total 131/131 tests PASS.
- PostgreSQL 17 real integration tersedia.
- Docker runtime masih BLOCKED.

Namun, audit terhadap `FULL-STACK-TESTING-REPORT.md` menemukan sejumlah ketidaksesuaian antara laporan pengujian, implementasi, dan enam dokumen resmi.

## PRIMARY GOAL

**MEMASTIKAN SEMUA FITUR WAJIB E-LAUNDRY 2.0 BENAR-BENAR LULUS PENGUJIAN SESUAI DOKUMEN RESMI, DENGAN BUKTI YANG VALID DAN DAPAT DIREPRODUKSI.**

Jika test gagal akibat bug implementasi, perbaiki source code dan jalankan ulang pengujian.

Jangan berhenti setelah menemukan masalah.

Jangan mengejar 100% PASS dengan mengubah expected result yang benar.

Jangan mengulang seluruh implementasi M0–M8 dari awal.

---

# 2. WORKSPACE

Project root:

`D:\Kuliah\joki\Kerja Praktek Aqil\kawan aqil\projek`

## Mandatory Documents

Baca lengkap:

1. `doc/PRD.md`
2. `doc/TRD.md`
3. `doc/AFD.md`
4. `doc/DBD.md`
5. `doc/BSD.md`
6. `doc/IPD.md`

Baca juga:

- `AGENTS.md`
- `doc/SKILLS-CATALOG.md`
- `doc/CODEGRAPH-GUIDE.md`
- `doc/api/openapi.json`
- `doc/implementation/DECISION-REGISTER.md`
- `doc/implementation/MASTER-TRACKER.md`
- `FULL-STACK-TESTING-REPORT.md` jika tersedia.
- Seluruh laporan Task 7 yang sudah ada pada `doc/testing/`.
- Source code frontend/backend.
- Existing test suites.
- Alembic migrations.

Gunakan dokumen resmi sebagai source of truth.

Jangan mengubah requirement asli untuk membenarkan bug.

---

# 3. MANDATORY PROJECT SKILLS & CODEGRAPH

Sebelum melakukan perubahan:

1. Baca `AGENTS.md`.
2. Identifikasi skills dari `doc/SKILLS-CATALOG.md`.
3. Periksa `.agents/skills/`.
4. Baca `SKILL.md` untuk setiap skill relevan.
5. Terapkan aturan masing-masing skill.

Gunakan skills relevan, termasuk jika tersedia:

- `fastapi`
- `tdd`
- `security-audit`
- `ui-taste`
- `ios-design`
- Relevant React, Playwright, database, debugging, and architecture skills.

Hormati skill yang memerlukan explicit invocation.

Gunakan CodeGraph-first untuk:

- Symbol discovery.
- Call graph.
- Dependency analysis.
- Blast radius analysis.
- Affected tests.
- Cross-module integration review.

Jangan mengklaim sebuah skill digunakan jika instruksinya tidak benar-benar diikuti.

---

# 4. STRICT OUTPUT POLICY — ONE MARKDOWN REPORT ONLY

## THIS REQUIREMENT IS MANDATORY

Seluruh output dokumentasi Task 8 wajib disatukan ke dalam:

`doc/testing/TASK8-FINAL-VERIFICATION.md`

**JANGAN MEMBUAT LAPORAN TERPISAH.**

Jangan membuat file laporan tambahan seperti:

- TASK8-SUMMARY.md
- TASK8-BUG-REPORT.md
- TASK8-PERFORMANCE.md
- TASK8-SECURITY.md
- TASK8-E2E-REPORT.md
- TASK8-COMPLIANCE.md

Semua informasi harus dimasukkan sebagai section pada satu Markdown utama.

Laporan Task 7 yang sudah ada boleh dibaca tetapi jangan diduplikasi.

Dokumen resmi PRD, TRD, AFD, DBD, BSD, IPD tidak boleh diubah untuk menyesuaikan implementasi yang salah.

## Allowed Changes

Anda boleh:

- Membuat atau memperbarui frontend tests.
- Membuat atau memperbarui backend tests.
- Memperbaiki source code frontend.
- Memperbaiki source code backend.
- Memperbaiki API integration.
- Memperbaiki database models.
- Menambahkan Alembic migration yang aman jika diperlukan.
- Memperbaiki test configuration.
- Menyesuaikan dependency testing bila diperlukan.
- Membuat konfigurasi visual regression.
- Membuat skrip test performance.
- Membuat CI test configuration.
- Membuat SATU laporan Markdown final.

File seperti screenshot baseline, JSON test results, traces, dan coverage artifacts boleh dihasilkan sebagai evidence teknis apabila diperlukan, tetapi simpan pada direktori artifact yang diabaikan Git, bukan sebagai laporan Markdown tambahan.

**One report file does not mean one changed source file.**

---

# 5. PHASE A — VERIFY TASK 7 TEST INTEGRITY

Audit seluruh 131 tests yang sebelumnya dinyatakan PASS.

Jangan mempercayai angka dari laporan tanpa menghitung ulang.

Lakukan:

1. Periksa Git status sebelum bekerja.
2. Inventaris seluruh test file.
3. Jalankan pytest collection.
4. Jalankan Vitest.
5. Jalankan Playwright.
6. Periksa skipped, xfailed, flaky, dan deselected tests.
7. Identifikasi test yang menggunakan mock.
8. Identifikasi test yang menggunakan PostgreSQL nyata.
9. Identifikasi test yang benar-benar menjalankan aplikasi melalui HTTP.
10. Verifikasi assertion yang digunakan.
11. Bandingkan hasil dengan klaim Task 7.
12. Periksa apakah test yang gagal sebelumnya disesuaikan secara keliru.

Audit khusus perubahan:

- `test_csrf.py`
- `test_rbac.py`
- `test_tracking_access.py`
- `test_orders.py`
- `test_payments.py`
- `test_pickup_conversion.py`
- `test_resilience.py`

Untuk setiap perubahan assertion:

- Periksa requirement.
- Periksa actual API contract.
- Periksa apakah expected behavior memang benar.
- Verifikasi tidak ada authorization atau validation yang dilemahkan.

Gunakan `pytest --collect-only` untuk merekonsiliasi total.

Laporan sebelumnya menyebut 90 backend tests, tetapi penjumlahan test yang dirinci menurut kategori hanya menjelaskan 86.

Temukan sumber perbedaan tersebut.

Jangan menghitung test yang sama dua kali sebagai test berbeda hanya karena memenuhi dua kategori.

---

# 6. PHASE B — FIX PRD ACCEPTANCE TEST MAPPING

## CRITICAL P0

Laporan Task 7 memiliki ketidaksesuaian serius pada mapping AT-01 sampai AT-30.

Contoh:

| AT ID | Official PRD Requirement                     | Incorrect Task 7 Mapping |
| ----- | -------------------------------------------- | ------------------------ |
| AT-02 | Password salah ditolak                       | Login throttling         |
| AT-03 | Kasir membuat pesanan                        | RBAC                     |
| AT-07 | Kasir membuat nota                           | Service catalog          |
| AT-15 | Admin mengonfirmasi pickup                   | Partial payment          |
| AT-23 | Kurir tidak boleh mengakses laporan keuangan | Public self-cancellation |
| AT-30 | Backup dipulihkan dengan data konsisten      | Audit log redaction      |

Ini wajib diperbaiki.

## Required Actions

1. Baca `doc/PRD.md` bagian §15.2 secara langsung.
2. Ekstrak seluruh AT-01 sampai AT-30.
3. Pertahankan exact official AT IDs.
4. Pertahankan deskripsi dan expected result dari PRD.
5. Petakan setiap AT ke executable tests aktual.
6. Pastikan test benar-benar menguji perilaku tersebut.
7. Jika belum ada test, buat test baru.
8. Jika test gagal karena kode salah, perbaiki kode.
9. Jika tidak dapat diverifikasi, tandai NOT_VERIFIED atau BLOCKED.
10. Jangan memberikan PASS hanya berdasarkan nama test file.

## Mandatory AT Matrix

Masukkan ke laporan tunggal:

| AT ID | Official Requirement | Test File::Test Name | Environment | Expected | Actual | Status |
| ----- | -------------------- | -------------------- | ----------- | -------- | ------ | ------ |

Pastikan semua 30 AT tercakup.

## Special AT-30

AT-30 resmi berkaitan dengan backup dan restore database.

Pengujian keberadaan skrip backup tidak sama dengan successful restore.

Gunakan database pengujian terisolasi.

Lakukan backup, restore ke database pengujian terpisah, dan verifikasi konsistensi data jika tool serta izin tersedia.

Jika restore tidak dijalankan, AT-30 tidak boleh PASS.

---

# 7. PHASE C — VERIFY CANONICAL DATABASE SCHEMA

## CRITICAL P0

BSD resmi mendefinisikan 19 entitas inti.

Periksa skema aktual menggunakan SQLAlchemy, Alembic, dan PostgreSQL catalog.

Jangan hanya menghitung total tabel.

Pastikan kesesuaian nama dan struktur, termasuk:

- `user_sessions`
- `delivery_status_history`
- `idempotency_records`
- `order_handoffs`
- `audit_logs`

Laporan Task 7 menggunakan nama alternatif seperti:

- `sessions`
- `idempotency_keys`
- `invoices`

Periksa apakah ini:

1. Kesalahan laporan.
2. Alias ORM.
3. Tabel tambahan yang memang diperlukan.
4. Ketidaksesuaian skema aktual.

Periksa:

- Table names.
- Column names.
- Column types.
- Numeric precision.
- Primary keys.
- Foreign keys.
- Unique constraints.
- Check constraints.
- Indexes.
- Migration revision chain.
- Transaction boundaries.

Khusus:

`order_items.quantity` harus dibandingkan terhadap spesifikasi BSD `NUMERIC(10,3)`.

Jangan melakukan rename atau drop tabel tanpa analisis dependency dan migration safety.

Jika perubahan schema diperlukan, buat migration yang kompatibel dan uji pada database testing terisolasi.

Jangan mengubah database produksi.

---

# 8. PHASE D — VERIFY BUSINESS RULE CONSISTENCY

Audit seluruh aturan bisnis utama.

## D1 — Unpaid Handoff

Laporan Task 7 mengklaim:

`RESOLVED_BY_OWNER`

dengan aturan bahwa pesanan harus lunas sebelum status COMPLETED.

PRD menyebutkan kemungkinan serah terima dengan piutang.

Periksa:

- PRD §5.5.
- PRD §6.
- PRD DEC-04.
- AFD state transitions.
- BSD domain invariants.
- Decision Register.
- Bukti persetujuan Owner.

Jangan menganggap kalimat `RESOLVED_BY_OWNER` sebagai bukti persetujuan.

Jika ada keputusan sah, catat sumber dan tanggalnya.

Jika belum ada, tandai DECISION_REQUIRED.

Jangan mengganti aturan bisnis secara sepihak.

## D2 — Duplicate Customer Phone

Verifikasi apakah shared family phone diperbolehkan.

Periksa unique constraints, normalisasi telepon, duplicate warning, dan perilaku API.

Hindari kehilangan data atau penggabungan pelanggan berbeda.

## D3 — Order State Machine

Verifikasi 9 canonical states:

- RECEIVED
- QUEUED
- WASHING
- DRYING
- IRONING
- QC_PACKING
- READY
- COMPLETED
- CANCELLED

Uji semua valid dan invalid transitions.

Periksa historical records, optimistic locking, handoff requirements, dan cancellation audit.

## D4 — Financial Invariants

Wajib uji:

- Partial payment.
- Full payment.
- Overpayment prevention.
- Concurrent payment.
- Idempotency.
- Payment void.
- Outstanding receivables.
- Order cancellation.
- Cash received.
- Expense recording.
- Financial reporting.
- Snapshot pricing.

Gunakan PostgreSQL nyata untuk transaksi dan locking.

---

# 9. PHASE E — COMPLETE FRONTEND TEST COVERAGE

Task 7 belum membuktikan semua kategori frontend secara memadai.

## FE-01 — Unit Tests

Verifikasi fungsi murni dan utility.

## FE-02 — Component Tests

Verifikasi komponen dengan meaningful assertions.

## FE-03 — Integration Tests

Verifikasi interaksi antar-komponen dan state updates dengan network mocks yang terdokumentasi.

## FE-04 — Real E2E

Gunakan:

Browser → React → FastAPI → PostgreSQL.

Tidak boleh menggunakan network interception untuk menggantikan business API.

Uji seluruh critical workflows.

## FE-05 — Visual Regression

Gunakan Playwright screenshot comparison.

Buat deterministic baseline:

- Fixed viewport.
- Fixed locale.
- Fixed clock.
- Stable data.
- Disabled nonessential animations.

Periksa screenshot diff.

Jangan menganggap tidak ada horizontal overflow sebagai visual regression PASS.

Jangan menerima snapshot baru otomatis tanpa inspeksi dan justifikasi.

## FE-06 — Cross-Browser & Cross-Device

Gunakan:

- Chromium.
- Firefox.
- WebKit.

Gunakan viewport DBD:

320, 360, 375, 390, 430, 768, 1024, 1440 px.

Jalankan critical smoke flows lintas browser.

Jangan mengklaim Safari asli diuji jika hanya WebKit automation.

## FE-07 — Accessibility

Uji:

- axe-core.
- Keyboard navigation.
- Focus visibility.
- Accessible labels.
- Dialog focus management.
- Color contrast.
- Touch targets.
- Screen reader semantics.

Gunakan WCAG 2.2 AA sebagai acuan DBD.

Catat manual review requirements secara terpisah.

## FE-08 — Client Performance

Ukur dengan Lighthouse dan browser tooling:

- LCP.
- FCP.
- CLS.
- TTFB.
- INP jika pengukuran valid.
- JavaScript bundle size.
- CSS bundle size.
- Route loading.
- Network requests.

Bedakan lab metrics dari field metrics.

## FE-09 — Localization

Uji:

- Indonesian locale.
- Rupiah currency.
- Timezone Asia/Jakarta.
- Dates.
- Decimal formatting.
- Long-text layout.
- Error messages.

RTL tidak wajib jika memang di luar scope PRD/DBD.

---

# 10. PHASE F — COMPLETE BACKEND TEST COVERAGE

Verifikasi seluruh 13 kategori berikut secara independen.

## BE-01 — Unit Testing

Domain logic dan validasi internal.

## BE-02 — Integration Testing

PostgreSQL 17, SQLAlchemy, migration, transaksi, locking, dan persistence.

## BE-03 — API Testing

Status, schema, headers, auth, CSRF, errors, filtering, side effects.

## BE-04 — Contract Testing

Jangan hanya membandingkan jumlah 48 routes.

Verifikasi request/response schemas, enums, required fields, error formats, authentication, dan compatibility.

## BE-05 — Business E2E

Jalankan seluruh critical journeys melalui API nyata dan database test.

## BE-06 — Load Testing

Uji traffic operasional normal.

## BE-07 — Stress Testing

Tingkatkan beban bertahap hingga batas pengujian yang aman.

## BE-08 — Spike Testing

Uji lonjakan traffic mendadak, recovery, dan integritas transaksi.

## BE-09 — Soak Testing

Jalankan beban konstan selama durasi terukur yang relevan.

Monitor memory dan database connections.

Jangan mengklaim soak PASS menggunakan benchmark kurang dari satu detik.

## BE-10 — Security Testing

RBAC, IDOR, CSRF, token, SQL injection, throttling, dan dependency security.

## BE-11 — Resilience Testing

Database connection interruption, rollback, retry, dan recovery.

## BE-12 — Smoke Testing

Jalankan terhadap runtime nyata.

## BE-13 — Sanity Testing

Verifikasi setiap bug fix dan targeted regression.

Gunakan kategori resmi Task 8 ini dalam laporan, tetapi simpan mapping ke label kategori dari Task 7 agar tidak menimbulkan kebingungan historis.

Jangan melakukan chaos, stress, atau soak terhadap database pengguna atau server produksi.

---

# 11. PERFORMANCE TESTING REQUIREMENTS

Pengujian Task 7 hanya menunjukkan:

- 200 requests untuk health endpoint.
- 100 requests untuk CSRF endpoint.
- Total benchmark kurang dari dua detik.

Ini tidak cukup membuktikan kapasitas operasional aplikasi.

Buat workload terpisah yang relevan:

1. Customer search.
2. Order listing.
3. Order creation.
4. Payment recording.
5. Status transition.
6. Public tracking.
7. Dashboard aggregation.
8. Report queries.

Ukur:

- RPS.
- Concurrent users.
- p50/p95/p99.
- Error rate.
- CPU.
- RAM.
- Database connection usage.
- Recovery time.

Gunakan target resmi TRD jika tersedia.

Tetapkan batas maksimum aman untuk beban, durasi, concurrency, dan konsumsi resource sebelum pengujian.

Jangan melakukan unbounded stress test.

Jika tidak tersedia staging representatif, lakukan local benchmark sebagai baseline dan tandai production-like performance NOT_VERIFIED.

---

# 12. AUTOMATIC BUG REMEDIATION POLICY

Jika sebuah test gagal:

1. Reproduce failure.
2. Capture stack trace.
3. Identify requirement.
4. Perform CodeGraph impact analysis.
5. Identify root cause.
6. Classify failure.
7. Write or strengthen regression test.
8. Fix actual source code if defective.
9. Run targeted test.
10. Run affected module tests.
11. Run full regression suite.
12. Document fix and result.

Klasifikasi:

- APPLICATION_BUG
- TEST_FIXTURE_DEFECT
- BUSINESS_RULE_MISMATCH
- API_CONTRACT_DEFECT
- DATABASE_SCHEMA_DEFECT
- SECURITY_DEFECT
- PERFORMANCE_DEFECT
- ENVIRONMENT_BLOCKER
- DOCUMENT_CONFLICT

Jika expected behavior masih membutuhkan keputusan Owner, jangan memaksakan implementasi.

Jangan:

- Menghapus failing test.
- Mengubah assertion agar bug menjadi PASS.
- Menonaktifkan CSRF/RBAC.
- Menghapus foreign keys.
- Mengabaikan financial invariants.
- Mengubah source-of-truth documents secara sepihak.
- Menjalankan destructive migration pada database yang belum diverifikasi sebagai test DB.

---

# 13. FINAL NUMERIC RECONCILIATION

Perbaiki seluruh ketidaksesuaian angka pada laporan.

Task 7 memiliki klaim:

- Backend: 90 tests.
- Frontend: 41 tests.
- Total: 131 tests.
- PRD: 121 PASS dari 131 item.
- TRD: 45 PASS, 2 BLOCKED.
- AFD: 57 PASS.
- DBD: 64 PASS.
- BSD: 29 PASS.
- IPD: 104 PASS, 4 BLOCKED.

Periksa dan hitung ulang:

1. Jumlah test collected.
2. Jumlah test executed.
3. Jumlah PASSED.
4. Jumlah FAILED.
5. Jumlah SKIPPED.
6. Jumlah XFAILED/XPASSED.
7. Jumlah test per kategori.
8. Jumlah requirement.
9. Jumlah requirement PASS.
10. Jumlah PARTIAL.
11. Jumlah OUT_OF_SCOPE.
12. Jumlah BLOCKED.
13. Jumlah NOT_VERIFIED.

Jangan menjumlahkan persentase dari denominator yang berbeda tanpa definisi.

Jangan menggunakan total test PASS sebagai persentase kepatuhan requirement.

Jangan mengklaim 100% production readiness selama acceptance gate penting belum terverifikasi.

---

# 14. ONE-FILE FINAL REPORT STRUCTURE

Buat atau perbarui hanya SATU laporan Markdown:

`doc/testing/TASK8-FINAL-VERIFICATION.md`

Gunakan struktur:

## 1. Executive Summary

- Objective.
- Actual execution scope.
- Baseline.
- Final verdict.

## 2. Environment & Tool Versions

- Python.
- Node.js.
- PostgreSQL.
- Frontend dependencies.
- Test frameworks.
- Browser engines.
- Environment limitations.

## 3. Skills & CodeGraph Execution Evidence

- Skills loaded.
- CodeGraph operations.
- Affected modules.

## 4. Test Inventory & Numeric Reconciliation

- Previous Task 7 totals.
- Actual collected tests.
- Actual executed tests.
- Test categories.
- PASS/FAIL/SKIPPED/BLOCKED counts.

## 5. Official PRD AT-01–AT-30 Matrix

Include exact official AT definitions, executable test references, environment, and actual results.

## 6. Database Schema & PostgreSQL Verification

- Canonical 19 tables.
- Actual PostgreSQL tables.
- Columns.
- Constraints.
- Migrations.
- Differences.
- Corrections.

## 7. Business Rule Verification

- Handoff.
- Payments.
- Customer duplicate handling.
- Status enums.
- Financial reports.
- Idempotency.
- Tracking.

## 8. Frontend FE-01–FE-09 Results

- Unit.
- Component.
- Integration.
- Real E2E.
- Visual regression.
- Cross-browser.
- Accessibility.
- Performance.
- Localization.

## 9. Backend BE-01–BE-13 Results

- Unit.
- Integration.
- API.
- Contract.
- Business E2E.
- Load.
- Stress.
- Spike.
- Soak.
- Security.
- Resilience.
- Smoke.
- Sanity.

## 10. Browser & Responsive Matrix

- Browser engines.
- Viewports.
- Results.
- Failures.
- Evidence paths.

## 11. Performance Benchmark

- Workloads.
- Durations.
- RPS.
- Latency.
- Memory.
- CPU.
- Recovery.

## 12. Security Verification

- Auth.
- CSRF.
- RBAC.
- IDOR.
- Data privacy.
- Dependency security.

## 13. Bug & Remediation Register

For each defect:

| Bug ID | Severity | Requirement | Root Cause | Code Changed | Test Evidence | Status |
| ------ | -------- | ----------- | ---------- | ------------ | ------------- | ------ |

## 14. Source Code Changes

For each changed file:

- Path.
- Reason.
- Description of change.
- Related requirement.
- Validation performed.

## 15. Regression Results

- Frontend.
- Backend.
- PostgreSQL.
- Browser E2E.
- Security.
- Contracts.

## 16. Outstanding Findings

- FAILED.
- BLOCKED.
- NOT_VERIFIED.
- PARTIAL.
- DECISION_REQUIRED.

## 17. Final Acceptance Scorecard

| Gate                   | Result | Evidence |
| ---------------------- | ------ | -------- |
| PRD P0 Compliance      |        |          |
| PRD AT-01–AT-30       |        |          |
| Frontend Test Suite    |        |          |
| Backend Test Suite     |        |          |
| PostgreSQL Integration |        |          |
| API Contract           |        |          |
| Real Browser E2E       |        |          |
| Cross-Browser          |        |          |
| Visual Regression      |        |          |
| Accessibility          |        |          |
| Performance            |        |          |
| Security               |        |          |
| Deployment Runtime     |        |          |
| Owner UAT              |        |          |
| Production Readiness   |        |          |

## 18. Final Verdict & Next Actions

State clearly:

- What was verified.
- What was fixed.
- What remains.
- Whether deployment readiness is proven.
- Whether owner approval is still required.

## 19. Reproduction Commands

Include exact commands needed to reproduce each test suite.

## 20. Git Change Integrity

Include:

- Baseline Git status.
- Final Git status.
- Modified source files.
- Added test files.
- Confirmation that no unrelated user changes were discarded.
- Confirmation that only one Markdown report was authored for Task 8.

---

# 15. ACCEPTANCE CRITERIA

Task 8 may be considered successfully executed when:

1. All official PRD AT IDs have correct mappings.
2. All mandatory P0 requirements have relevant test coverage.
3. All critical business tests pass or genuine blockers are documented.
4. PostgreSQL schema matches canonical requirements or differences are explained and fixed safely.
5. Financial invariants are verified.
6. All critical frontend workflows are tested.
7. Browser and viewport coverage matches DBD requirements.
8. Cross-browser results are correctly classified.
9. Visual regression has valid evidence.
10. Security-critical tests pass.
11. Performance testing accurately reflects measured workloads.
12. Numerical inconsistencies are corrected.
13. Bug fixes have regression tests.
14. No previously working feature is broken.
15. Exactly one Task 8 Markdown report is produced.

Do not confuse TASK_EXECUTION_COMPLETE with FULL_PRODUCT_ACCEPTANCE.

A task may complete with external blockers explicitly documented.

---

# 16. SAFETY RULES

Do not:

- Delete or overwrite production data.
- Run destructive database commands on non-test databases.
- Deploy publicly without approval.
- Send WhatsApp messages to real customers.
- Use paid services without approval.
- Expose secrets in logs or Markdown reports.
- Perform force push.
- Delete unrelated user work.
- Modify canonical requirements to hide defects.
- Claim Docker PASS if Docker CLI/runtime is unavailable.

Use isolated database testing and synthetic records.

Respect all existing application security policies.

---

# 17. AUTONOMOUS EXECUTION ORDER

Execute:

1. Read authoritative documents.
2. Read skills.
3. Inspect CodeGraph.
4. Audit Git status.
5. Reconcile Task 7 test counts.
6. Fix PRD AT mappings.
7. Verify canonical database schema.
8. Audit business rules.
9. Complete frontend verification.
10. Complete backend verification.
11. Fix actual code defects.
12. Run targeted tests.
13. Run full regression tests.
14. Recalculate all test and compliance metrics.
15. Write one Markdown report.
16. Verify file references and final Git diff.

Continue completing safe, independent tasks even if some environment dependencies are blocked.

Do not stop after writing a plan.

Do not stop after writing tests.

Do not stop after finding bugs.

---

# FINAL ABSOLUTE DIRECTIVE

**FOLLOW PRD, TRD, AFD, DBD, BSD, AND IPD.**

**USE THE INSTALLED PROJECT SKILLS.**

**USE CODEGRAPH-FIRST.**

**FIX WRONG ACCEPTANCE TEST MAPPINGS.**

**VERIFY REAL POSTGRESQL SCHEMA.**

**FIX APPLICATION CODE WHEN TESTS REVEAL REAL BUGS.**

**DO NOT MODIFY TEST EXPECTATIONS TO HIDE DEFECTS.**

**RUN REAL BROWSER E2E.**

**VERIFY FRONTEND AND BACKEND TEST CATEGORIES WITH ACTUAL EVIDENCE.**

**NO FALSE 100% CLAIMS.**

**NO FALSE PRODUCTION READY CLAIMS.**

**WRITE ALL TASK 8 RESULTS INTO ONE MARKDOWN FILE ONLY.**

## FINAL OUTPUT PATH

`doc/testing/TASK8-FINAL-VERIFICATION.md`

## START TASK 8 NOW.
