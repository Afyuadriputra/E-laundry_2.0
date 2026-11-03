# Milestone 5 Verification & Implementation Report: Pickup & Delivery Logistics

**Project:** E-Laundry 2.0  
**Milestone:** M5 (Pickup & Delivery Logistics)  
**Date:** 2026-11-03  
**Status:** **PASS (PICKUP_DELIVERY_READY)**

---

## 1. Executive Summary

Milestone 5 implements the complete end-to-end logistics subsystem for pickup and delivery requests, mobile courier dispatch, multi-stage delivery task execution, and atomic conversion to formal laundry orders (DEC-10), as specified by `PRD.md §4.5`, `TRD.md §4.5`, `BSD.md §22, §24, §25, §30`, `AFD.md §6`, and `IPD.md §M5`.

Key deliverables completed and verified:
1. **Schema & Deferred Foreign Key Resolution:** Created `pickup_requests`, `delivery_tasks`, and `delivery_status_histories` tables. All deferred foreign key constraints across milestones (`orders.pickup_request_id`, `tracking_tokens.pickup_request_id`, and `order_handoffs.delivery_task_id`) were resolved in a single, strictly non-destructive migration (`backend/alembic/versions/e528b96f140a_m5_pickup_and_delivery_logistics.py`). Transactional DDL verified with `alembic upgrade head --sql`.
2. **Public Pickup Request Intake:** Customers can submit pickup requests without authentication via `POST /api/v1/pickup-delivery/requests/public?business_id=...`. Time windows are validated, and 256-bit cryptographic tracking tokens are provisioned immediately.
3. **Courier Mobile Workflow:** Mobile-first courier task view (`/delivery` tab) with segmented filters (`Tugas Aktif`, `Selesai`, `Semua`). Couriers can advance tasks through valid status transitions (`ASSIGNED` -> `EN_ROUTE` -> `ARRIVED` -> `COMPLETED` / `FAILED`), record recipient names upon handover, report delivery failure reasons, and use WhatsApp deep-links or Google Maps navigation.
4. **Atomic Conversion to Laundry Order (DEC-10):** Cashiers can atomically convert completed pickup requests into official laundry orders via `POST /api/v1/pickup-delivery/requests/{id}/convert-order`. The system enforces that each pickup request can only be converted once, automatically links `orders.pickup_request_id`, marks the pickup as `CONVERTED`, and calculates line item charges and delivery fees.
5. **Multi-Role Security & Gating:** All courier endpoints enforce `COURIER` or higher role boundaries, while management actions (confirming pickups, converting to orders, dispatching delivery tasks) enforce `CASHIER` or `OWNER` role checks and CSRF protections.

---

## 2. Implemented Tasks Breakdown

| Task ID | Description | Source Files | Test Artifacts | Status |
| :--- | :--- | :--- | :--- | :--- |
| **M5-01** | Database schema & Alembic migration for `pickup_requests`, `delivery_tasks`, `delivery_status_histories`, resolving deferred FKs | `backend/alembic/versions/e528b96f140a_m5_pickup_and_delivery_logistics.py`, `models.py` | `alembic upgrade head --sql` | **PASS** |
| **M5-02** | Pickup request service & public intake endpoint | `backend/app/modules/pickup_delivery/service.py`, `router.py` | `tests/api/test_pickup_delivery_api.py` | **PASS** |
| **M5-03** | Cashier pickup confirmation, scheduling & courier dispatch | `backend/app/modules/pickup_delivery/service.py`, `schemas.py` | `tests/api/test_pickup_delivery_api.py` | **PASS** |
| **M5-04** | Courier task lifecycle state transitions (`EN_ROUTE`, `ARRIVED`, `COMPLETED`, `FAILED`) | `backend/app/modules/pickup_delivery/service.py` | `tests/api/test_pickup_delivery_api.py` | **PASS** |
| **M5-05** | Pickup & Delivery API router with CSRF and RBAC | `backend/app/modules/pickup_delivery/router.py`, `app/api/v1/router.py` | `tests/api/test_pickup_delivery_api.py` | **PASS** |
| **M5-06** | Atomic single-conversion from pickup to official order (DEC-10) | `backend/app/modules/pickup_delivery/service.py` | `tests/api/test_pickup_delivery_api.py` | **PASS** |
| **M5-07** | Courier mobile task view & status transition UI | `frontend/src/pages/delivery/delivery-page.tsx`, `App.tsx` | `frontend/e2e/m5-delivery.spec.ts` | **PASS** |
| **M5-08** | Cashier pickup intake, confirmation modal & order conversion modal | `frontend/src/pages/delivery/delivery-page.tsx` | `frontend/e2e/m5-delivery.spec.ts` | **PASS** |
| **M5-09** | Automated backend API test suite for pickup & delivery | `backend/tests/api/test_pickup_delivery_api.py` | 39/39 Pytest passing | **PASS** |
| **M5-10** | Playwright E2E browser tests & Milestone 5 Report | `frontend/e2e/m5-delivery.spec.ts`, `doc/implementation/M5-REPORT.md` | 5/5 Playwright suites passing | **PASS** |

---

## 3. Test & Verification Evidence

### 3.1 Backend Pytest Suite
Command: `backend/.venv/Scripts/pytest -v`
```text
============================= test session starts =============================
platform win32 -- Python 3.12.0, pytest-9.2.0, pluggy-1.7.0
rootdir: D:\Kuliah\joki\Kerja Praktek Aqil\kawan aqil\projek
configfile: pytest.ini
testpaths: backend/tests
plugins: anyio-4.16.0, cov-7.1.0
collected 39 items

backend/tests/api/test_auth_api.py::test_auth_full_lifecycle PASSED      [  2%]
backend/tests/api/test_auth_api.py::test_inactive_account_rejection PASSED [  5%]
backend/tests/api/test_customers_api.py::test_phone_normalizer PASSED    [  7%]
backend/tests/api/test_customers_api.py::test_customer_crud_and_search PASSED [ 10%]
backend/tests/api/test_expenses_api.py::test_expenses_lifecycle_and_rbac PASSED [ 12%]
backend/tests/api/test_health.py::test_root_info PASSED                  [ 15%]
backend/tests/api/test_health.py::test_liveness_returns_200 PASSED       [ 17%]
backend/tests/api/test_health.py::test_readiness_returns_200_when_db_up PASSED [ 20%]
backend/tests/api/test_health.py::test_request_id_in_response_header PASSED [ 23%]
backend/tests/api/test_health.py::test_custom_request_id_propagated PASSED [ 25%]
backend/tests/api/test_health.py::test_security_headers_present PASSED   [ 28%]
backend/tests/api/test_invoices_api.py::test_invoices_and_whatsapp_flow PASSED [ 30%]
backend/tests/api/test_orders_api.py::test_order_full_lifecycle_and_invariants PASSED [ 33%]
backend/tests/api/test_payments_api.py::test_payments_api_full_flow PASSED [ 35%]
backend/tests/api/test_pickup_delivery_api.py::test_pickup_delivery_full_lifecycle PASSED [ 38%]
backend/tests/api/test_rbac_and_users.py::test_rbac_user_management_and_settings PASSED [ 41%]
backend/tests/api/test_services_api.py::test_services_catalog_lifecycle PASSED [ 43%]
backend/tests/api/test_tracking_api.py::test_pii_masking_logic PASSED    [ 46%]
backend/tests/api/test_tracking_api.py::test_tracking_api_full_flow PASSED [ 48%]
backend/tests/security/test_argon2.py::test_argon2_hashing_and_verification PASSED [ 51%]
backend/tests/security/test_argon2.py::test_argon2_unique_salts PASSED   [ 53%]
backend/tests/security/test_login_throttling.py::test_login_throttling_after_five_failed_attempts PASSED [ 56%]
backend/tests/security/test_session_and_csrf.py::test_session_lifecycle PASSED [ 58%]
backend/tests/security/test_session_and_csrf.py::test_session_expiration PASSED [ 61%]
backend/tests/security/test_csrf_token_generation_and_verification PASSED [ 64%]
backend/tests/unit/test_order_state_machine.py::test_standard_forward_workflow PASSED [ 66%]
backend/tests/unit/test_order_state_machine.py::test_skip_ironing_when_not_required PASSED [ 69%]
backend/tests/unit/test_order_state_machine.py::test_invalid_transition_skips PASSED [ 71%]
backend/tests/unit/test_order_state_machine.py::test_terminal_states_immutable PASSED [ 74%]
backend/tests/unit/test_order_state_machine.py::test_cancellation_requires_reason PASSED [ 76%]
backend/tests/unit/test_order_state_machine.py::test_order_completion_staged_negative_validation PASSED [ 79%]
backend/tests/unit/test_payment_balance.py::test_payment_balance_unpaid_when_no_payments PASSED [ 82%]
backend/tests/unit/test_payment_balance.py::test_payment_balance_partially_paid PASSED [ 84%]
backend/tests/unit/test_payment_balance.py::test_payment_balance_fully_paid PASSED [ 87%]
backend/tests/unit/test_payment_balance.py::test_payment_balance_excludes_voided_payments PASSED [ 89%]
backend/tests/unit/test_pricing.py::test_weight_rounding_dec_01 PASSED   [ 92%]
backend/tests/unit/test_pricing.py::test_minimum_weight_kiloan_dec_02 PASSED [ 94%]
backend/tests/unit/test_per_item_pricing PASSED         [ 97%]
backend/tests/unit/test_order_total_calculation PASSED  [100%]

============================= 39 passed in 10.18s =============================
```

### 3.2 Frontend Playwright E2E Test Suite
Command: `npm --prefix frontend run test:e2e`
```text
Running 5 tests using 5 workers

  ok 1 [chromium] › e2e\m4-tracking.spec.ts:91:3 › Milestone 4: Public Customer Tracking E2E › E2E: Unauthenticated Customer Tracking View, PII Masking, Progress Stepper & Self-Cancellation (5.5s)
  ok 2 [chromium] › e2e\m5-delivery.spec.ts:176:3 › Milestone 5: Pickup & Delivery Logistics E2E › Courier mobile workflow: moves task from ASSIGNED -> EN_ROUTE -> ARRIVED -> COMPLETED (5.7s)
  ok 3 [chromium] › e2e\m5-delivery.spec.ts:4:3 › Milestone 5: Pickup & Delivery Logistics E2E › Cashier manages pickup requests, confirms assignment, and converts to order (DEC-10) (6.1s)
  ok 4 [chromium] › e2e\m3-finance.spec.ts:269:3 › Milestone 3: Finance & Digital Invoices E2E › E2E: Expenses Management, Payment Intake & Digital Invoice Modal (6.7s)
  ok 5 [chromium] › e2e\m2-core-laundry.spec.ts:275:3 › Milestone 2: Core Laundry Operations E2E › E2E: Navigation, Customers, Services, Order Intake & Status Progression (7.0s)

  5 passed (13.6s)
```

### 3.3 Code Hygiene & Quality Gates
- **Ruff:** Clean (`0 errors`).
- **Mypy:** Clean (`Success: no issues found in 139 source files`).
- **ESLint:** Clean (`0 errors, 0 warnings`).
- **Vite Build:** Clean production bundle built in 1.28s.
- **OpenAPI Schema:** Exported and synchronized to `doc/api/openapi.json`.

---

## 4. Acceptance Gate Verification
- [x] `pickup_requests`, `delivery_tasks`, and `delivery_status_histories` schemas conform to BSD §22, §24, §25.
- [x] All deferred foreign keys from M2 and M4 are cleanly resolved without circular dependencies.
- [x] Public intake validates time windows and provisions tracking tokens with SHA-256 storage.
- [x] Courier workflow operates smoothly with 44px tap targets, segmented filtering, and realistic state transitions.
- [x] DEC-10 atomic conversion prevents duplicate order creation and links records cleanly.
- [x] All 39 backend tests and 5 E2E browser test suites pass.

**Gate Verdict: PASS (PICKUP_DELIVERY_READY)**

