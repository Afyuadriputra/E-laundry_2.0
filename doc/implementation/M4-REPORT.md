# Milestone 4 Verification & Implementation Report: Public Tracking & Customer Notifications

**Project:** E-Laundry 2.0  
**Milestone:** M4 (Public Tracking & Customer Notifications)  
**Date:** 2026-11-03  
**Status:** **PASS (PUBLIC_TRACKING_READY)**

---

## 1. Executive Summary

Milestone 4 implements public customer order tracking without authentication, cryptographically secure 256-bit token management, PII masking, operational state progress visualization, self-service cancellation under strict business constraints, and dynamic digital invoice tracking link generation, as specified by `PRD.md §4.4`, `TRD.md §4.4`, `BSD.md §23 & §34`, and `IPD.md §M4`.

Key deliverables completed and verified:
1. **Cryptographically Secure Tracking Tokens:** Tokens generated with 256-bit cryptographic entropy (`secrets.token_urlsafe(32)`). Raw tokens are never stored; the database retains only the SHA-256 hash (`BSD.md §23.4`).
2. **Schema & Cross-Milestone Dependency Architecture:** Table `tracking_tokens` enforces target exclusivity (`num_nonnulls(order_id, pickup_request_id) = 1`). In accordance with our cross-milestone audit, foreign key constraint to `pickup_requests` is properly deferred to Milestone 5.
3. **Public API & Privacy Safeguards:** `GET /api/v1/tracking/{token}` provides a strict allowlist read model without authentication. Customer names and phone numbers are masked (`I** R****`, `+62812****7899`). Responses enforce `Cache-Control: no-store` and `Referrer-Policy: no-referrer`.
4. **Guarded Customer Self-Cancellation:** Customers can cancel orders via the public tracking interface only while in `RECEIVED` or `QUEUED` operational status and if unpaid. Requests to cancel orders already in production (`WASHING`, `DRYING`, etc.) or already paid are strictly rejected (`422 Unprocessable Content`).
5. **Mobile-First Public Tracking UI:** Responsive, standalone screen (`/track/:token`) featuring an 8-stage visual progress stepper, item breakdown, financial summary badge, outlet WhatsApp contact button, and cancellation confirmation dialog.

---

## 2. Implemented Tasks Breakdown

| Task ID | Description | Source Files | Test Artifacts | Status |
| :--- | :--- | :--- | :--- | :--- |
| **M4-01** | Database schema & Alembic migration for `tracking_tokens` table | `backend/alembic/versions/c018a74e512b_m4_customer_public_tracking.py` | `alembic upgrade head --sql` | **PASS** |
| **M4-02** | 256-bit cryptographic token service & PII masking utilities | `backend/app/modules/tracking/service.py`, `models.py` | `tests/api/test_tracking_api.py` | **PASS** |
| **M4-03** | Public tracking API endpoint with privacy headers | `backend/app/modules/tracking/router.py`, `schemas.py` | `tests/api/test_tracking_api.py` | **PASS** |
| **M4-04** | Guarded public order cancellation endpoint | `backend/app/modules/tracking/router.py`, `service.py` | `tests/api/test_tracking_api.py` | **PASS** |
| **M4-05** | Automatic token generation hook & invoice integration | `backend/app/modules/orders/service.py`, `invoices/service.py` | `tests/api/test_invoices_api.py` | **PASS** |
| **M4-06** | Mobile-first public tracking screen (`/track/:token`) | `frontend/src/pages/tracking/public-tracking-page.tsx`, `App.tsx` | `frontend/e2e/m4-tracking.spec.ts` | **PASS** |
| **M4-07** | 8-Stage operational progress stepper & financial card | `frontend/src/pages/tracking/public-tracking-page.tsx` | `frontend/e2e/m4-tracking.spec.ts` | **PASS** |
| **M4-08** | Customer self-cancellation confirmation dialog | `frontend/src/pages/tracking/public-tracking-page.tsx` | `frontend/e2e/m4-tracking.spec.ts` | **PASS** |
| **M4-09** | Automated backend unit and API test suite | `backend/tests/api/test_tracking_api.py` | 38/38 Pytest passing | **PASS** |
| **M4-10** | Playwright E2E browser tests & Milestone 4 Report | `frontend/e2e/m4-tracking.spec.ts`, `doc/implementation/M4-REPORT.md` | 3/3 Playwright suites passing | **PASS** |

---

## 3. Test & Verification Evidence

### 3.1 Backend Pytest Suite
Command: `backend/.venv/Scripts/pytest -v`
```text
============================= test session starts =============================
platform win32 -- Python 3.12.0, pytest-9.2.0, pluggy-1.7.0
rootdir: D:\Kuliah\joki\Kerja Praktek Aqil\kawan aqil\projek
plugins: anyio-4.16.0, cov-7.1.0
collected 38 items

backend/tests/api/test_auth_api.py::test_auth_full_lifecycle PASSED      [  2%]
backend/tests/api/test_auth_api.py::test_inactive_account_rejection PASSED [  5%]
backend/tests/api/test_customers_api.py::test_phone_normalizer PASSED    [  7%]
backend/tests/api/test_customers_api.py::test_customer_crud_and_search PASSED [ 10%]
backend/tests/api/test_expenses_api.py::test_expenses_lifecycle_and_rbac PASSED [ 13%]
backend/tests/api/test_health.py::test_root_info PASSED                  [ 15%]
backend/tests/api/test_health.py::test_liveness_returns_200 PASSED       [ 18%]
backend/tests/api/test_health.py::test_readiness_returns_200_when_db_up PASSED [ 21%]
backend/tests/api/test_health.py::test_request_id_in_response_header PASSED [ 23%]
backend/tests/api/test_health.py::test_custom_request_id_propagated PASSED [ 26%]
backend/tests/api/test_health.py::test_security_headers_present PASSED   [ 28%]
backend/tests/api/test_invoices_api.py::test_invoices_and_whatsapp_flow PASSED [ 31%]
backend/tests/api/test_orders_api.py::test_order_full_lifecycle_and_invariants PASSED [ 34%]
backend/tests/api/test_payments_api.py::test_payments_api_full_flow PASSED [ 36%]
backend/tests/api/test_rbac_and_users.py::test_rbac_user_management_and_settings PASSED [ 39%]
backend/tests/api/test_services_api.py::test_services_catalog_lifecycle PASSED [ 42%]
backend/tests/api/test_tracking_api.py::test_pii_masking_logic PASSED    [ 44%]
backend/tests/api/test_tracking_api.py::test_tracking_api_full_flow PASSED [ 47%]
backend/tests/security/test_argon2.py::test_argon2_hashing_and_verification PASSED [ 50%]
backend/tests/security/test_argon2.py::test_argon2_unique_salts PASSED   [ 52%]
backend/tests/security/test_login_throttling.py::test_login_throttling_after_five_failed_attempts PASSED [ 55%]
backend/tests/security/test_session_and_csrf.py::test_session_lifecycle PASSED [ 57%]
backend/tests/security/test_session_and_csrf.py::test_session_expiration PASSED [ 60%]
backend/tests/security/test_session_and_csrf.py::test_csrf_token_generation_and_verification PASSED [ 63%]
backend/tests/unit/test_order_state_machine.py::test_standard_forward_workflow PASSED [ 65%]
backend/tests/unit/test_order_state_machine.py::test_skip_ironing_when_not_required PASSED [ 68%]
backend/tests/unit/test_order_state_machine.py::test_invalid_transition_skips PASSED [ 71%]
backend/tests/unit/test_order_state_machine.py::test_terminal_states_immutable PASSED [ 73%]
backend/tests/unit/test_order_state_machine.py::test_cancellation_requires_reason PASSED [ 76%]
backend/tests/unit/test_order_state_machine.py::test_order_completion_staged_negative_validation PASSED [ 78%]
backend/tests/unit/test_payment_balance.py::test_payment_balance_unpaid_when_no_payments PASSED [ 81%]
backend/tests/unit/test_payment_balance.py::test_payment_balance_partially_paid PASSED [ 84%]
backend/tests/unit/test_payment_balance.py::test_payment_balance_fully_paid PASSED [ 86%]
backend/tests/unit/test_payment_balance.py::test_payment_balance_excludes_voided_payments PASSED [ 89%]
backend/tests/unit/test_pricing.py::test_weight_rounding_dec_01 PASSED   [ 92%]
backend/tests/unit/test_pricing.py::test_minimum_weight_kiloan_dec_02 PASSED [ 94%]
backend/tests/unit/test_pricing.py::test_per_item_pricing PASSED         [ 97%]
backend/tests/unit/test_pricing.py::test_order_total_calculation PASSED  [100%]

============================= 38 passed in 8.50s ==============================
```

### 3.2 Frontend Playwright E2E Suite
Command: `npm --prefix frontend run test:e2e`
```text
Running 3 tests using 3 workers

  ok 2 [chromium] › e2e\m4-tracking.spec.ts:91:3 › Milestone 4: Public Customer Tracking E2E › E2E: Unauthenticated Customer Tracking View, PII Masking, Progress Stepper & Self-Cancellation (4.1s)
  ok 1 [chromium] › e2e\m3-finance.spec.ts:269:3 › Milestone 3: Finance & Digital Invoices E2E › E2E: Expenses Management, Payment Intake & Digital Invoice Modal (5.2s)
  ok 3 [chromium] › e2e\m2-core-laundry.spec.ts:275:3 › Milestone 2: Core Laundry Operations E2E › E2E: Navigation, Customers, Services, Order Intake & Status Progression (5.4s)

  3 passed (11.5s)
```

### 3.3 Static Analysis & Build Status
- **Ruff:** All checks passed (0 errors, 0 warnings).
- **Mypy:** `Success: no issues found in 137 source files`.
- **ESLint:** Clean (0 errors, 0 warnings).
- **Vite Build:** Clean production build in 736ms (`375.64 kB gzip: 98.48 kB`).
- **OpenAPI Schema:** Exported and synced to `doc/api/openapi.json`.

---

## 4. Conclusion & Handover

Milestone 4 is verified complete with evidence across all layers. The project is ready for immediate autonomous execution of **Milestone 5: Pickup & Delivery Logistics**.

