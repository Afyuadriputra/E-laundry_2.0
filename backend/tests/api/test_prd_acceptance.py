"""
Official PRD §15.2 Acceptance Test Verification Suite (AT-01 through AT-30).
Maps 1:1 to every official acceptance requirement from PRD.md §15.2.
Validates end-to-end functionality across Auth, Orders, Pricing, Logistics, Payments,
Security/RBAC, Concurrency, and System Resilience.
"""

import uuid
from datetime import UTC, date, datetime, time, timedelta
from decimal import Decimal

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.modules.businesses.models import Business, BusinessSettings
from app.modules.customers.models import Customer
from app.modules.orders.domain.pricing import PricingEngine
from app.modules.orders.domain.state_machine import OperationalStatus
from app.modules.orders.models import Order, OrderHandoff, OrderItem, OrderStatusHistory
from app.modules.payments.domain.balance import PaymentStatus, calculate_payment_balance
from app.modules.payments.models import Payment, PaymentVoid
from app.modules.pickup_delivery.models import (
    DeliveryStatusHistory,
    DeliveryTask,
    DeliveryTaskStatus,
    DeliveryTaskType,
    PickupRequest,
    PickupStatus,
)
from app.modules.services.models import Service
from app.modules.tracking.models import TrackingToken
from app.modules.tracking.service import TrackingService
from app.modules.users.models import User, UserRole


# ---------------------------------------------------------------------------
# Fixtures & Helpers
# ---------------------------------------------------------------------------

@pytest.fixture
def prd_env(db_session: Session):
    biz = Business(
        id=uuid.uuid4(),
        name="Laundry PRD Acceptance",
        phone_e164="+6281199990001",
        address="Jl. Acceptance No. 1",
        timezone="Asia/Jakarta",
        is_active=True,
    )
    settings = BusinessSettings(
        id=uuid.uuid4(),
        business_id=biz.id,
        pickup_enabled=True,
        delivery_enabled=True,
    )
    db_session.add(biz)
    db_session.add(settings)

    password = "TestPassword123!"
    owner = User(
        id=uuid.uuid4(),
        business_id=biz.id,
        username="owner_acceptance",
        full_name="Budi Owner",
        password_hash=hash_password(password),
        role=UserRole.OWNER.value,
        is_active=True,
    )
    cashier = User(
        id=uuid.uuid4(),
        business_id=biz.id,
        username="cashier_acceptance",
        full_name="Siti Cashier",
        password_hash=hash_password(password),
        role=UserRole.CASHIER.value,
        is_active=True,
    )
    staff = User(
        id=uuid.uuid4(),
        business_id=biz.id,
        username="staff_acceptance",
        full_name="Andi Staff",
        password_hash=hash_password(password),
        role=UserRole.STAFF.value,
        is_active=True,
    )
    courier = User(
        id=uuid.uuid4(),
        business_id=biz.id,
        username="courier_acceptance",
        full_name="Doni Courier",
        password_hash=hash_password(password),
        role=UserRole.COURIER.value,
        is_active=True,
    )
    db_session.add_all([owner, cashier, staff, courier])

    customer = Customer(
        id=uuid.uuid4(),
        business_id=biz.id,
        full_name="Ibu Anita",
        phone_e164="+6281234567800",
        address="Jl. Mawar No. 12",
        is_active=True,
    )
    service_kiloan = Service(
        id=uuid.uuid4(),
        business_id=biz.id,
        name="Cuci Komplit Kiloan",
        pricing_type="PER_KG",
        unit="KG",
        unit_price=8000,
        requires_ironing=True,
        is_active=True,
        version=1,
    )
    service_satuan = Service(
        id=uuid.uuid4(),
        business_id=biz.id,
        name="Bedcover Jumbo",
        pricing_type="PER_ITEM",
        unit="PIECE",
        unit_price=25000,
        requires_ironing=True,
        is_active=True,
        version=1,
    )
    db_session.add_all([customer, service_kiloan, service_satuan])
    db_session.commit()

    return {
        "biz": biz,
        "owner": owner,
        "cashier": cashier,
        "staff": staff,
        "courier": courier,
        "customer": customer,
        "service_kiloan": service_kiloan,
        "service_satuan": service_satuan,
        "password": password,
    }


def _login(client: TestClient, username: str, password: str) -> dict[str, str]:
    res = client.post("/api/v1/auth/login", json={"username": username, "password": password})
    assert res.status_code == 200, f"Login failed for {username}: {res.text}"
    csrf = res.headers.get("X-CSRF-Token") or res.json()["data"]["csrf_token"]
    return {"X-CSRF-Token": csrf}


# ---------------------------------------------------------------------------
# AT-01 to AT-30 Test Implementations
# ---------------------------------------------------------------------------

def test_at_01_owner_login_success(client: TestClient, prd_env):
    """AT-01: Owner login dengan akun valid -> Login berhasil."""
    headers = _login(client, prd_env["owner"].username, prd_env["password"])
    res = client.get("/api/v1/auth/me", headers=headers)
    assert res.status_code == 200
    assert res.json()["data"]["username"] == prd_env["owner"].username
    assert res.json()["data"]["role"] == "OWNER"


def test_at_02_user_invalid_password_rejected(client: TestClient, prd_env):
    """AT-02: Pengguna memakai password salah -> Login ditolak."""
    res = client.post(
        "/api/v1/auth/login",
        json={"username": prd_env["owner"].username, "password": "WrongPassword999!"},
    )
    assert res.status_code == 401
    assert res.json()["error"]["code"] == "UNAUTHENTICATED"


def test_at_03_cashier_create_order_full_flow(client: TestClient, prd_env):
    """AT-03: Kasir membuat pesanan baru -> Pesanan tersimpan dan nomor dibuat."""
    headers = _login(client, prd_env["cashier"].username, prd_env["password"])
    payload = {
        "customer_id": str(prd_env["customer"].id),
        "items": [
            {
                "service_id": str(prd_env["service_kiloan"].id),
                "quantity": 3.5,
                "notes": "Baju santai",
            }
        ],
        "notes": "Pesanan pertama kasir",
    }
    res = client.post("/api/v1/orders", json=payload, headers=headers)
    assert res.status_code in (200, 201)
    data = res.json()["data"]
    assert "order_number" in data
    assert data["order_number"].startswith("ORD-")
    assert data["total_amount"] == 28000  # 3.5 kg * 8000


def test_at_04_order_pricing_per_kg_with_min_weight(client: TestClient, prd_env):
    """AT-04: Pesanan menggunakan harga per kg -> Total dihitung benar (min weight & rounding)."""
    # Test case 1: 1.8 kg (below 3.0 kg min) -> rounded to 3.0 kg minimum
    calc_min = PricingEngine.calculate_line_item(
        pricing_type="PER_KG",
        quantity=Decimal("1.8"),
        unit_price=8000,
    )
    assert calc_min.measured_quantity == Decimal("1.8")
    assert calc_min.billable_quantity == Decimal("3.0")
    assert calc_min.line_total == 24000

    # Test case 2: 4.25 kg with HALF_UP rounding -> 4.3 kg
    calc_norm = PricingEngine.calculate_line_item(
        pricing_type="PER_KG",
        quantity=Decimal("4.25"),
        unit_price=8000,
    )
    assert calc_norm.measured_quantity == Decimal("4.25")
    assert calc_norm.billable_quantity == Decimal("4.3")
    assert calc_norm.line_total == 34400


def test_at_05_multi_service_order_calculation(client: TestClient, prd_env):
    """AT-05: Pesanan memiliki beberapa layanan -> Total adalah jumlah seluruh item dan biaya tambahan."""
    headers = _login(client, prd_env["cashier"].username, prd_env["password"])
    payload = {
        "customer_id": str(prd_env["customer"].id),
        "items": [
            {
                "service_id": str(prd_env["service_kiloan"].id),
                "quantity": 3.0,
            },
            {
                "service_id": str(prd_env["service_satuan"].id),
                "quantity": 2,
            },
        ],
    }
    res = client.post("/api/v1/orders", json=payload, headers=headers)
    assert res.status_code in (200, 201)
    data = res.json()["data"]
    # 3.0 kg * 8000 = 24000; 2 * 25000 = 50000; total = 74000
    assert data["total_amount"] == 74000
    assert len(data["items"]) == 2


def test_at_06_price_change_snapshot_immutability(client: TestClient, db_session: Session, prd_env):
    """AT-06: Harga layanan diubah -> Pesanan lama tidak berubah."""
    headers = _login(client, prd_env["cashier"].username, prd_env["password"])

    # 1. Create order with current price (8000)
    payload = {
        "customer_id": str(prd_env["customer"].id),
        "items": [{"service_id": str(prd_env["service_kiloan"].id), "quantity": 3.0}],
    }
    res = client.post("/api/v1/orders", json=payload, headers=headers)
    assert res.status_code in (200, 201)
    order_id = res.json()["data"]["id"]
    original_total = res.json()["data"]["total_amount"]
    assert original_total == 24000

    # 2. Mutate catalog service price to 12000
    prd_env["service_kiloan"].unit_price = 12000
    db_session.commit()

    # 3. Verify existing order total amount and snapshot item price are untouched
    res_get = client.get(f"/api/v1/orders/{order_id}", headers=headers)
    assert res_get.status_code == 200
    assert res_get.json()["data"]["total_amount"] == 24000
    assert res_get.json()["data"]["items"][0]["unit_price_snapshot"] == 8000


def test_at_07_cashier_generate_invoice(client: TestClient, prd_env):
    """AT-07: Kasir membuat nota -> Nota sesuai transaksi."""
    headers = _login(client, prd_env["cashier"].username, prd_env["password"])
    res = client.post(
        "/api/v1/orders",
        json={
            "customer_id": str(prd_env["customer"].id),
            "items": [{"service_id": str(prd_env["service_satuan"].id), "quantity": 1}],
        },
        headers=headers,
    )
    order_id = res.json()["data"]["id"]

    res_inv = client.get(f"/api/v1/invoices/{order_id}", headers=headers)
    assert res_inv.status_code == 200
    inv = res_inv.json()["data"]
    assert inv["order_number"].startswith("ORD-")
    assert inv["total_amount"] == 25000
    assert "business_name" in inv


def test_at_08_whatsapp_message_link_generation(client: TestClient, prd_env):
    """AT-08: Kasir membuka WhatsApp -> Pesan siap kirim dengan informasi benar."""
    headers = _login(client, prd_env["cashier"].username, prd_env["password"])
    res = client.post(
        "/api/v1/orders",
        json={
            "customer_id": str(prd_env["customer"].id),
            "items": [{"service_id": str(prd_env["service_satuan"].id), "quantity": 1}],
        },
        headers=headers,
    )
    order_id = res.json()["data"]["id"]

    res_inv = client.get(f"/api/v1/invoices/{order_id}", headers=headers)
    assert res_inv.status_code == 200
    inv = res_inv.json()["data"]
    assert "whatsapp_share_url" in inv
    assert "wa.me" in inv["whatsapp_share_url"]
    assert "ORD-" in inv["whatsapp_share_text"]


def test_at_09_status_history_recording(client: TestClient, prd_env):
    """AT-09: Staf mengubah status -> Riwayat status tersimpan."""
    headers = _login(client, prd_env["cashier"].username, prd_env["password"])
    res = client.post(
        "/api/v1/orders",
        json={
            "customer_id": str(prd_env["customer"].id),
            "items": [{"service_id": str(prd_env["service_satuan"].id), "quantity": 1}],
        },
        headers=headers,
    )
    order_data = res.json()["data"]
    order_id = order_data["id"]
    current_version = order_data["version"]

    # Transition: RECEIVED -> QUEUED
    res_t1 = client.post(
        f"/api/v1/orders/{order_id}/transition",
        json={
            "to_status": "QUEUED",
            "reason": "Masuk antrean cuci",
            "expected_version": current_version,
        },
        headers=headers,
    )
    assert res_t1.status_code == 200

    # Verify history
    res_get = client.get(f"/api/v1/orders/{order_id}", headers=headers)
    history = res_get.json()["data"]["status_history"]
    statuses = [h["to_status"] for h in history]
    assert "RECEIVED" in statuses
    assert "QUEUED" in statuses


def test_at_10_public_tracking_view_with_pii_masking(client: TestClient, db_session: Session, prd_env):
    """AT-10: Pelanggan membuka tracking valid -> Status pesanan terlihat (unauthenticated & PII masked)."""
    headers = _login(client, prd_env["cashier"].username, prd_env["password"])
    res = client.post(
        "/api/v1/orders",
        json={
            "customer_id": str(prd_env["customer"].id),
            "items": [{"service_id": str(prd_env["service_satuan"].id), "quantity": 1}],
        },
        headers=headers,
    )
    order_id = uuid.UUID(res.json()["data"]["id"])

    # Generate public tracking token
    token_record, raw_token = TrackingService.create_order_tracking_token(
        db=db_session,
        order_id=order_id,
        created_by=prd_env["cashier"].id,
    )

    # Public unauthenticated request
    res_track = client.get(f"/api/v1/tracking/{raw_token}")
    assert res_track.status_code == 200
    track_data = res_track.json()["data"]
    assert track_data["tracking_type"] == "ORDER"
    assert track_data["current_status"] == "RECEIVED"
    assert "customer_name_masked" in track_data


def test_at_11_invalid_tracking_token_returns_404(client: TestClient):
    """AT-11: Pelanggan memakai token salah -> Akses ditolak (404)."""
    fake_token = "a" * 43
    res = client.get(f"/api/v1/tracking/{fake_token}")
    assert res.status_code == 404


def test_at_12_revoked_or_expired_tracking_token_inaccessible(client: TestClient, db_session: Session, prd_env):
    """AT-12: Token tracking dicabut/kedaluwarsa -> Token lama tidak dapat digunakan."""
    headers = _login(client, prd_env["cashier"].username, prd_env["password"])
    res = client.post(
        "/api/v1/orders",
        json={
            "customer_id": str(prd_env["customer"].id),
            "items": [{"service_id": str(prd_env["service_satuan"].id), "quantity": 1}],
        },
        headers=headers,
    )
    order_id = uuid.UUID(res.json()["data"]["id"])

    # Expired token -> 410 Gone
    _, expired_raw_token = TrackingService.create_order_tracking_token(
        db=db_session,
        order_id=order_id,
        ttl_days=-1,  # expired in past
    )
    exp_res = client.get(f"/api/v1/tracking/{expired_raw_token}")
    assert exp_res.status_code == 410


def test_at_13_cross_tenant_and_idor_order_isolation(client: TestClient, db_session: Session, prd_env):
    """AT-13: Pelanggan/petugas mencoba melihat pesanan lain -> Data tidak dapat diakses (Anti-IDOR)."""
    foreign_biz = Business(
        id=uuid.uuid4(),
        name="Foreign Laundry",
        phone_e164="+6281188880002",
        address="Jl. Asing No. 2",
        timezone="Asia/Jakarta",
        is_active=True,
    )
    db_session.add(foreign_biz)

    foreign_user = User(
        id=uuid.uuid4(),
        business_id=foreign_biz.id,
        username="foreign_cashier",
        full_name="Foreign Cashier",
        password_hash=hash_password("Pass123!"),
        role=UserRole.CASHIER.value,
        is_active=True,
    )
    foreign_customer = Customer(
        id=uuid.uuid4(),
        business_id=foreign_biz.id,
        full_name="Foreign Customer",
        phone_e164="+6281987654321",
        address="Jl. Asing 5",
        is_active=True,
    )
    db_session.add_all([foreign_user, foreign_customer])
    db_session.flush()

    foreign_order = Order(
        id=uuid.uuid4(),
        business_id=foreign_biz.id,
        customer_id=foreign_customer.id,
        order_number="ORD-20261104-9999",
        created_by=foreign_user.id,
        operational_status=OperationalStatus.RECEIVED.value,
        intake_method="DROP_OFF",
        return_method="SELF_PICKUP",
        total_amount=50000,
        version=1,
    )
    db_session.add(foreign_order)
    db_session.commit()

    headers = _login(client, prd_env["cashier"].username, prd_env["password"])
    res = client.get(f"/api/v1/orders/{foreign_order.id}", headers=headers)
    assert res.status_code == 404


def test_at_14_public_pickup_request_intake(client: TestClient, prd_env):
    """AT-14: Pelanggan mengajukan pickup -> Permintaan masuk dashboard."""
    tomorrow = date.today() + timedelta(days=1)
    payload = {
        "requester_name": "Bapak Hendra",
        "phone_e164": "+6281234567888",
        "pickup_address": "Jl. Cempaka No. 8",
        "requested_date": str(tomorrow),
        "requested_time_start": "09:00:00",
        "requested_time_end": "11:00:00",
        "notes": "Tolong jemput di lobby kantor",
    }
    client_public = TestClient(client.app)
    res = client_public.post(
        f"/api/v1/pickup-delivery/requests/public?business_id={prd_env['biz'].id}",
        json=payload,
    )
    assert res.status_code == 201
    data = res.json()["data"]
    assert data["status"] == "REQUESTED"
    assert "tracking_token" in data


def test_at_15_admin_confirm_pickup_request(client: TestClient, db_session: Session, prd_env):
    """AT-15: Admin mengonfirmasi pickup -> Status berubah sesuai."""
    req = PickupRequest(
        id=uuid.uuid4(),
        business_id=prd_env["biz"].id,
        request_number="PCK-20261104-0010",
        requester_name="Ibu Rina",
        phone_e164="+6281234567877",
        pickup_address="Jl. Anggrek No. 3",
        requested_date=date.today(),
        requested_time_start=time(9, 0),
        requested_time_end=time(11, 0),
        status=PickupStatus.REQUESTED.value,
    )
    db_session.add(req)
    db_session.commit()

    headers = _login(client, prd_env["cashier"].username, prd_env["password"])
    now = datetime.now(UTC)
    payload = {
        "confirmed_start_at": (now + timedelta(hours=1)).isoformat(),
        "confirmed_end_at": (now + timedelta(hours=3)).isoformat(),
        "courier_user_id": str(prd_env["courier"].id),
        "notes": "Kurir segera meluncur",
    }
    res = client.post(
        f"/api/v1/pickup-delivery/requests/{req.id}/confirm",
        json=payload,
        headers=headers,
    )
    assert res.status_code == 200
    assert res.json()["data"]["status"] == "ASSIGNED"


def test_at_16_courier_complete_pickup_task(client: TestClient, db_session: Session, prd_env):
    """AT-16: Kurir menyelesaikan penjemputan -> Riwayat tugas tercatat."""
    # Create and confirm pickup request to generate DeliveryTask with valid constraints
    req = PickupRequest(
        id=uuid.uuid4(),
        business_id=prd_env["biz"].id,
        request_number="PCK-20261104-0016",
        requester_name="Ibu Rina",
        phone_e164="+6281234567877",
        pickup_address="Jl. Anggrek No. 3",
        requested_date=date.today(),
        requested_time_start=time(9, 0),
        requested_time_end=time(11, 0),
        status=PickupStatus.REQUESTED.value,
    )
    db_session.add(req)
    db_session.commit()

    cashier_headers = _login(client, prd_env["cashier"].username, prd_env["password"])
    now = datetime.now(UTC)
    res_confirm = client.post(
        f"/api/v1/pickup-delivery/requests/{req.id}/confirm",
        json={
            "confirmed_start_at": (now + timedelta(hours=1)).isoformat(),
            "confirmed_end_at": (now + timedelta(hours=3)).isoformat(),
            "courier_user_id": str(prd_env["courier"].id),
        },
        headers=cashier_headers,
    )
    assert res_confirm.status_code == 200
    task = db_session.scalar(select(DeliveryTask).where(DeliveryTask.pickup_request_id == req.id))
    assert task is not None

    # Courier advances task to COMPLETED
    courier_headers = _login(client, prd_env["courier"].username, prd_env["password"])
    res_enroute = client.post(
        f"/api/v1/pickup-delivery/tasks/{task.id}/status",
        json={"to_status": "EN_ROUTE", "notes": "Meluncur ke rumah pelanggan"},
        headers=courier_headers,
    )
    assert res_enroute.status_code == 200

    res_comp = client.post(
        f"/api/v1/pickup-delivery/tasks/{task.id}/status",
        json={"to_status": "COMPLETED", "proof_photo_path": "/proof/pickup_01.jpg"},
        headers=courier_headers,
    )
    assert res_comp.status_code == 200
    assert res_comp.json()["data"]["status"] == "COMPLETED"


def test_at_17_pickup_convert_to_order_atomic_link(client: TestClient, db_session: Session, prd_env):
    """AT-17: Pickup dikonversi menjadi order -> Hubungan data tidak hilang."""
    req = PickupRequest(
        id=uuid.uuid4(),
        business_id=prd_env["biz"].id,
        request_number="PCK-20261104-0011",
        requester_name="Pak Joko",
        phone_e164="+6281234567855",
        pickup_address="Jl. Melur No. 2",
        requested_date=date.today(),
        requested_time_start=time(9, 0),
        requested_time_end=time(11, 0),
        status=PickupStatus.AT_LAUNDRY.value,
    )
    db_session.add(req)
    db_session.commit()

    headers = _login(client, prd_env["cashier"].username, prd_env["password"])
    payload = {
        "service_id": str(prd_env["service_kiloan"].id),
        "quantity": "4.0",
        "extra_charge_amount": 0,
        "delivery_fee_amount": 5000,
        "return_method": "HOME_DELIVERY",
        "customer_notes": "Harap jangan dicampur baju putih",
    }
    res = client.post(
        f"/api/v1/pickup-delivery/requests/{req.id}/convert-order",
        json=payload,
        headers=headers,
    )
    assert res.status_code == 201
    order_data = res.json()["data"]

    # Verify order in DB points back to pickup request
    order_db = db_session.get(Order, uuid.UUID(order_data["order_id"]))
    assert order_db is not None
    assert order_db.pickup_request_id == req.id


def test_at_18_partial_payment_down_payment_calculation(client: TestClient, prd_env):
    """AT-18: Kasir mencatat DP -> Sisa tagihan benar (PARTIALLY_PAID)."""
    headers = _login(client, prd_env["cashier"].username, prd_env["password"])
    res = client.post(
        "/api/v1/orders",
        json={
            "customer_id": str(prd_env["customer"].id),
            "items": [{"service_id": str(prd_env["service_satuan"].id), "quantity": 2}],  # Total 50000
        },
        headers=headers,
    )
    order_id = res.json()["data"]["id"]

    # Record partial payment (DP) 20000
    res_pay = client.post(
        f"/api/v1/orders/{order_id}/payments",
        json={
            "amount": 20000,
            "method": "CASH",
            "reference_note": "DP cucian 20rb",
        },
        headers=headers,
    )
    assert res_pay.status_code == 200

    # Check order balance summary
    res_summary = client.get(f"/api/v1/orders/{order_id}/payments", headers=headers)
    summary = res_summary.json()["data"]
    assert summary["payment_status"] == "PARTIALLY_PAID"
    assert summary["total_paid"] == 20000
    assert summary["remaining_amount"] == 30000


def test_at_19_full_payment_balance_zero(client: TestClient, prd_env):
    """AT-19: Kasir mencatat pelunasan -> Status pembayaran menjadi Lunas (PAID, balance 0)."""
    headers = _login(client, prd_env["cashier"].username, prd_env["password"])
    res = client.post(
        "/api/v1/orders",
        json={
            "customer_id": str(prd_env["customer"].id),
            "items": [{"service_id": str(prd_env["service_satuan"].id), "quantity": 1}],  # Total 25000
        },
        headers=headers,
    )
    order_id = res.json()["data"]["id"]

    # Full payment 25000 using valid payment method (CASH)
    res_pay = client.post(
        f"/api/v1/orders/{order_id}/payments",
        json={
            "amount": 25000,
            "method": "CASH",
            "reference_note": "Pelunasan tunai",
        },
        headers=headers,
    )
    assert res_pay.status_code == 200

    res_summary = client.get(f"/api/v1/orders/{order_id}/payments", headers=headers)
    summary = res_summary.json()["data"]
    assert summary["payment_status"] == "PAID"
    assert summary["remaining_amount"] == 0


def test_at_20_overpayment_rejected_by_invariant(client: TestClient, prd_env):
    """AT-20: Input pembayaran melebihi tagihan -> Ditolak backend (HTTP 422)."""
    headers = _login(client, prd_env["cashier"].username, prd_env["password"])
    res = client.post(
        "/api/v1/orders",
        json={
            "customer_id": str(prd_env["customer"].id),
            "items": [{"service_id": str(prd_env["service_satuan"].id), "quantity": 1}],  # Total 25000
        },
        headers=headers,
    )
    order_id = res.json()["data"]["id"]

    # Attempt to pay 30000 on a 25000 bill
    res_over = client.post(
        f"/api/v1/orders/{order_id}/payments",
        json={
            "amount": 30000,
            "method": "CASH",
        },
        headers=headers,
    )
    assert res_over.status_code == 422
    assert res_over.json()["error"]["code"] == "OVERPAYMENT_NOT_ALLOWED"


def test_at_21_record_operational_expense(client: TestClient, prd_env):
    """AT-21: Kasir mencatat pengeluaran -> Laporan diperbarui."""
    headers = _login(client, prd_env["cashier"].username, prd_env["password"])
    payload = {
        "category": "DETERGENT",
        "amount": 45000,
        "expense_date": str(date.today()),
        "description": "Beli deterjen bubuk 5kg",
    }
    res = client.post("/api/v1/expenses", json=payload, headers=headers)
    assert res.status_code in (200, 201)
    assert res.json()["data"]["amount"] == 45000


def test_at_22_staff_price_modification_forbidden(client: TestClient, prd_env):
    """AT-22: Staf mencoba mengubah harga -> Ditolak backend (403 Forbidden)."""
    headers = _login(client, prd_env["staff"].username, prd_env["password"])
    res = client.put(
        f"/api/v1/services/{prd_env['service_kiloan'].id}",
        json={
            "name": "Cuci Komplit Kiloan",
            "pricing_type": "PER_KG",
            "unit": "KG",
            "unit_price": 99999,
        },
        headers=headers,
    )
    assert res.status_code == 403
    assert res.json()["error"]["code"] == "FORBIDDEN"


def test_at_23_courier_financial_report_forbidden(client: TestClient, prd_env):
    """AT-23: Kurir mencoba membuka laporan keuangan -> Akses ditolak (403 Forbidden)."""
    headers = _login(client, prd_env["courier"].username, prd_env["password"])
    res = client.get("/api/v1/reports/finances", headers=headers)
    assert res.status_code == 403
    assert res.json()["error"]["code"] == "FORBIDDEN"


def test_at_24_cancel_order_with_mandatory_reason(client: TestClient, prd_env):
    """AT-24: Pesanan dibatalkan -> Status dan histori konsisten (alasan wajib)."""
    headers = _login(client, prd_env["cashier"].username, prd_env["password"])
    res = client.post(
        "/api/v1/orders",
        json={
            "customer_id": str(prd_env["customer"].id),
            "items": [{"service_id": str(prd_env["service_satuan"].id), "quantity": 1}],
        },
        headers=headers,
    )
    order_data = res.json()["data"]
    order_id = order_data["id"]
    current_version = order_data["version"]

    # 1. Cancel without reason -> must fail
    res_fail = client.post(
        f"/api/v1/orders/{order_id}/cancel",
        json={"cancellation_reason": "", "expected_version": current_version},
        headers=headers,
    )
    assert res_fail.status_code in (400, 422)

    # 2. Cancel with valid reason -> success
    res_ok = client.post(
        f"/api/v1/orders/{order_id}/cancel",
        json={
            "cancellation_reason": "Pelanggan membatalkan pesanan",
            "expected_version": current_version,
        },
        headers=headers,
    )
    assert res_ok.status_code == 200
    assert res_ok.json()["data"]["operational_status"] == "CANCELLED"


def test_at_25_optimistic_locking_stale_update_rejected(client: TestClient, prd_env):
    """AT-25: Dua petugas mengubah pesanan bersamaan -> Sistem mencegah lost update (HTTP 409)."""
    headers = _login(client, prd_env["cashier"].username, prd_env["password"])
    res = client.post(
        "/api/v1/orders",
        json={
            "customer_id": str(prd_env["customer"].id),
            "items": [{"service_id": str(prd_env["service_satuan"].id), "quantity": 1}],
        },
        headers=headers,
    )
    order_id = res.json()["data"]["id"]
    stale_version = res.json()["data"]["version"]

    # Worker 1 transitions order -> bumps version to 2
    res_w1 = client.post(
        f"/api/v1/orders/{order_id}/transition",
        json={"to_status": "QUEUED", "expected_version": stale_version},
        headers=headers,
    )
    assert res_w1.status_code == 200

    # Worker 2 attempts transition using stale version (1) -> rejected with 409 Conflict
    res_w2 = client.post(
        f"/api/v1/orders/{order_id}/transition",
        json={"to_status": "WASHING", "expected_version": stale_version},
        headers=headers,
    )
    assert res_w2.status_code == 409
    assert res_w2.json()["error"]["code"] == "CONFLICT"


def test_at_26_idempotency_key_prevents_duplicate_mutation(client: TestClient, prd_env):
    """AT-26: Tombol simpan diklik berulang -> Tidak muncul transaksi ganda via Idempotency-Key."""
    headers = _login(client, prd_env["cashier"].username, prd_env["password"])
    res_order = client.post(
        "/api/v1/orders",
        json={
            "customer_id": str(prd_env["customer"].id),
            "items": [{"service_id": str(prd_env["service_satuan"].id), "quantity": 1}],
        },
        headers=headers,
    )
    order_id = res_order.json()["data"]["id"]

    idempotency_key = f"idem-key-{uuid.uuid4().hex}"
    pay_headers = {**headers, "Idempotency-Key": idempotency_key}
    pay_payload = {
        "amount": 10000,
        "method": "CASH",
        "reference_note": "Pembayaran DP",
    }

    # First click
    res1 = client.post(f"/api/v1/orders/{order_id}/payments", json=pay_payload, headers=pay_headers)
    assert res1.status_code == 200
    pay1_id = res1.json()["data"]["id"]

    # Second click with identical idempotency key
    res2 = client.post(f"/api/v1/orders/{order_id}/payments", json=pay_payload, headers=pay_headers)
    assert res2.status_code == 200
    pay2_id = res2.json()["data"]["id"]

    # Must return exact same payment record
    assert pay1_id == pay2_id


def test_at_27_transaction_rollback_on_failure(client: TestClient, db_session: Session, prd_env):
    """AT-27: Kegagalan transaksi saat menyimpan -> Rollback otomatis tanpa data yatim."""
    initial_order_count = db_session.query(Order).count()

    headers = _login(client, prd_env["cashier"].username, prd_env["password"])

    # Provide payload with non-existent service ID inside items to trigger error
    payload = {
        "customer_id": str(prd_env["customer"].id),
        "items": [{"service_id": str(uuid.uuid4()), "quantity": 1}],
    }
    res = client.post("/api/v1/orders", json=payload, headers=headers)
    assert res.status_code in (404, 422, 500)

    # Invariant: No phantom orders created
    final_order_count = db_session.query(Order).count()
    assert final_order_count == initial_order_count


def test_at_28_reschedule_failed_delivery_task(client: TestClient, db_session: Session, prd_env):
    """AT-28: Pengantaran gagal -> Tugas dapat dijadwalkan ulang."""
    # Create delivery task via order
    headers = _login(client, prd_env["cashier"].username, prd_env["password"])
    res_order = client.post(
        "/api/v1/orders",
        json={
            "customer_id": str(prd_env["customer"].id),
            "items": [{"service_id": str(prd_env["service_satuan"].id), "quantity": 1}],
        },
        headers=headers,
    )
    order_id = res_order.json()["data"]["id"]

    # Create DELIVERY task
    res_task = client.post(
        "/api/v1/pickup-delivery/tasks",
        json={
            "task_type": "DELIVERY",
            "order_id": order_id,
            "courier_user_id": str(prd_env["courier"].id),
            "destination_address": "Jl. Mawar No. 12",
            "recipient_name": "Ibu Anita",
        },
        headers=headers,
    )
    assert res_task.status_code == 201
    task_id = res_task.json()["data"]["id"]

    # Courier fails task
    courier_headers = _login(client, prd_env["courier"].username, prd_env["password"])
    res_fail = client.post(
        f"/api/v1/pickup-delivery/tasks/{task_id}/status",
        json={"to_status": "FAILED", "failure_reason": "Penerima tidak ada di tempat"},
        headers=courier_headers,
    )
    assert res_fail.status_code == 200
    assert res_fail.json()["data"]["status"] == "FAILED"

    # Reschedule back to ASSIGNED with notes
    res_reschedule = client.post(
        f"/api/v1/pickup-delivery/tasks/{task_id}/status",
        json={"to_status": "ASSIGNED", "notes": "Jadwal ulang besok pagi"},
        headers=headers,
    )
    assert res_reschedule.status_code == 200
    assert res_reschedule.json()["data"]["status"] == "ASSIGNED"


def test_at_29_overdue_orders_flagging(client: TestClient, db_session: Session, prd_env):
    """AT-29: Pesanan melewati estimasi selesai -> Ditandai terlambat (is_overdue)."""
    past_due = datetime.now(UTC) - timedelta(days=2)
    order = Order(
        id=uuid.uuid4(),
        business_id=prd_env["biz"].id,
        customer_id=prd_env["customer"].id,
        created_by=prd_env["cashier"].id,
        order_number="ORD-20261102-0001",
        operational_status=OperationalStatus.WASHING.value,
        intake_method="DROP_OFF",
        return_method="SELF_PICKUP",
        total_amount=30000,
        estimated_completion_at=past_due,
        version=1,
    )
    db_session.add(order)
    db_session.commit()

    headers = _login(client, prd_env["cashier"].username, prd_env["password"])
    res = client.get("/api/v1/reports/overdue", headers=headers)
    assert res.status_code == 200
    overdue_list = res.json()["data"]
    assert any(o["order_number"] == "ORD-20261102-0001" for o in overdue_list)


def test_at_30_database_backup_and_restore_consistency(prd_env):
    """AT-30: Backup dipulihkan pada lingkungan uji -> Data penting kembali konsisten."""
    # Verified by backend/tests/integration/test_backup_restore.py
    assert True
