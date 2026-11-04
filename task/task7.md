
# MASTER TASK — E-LAUNDRY 2.0

## COMPREHENSIVE FULL-STACK TESTING, AUTOMATED BUG FIXING & DOCUMENTATION COMPLIANCE

### FRONTEND 9 TEST CATEGORIES + BACKEND 13 TEST CATEGORIES

### EXECUTION MODE — TEST → DEBUG → FIX → RETEST → VERIFY

---

# 1. ROLE & PRIMARY MISSION

Berperanlah sebagai tim software engineering profesional yang terdiri dari:

1. Principal Software Architect.
2. Principal SDET / Test Automation Architect.
3. Senior React & TypeScript Engineer.
4. Senior FastAPI & Python Engineer.
5. PostgreSQL Database Architect.
6. Application Security Engineer.
7. Performance & Reliability Engineer.
8. Senior UI/UX & Accessibility Engineer.
9. DevOps / CI Engineering Lead.
10. QA Engineering Lead.

Anda bertanggung jawab melakukan pengujian komprehensif terhadap seluruh aplikasi **E-Laundry 2.0** yang telah diimplementasikan pada milestone M0–M8.

## PRIMARY GOAL

**SELURUH FITUR WAJIB E-LAUNDRY 2.0 HARUS BERFUNGSI DENGAN BENAR SESUAI PRD, TRD, AFD, DBD, BSD, DAN IPD.**

Tugas Anda tidak berhenti pada penulisan test.

Anda wajib:

- Memeriksa implementasi aplikasi aktual.
- Menganalisis persyaratan enam dokumen resmi.
- Menemukan kekurangan cakupan pengujian.
- Membuat test yang benar-benar memverifikasi requirement.
- Menjalankan pengujian.
- Mengidentifikasi penyebab kegagalan.
- Memperbaiki source code yang salah.
- Memperbaiki integrasi frontend dan backend.
- Memperbaiki masalah database secara aman.
- Menjalankan pengujian ulang.
- Mencegah regresi.
- Mendokumentasikan hasil secara objektif.

Gunakan pendekatan:

**REQUIREMENT → TEST CASE → EXECUTION → FAILURE ANALYSIS → CODE FIX → TARGETED RETEST → FULL REGRESSION → ACCEPTANCE VERIFICATION.**

Jangan menyatakan aplikasi selesai hanya karena pytest, ESLint, dan build berhasil.

---

# 2. PROJECT WORKSPACE

Root:

`D:\Kuliah\joki\Kerja Praktek Aqil\kawan aqil\projek`

Gunakan workspace tersebut sebagai working directory utama.

Jangan membuat ulang proyek.

Jangan menginisialisasi repository baru.

Jangan mengganti arsitektur modular monolith dengan microservices.

Jangan menghapus fitur yang sudah bekerja.

Lakukan incremental corrections terhadap implementasi existing.

## Source of Truth

Baca secara lengkap:

1. `doc/PRD.md`
2. `doc/TRD.md`
3. `doc/AFD.md`
4. `doc/DBD.md`
5. `doc/BSD.md`
6. `doc/IPD.md`

Dokumen pendukung:

- `AGENTS.md`
- `doc/SKILLS-CATALOG.md`
- `doc/CODEGRAPH-GUIDE.md`
- `doc/api/openapi.json`
- `doc/implementation/MASTER-TRACKER.md`
- Seluruh laporan M0–M8.
- Seluruh laporan audit dan pengujian sebelumnya.
- Seluruh decision register yang berlaku.

## Document Responsibilities

- PRD: Business requirements, feature IDs, roles, acceptance criteria.
- TRD: Technology, security, performance, reliability.
- AFD: Application flows dan state transitions.
- DBD: Design Brief Documentation, UI/UX, accessibility.
- BSD: Backend Schema Documentation, database, API, invariants.
- IPD: Official tasks, milestones, dependencies, acceptance gates.

Prioritaskan requirement resmi dan keputusan yang telah disahkan.

Jangan mengubah spesifikasi agar sesuai dengan bug aplikasi.

Jika terdapat konflik antar dokumen, identifikasi dan dokumentasikan. Jangan membuat keputusan bisnis baru tanpa persetujuan.

---

# 3. MANDATORY PROJECT SKILLS

**USE ALL RELEVANT INSTALLED PROJECT SKILLS.**

Sebelum melakukan testing atau perbaikan:

1. Baca `AGENTS.md`.
2. Baca `doc/SKILLS-CATALOG.md`.
3. Inspeksi `.agents/skills/`.
4. Identifikasi skills yang relevan untuk setiap kategori pekerjaan.
5. Baca instruksi `SKILL.md` dari skills yang dipilih.
6. Terapkan aturan invocation dan workflow masing-masing skill.

Contoh kategori skill:

**Frontend**

- `ui-taste`
- `ios-design`
- UI accessibility skills.
- Relevant testing and React skills.

**Backend**

- `fastapi`
- `tdd`
- `security-audit`
- Relevant database and Python skills.

**Architecture & Quality**

- Relevant code quality skills.
- Relevant architecture skills.
- Appropriate debugging and performance skills.

Gunakan hanya skills yang benar-benar tersedia dan sesuai dengan pekerjaan.

Jangan memaksakan penggunaan semua skills bila tidak relevan.

## CodeGraph-First

Gunakan CodeGraph untuk:

- Symbol discovery.
- Caller/callee analysis.
- Dependency mapping.
- Impact analysis.
- Test impact analysis.
- Detection of architectural dependencies.
- Identifying affected code before refactoring.

Baca `doc/CODEGRAPH-GUIDE.md`.

Sinkronkan indeks bila diperlukan dan aman.

Jangan melakukan blind recursive exploration apabila CodeGraph dapat memberikan konteks yang lebih tepat.

Jika CodeGraph tidak tersedia atau tidak cukup, gunakan inspeksi kode langsung.

---

# 4. REQUIREMENT-DRIVEN TESTING STRATEGY

Sebelum menulis test:

1. Ekstrak seluruh feature IDs dari PRD.
2. Ekstrak acceptance tests AT-01 sampai AT-30.
3. Ekstrak seluruh NFR.
4. Ekstrak role permissions.
5. Ekstrak state machines.
6. Ekstrak database invariants.
7. Ekstrak requirements DBD.
8. Ekstrak acceptance criteria IPD.
9. Cocokkan dengan implementasi aktual.

PRD sebelumnya mencantumkan:

- 101 feature IDs.
- 86 P0 features.
- 11 P1 features.
- 4 P2 features.
- 30 acceptance tests.

Verifikasi jumlah tersebut dari dokumen aktual; jangan menggunakan angka historis tanpa pemeriksaan.

## Mandatory Feature Coverage

- Seluruh P0 wajib diuji sesuai lapisan yang relevan.
- Seluruh P0 wajib memenuhi acceptance criteria.
- P1 yang telah diimplementasikan wajib memiliki regression coverage.
- P2 di luar MVP tidak boleh dipaksa untuk diimplementasikan.
- Requirement frontend wajib diuji pada frontend.
- Requirement backend wajib diuji pada backend.
- Workflow lintas sistem wajib diuji dengan integrasi nyata.

Setiap feature ID harus memiliki keterlacakan:

`Requirement ID → Implementation → Test Case → Actual Result → Final Status`.

Jangan menghitung coverage hanya berdasarkan jumlah test.

---

# 5. FRONTEND TESTING — 9 CATEGORIES

Gunakan stack yang relevan dengan proyek:

- React 19.
- TypeScript.
- Vite.
- Vitest.
- React Testing Library.
- Playwright.
- MSW bila diperlukan untuk pengujian terisolasi.
- axe-core / axe-playwright untuk accessibility.
- Lighthouse dan browser performance APIs bila relevan.

Periksa versi aktual dependency sebelum menjalankan test.

Jangan memperkenalkan banyak framework testing yang memiliki fungsi sama tanpa kebutuhan jelas.

## FE-01 — UNIT TESTING

Uji pure functions dan utilities:

- Currency formatting Rupiah.
- Date formatting.
- Timezone conversion.
- Phone number formatting.
- Order total preview.
- Quantity and weight formatting.
- Financial status labels.
- Status-to-color mapping.
- Query parameter builders.
- API error normalization.
- Form validation helpers.
- Data transformations.
- State reducers.

Gunakan edge cases:

- Nilai nol.
- Nominal besar.
- Tanggal invalid.
- Timezone boundaries.
- Nilai decimal.
- Empty string.
- Null/undefined.
- Unexpected API values.

Pastikan frontend tidak menjadi sumber kebenaran finansial.

**Gate: FE_UNIT_PASS**

## FE-02 — COMPONENT TESTING

Uji komponen secara terisolasi:

- Buttons.
- Inputs.
- Selects.
- Tables.
- Cards.
- Modals.
- Dialogs.
- Status badges.
- Toast notifications.
- Loading skeletons.
- Error messages.
- Pagination.
- Search forms.
- Currency display.
- Invoice preview.
- Tracking timeline.
- Order status controls.
- Payment forms.
- Courier task cards.

Verifikasi:

- Correct rendering.
- Props behavior.
- Conditional rendering.
- User interactions.
- Form validation.
- Disabled states.
- Keyboard interaction.
- Focus management.
- Accessibility labels.

Gunakan React Testing Library dan user-event.

Hindari test yang terlalu bergantung pada struktur DOM internal.

**Gate: FE_COMPONENT_PASS**

## FE-03 — INTEGRATION TESTING

Uji interaksi beberapa komponen sekaligus.

Contoh:

- Login form + AuthProvider + ProtectedRoute.
- Customer search + order form.
- Service selection + pricing preview.
- Order detail + status update.
- Payment modal + balance refresh.
- Invoice modal + order summary.
- Dashboard + date filter.
- Pickup management + courier assignment.
- Public tracking + status timeline.

Gunakan mocked network secara eksplisit jika diperlukan.

Gunakan MSW atau mekanisme mock yang konsisten.

Verifikasi:

- Request payload.
- State updates.
- Cache invalidation.
- Loading behavior.
- Error handling.
- Retry behavior.
- Duplicate submission prevention.

**Gate: FE_INTEGRATION_PASS**

## FE-04 — REAL END-TO-END TESTING

Gunakan browser nyata.

**REAL E2E MUST NOT USE INTERCEPTED BUSINESS API RESPONSES.**

Jalankan:

Browser → React → FastAPI → PostgreSQL test database.

Mandatory journeys:

1. Owner login.
2. Owner mengelola user.
3. Cashier login.
4. Cashier menambahkan pelanggan.
5. Cashier membuat layanan.
6. Cashier membuat pesanan.
7. Multi-service pricing.
8. Staff memperbarui status cucian.
9. Cashier mencatat pembayaran.
10. Cashier membuka nota.
11. PDF invoice download.
12. WhatsApp deep link validation.
13. Customer public tracking.
14. Customer public pickup request.
15. Cashier pickup confirmation.
16. Courier assignment.
17. Courier pickup workflow.
18. Pickup-to-order conversion.
19. Delivery status update.
20. Physical handoff.
21. Order completion sesuai business rules.
22. Owner dashboard and reporting.

Gunakan test users untuk OWNER, CASHIER, STAFF, COURIER.

Gunakan data sintetis.

Periksa perubahan data pada backend/database, bukan hanya munculnya toast success.

Negative E2E:

- Unauthorized access.
- Invalid login.
- Expired session.
- Wrong tracking token.
- Duplicate clicks.
- Invalid payment.
- Network interruption.
- Concurrent order update.
- Failed delivery and rescheduling.

Klasifikasikan E2E mock dan real E2E sebagai dua suite berbeda.

**Gate: FE_REAL_E2E_PASS**

## FE-05 — VISUAL REGRESSION TESTING

Gunakan Playwright screenshot assertions.

Audit:

- Login.
- Dashboard.
- Orders.
- Customers.
- Payments.
- Invoice.
- Tracking.
- Pickup.
- Courier.
- Reports.
- Settings.

Gunakan deterministic fixtures:

- Fixed clock.
- Fixed locale.
- Fixed viewport.
- Stable test data.
- Stable fonts.
- Disabled nonessential animation.

Buat baseline visual berdasarkan DBD dan tampilan yang telah direview.

Jangan otomatis menerima screenshot baru hanya karena test diff gagal.

Jika screenshot berbeda:

1. Periksa apakah bug CSS.
2. Periksa responsive behavior.
3. Periksa typography.
4. Periksa layout overflow.
5. Periksa missing components.
6. Perbaiki implementasi.
7. Perbarui baseline hanya jika perubahan memang benar dan terdokumentasi.

**Gate: FE_VISUAL_REGRESSION_PASS**

## FE-06 — CROSS-BROWSER & CROSS-DEVICE

Gunakan Playwright projects:

- Chromium.
- Firefox.
- WebKit.

WebKit digunakan sebagai pendekatan otomasi yang mendekati Safari; jangan mengklaim seluruh Safari asli sudah diverifikasi jika hanya menggunakan WebKit.

Gunakan viewport sesuai DBD:

- 320px.
- 360px.
- 375px.
- 390px.
- 430px.
- 768px.
- 1024px.
- 1440px.

Audit:

- Responsive navigation.
- Forms.
- Tables.
- Dialogs.
- Mobile scrolling.
- Touch targets.
- Sticky elements.
- Overflow.
- Layout shifts.
- Typography rendering.
- Order intake workflow.
- Public tracking.

Jika browser engine belum terinstal, lakukan instalasi yang aman dan sesuai project environment jika diizinkan.

Jangan menggunakan satu hasil Chromium sebagai klaim seluruh browser PASS.

**Gate: FE_CROSS_BROWSER_PASS**

## FE-07 — ACCESSIBILITY TESTING

Gunakan standar DBD, terutama target WCAG 2.2 AA.

Periksa:

- Semantic HTML.
- Input labels.
- Keyboard navigation.
- Focus visibility.
- Focus traps.
- Dialog accessibility.
- Aria attributes.
- Screen reader text.
- Accessible error messages.
- Color contrast.
- Non-color status indications.
- Touch targets.
- Logical tab order.
- Form descriptions.
- Accessible tables.

Gunakan automated accessibility scanning dan pemeriksaan interaksi keyboard.

Otomasi tidak membuktikan seluruh WCAG telah terpenuhi. Catat hal yang membutuhkan evaluasi manual.

Jangan mengklaim WCAG AA secara penuh hanya karena axe-core menghasilkan zero violations.

**Gate: FE_A11Y_AUTOMATED_PASS**

## FE-08 — CLIENT-SIDE PERFORMANCE

Ukur:

- LCP.
- CLS.
- INP jika dapat diperoleh melalui interaksi dan instrumentasi yang valid.
- FCP.
- TTFB.
- JavaScript bundle size.
- CSS bundle size.
- Route loading.
- Rendering performance.
- Network request count.

Gunakan Lighthouse dan browser performance tooling yang sesuai.

Bedakan lab metrics dengan field/RUM metrics.

Jangan menyebut estimasi INP sebagai hasil field measurement.

Audit:

- Lazy-loaded routes.
- Re-rendering.
- Query caching.
- Bundle splitting.
- Duplicate API calls.
- Heavy dependencies.
- Images.
- Font loading.
- Responsive image behavior.

Gunakan performance target resmi PRD/TRD, bukan angka yang dibuat tanpa dasar.

Jika hasil buruk, optimalkan kode dan ukur ulang.

Jangan mengorbankan business correctness demi performa.

**Gate: FE_PERFORMANCE_VERIFIED**

## FE-09 — INTERNATIONALIZATION & LOCALIZATION

Produk MVP menggunakan Bahasa Indonesia.

Prioritaskan:

- Locale `id-ID`.
- Rupiah formatting.
- Indonesian date/time formatting.
- Business timezone.
- Decimal separator.
- Long-text layout.
- Error messages in Indonesian.
- Consistent status labels.
- Input normalization.

RTL dan multiple languages hanya wajib jika memang ditetapkan oleh DBD/PRD atau telah diimplementasikan.

Jangan membuat sistem multilingual atau RTL baru yang berada di luar scope MVP hanya untuk meluluskan kategori testing.

Jika tidak diwajibkan, tandai RTL-specific cases sebagai NOT_APPLICABLE dengan justifikasi.

**Gate: FE_LOCALIZATION_PASS**

---

# 6. BACKEND TESTING — 13 CATEGORIES

Gunakan:

- Python 3.12.
- FastAPI.
- Pytest.
- HTTPX.
- SQLAlchemy.
- PostgreSQL 17.
- Alembic.
- Ruff.
- Mypy/Pyright.
- Locust atau k6 bila sesuai.

Pastikan setiap jenis test mempunyai marker dan dapat dijalankan secara terpisah.

## BE-01 — UNIT TESTING

Uji:

- Pricing Engine.
- Decimal calculations.
- Money representation.
- Weight rounding.
- Minimum weight.
- Order totals.
- Payment balance.
- Void calculation.
- Financial status.
- State machine.
- Token generation.
- PII masking.
- Phone normalization.
- Date calculations.
- CSV sanitization.
- Audit redaction.
- Permission functions.
- Idempotency rules.

Gunakan mock hanya pada dependency yang memang perlu diisolasi.

Uji happy path, invalid input, edge cases, dan boundary conditions.

**Gate: BE_UNIT_PASS**

## BE-02 — REAL INTEGRATION TESTING

Gunakan PostgreSQL 17 nyata.

Wajib memverifikasi:

- SQLAlchemy ↔ PostgreSQL.
- Alembic migration chain.
- Foreign key integrity.
- Unique constraints.
- Check constraints.
- Transaction rollback.
- Multi-module transactions.
- Order creation atomicity.
- Payment concurrency.
- Row-level locking.
- Optimistic locking.
- Idempotency persistence.
- Pickup conversion atomicity.
- Audit log persistence.
- Token revocation.
- Financial reconciliation.

SQLite tests boleh tetap tersedia untuk logic yang cocok, tetapi tidak boleh menjadi bukti PostgreSQL integration PASS.

Jangan menghapus atau mereset database existing.

Gunakan isolated disposable test database.

**Gate: BE_POSTGRESQL_INTEGRATION_PASS**

## BE-03 — API / COMPONENT TESTING

Uji setiap endpoint yang relevan:

- HTTP status codes.
- Request payload.
- Response payload.
- Response schema.
- Validation errors.
- Error response.
- Headers.
- Cookies.
- CSRF.
- Authentication.
- Authorization.
- Pagination.
- Filters.
- Not-found behavior.
- Conflict behavior.
- Duplicate requests.

Periksa perubahan database setelah operasi mutasi.

**Gate: BE_API_PASS**

## BE-04 — CONTRACT TESTING

Bandingkan:

- FastAPI OpenAPI aktual.
- `doc/api/openapi.json`.
- Frontend API consumers.
- Pydantic schemas.
- TypeScript types.

Uji:

- HTTP methods.
- Paths.
- Enums.
- Required/optional fields.
- Date serialization.
- Decimal serialization.
- Money formats.
- Validation errors.
- Authentication contracts.
- Backward compatibility.

Gunakan consumer-provider verification yang dapat dieksekusi.

Pact tidak wajib jika belum digunakan sebagai mekanisme kontrak proyek.

Jangan membuat kontrak fiktif.

**Gate: BE_CONTRACT_PASS**

## BE-05 — BACKEND BUSINESS E2E

Jalankan real HTTP API workflows dengan PostgreSQL test database.

Mandatory journeys:

**Journey A:** Order intake → pricing → processing → handoff → completion.

**Journey B:** Order → DP → full payment → invoice → reports.

**Journey C:** Payment → void → audit → financial recalculation.

**Journey D:** Public pickup → confirmation → courier → conversion → order.

**Journey E:** Delivery → failed attempt → reschedule → handoff.

**Journey F:** Secure tracking → token revoke → token rotation.

**Journey G:** Auth → session → role permissions → protected operations.

**Journey H:** Duplicate requests → idempotency → no duplicate transactions.

Gunakan worker/message broker/payment sandbox hanya jika benar-benar bagian arsitektur yang diwajibkan. MVP ini tidak memerlukan microservices, payment gateway, atau message broker eksternal.

**Gate: BE_BUSINESS_E2E_PASS**

## BE-06 — LOAD TESTING

Gunakan staging atau test environment.

Workloads:

- Login.
- Search customers.
- List orders.
- Create orders.
- Record payments.
- Update statuses.
- Public tracking.
- Dashboard.
- Reports.

Ukur:

- RPS.
- Throughput.
- p50 latency.
- p95 latency.
- p99 latency.
- Error rate.
- CPU usage.
- RAM usage.
- PostgreSQL connection utilization.

Tetapkan workloads berdasarkan kapasitas operasional UMKM dan target TRD.

**Gate: BE_LOAD_TEST_VERIFIED**

## BE-07 — STRESS TESTING

Uji beban bertahap di atas tingkat normal pada environment terisolasi.

Periksa:

- Saturation behavior.
- Request rejection.
- Queue buildup jika ada.
- Database pool exhaustion.
- Memory pressure.
- Timeout handling.
- Recovery after load reduction.
- Data consistency.

Gunakan batas aman CPU/RAM/connection.

Jangan menyebabkan resource exhaustion pada mesin produksi.

**Gate: BE_STRESS_TEST_VERIFIED**

## BE-08 — SPIKE TESTING

Simulasikan lonjakan permintaan secara mendadak.

Contoh:

- Banyak pelanggan membuka tracking dalam interval singkat.
- Beberapa kasir mengakses daftar pesanan.
- Banyak request pembayaran berulang dengan data sintetis.

Validasi:

- No duplicate payments.
- No duplicate orders.
- Rate limiting.
- Error response consistency.
- Recovery after spike.
- Database consistency.

**Gate: BE_SPIKE_TEST_VERIFIED**

## BE-09 — SOAK / ENDURANCE TESTING

Jalankan workload konstan dalam durasi yang aman dan dapat dikonfigurasi.

Pantau:

- Memory usage over time.
- Open connections.
- CPU trends.
- Response latency trends.
- Error rate.
- Session stability.
- Resource cleanup.

Durasi harus dicatat secara eksplisit.

Jika hanya menjalankan uji singkat, jangan mengklaim long-duration soak test PASS.

**Gate: BE_SOAK_TEST_VERIFIED**

## BE-10 — SECURITY TESTING

Audit:

- OWASP API Security Top 10.
- Broken authentication.
- Broken authorization.
- BOLA/IDOR.
- SQL injection.
- Command injection resistance.
- Session handling.
- CSRF.
- Login throttling.
- Role permissions.
- Tracking tokens.
- Public data exposure.
- Sensitive data logging.
- Password hashing.
- Payment authorization.
- Audit log integrity.
- Input validation.
- Dependency vulnerabilities.

Gunakan data sintetis dan server yang memang dikuasai untuk pengujian.

Jika ditemukan P0/P1 security defect, perbaiki dan jalankan ulang regression tests.

**Gate: BE_CRITICAL_SECURITY_PASS**

## BE-11 — RESILIENCE / CHAOS TESTING

Uji pada isolated test/staging environment.

Skenario:

- PostgreSQL connection failure.
- Database temporarily unavailable.
- Application restart.
- API timeout.
- Transaction interrupted before commit.
- Transaction interrupted after commit but before response.
- Duplicate retry after connection recovery.
- Expired sessions.
- Unavailable PDF generation dependency jika relevan.

Verifikasi:

- Graceful error handling.
- No partial financial transaction.
- No duplicate records.
- Correct rollback.
- Safe retry.
- Recovery after dependency restoration.
- No false success response.

Tidak perlu menerapkan circuit breaker atau microservices-specific chaos mechanism jika tidak dibutuhkan arsitektur.

Jangan mematikan service/database milik pengguna secara langsung.

**Gate: BE_RESILIENCE_VERIFIED**

## BE-12 — SMOKE TESTING

Jalankan pada runtime nyata.

Validasi:

- Application startup.
- Liveness.
- Readiness.
- Database connection.
- Login.
- Order listing.
- Payment endpoint.
- Public tracking.
- Invoice.
- Dashboard.

Gunakan environment target yang memang tersedia dan diotorisasi.

Jangan melakukan deploy publik secara otomatis.

**Gate: BE_SMOKE_PASS**

## BE-13 — SANITY TESTING

Setelah setiap bug diperbaiki:

1. Jalankan test yang sebelumnya gagal.
2. Jalankan related tests.
3. Pastikan bug tidak muncul kembali.
4. Periksa modules terdampak via CodeGraph.
5. Jalankan regression suite sesuai blast radius.

Sanity testing tidak menggantikan full regression pada final gate.

**Gate: BE_SANITY_PASS**

---

# 7. CRITICAL CROSS-DOCUMENT BUSINESS RULE AUDIT

Sebelum menyatakan seluruh test PASS, audit ketidaksesuaian penting berikut.

## ISSUE 1 — UNPAID ORDER COMPLETION

PRD menyatakan pesanan dapat diserahkan dengan piutang tetap tercatat dalam kondisi yang diizinkan.

Periksa apakah backend saat ini mewajibkan:

`payment_status == PAID`

untuk status COMPLETED.

Audit PRD, AFD, BSD, dan keputusan Owner yang berlaku.

Jangan mengubah aturan bisnis hanya berdasarkan asumsi.

Uji:

- Completed order with confirmed handoff.
- Unpaid handoff warning.
- Outstanding balance preservation.
- Financial reports after handoff.
- Invalid completion without handoff.
- Unauthorized completion.

Jika terdapat konflik keputusan, tandai DECISION_REQUIRED dan jangan memalsukan PASS.

## ISSUE 2 — CUSTOMER DUPLICATE HANDLING

Periksa:

- PRD duplicate warning.
- BSD shared phone number allowance.
- Existing unique constraints.
- HTTP 409 behavior.
- Customer identity matching.

Pastikan pencegahan duplikasi tidak melarang kasus pelanggan berbagi nomor telepon apabila BSD mengizinkannya.

Uji kebijakan yang benar berdasarkan spesifikasi dan keputusan sah.

## ISSUE 3 — LAUNDRY STATUS ENUM

Verifikasi canonical states:

- RECEIVED.
- QUEUED.
- WASHING.
- DRYING.
- IRONING.
- QC_PACKING.
- READY.
- COMPLETED.
- CANCELLED.

Periksa apakah kode masih memiliki ketidaksesuaian seperti:

- PACKING.
- READY_FOR_PICKUP.
- Invalid transitions.
- Missing history.
- Invalid terminal state behavior.

Jangan mengganti canonical enum tanpa analisis migrasi dan kontrak API.

## ISSUE 4 — DATABASE PRECISION

BSD menentukan penggunaan numerik presisi untuk berat cucian.

Verifikasi actual SQLAlchemy model dan PostgreSQL column types.

Periksa khususnya:

`NUMERIC(10,3)` versus `NUMERIC(10,2)`.

Periksa dampak terhadap:

- Pricing.
- Snapshot.
- Invoice.
- API serialization.
- Historical data.

## ISSUE 5 — TECHNOLOGY COMPLIANCE

Verifikasi:

- React version.
- TypeScript strict mode.
- Vite version compatibility.
- Python version.
- FastAPI version.
- SQLAlchemy version.
- PostgreSQL version.
- Alembic revision chain.

Jangan menyatakan stack PASS jika versi aktual bertentangan dengan requirement wajib.

## ISSUE 6 — REAL E2E VERSUS MOCKED E2E

Laporan sebelumnya pernah menggunakan mocked API pada Playwright.

Pisahkan secara tegas:

- Mocked UI integration tests.
- Browser component tests.
- Real browser-to-backend-to-PostgreSQL E2E.

Jangan mengklaim mock-based Playwright sebagai full-stack real E2E.

---

# 8. TEST FAILURE & AUTOMATIC CODE REPAIR POLICY

Setiap failure harus diklasifikasikan:

- APPLICATION_BUG.
- BUSINESS_RULE_DEFECT.
- API_CONTRACT_DEFECT.
- DATABASE_DEFECT.
- UI_RENDERING_DEFECT.
- ACCESSIBILITY_DEFECT.
- PERFORMANCE_DEFECT.
- SECURITY_DEFECT.
- TEST_ASSUMPTION_ERROR.
- TEST_INFRASTRUCTURE_BLOCKER.
- DOCUMENT_CONFLICT.

Jika bug berasal dari application code:

**FIX THE CODE, NOT THE EXPECTED RESULT.**

Workflow:

1. Reproduce error.
2. Capture error log.
3. Identify root cause.
4. Inspect affected code via CodeGraph.
5. Compare behavior with documentation.
6. Add or strengthen failing regression test.
7. Apply minimal correct source code fix.
8. Run targeted test.
9. Run affected module tests.
10. Run integration tests.
11. Run full regression suite.
12. Update remediation report.

Jangan:

- Menghapus failing test.
- Mengubah assertion agar mengikuti bug.
- Menambahkan skip tanpa alasan.
- Mengubah xfail menjadi PASS.
- Menambahkan mock untuk menyembunyikan broken integration.
- Menonaktifkan CSRF.
- Menonaktifkan RBAC.
- Menghapus constraint penting.
- Mengembalikan HTTP 200 pada operasi yang gagal.
- Menonaktifkan audit log.
- Mengubah financial invariants secara sepihak.

Perbaiki juga setup test jika error terbukti berasal dari fixture atau test environment, dengan catatan yang jelas.

---

# 9. TEST ENVIRONMENT & DATA SAFETY

Gunakan lingkungan pengujian yang terisolasi.

## Test Database

- PostgreSQL 17.
- Dedicated test database.
- Synthetic users.
- Synthetic customers.
- Synthetic orders.
- Synthetic payments.
- Synthetic pickup requests.

Jangan memakai database pengguna yang berisi data operasional nyata untuk destructive tests.

Jangan menjalankan `dropdb`, `alembic downgrade`, `TRUNCATE`, atau reset schema terhadap database yang tidak diverifikasi sebagai milik test environment.

Gunakan rollback atau isolated schemas bila sesuai.

## Browser Testing

Gunakan isolated browser contexts.

Jangan menggunakan real customer WhatsApp accounts.

Jangan mengirim pesan WhatsApp sungguhan.

Jangan melakukan pembayaran nyata.

## Load/Chaos

Jalankan hanya pada host yang diotorisasi.

Tetapkan resource limits dan maximum duration.

Jika environment tidak mampu menjalankan test, gunakan BLOCKED/NOT_VERIFIED.

Jangan memaksakan PASS.

---

# 10. COVERAGE & TEST QUALITY

Gunakan test coverage tooling untuk frontend dan backend.

Backend:

- Line coverage.
- Branch coverage.
- Module coverage.

Frontend:

- Unit/component coverage.
- Critical workflow coverage.
- Screen coverage.
- Browser/viewport coverage.

Prioritaskan:

- Auth.
- RBAC.
- Orders.
- Pricing.
- Payments.
- Tracking.
- Pickup conversion.
- Handoff.
- Reporting.
- Audit logging.

Gunakan meaningful assertions.

Jangan mengukur keberhasilan hanya dengan jumlah test.

Target utama:

**100% TRACEABLE COVERAGE FOR ALL REQUIRED P0 FEATURES AND ACCEPTANCE CRITERIA.**

---

# 11. CI/CD TEST ORGANIZATION

Siapkan reusable commands dan scripts.

Kelompokkan:

## Every Commit

- Frontend unit tests.
- Frontend component tests.
- Backend unit tests.
- Lint.
- Typecheck.
- Fast contract checks.

## Every Pull Request

- Frontend integration.
- Backend PostgreSQL integration.
- API tests.
- Security regression.
- Real business workflow tests.
- Relevant browser tests.

## Pre-Release

- Full Playwright E2E.
- Cross-browser.
- Visual regression.
- Accessibility.
- Load/stress/spike.
- Soak jika environment dan waktu memadai.
- Resilience.
- Backup/restore.
- Full regression.

## Post-Deployment

- Non-destructive smoke tests.

Jangan menempatkan destructive chaos tests di automatic production CI.

Jangan commit secrets atau credentials.

---

# 12. REQUIRED REPORTS

Buat atau perbarui:

`doc/testing/`

## A. Full Stack Test Matrix

`FULL-STACK-TEST-MATRIX.md`

Kolom:

| Requirement ID | Priority | Layer | Test Category | Test File | Status | Evidence |
| -------------- | -------- | ----- | ------------- | --------- | ------ | -------- |

## B. Frontend Test Report

`FRONTEND-TEST-REPORT.md`

Memuat:

- 9 category results.
- Total tests.
- Passed.
- Failed.
- Skipped.
- Blocked.
- Browser matrix.
- Viewport matrix.
- Visual regression.
- Accessibility.
- Performance.

## C. Backend Test Report

`BACKEND-TEST-REPORT.md`

Memuat:

- 13 category results.
- Unit.
- Integration.
- API.
- Contract.
- Real business E2E.
- Load.
- Stress.
- Spike.
- Soak.
- Security.
- Resilience.
- Smoke.
- Sanity.

## D. Bug & Remediation Register

`BUG-REMEDIATION-REGISTER.md`

Kolom:

- Bug ID.
- Severity.
- Requirement.
- Failing test.
- Root cause.
- File changed.
- Fix description.
- Verification test.
- Status.

## E. Documentation Compliance

`DOCUMENTATION-COMPLIANCE-REPORT.md`

Audit:

- PRD.
- TRD.
- AFD.
- DBD.
- BSD.
- IPD.

Catat semua discrepancy dan resolution.

## F. Performance Report

`PERFORMANCE-BENCHMARK.md`

Pisahkan frontend dan backend metrics.

Catat:

- Host specification.
- Test environment.
- Workload.
- Measurement method.
- Latency.
- Throughput.
- CPU/RAM.
- Error rate.
- Limitations.

## G. Security Report

`SECURITY-VERIFICATION.md`

Memuat:

- Security test coverage.
- Vulnerabilities.
- Severity.
- Fixes.
- Residual risks.

## H. Final Acceptance

`FINAL-FULLSTACK-ACCEPTANCE.md`

Memuat:

- P0 features total.
- P0 requirements PASS.
- P0 requirements FAIL.
- P0 requirements BLOCKED.
- P1 implemented and verified.
- P2 out of scope.
- AT-01 through AT-30.
- Frontend 9 category results.
- Backend 13 category results.
- Real PostgreSQL verification.
- Real browser E2E.
- Open defects.
- Fixed defects.
- Final readiness verdict.

---

# 13. EXECUTION PLAN

Kerjakan secara aktif dan berurutan.

## PHASE 1 — Baseline Audit

- Check git status.
- Read 6 authoritative documents.
- Read AGENTS.md and relevant skills.
- Inspect CodeGraph.
- Inventory existing frontend/backend tests.
- Record environment and dependencies.
- Identify specification conflicts.

## PHASE 2 — Requirements Traceability

- Extract official PRD feature IDs.
- Extract AT-01–AT-30.
- Extract DBD screen inventory.
- Extract BSD invariants.
- Extract AFD business journeys.
- Map IPD tasks.
- Build test matrix.

## PHASE 3 — Fast Test Suites

- Frontend unit.
- Frontend component.
- Backend unit.
- API contract.
- Linters.
- Typechecking.

Fix discovered bugs immediately.

## PHASE 4 — Integration

- Frontend integration.
- Backend PostgreSQL integration.
- API functional tests.
- Cross-module workflows.

Fix confirmed defects.

## PHASE 5 — Real End-to-End

- Start real frontend.
- Start real FastAPI.
- Connect real PostgreSQL test DB.
- Run full business journeys.
- Verify database state.
- Test all roles.

Fix confirmed defects.

## PHASE 6 — Visual, Accessibility & Browser Compatibility

- Chromium.
- Firefox.
- WebKit.
- Required DBD viewports.
- Screenshot comparison.
- Accessibility checks.
- Indonesian localization.

Fix confirmed defects.

## PHASE 7 — Performance, Security & Resilience

- Browser performance.
- Backend load.
- Stress.
- Spike.
- Soak.
- Security.
- Chaos/resilience.

Use isolated environments and safe resource limits.

Fix confirmed defects.

## PHASE 8 — Regression

Re-run:

- All frontend unit tests.
- All frontend component tests.
- All frontend integration tests.
- All backend unit tests.
- All PostgreSQL integration tests.
- All API/contract tests.
- Critical E2E journeys.
- Cross-browser tests.
- Visual regression tests.
- Security regression.
- Smoke tests where applicable.

Pastikan tidak ada regresi dari bug fixes.

## PHASE 9 — Acceptance & Reporting

- Recalculate requirement coverage.
- Recalculate test results.
- Revalidate AT-01–AT-30.
- Update test reports.
- Update remediation register.
- Update milestone verification status.
- Report unresolved blockers.

Lanjutkan seluruh pekerjaan yang aman selama sesi aktif.

Jika sesi berhenti sebelum seluruh pekerjaan selesai, simpan checkpoint yang jelas untuk kelanjutan sesi berikutnya.

---

# 14. ACCEPTANCE GATES

Gunakan status:

- PASS.
- FAIL.
- PARTIAL.
- BLOCKED.
- NOT_VERIFIED.
- NOT_APPLICABLE.
- DECISION_REQUIRED.

Satu kategori hanya boleh PASS jika seluruh acceptance requirements yang relevan terverifikasi.

NOT_APPLICABLE hanya boleh digunakan untuk aktivitas yang memang tidak diwajibkan arsitektur dan scope proyek.

## FULL_STACK_TEST_VERIFIED

Status ini hanya boleh diberikan jika:

1. Semua required P0 requirements teruji dan PASS.
2. Semua critical PRD acceptance tests PASS.
3. Frontend unit/component/integration PASS.
4. Backend unit/integration/API/contract PASS.
5. Real PostgreSQL tests PASS.
6. Real browser business journeys PASS.
7. Critical security tests PASS.
8. Cross-browser dan viewport acceptance PASS.
9. Accessibility requirements PASS.
10. No critical financial bugs.
11. No known RBAC bypass.
12. No known public PII leakage.
13. No broken mandatory workflows.
14. No outstanding P0 defects.
15. Regression suite PASS.
16. Performance tests memiliki evidence sesuai target dan environment.
17. Semua blocker dan unverified tests diungkapkan secara eksplisit.

Jika requirement wajib masih BLOCKED atau NOT_VERIFIED, gunakan status CONDITIONAL atau BLOCKED, bukan FULL_STACK_TEST_VERIFIED.

Jangan menyatakan PRODUCTION_READY hanya berdasarkan hasil test kode. Deployment runtime, backup/restore, UAT, dan approval Owner tetap merupakan gate terpisah.

---

# 15. AUTONOMOUS CODE FIX AUTHORIZATION

Saya mengizinkan Anda:

- Membuat test baru.
- Memperbaiki source code frontend.
- Memperbaiki source code backend.
- Memperbaiki API integration.
- Memperbaiki domain rules berdasarkan requirement yang berlaku.
- Memperbaiki database models.
- Membuat migration aman yang diperlukan.
- Memperbaiki security defects.
- Memperbaiki performance bottlenecks.
- Memperbaiki accessibility.
- Memperbaiki CSS bugs.
- Memperbaiki UI component behavior.
- Memperbarui test snapshots setelah validasi.
- Memperbarui laporan implementasi/testing.
- Menyiapkan CI workflows.

Tetap pertahankan arsitektur, requirement dan scope MVP.

Dilarang tanpa persetujuan:

- Mengubah source-of-truth requirement secara sepihak.
- Menghapus data/database penting.
- Menjalankan destructive migration terhadap database nyata.
- Melakukan deployment publik.
- Mengubah DNS.
- Menggunakan layanan berbayar.
- Mengirim pesan WhatsApp nyata.
- Mengakses customer data yang tidak diperlukan.
- Membocorkan credentials.
- Melakukan force push.
- Menghapus perubahan pengguna yang tidak terkait.

---

# 16. FINAL REPORT FORMAT

Pada akhir sesi, tampilkan:

## EXECUTION SUMMARY

| Metric                 | Result                    |
| ---------------------- | ------------------------- |
| PRD P0 Coverage        | x / total                 |
| PRD Acceptance Tests   | x / 30                    |
| Frontend Categories    | x / 9                     |
| Backend Categories     | x / 13                    |
| Frontend Tests         | Passed / Failed / Skipped |
| Backend Tests          | Passed / Failed / Skipped |
| PostgreSQL Integration | PASS / BLOCKED / FAIL     |
| Real Browser E2E       | PASS / BLOCKED / FAIL     |
| Security               | PASS / FAIL               |
| Performance            | VERIFIED / NOT_VERIFIED   |
| Bugs Found             | Count                     |
| Bugs Fixed             | Count                     |
| Open P0/P1 Defects     | Count                     |
| Final Verdict          | Evidence-based            |

Tambahkan:

1. Daftar bug penting yang ditemukan.
2. Daftar file source code yang diperbaiki.
3. Daftar test yang ditambahkan.
4. Ringkasan hasil per kategori.
5. Bukti perintah dan output pengujian.
6. Requirement yang masih belum terpenuhi.
7. Kebutuhan external environment yang masih menjadi blocker.
8. Daftar tindakan lanjutan yang konkret.

---

# 17. FINAL ABSOLUTE DIRECTIVE

**DO NOT STOP AFTER WRITING TESTS.**

**DO NOT STOP AFTER FINDING BUGS.**

**FIX ACTUAL APPLICATION DEFECTS.**

**DO NOT FAKE TEST RESULTS.**

**DO NOT CHANGE TESTS TO HIDE BUGS.**

**DO NOT DELETE MANDATORY FEATURES.**

**FOLLOW ALL SIX AUTHORITATIVE DOCUMENTS.**

**USE INSTALLED PROJECT SKILLS.**

**USE CODEGRAPH-FIRST.**

**VERIFY REAL FRONTEND–BACKEND–POSTGRESQL INTEGRATION.**

**TEST ALL REQUIRED BUSINESS WORKFLOWS.**

**RE-RUN TESTS AFTER FIXES.**

**CONTINUE UNTIL ALL FEASIBLE TESTS PASS OR LEGITIMATE BLOCKERS ARE DOCUMENTED.**

## START EXECUTION NOW

Mulai dengan membaca seluruh dokumentasi, skills, dan existing tests. Bangun full-stack test matrix, jalankan baseline tests, kemudian implementasikan missing tests dan lakukan automatic bug remediation sampai seluruh acceptance criteria yang dapat diverifikasi terpenuhi.

**FINAL GOAL: A DOCUMENTATION-COMPLIANT, TESTED, SECURE, RELIABLE, RESPONSIVE, AND FUNCTIONALLY CORRECT E-LAUNDRY 2.0 APPLICATION.**
