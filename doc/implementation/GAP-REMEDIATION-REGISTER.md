# GAP & REMEDIATION REGISTER — E-LAUNDRY 2.0
## Milestone Scope: M0–M8 Comprehensive Compliance Audit (Task 4)

**Audit Date:** 2026-11-03  
**Auditor Roles:** Principal Software Architect, PostgreSQL Database Architect, Senior Full-Stack Engineer, Security Architect, QA Automation Lead  
**Audit Baseline:** PRD.md, TRD.md, AFD.md, DBD.md, BSD.md, IPD.md, SKILLS-CATALOG.md  
**Overall Status:** ALL IDENTIFIED GAPS CLOSED & VERIFIED  

---

## 1. Summary of Audit Findings

| Priority | Total Identified | Remediated | Blocked / External | Final Status |
| :--- | :---: | :---: | :---: | :--- |
| **P0 (Critical)** | 2 | 2 | 0 | **100% CLOSED** |
| **P1 (High)** | 1 | 1 | 0 | **100% CLOSED** |
| **P2 (Medium)** | 1 | 1 | 0 | **100% CLOSED** |
| **P3 (Low)** | 0 | 0 | 0 | **N/A** |
| **Total** | **4** | **4** | **0** | **ALL CLOSED** |

---

## 2. Detailed Findings & Remediation Log

### GAP-01 (P0): Missing Table 19 `audit_logs` in Database Schema & Service Layer
- **Finding ID:** GAP-01
- **Severity / Priority:** P0 — Critical (Data Integrity & Regulatory Auditability)
- **Requirement Reference:**
  - `BSD.md` §25 (*Tabel 19: audit_logs*) & §6.1 (*19 Core Tables Catalog*)
  - `PRD.md` §10.2 (*Auditability of state transitions, cancellations, and voids*)
  - `TRD.md` §6.1 (*Security logging & compliance*)
  - `IPD.md` Task M7-04 (*Security Hardening & Audit Logging*)
- **Root Cause:**
  During the autonomous M7 execution, while security middlewares (CSRF, Request ID, Rate Limiter) were built, Table 19 `audit_logs` and its persistent service were omitted from Alembic migrations and the database catalog.
- **Affected Modules:**
  - Database schema & migrations: `backend/app/db/models_registry.py`, `backend/alembic/versions/`
  - Core domain hooks: `orders`, `payments`, `services`, `users`
- **Corrective Action Taken:**
  1. Created SQLAlchemy entity model [`backend/app/modules/audit/models.py`](file:///d:/Kuliah/joki/Kerja%20Praktek%20Aqil/kawan%20aqil/projek/backend/app/modules/audit/models.py) matching BSD §25: columns `id`, `business_id`, `actor_user_id`, `action`, `resource_type`, `resource_id`, `before_data`, `after_data`, `reason`, `ip_address`, `created_at` with composite B-tree index on `(resource_type, resource_id, created_at)`.
  2. Implemented `AuditService.record()` with automated credential/token redaction (`password`, `access_token`, `refresh_token`, `csrf_token`, `pin`).
  3. Registered `AuditLog` in [`backend/app/db/models_registry.py`](file:///d:/Kuliah/joki/Kerja%20Praktek%20Aqil/kawan%20aqil/projek/backend/app/db/models_registry.py) to complete all 19 BSD core tables.
  4. Created migration [`backend/alembic/versions/a619c28e401b_m7_audit_logs.py`](file:///d:/Kuliah/joki/Kerja%20Praktek%20Aqil/kawan%20aqil/projek/backend/alembic/versions/a619c28e401b_m7_audit_logs.py) chained to previous head `e528b96f140a`.
  5. Integrated audit recording hooks in:
     - `orders/service.py`: `ORDER_CANCELLED`
     - `payments/service.py`: `PAYMENT_VOIDED`
     - `services/service.py`: `SERVICE_CREATED`, `SERVICE_UPDATED`
     - `users/service.py`: `USER_CREATED`, `USER_DEACTIVATED`
  6. Added dedicated unit tests in [`backend/tests/unit/test_audit_logs.py`](file:///d:/Kuliah/joki/Kerja%20Praktek%20Aqil/kawan%20aqil/projek/backend/tests/unit/test_audit_logs.py).
- **Files Changed:**
  - `backend/app/modules/audit/models.py`
  - `backend/app/modules/audit/service.py`
  - `backend/app/db/models_registry.py`
  - `backend/alembic/versions/a619c28e401b_m7_audit_logs.py`
  - `backend/app/modules/orders/service.py`
  - `backend/app/modules/payments/service.py`
  - `backend/app/modules/services/service.py`
  - `backend/app/modules/users/service.py`
  - `backend/tests/unit/test_audit_logs.py`
- **Test Evidence:**
  - `backend/tests/unit/test_audit_logs.py` passed (2/2 tests: redaction & lifecycle).
- **Status:** **CLOSED (VERIFIED)**

---

### GAP-02 (P0): Customer Public Self-Cancellation Out-of-Scope
- **Finding ID:** GAP-02
- **Severity / Priority:** P0 — Critical (Business Rule & Trust Boundary Violation)
- **Requirement Reference:**
  - `PRD.md` §5.7 Item 9 (*"Pelanggan tidak bisa mengubah status pesanan melalui halaman tracking."*)
  - `BSD.md` §34.1 (*Tracking tokens are strictly read-only allowlist views*)
  - `task/task4.md` Line 417 (*"Customer Public Self-Cancellation Out-of-Scope"*)
- **Root Cause:**
  A speculative convenience feature (`POST /api/v1/tracking/{token}/cancel`) was added in M4 which allowed unauthenticated external web clients to directly cancel laundry orders. This violated the foundational business constraint of PRD §5.7 #9 and presented an operational griefing risk.
- **Affected Modules:**
  - Backend tracking service & router: `backend/app/modules/tracking/service.py`, `backend/app/modules/tracking/router.py`
  - Frontend public tracking page: `frontend/src/pages/tracking/public-tracking-page.tsx`
  - Playwright E2E test: `frontend/e2e/m4-tracking.spec.ts`
  - Backend API test: `backend/tests/api/test_tracking_api.py`
- **Corrective Action Taken:**
  1. Enforced strict read-only boundary in `TrackingService.cancel_order()` by raising `ForbiddenException` (HTTP 403 Forbidden) explaining that public cancellations are disabled per PRD §5.7 #9 and directing customers to cashier assistance. Hardcoded `can_cancel = False` in public read models.
  2. Removed cancellation modal dialog, cancel reason form, and self-cancellation button from [`frontend/src/pages/tracking/public-tracking-page.tsx`](file:///d:/Kuliah/joki/Kerja%20Praktek%20Aqil/kawan%20aqil/projek/frontend/src/pages/tracking/public-tracking-page.tsx).
  3. Added an explicit WhatsApp cashier inquiry button (`data-testid="contact-cashier-btn"`) pre-filling the order number for legitimate cancellation/change inquiries.
  4. Updated [`backend/tests/api/test_tracking_api.py`](file:///d:/Kuliah/joki/Kerja%20Praktek%20Aqil/kawan%20aqil/projek/backend/tests/api/test_tracking_api.py) to assert HTTP 403 Forbidden on the public cancel route and verified that only authenticated cashiers/owners can cancel via `POST /api/v1/orders/{id}/cancel`.
  5. Updated Playwright E2E [`frontend/e2e/m4-tracking.spec.ts`](file:///d:/Kuliah/joki/Kerja%20Praktek%20Aqil/kawan%20aqil/projek/frontend/e2e/m4-tracking.spec.ts) to assert that public tracking is read-only and displays the cashier assistance link.
- **Files Changed:**
  - `backend/app/modules/tracking/service.py`
  - `backend/tests/api/test_tracking_api.py`
  - `frontend/src/pages/tracking/public-tracking-page.tsx`
  - `frontend/e2e/m4-tracking.spec.ts`
- **Test Evidence:**
  - `backend/tests/api/test_tracking_api.py` passed (2/2 tests).
  - Playwright `m4-tracking.spec.ts` passed (1/1 test).
- **Status:** **CLOSED (VERIFIED)**

---

### GAP-03 (P1): Attribute Name Mismatch in Payment Void Audit Hook
- **Finding ID:** GAP-03
- **Severity / Priority:** P1 — High (Operational Failure on Payment Voiding)
- **Requirement Reference:**
  - `BSD.md` §17.1 (*Payment entity schema*)
  - `BSD.md` §25 (*Audit log entity*)
- **Root Cause:**
  In `PaymentService.void_payment()`, the audit payload referenced `payment.payment_method`. The `Payment` SQLAlchemy model defines the field as `method` (String(30)), triggering an `AttributeError` upon voiding payments.
- **Affected Modules:**
  - `backend/app/modules/payments/service.py`
- **Corrective Action Taken:**
  Changed `payment.payment_method` to `payment.method` in [`backend/app/modules/payments/service.py`](file:///d:/Kuliah/joki/Kerja%20Praktek%20Aqil/kawan%20aqil/projek/backend/app/modules/payments/service.py#L203).
- **Files Changed:**
  - `backend/app/modules/payments/service.py`
- **Test Evidence:**
  - `backend/tests/api/test_payments_api.py` passed cleanly (1/1 test).
  - Full suite `pytest backend/tests/` passed (45/45 tests).
- **Status:** **CLOSED (VERIFIED)**

---

### GAP-04 (P2): Unused Imports and Linter Warnings
- **Finding ID:** GAP-04
- **Severity / Priority:** P2 — Medium (Codebase Hygiene & Quality Standards)
- **Requirement Reference:**
  - `AGENTS.md` §2 (*Engineering Standards & Anti-Overengineering*)
  - `TRD.md` §8 (*Code Quality & Tooling*)
- **Root Cause:**
  Post-audit edits left unused imports in `tracking/service.py` and `test_tracking_api.py`, and un-sorted imports in migration `a619c28e401b`.
- **Affected Modules:**
  - `backend/alembic/versions/a619c28e401b_m7_audit_logs.py`
  - `backend/app/modules/tracking/service.py`
  - `backend/tests/api/test_tracking_api.py`
- **Corrective Action Taken:**
  Ran `ruff check backend --fix` to clean unused imports and organize Alembic imports. Ran ESLint across frontend.
- **Files Changed:**
  - `backend/alembic/versions/a619c28e401b_m7_audit_logs.py`
  - `backend/app/modules/tracking/service.py`
  - `backend/tests/api/test_tracking_api.py`
- **Test Evidence:**
  - `ruff check backend` returned 0 errors.
  - `npm --prefix frontend run lint` returned 0 errors.
  - `npm --prefix frontend run build` returned 0 errors.
- **Status:** **CLOSED (VERIFIED)**

---

## 3. Residual Risk & Verification Conclusion

All four findings were directly resolved and verified via automated test suites.
- No unresolved P0 or P1 architectural, security, or business rule defects exist in the codebase.
- The 19 BSD core tables are now fully registered and migrated.
- The public tracking surface is strictly read-only, honoring PRD §5.7 #9.
- The entire backend test suite (45/45) and frontend Playwright E2E suite (15/15) pass without failures.

