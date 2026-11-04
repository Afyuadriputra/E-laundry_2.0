
# MASTER TASK — PRD-DRIVEN BACKEND TESTING & AUTOMATED BUG REMEDIATION

## Project: E-Laundry 2.0

### Mission: 100% P0 Feature Coverage, Evidence-Based Testing & Business Logic Correctness

# 1. ROLE & OBJECTIVE

Berperanlah sebagai:

- Principal Software Development Engineer in Test (SDET)
- Senior FastAPI Backend Engineer
- PostgreSQL Database Engineer
- QA Automation Architect
- Application Security Engineer
- Performance & Reliability Engineer
- Software Quality Assurance Lead

Tugas Anda adalah melakukan **pengujian backend secara menyeluruh berdasarkan Product Requirements Document (PRD) E-Laundry 2.0**, kemudian memperbaiki semua masalah kode yang terbukti menyebabkan pengujian gagal.

**PRIMARY GOAL: EVERY REQUIRED MVP FEATURE MUST WORK CORRECTLY ACCORDING TO THE PRD, NOT MERELY RETURN SUCCESSFUL HTTP RESPONSES.**

Saya tidak membutuhkan sekadar jumlah test yang banyak.

Saya membutuhkan bukti bahwa setiap fitur benar-benar memenuhi aturan bisnis, hak akses, validasi, alur transaksi, integritas database, dan acceptance criteria dari PRD.

## Prinsip utama

**READ PRD → EXTRACT REQUIREMENTS → DESIGN TESTS → EXECUTE → FIND BUG → FIX SOURCE CODE → REGRESSION TEST → VERIFY.**

Jangan berhenti pada pembuatan test suite.

Jika test gagal karena bug pada kode aplikasi, lakukan root-cause analysis dan perbaiki implementasi.

Jangan mengubah expected result menjadi sesuai dengan bug.

Jangan memalsukan hasil pengujian.

Jangan menghapus test yang gagal untuk meningkatkan pass rate.

---

# 2. WORKSPACE & SOURCE OF TRUTH

Repository:

`D:\Kuliah\joki\Kerja Praktek Aqil\kawan aqil\projek`

## Dokumen utama

**Primary product source of truth:**

`doc/PRD.md`

Periksa juga:

- `doc/TRD.md`
- `doc/AFD.md`
- `doc/BSD.md`
- `doc/DBD.md`
- `doc/IPD.md`
- `doc/SKILLS-CATALOG.md`
- `doc/api/openapi.json`
- `AGENTS.md`
- `doc/implementation/MASTER-TRACKER.md`
- `doc/implementation/FULL-COMPLIANCE-MATRIX.md`
- `doc/implementation/GAP-REMEDIATION-REGISTER.md`
- `doc/implementation/REAL-INTEGRATION-TEST-REPORT.md`

Gunakan `PRD.md` untuk memastikan expected business behavior, TRD untuk nonfunctional requirements, AFD untuk workflows, BSD untuk database/domain contracts, dan OpenAPI untuk HTTP contracts.

Jangan menganggap previous PASS reports sebagai bukti final.

Jika ada konflik antar dokumen, tunjukkan pasal yang bertentangan dan identifikasi aturan yang sudah disetujui. Jangan diam-diam mengubah aturan bisnis atau menganggap keputusan terbuka telah disetujui.

---

# 3. CODEGRAPH-FIRST & SKILL-AWARE TESTING

Sebelum membaca dan mengubah kode:

1. Periksa CodeGraph index.
2. Sinkronkan graph bila diperlukan.
3. Gunakan CodeGraph untuk menemukan implementasi setiap fitur.
4. Telusuri call graph dan dependensi antar modul.
5. Identifikasi service, repository, model, router, dan test terkait.
6. Periksa dampak setiap perbaikan sebelum melakukan perubahan.

Gunakan skills relevan yang telah terpasang dan dikonfigurasi dalam `AGENTS.md` dan `doc/SKILLS-CATALOG.md`.

Prioritaskan:

- `tdd`
- `fastapi`
- `security-audit`
- Skills code quality dan architecture yang relevan.

Baca instruksi `SKILL.md` ketika menggunakan sebuah skill.

Jangan mengklaim skill telah digunakan tanpa benar-benar menerapkan instruksinya.

---

# 4. EXTRACT ALL PRD REQUIREMENTS

PRD memuat 101 feature IDs dari delapan modul.

| Module            | Feature IDs      |         Total |
| ----------------- | ---------------- | ------------: |
| Dashboard         | DASH-01–DASH-10 |            10 |
| Orders            | ORD-01–ORD-18   |            18 |
| Customers         | CUS-01–CUS-09   |             9 |
| Pickup & Delivery | PUD-01–PUD-14   |            14 |
| Finance           | FIN-01–FIN-15   |            15 |
| Digital Invoice   | INV-01–INV-10   |            10 |
| Public Tracking   | TRK-01–TRK-12   |            12 |
| Settings          | SET-01–SET-13   |            13 |
| **TOTAL**   |                  | **101** |

Berdasarkan PRD, terdapat:

- 86 fitur P0.
- 11 fitur P1.
- 4 fitur P2.

Verifikasi kembali hitungan ini terhadap `doc/PRD.md` aktual.

## Mandatory coverage rules

1. Semua 86 fitur P0 wajib memiliki pemetaan acceptance test yang relevan.
2. Semua fitur P0 harus lulus pengujian yang sesuai sebelum dinyatakan MVP-ready.
3. Fitur P1 yang sudah diimplementasikan tetap harus diuji dan diperbaiki jika rusak.
4. Fitur P1 yang belum diimplementasikan ditandai sebagai scope pengembangan berikutnya sesuai prioritas PRD.
5. Fitur P2 yang berada di luar MVP tidak perlu dibuat hanya untuk mencapai angka 100%.
6. Semua fitur harus dipetakan, termasuk fitur yang tidak memerlukan backend testing secara langsung.
7. Jangan membuat satu test kosong untuk setiap ID hanya demi memenuhi coverage.

Untuk setiap fitur, buat traceability:

`Feature ID → PRD Section → Business Rule → Implementation → Test Cases → Results → Bug/Fix → Evidence`.

---

# 5. EIGHT REQUIRED TEST CATEGORIES

Implementasikan delapan kategori pengujian berikut.

## A. UNIT TESTING

**Tujuan:** Memverifikasi logika internal secara terisolasi.

Gunakan pytest, parametrized tests, fixtures, mocks/stubs apabila diperlukan.

Fokus:

- Pricing calculation.
- Decimal precision.
- Weight rounding.
- Minimum weight configuration.
- Order total calculation.
- Payment balance.
- Payment status derivation.
- Payment void exclusion.
- State machine transitions.
- Token generation and masking.
- Date/time calculations.
- Overdue calculation.
- Role/permission logic.
- CSV sanitization.
- WhatsApp message formatting.
- Domain invariants.

Setiap domain rule wajib memiliki:

- Happy-path tests.
- Boundary-value tests.
- Invalid-input tests.
- Negative tests.
- Edge-case tests.

Gunakan property-based testing apabila benar-benar memberi manfaat terhadap aturan matematis dan invariants, tanpa menambah dependency yang tidak diperlukan.

**Gate: UNIT_TESTS_PASS**

---

## B. INTEGRATION TESTING

**Tujuan:** Membuktikan interaksi backend dan database nyata.

Database wajib menggunakan PostgreSQL untuk verifikasi fitur yang bergantung pada PostgreSQL.

Gunakan:

- FastAPI.
- SQLAlchemy.
- PostgreSQL 17.
- Alembic.
- pytest.
- HTTPX/TestClient sesuai karakter pengujian.

Jangan menggunakan SQLite untuk mengklaim PostgreSQL integration test PASS.

Test mencakup:

- Model persistence.
- Foreign keys.
- Unique constraints.
- Check constraints.
- Transaction commit/rollback.
- Concurrent transactions.
- Optimistic locking.
- Pessimistic locking.
- Idempotency.
- Order/payment relationship.
- Pickup-to-order conversion.
- Payment void and audit logging.
- Token lifecycle.
- Financial reconciliation.

Gunakan database pengujian yang terisolasi.

Lakukan migration from empty database to head untuk menguji seluruh revision chain.

Jangan menebak password atau mereset database pengguna.

Jika PostgreSQL belum tersedia, tandai BLOCKED dan jangan menggantinya dengan klaim PASS dari SQLite.

**Gate: POSTGRESQL_INTEGRATION_PASS**

---

## C. CONTRACT TESTING

**Tujuan:** Memastikan API backend konsisten dengan kontrak yang digunakan frontend dan konsumen lainnya.

Gunakan `doc/api/openapi.json` serta kontrak aktual dari FastAPI.

Pact dapat digunakan jika benar-benar terdapat consumer-provider Pact contract yang disepakati. Jangan membuat kontrak Pact fiktif hanya untuk menampilkan PASS.

Validasi:

- Endpoint path.
- HTTP methods.
- Request schemas.
- Response schemas.
- Required fields.
- Optional/null fields.
- Enum values.
- Validation errors.
- HTTP status codes.
- Error response structures.
- Authentication requirements.
- CSRF requirements.
- Pagination.
- Date/time serialization.
- Decimal/money representation.
- Backward compatibility.

Lakukan pengujian terhadap API aktual, bukan hanya membandingkan dua file JSON.

Periksa apakah frontend contract cocok dengan OpenAPI.

**Gate: API_CONTRACT_PASS**

---

## D. FUNCTIONAL API TESTING

**Tujuan:** Memvalidasi fitur bisnis dari perspektif pengguna melalui endpoint.

Setiap fitur P0 harus mempunyai skenario fungsional yang relevan.

Untuk setiap endpoint, uji:

1. Request valid.
2. Request invalid.
3. Missing required fields.
4. Invalid data types.
5. Unauthorized user.
6. Forbidden role.
7. Missing CSRF untuk operasi relevan.
8. Resource not found.
9. Duplicate request.
10. Data integrity after request.
11. Proper response payload.
12. Proper response status and headers.

Jangan hanya menguji bahwa endpoint mengembalikan HTTP 200.

Validasi perubahan yang benar-benar tersimpan di database dan side effect yang diwajibkan.

**Gate: FUNCTIONAL_API_PASS**

---

## E. BACKEND END-TO-END BUSINESS WORKFLOW

**Tujuan:** Memverifikasi keseluruhan transaksi melalui rangkaian API nyata, menggunakan database test yang sama.

Jalankan journey yang menghubungkan beberapa modul:

### Journey 1 — Walk-in laundry order

Owner/Kasir login → Cari atau buat pelanggan → Pilih layanan → Input berat atau jumlah → Hitung harga → Buat order → Staf memproses cucian → Update status → Buat nota PDF → Pembayaran → Serah terima → Selesai → Dashboard dan laporan diperbarui.

### Journey 2 — Pickup to delivery

Pelanggan mengajukan pickup tanpa login → Admin mengonfirmasi → Kurir ditugaskan → Pickup → Cucian tiba di laundry → Penimbangan → Konversi menjadi order → Laundry processing → Delivery assignment → Handoff → Order completed.

### Journey 3 — Partial payment

Buat order Rp50.000 → Bayar DP Rp20.000 → Sisa Rp30.000 → Bayar Rp30.000 → Status Lunas → Verifikasi laporan keuangan.

### Journey 4 — Financial correction

Pembayaran tercatat → Void dengan izin dan alasan sah → Audit log tercatat → Saldo dihitung ulang → Laporan berubah dengan benar.

### Journey 5 — Public tracking

Generate token → Akses tanpa login → Update status oleh petugas → Tracking menampilkan status baru → Revoke token → Token lama tidak dapat dipakai → Tidak ada data pelanggan lain bocor.

### Journey 6 — Permission & security

Owner, Cashier, Staff, dan Courier menggunakan endpoint berdasarkan hak akses PRD §4.2.

Semua akses yang tidak sah wajib ditolak backend, sekalipun URL atau request dibuat secara manual.

**Gate: BACKEND_BUSINESS_E2E_PASS**

---

## F. LOAD & STRESS TESTING

**Tujuan:** Menguji performa backend, kestabilan transaksi, dan resource usage.

Gunakan Locust, k6, atau tooling yang paling sesuai dengan environment dan stack proyek.

Baca target dari PRD §12.2 dan TRD sebelum menentukan threshold.

Uji workload representatif:

- Login.
- List orders.
- Search customers.
- Create order.
- Record payment.
- Update order status.
- Public tracking.
- Dashboard aggregation.
- Reports.
- Concurrent cashier operations.

Ukur:

- Requests per second.
- Throughput.
- p50/p95/p99 latency.
- Error rate.
- CPU utilization.
- RAM utilization.
- Database connection pool.
- Transaction contention.

Wajib ada stress scenarios:

- Simultaneous payment attempts.
- Concurrent order modifications.
- Repeated idempotency keys.
- High-frequency public tracking requests.
- Concurrent order creation.
- Slow database queries.

Jangan melakukan destructive stress testing pada database produksi.

Gunakan staging/test environment dengan spesifikasi yang dicatat secara jelas.

Jika staging representatif tidak tersedia, lakukan benchmark lokal terbatas, lalu tandai production-like load test sebagai NOT_VERIFIED.

**Gate: PERFORMANCE_BASELINE_VERIFIED**

---

## G. SECURITY TESTING

**Tujuan:** Memverifikasi autentikasi, otorisasi, perlindungan data, dan integritas bisnis.

Gunakan PRD §12.1 dan OWASP sebagai panduan teknis.

Wajib uji:

- Password hashing.
- Invalid credentials.
- Session expiration.
- Session revocation.
- Secure cookie configuration.
- CSRF enforcement.
- RBAC.
- IDOR.
- SQL injection resistance.
- XSS-related output handling.
- Public token enumeration.
- Token revocation.
- Tracking data leakage.
- Rate limiting.
- Sensitive data in logs.
- Audit log immutability.
- Owner-only operations.
- Courier scope restriction.
- Staff scope restriction.
- Improper payment modification.
- Unauthorized price changes.
- Repeated or replayed requests.

Gunakan pengujian terotorisasi pada environment sendiri.

Jangan melakukan penetration testing terhadap host di luar proyek.

**Gate: CRITICAL_SECURITY_TESTS_PASS**

---

## H. SMOKE TESTING

**Tujuan:** Memastikan service utama dapat digunakan setelah aplikasi dijalankan pada environment target.

Uji:

- Backend startup.
- API health/liveness.
- Readiness.
- Database connectivity.
- Authentication.
- Customer endpoint.
- Order endpoint.
- Payment endpoint.
- Public tracking endpoint.
- Invoice endpoint.
- Dashboard endpoint.

Smoke test harus menggunakan runtime nyata, bukan import module saja.

Jika belum melakukan deployment staging, tandai STAGING_SMOKE_NOT_VERIFIED.

Jangan menggunakan status smoke PASS untuk mengklaim bahwa seluruh functional tests telah lulus.

**Gate: TARGET_ENVIRONMENT_SMOKE_PASS**

---

# 6. MANDATORY PRD ACCEPTANCE TESTS

PRD §15.2 mendefinisikan 30 acceptance tests.

Buat executable test coverage untuk:

- AT-01 sampai AT-30.

Jangan menghilangkan satu pun ID.

Pastikan:

- AT-01–AT-02: Login.
- AT-03–AT-06: Order creation, pricing, multiple services, historical price snapshot.
- AT-07–AT-08: Invoice dan WhatsApp manual.
- AT-09–AT-13: Status history dan secure tracking.
- AT-14–AT-17: Pickup, courier, conversion.
- AT-18–AT-20: DP, settlement, overpayment prevention.
- AT-21–AT-23: Expenses dan RBAC.
- AT-24–AT-26: Cancellation, concurrent edits, duplicate prevention.
- AT-27: Network failure dan konsistensi transaksi.
- AT-28: Failed delivery dan rescheduling.
- AT-29: Overdue identification.
- AT-30: Backup/restore.

Satu AT boleh diuji oleh beberapa test jika dibutuhkan.

Test dengan fixture mock tidak boleh menjadi satu-satunya bukti untuk AT yang membutuhkan transaksi database nyata.

**AT-30 wajib diuji pada database yang aman sebelum production sign-off.**

---

# 7. CRITICAL PRD BUSINESS RULE RECONCILIATION

Periksa seluruh aturan bisnis existing terhadap PRD.

## CRITICAL — Unpaid Order Handoff

PRD §5.5, §6.1, dan §6.4 menjelaskan bahwa cucian dapat diserahkan meskipun tagihan belum lunas, dengan peringatan dan piutang tetap tercatat.

Implementation plan sebelumnya pernah menggunakan invariant:

`COMPLETED requires payment_status == PAID`

Ini berpotensi bertentangan dengan PRD.

Audit:

- Order completion rules.
- Handoff requirements.
- Payment invariants.
- Outstanding balance preservation.
- Warning behavior.
- Audit records.

Jangan menganggap pelunasan merupakan syarat mutlak jika aturan yang berlaku mengizinkan serah terima dengan piutang.

Buat test yang membuktikan:

1. Serah terima membutuhkan bukti/konfirmasi yang sah.
2. Order yang masih memiliki sisa tagihan dapat mengikuti alur serah terima yang diizinkan oleh PRD.
3. Sistem memberikan peringatan sesuai business requirement.
4. Piutang tetap tercatat.
5. Status pembayaran tidak otomatis menjadi PAID.
6. Laporan piutang tetap akurat.

Jika dokumen implementasi yang lebih baru secara sah mengubah aturan ini, catat keputusan dan sumber persetujuannya. Jangan membuat asumsi sendiri.

## CRITICAL — Decision Register Conflicts

PRD §19.3 memuat keputusan terbuka DEC-01 sampai DEC-10.

Penomoran tersebut tidak otomatis sama dengan keputusan pada implementation register sebelumnya.

Jangan memetakan dua decision ID yang memiliki makna berbeda hanya karena nomor identik.

Verifikasi semua keputusan terhadap konteks, versi, dan status persetujuannya.

## CRITICAL — Pricing Configuration

PRD §8.1 menyatakan presisi berat dan aturan pembulatan/minimum dapat dikonfigurasi sesuai praktik usaha.

Jangan hanya menguji aturan hardcoded 0.1 kg atau minimum 3.0 kg.

Verifikasi konfigurasi aktual dan keputusan yang telah disetujui.

Jika aturan bersifat configurable, uji beberapa konfigurasi dan pastikan harga historis tetap menggunakan snapshot lama.

---

# 8. AUTOMATED BUG FIXING POLICY

Setiap test gagal harus diklasifikasikan.

Gunakan kategori:

- APPLICATION_BUG
- BUSINESS_RULE_MISMATCH
- API_CONTRACT_MISMATCH
- DATABASE_SCHEMA_DEFECT
- TRANSACTION_INTEGRITY_DEFECT
- SECURITY_DEFECT
- INVALID_TEST_ASSUMPTION
- TEST_INFRASTRUCTURE_ERROR
- EXTERNAL_DEPENDENCY_BLOCKER

Jika `APPLICATION_BUG`, `BUSINESS_RULE_MISMATCH`, atau defect implementasi lain ditemukan:

1. Reproduce failure.
2. Catat failing test.
3. Identifikasi root cause.
4. Telusuri CodeGraph.
5. Periksa PRD expected behavior.
6. Perbaiki application source code.
7. Jalankan targeted test.
8. Jalankan related regression tests.
9. Jalankan full backend suite.
10. Perbarui audit log dan laporan.

Jangan memperbaiki test agar mengikuti perilaku salah pada aplikasi.

Jika asumsi test terbukti bertentangan dengan PRD, perbaiki test dan catat alasan serta sumber requirement.

Jangan menambah mock untuk menutupi bug integrasi nyata.

Jangan menangkap semua exception lalu mengembalikan HTTP 200.

Jangan menonaktifkan authorization, CSRF, database constraints, atau financial invariants untuk mempercepat kelulusan.

Jangan menghapus fitur wajib.

---

# 9. TEST ARCHITECTURE

Pertahankan struktur pengujian existing bila masih sesuai.

Tambahkan pengelompokan yang diperlukan di bawah `backend/tests/`, misalnya:

- `unit/`
- `integration/`
- `contract/`
- `functional/`
- `e2e/`
- `security/`
- `smoke/`
- `performance/`

Jangan memindahkan seluruh test lama tanpa alasan.

Gunakan pytest markers:

`unit`, `integration`, `contract`, `functional`, `e2e`, `security`, `smoke`, `performance`, `postgres`.

Setiap test harus:

- Deterministic.
- Reproducible.
- Independent.
- Have meaningful assertions.
- Use isolated data.
- Clean up test resources.
- Avoid production credentials.
- Avoid hardcoded secrets.
- Avoid network access to real customers.

Gunakan factories dan synthetic test data.

Pastikan test tidak bergantung pada urutan eksekusi.

Jika memerlukan waktu, gunakan clock injection/frozen time agar tidak flaky.

Untuk concurrency, gunakan koneksi dan transaksi database yang benar-benar independen, bukan simulasi single-thread yang tidak membuktikan locking.

---

# 10. COVERAGE & QUALITY GATES

Gunakan `pytest-cov` atau tooling yang setara apabila tersedia.

Laporkan:

- Line coverage.
- Branch coverage.
- Coverage per module.
- Missing business-critical paths.
- Test execution time.
- Failed test list.
- Skipped test list.
- Blocked test list.

Target utama:

**100% PRD P0 REQUIREMENT TRACEABILITY AND ACCEPTANCE SATISFACTION.**

Angka code coverage bukan pengganti requirement coverage.

Prioritaskan branch coverage pada:

- Payments.
- Orders.
- State transitions.
- Authentication.
- Authorization.
- Tracking.
- Pickup conversion.
- Audit logging.
- Idempotency.

Jangan mengklaim semua fitur berjalan hanya karena coverage tinggi.

Test yang `SKIPPED`, `XFAIL`, `BLOCKED`, atau bergantung pada mock tidak boleh diklaim PASS sebagai real integration test.

---

# 11. REQUIRED REPORTS

Buat direktori:

`doc/testing/`

Buat laporan:

## A. PRD Test Traceability

`doc/testing/PRD-TEST-MATRIX.md`

Format:

| PRD ID | Priority | Expected Behavior | Test Type | Test File | Result | Evidence |
| ------ | -------- | ----------------- | --------- | --------- | ------ | -------- |

## B. Test Execution Summary

`doc/testing/BACKEND-TEST-REPORT.md`

Memuat total test, passed, failed, skipped, blocked, duration, warnings, dan environment.

## C. Bug & Fix Register

`doc/testing/BUG-REMEDIATION-REPORT.md`

Memuat:

- Bug ID.
- Requirement ID.
- Failure reproduction.
- Root cause.
- Source code fix.
- Regression test.
- Verification evidence.
- Status.

## D. Integration Verification

`doc/testing/POSTGRESQL-INTEGRATION-REPORT.md`

Memuat koneksi, schema, migrations, constraints, concurrency, locking, dan test results.

## E. Contract Verification

`doc/testing/API-CONTRACT-REPORT.md`

Memuat OpenAPI drift, schema compatibility, request/response validation, dan error contract.

## F. Security Report

`doc/testing/SECURITY-TEST-REPORT.md`

Memuat vulnerability findings, severity, remediation, residual risks, dan test evidence.

## G. Performance Report

`doc/testing/PERFORMANCE-TEST-REPORT.md`

Memuat workload, environment, latency, throughput, error rate, dan resource usage.

## H. Final PRD Acceptance Report

`doc/testing/FINAL-PRD-ACCEPTANCE.md`

Memuat:

- Total PRD features.
- Total P0/P1/P2.
- P0 requirements passed.
- P0 requirements failed.
- P0 requirements blocked.
- AT-01–AT-30 results.
- Test categories completed.
- Defects fixed.
- Open defects.
- Database readiness.
- Security readiness.
- Performance findings.
- Final acceptance verdict.

---

# 12. CI/CD TEST STRATEGY

Siapkan test commands/scripts agar dapat digunakan ulang.

Pisahkan:

**Fast Suite — Every Commit**

- Unit tests.
- Static analysis.
- Targeted contract checks.

**Integration Suite — Pull Requests**

- PostgreSQL integration tests.
- API functional tests.
- Security regression.
- Relevant migration checks.

**Pre-Release Suite**

- Full backend E2E.
- Load/performance.
- Security audit.
- Recovery verification.
- Full contract validation.

**Post-Deployment Suite**

- Safe smoke tests on authorized environment.

Jangan menjalankan destructive tests secara otomatis pada production.

Jangan membuat workflow CI yang membutuhkan secret nyata di repository.

---

# 13. EXECUTION SEQUENCE

Lakukan pekerjaan ini secara bertahap tanpa berhenti setelah menyusun rencana.

## Phase 1 — PRD Requirement Extraction

- Read the entire PRD.
- Extract all feature IDs.
- Extract AT-01–AT-30.
- Extract business rules.
- Extract role permission matrix.
- Extract security and performance NFRs.
- Build PRD test traceability matrix.

## Phase 2 — Existing Test Audit

- Discover all existing backend tests.
- Identify false coverage claims.
- Identify missing requirements.
- Classify mock vs PostgreSQL-real tests.
- Identify broken or weak assertions.

## Phase 3 — Unit & Functional Tests

- Implement missing tests.
- Run tests.
- Fix application code.
- Re-run until tests pass or genuine blockers are documented.

## Phase 4 — PostgreSQL Integration Tests

- Verify test DB.
- Verify migrations.
- Test database invariants.
- Test concurrency.
- Fix code and migration defects safely.

## Phase 5 — Contract & Security Tests

- Validate OpenAPI.
- Validate request/response behavior.
- Validate RBAC and CSRF.
- Validate tracking and data isolation.
- Fix confirmed defects.

## Phase 6 — Backend Business E2E

- Execute real API business journeys.
- Use shared isolated PostgreSQL test environment.
- Verify data changes after each operation.
- Test rollback and business invariants.

## Phase 7 — Performance & Stress

- Execute safe workloads.
- Measure actual latency and throughput.
- Fix performance defects within scope.
- Compare with TRD/PRD targets.

## Phase 8 — Smoke & Full Regression

- Re-run all backend tests.
- Verify no regressions.
- Execute available environment smoke tests.
- Update compliance matrix.

## Phase 9 — Final Acceptance

- Recalculate P0 coverage.
- Recalculate AT-01–AT-30 results.
- Update final reports.
- Present evidence-based verdict.

---

# 14. FINAL ACCEPTANCE RULES

Gunakan status:

- PASS
- FAIL
- BLOCKED
- NOT_VERIFIED
- NOT_APPLICABLE
- OUT_OF_SCOPE

**PRD_BACKEND_ACCEPTANCE_PASS** hanya boleh diberikan jika:

1. Seluruh fitur backend P0 yang relevan memenuhi acceptance criteria.
2. Seluruh acceptance tests kritis lulus.
3. Tidak ada critical financial bugs.
4. Tidak ada known RBAC bypass.
5. Tidak ada known cross-customer data leakage.
6. Tidak ada duplicate payment/order dalam skenario concurrency yang diuji.
7. PostgreSQL integration tests lulus.
8. Contract tests relevan lulus.
9. Security tests kritis lulus.
10. Backend business E2E lulus.
11. Tidak ada P0 defect yang masih terbuka.
12. Semua test evidence tersedia dan dapat diperiksa.

Untuk readiness MVP penuh, PRD juga memerlukan pengujian mobile, backup/restore, UAT, serta persetujuan Owner. Jangan menganggap backend acceptance otomatis berarti keseluruhan produk sudah production-ready.

Jika environment eksternal tidak tersedia, tandai BLOCKED secara jujur.

Jangan memaksa status PASS.

---

# 15. AUTONOMOUS REMEDIATION AUTHORIZATION

Anda diperbolehkan:

- Membuat automated tests.
- Memperbaiki backend application code.
- Memperbaiki API contract mismatches.
- Memperbaiki domain/business logic.
- Memperbaiki database migrations pada lingkungan pengembangan secara aman.
- Menambahkan validation dan constraints yang dibutuhkan.
- Memperbaiki security defects.
- Memperbaiki performance issues.
- Memperbarui testing documentation.
- Menambahkan CI test workflows bila sesuai.

Anda tidak diperbolehkan tanpa persetujuan:

- Mengubah PRD resmi.
- Mengubah keputusan bisnis yang belum disetujui.
- Menghapus database existing.
- Mengubah database production.
- Melakukan public deployment.
- Mengirim WhatsApp nyata.
- Mengakses layanan berbayar.
- Menghapus data pelanggan.
- Melakukan force push.
- Melemahkan security controls.

Jika ditemukan konflik bisnis yang tidak bisa diputuskan berdasarkan dokumen, catat sebagai DECISION_REQUIRED, buat test yang relevan tanpa memaksakan expected behavior yang belum sah, dan lanjutkan pekerjaan independen.

---

# 16. FINAL DIRECTIVE

**BUILD REAL TESTS.**

**TEST EVERY PRD P0 BACKEND REQUIREMENT.**

**VERIFY ALL 30 PRD ACCEPTANCE TESTS.**

**FIX APPLICATION CODE WHEN TESTS REVEAL BUGS.**

**DO NOT CHANGE TEST EXPECTATIONS TO HIDE BUGS.**

**USE REAL POSTGRESQL FOR INTEGRATION TESTS.**

**VERIFY BUSINESS WORKFLOWS END TO END.**

**VERIFY RBAC, SECURITY, FINANCIAL INVARIANTS, AND TRANSACTION ATOMICITY.**

**DO NOT CLAIM PASS WITHOUT EVIDENCE.**

**CONTINUE AUDIT → FIX → RETEST UNTIL ALL FEASIBLE REQUIREMENTS PASS.**

## START NOW

Mulai dengan membaca `doc/PRD.md` secara menyeluruh, membuat PRD-to-Test traceability matrix, mengaudit existing backend tests, lalu langsung mengimplementasikan seluruh missing tests dan memperbaiki kode yang terbukti tidak sesuai.

Berikan hasil akhir berupa executable test suite, kode backend yang telah diperbaiki, dan laporan kelulusan setiap fitur terhadap PRD.
