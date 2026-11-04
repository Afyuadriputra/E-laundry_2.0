"""
Standalone Seed Script for E-Laundry 2.0.
Populates all 19 core tables (BSD §6.1) with rich, realistic Indonesian UMKM laundry data.
Uses Faker ('id_ID') and respects all domain pricing, state machine, and balance invariants.
"""
# ruff: noqa: E402

from __future__ import annotations

import argparse
import hashlib
import random
import secrets
import sys
import uuid
from datetime import UTC, datetime, time, timedelta
from decimal import Decimal
from pathlib import Path

# Ensure backend root is on sys.path
backend_dir = Path(__file__).resolve().parent.parent
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

# Ensure stdout can handle utf-8 if possible
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

from faker import Faker
from sqlalchemy import create_engine, event, select, text
from sqlalchemy.orm import Session, sessionmaker

# Import all SQLAlchemy models through registry to guarantee metadata awareness
from app.core.config import settings
from app.core.security import hash_password
from app.db.base import Base
from app.modules.audit.models import AuditLog
from app.modules.auth.models import UserSession
from app.modules.businesses.models import Business, BusinessSettings
from app.modules.customers.models import Customer
from app.modules.expenses.models import Expense
from app.modules.idempotency.models import IdempotencyRecord
from app.modules.orders.domain.pricing import PricingEngine
from app.modules.orders.models import Order, OrderHandoff, OrderItem, OrderStatusHistory
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
from app.modules.users.models import User, UserRole

# Seed Faker for reproducible deterministic generation
fake = Faker("id_ID")
Faker.seed(42)
random.seed(42)


def clean_existing_data(db: Session, engine) -> None:
    """Purges data from all 19 tables in reverse dependency order."""
    print("[*] Cleaning existing seed data across all 19 tables...")
    table_order = [
        "audit_logs",
        "payment_voids",
        "payments",
        "order_handoffs",
        "delivery_status_history",
        "delivery_tasks",
        "tracking_tokens",
        "order_status_history",
        "order_items",
        "orders",
        "pickup_requests",
        "idempotency_records",
        "expenses",
        "services",
        "customers",
        "user_sessions",
        "users",
        "business_settings",
        "businesses",
    ]

    is_sqlite = engine.url.drivername.startswith("sqlite")
    if is_sqlite:
        db.execute(text("PRAGMA foreign_keys = OFF;"))
        for table in table_order:
            try:
                db.execute(text(f"DELETE FROM {table};"))
            except Exception as e:
                print(f"   [Note] Table {table} clean skipped: {e}")
        db.execute(text("PRAGMA foreign_keys = ON;"))
    else:
        for table in table_order:
            try:
                db.execute(text(f"TRUNCATE TABLE {table} CASCADE;"))
            except Exception as e:
                print(f"   [Note] Table {table} truncate skipped: {e}")
    db.commit()
    print("   [+] Clean complete.")


def seed_database(db: Session, customer_count: int = 30, order_count: int = 50) -> dict[str, int]:
    """Inserts realistic Indonesian laundry dummy data into all 19 tables."""
    counts: dict[str, int] = {}
    now = datetime.now(UTC)

    # -------------------------------------------------------------
    # 1. businesses (Table 1)
    # -------------------------------------------------------------
    print("[+] 1. Seeding businesses...")
    business = Business(
        id=uuid.uuid4(),
        name="Kawan Laundry Express",
        phone_e164="+6281234567890",
        address="Jl. Fatmawati Raya No. 45, Cilandak Barat, Jakarta Selatan",
        timezone="Asia/Jakarta",
        is_active=True,
    )
    db.add(business)
    db.flush()
    counts["businesses"] = 1

    # -------------------------------------------------------------
    # 2. business_settings (Table 2)
    # -------------------------------------------------------------
    print("[+] 2. Seeding business_settings...")
    settings_obj = BusinessSettings(
        id=uuid.uuid4(),
        business_id=business.id,
        pickup_enabled=True,
        delivery_enabled=True,
        default_delivery_fee=10000,
        default_completion_hours=48,
        weight_precision=1,
        weight_rounding_mode="HALF_UP",
        operating_hours={"monday_friday": "08:00 - 21:00", "saturday_sunday": "08:00 - 20:00"},
    )
    db.add(settings_obj)
    db.flush()
    counts["business_settings"] = 1

    # -------------------------------------------------------------
    # 3. users (Table 3)
    # -------------------------------------------------------------
    print("[+] 3. Seeding users (Owner, Cashiers, Couriers)...")
    user_definitions = [
        ("owner", "Budi Setiawan", UserRole.OWNER.value, "+628111222333", "Owner123!"),
        ("kasir_ani", "Ani Wijaya", UserRole.CASHIER.value, "+628123456781", "Kasir123!"),
        ("kasir_budi", "Budi Prasetyo", UserRole.CASHIER.value, "+628123456782", "Kasir123!"),
        ("kurir_doni", "Doni Hermawan", UserRole.COURIER.value, "+628123456783", "Kurir123!"),
        ("kurir_agus", "Agus Santoso", UserRole.COURIER.value, "+628123456784", "Kurir123!"),
    ]
    users_dict: dict[str, User] = {}
    for username, full_name, role, phone, raw_pwd in user_definitions:
        pwd_hash = hash_password(raw_pwd)
        user_entity = User(
            id=uuid.uuid4(),
            business_id=business.id,
            username=username,
            full_name=full_name,
            role=role,
            phone_e164=phone,
            password_hash=pwd_hash,
            is_active=True,
        )
        db.add(user_entity)
        users_dict[username] = user_entity
    db.flush()
    counts["users"] = len(users_dict)

    owner_user = users_dict["owner"]
    cashiers = [users_dict["kasir_ani"], users_dict["kasir_budi"]]
    couriers = [users_dict["kurir_doni"], users_dict["kurir_agus"]]

    # -------------------------------------------------------------
    # 4. user_sessions (Table 4)
    # -------------------------------------------------------------
    print("[+] 4. Seeding user_sessions...")
    sessions_count = 0
    for usr in users_dict.values():
        token_plain = secrets.token_hex(32)
        sess = UserSession(
            id=uuid.uuid4(),
            user_id=usr.id,
            session_token_hash=hashlib.sha256(token_plain.encode()).hexdigest(),
            created_at=now - timedelta(hours=random.randint(1, 24)),
            last_activity_at=now - timedelta(minutes=random.randint(5, 60)),
            expires_at=now + timedelta(days=7),
            absolute_expires_at=now + timedelta(days=30),
            revoked_at=None,
            user_agent_summary="Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/130.0",
        )
        db.add(sess)
        sessions_count += 1
    db.flush()
    counts["user_sessions"] = sessions_count

    # -------------------------------------------------------------
    # 5. customers (Table 5)
    # -------------------------------------------------------------
    print(f"[+] 5. Seeding {customer_count} customers...")
    customer_notes_pool = [
        "Pisahkan pakaian warna putih.",
        "Gunakan softener aroma Sakura.",
        "Setrika ekstra licin bagian kemeja kerja.",
        "Jangan menggunakan sikat kasar pada celana jeans.",
        "Packing plastik per 2 setel pakaian.",
        "Parfum Ocean Fresh, jangan terlalu menyengat.",
        "Mohon hubungi WhatsApp sebelum pengantaran.",
        "Pelanggan langganan kos-kosan dekat outlet.",
        "Pakaian kantor mohon diberi gantungan / hanger.",
        None,
    ]
    customers: list[Customer] = []
    for _ in range(customer_count):
        first = fake.first_name()
        last = fake.last_name()
        name = f"{first} {last}"
        phone = f"+628{random.randint(11, 99)}{random.randint(1000000, 9999999)}"
        street = fake.street_address()
        district = fake.city()
        full_address = f"{street}, {district}"
        note = random.choice(customer_notes_pool)

        cust = Customer(
            id=uuid.uuid4(),
            business_id=business.id,
            full_name=name,
            phone_e164=phone,
            address=full_address,
            notes=note,
            is_active=True,
            created_at=now - timedelta(days=random.randint(5, 60)),
        )
        db.add(cust)
        customers.append(cust)
    db.flush()
    counts["customers"] = len(customers)

    # -------------------------------------------------------------
    # 6. services (Table 6)
    # -------------------------------------------------------------
    print("[+] 6. Seeding services catalog...")
    service_defs = [
        # Kiloan
        ("Cuci Komplit Reguler", "PER_KG", "KG", 8000, 48, True),
        ("Cuci Kering Lipat", "PER_KG", "KG", 6000, 24, False),
        ("Cuci Express 6 Jam", "PER_KG", "KG", 15000, 6, True),
        ("Cuci Express 24 Jam", "PER_KG", "KG", 12000, 24, True),
        ("Setrika Saja", "PER_KG", "KG", 5000, 24, True),
        # Satuan
        ("Bed Cover King / Queen", "PER_ITEM", "PCS", 35000, 48, True),
        ("Bed Cover Single", "PER_ITEM", "PCS", 25000, 48, True),
        ("Selimut Tebal", "PER_ITEM", "PCS", 20000, 48, True),
        ("Sprei Set", "PER_ITEM", "PCS", 15000, 24, True),
        ("Boneka Besar", "PER_ITEM", "PCS", 25000, 48, False),
        ("Boneka Kecil", "PER_ITEM", "PCS", 10000, 24, False),
        ("Jas / Blazer Kantor", "PER_ITEM", "PCS", 30000, 48, True),
        ("Sepatu Sneaker", "PER_ITEM", "PCS", 35000, 72, False),
        # Satuan Tambahan
        ("Gorden / Vitrase Tipis", "PER_ITEM", "PCS", 18000, 48, True),
        ("Karpet Tebal", "PER_ITEM", "PCS", 45000, 72, False),
    ]
    services: list[Service] = []
    for name, ptype, unit, price, est_hours, req_iron in service_defs:
        srv = Service(
            id=uuid.uuid4(),
            business_id=business.id,
            name=name,
            pricing_type=ptype,
            unit=unit,
            unit_price=price,
            estimated_hours=est_hours,
            requires_ironing=req_iron,
            is_active=True,
            version=1,
            created_at=now - timedelta(days=60),
        )
        db.add(srv)
        services.append(srv)
    db.flush()
    counts["services"] = len(services)

    # -------------------------------------------------------------
    # 7. pickup_requests (Table 7)
    # -------------------------------------------------------------
    print("[+] 7. Seeding pickup_requests...")
    pickup_requests: list[PickupRequest] = []
    pickup_statuses = [
        PickupStatus.REQUESTED.value,
        PickupStatus.ASSIGNED.value,
        PickupStatus.PICKED_UP.value,
        PickupStatus.CONVERTED.value,
    ]
    for i in range(12):
        cust = random.choice(customers)
        status_choice = pickup_statuses[i % len(pickup_statuses)]
        req_date = (now - timedelta(days=random.randint(0, 7))).date()
        req_num = f"REQ-PKP-{(now.strftime('%Y%m%d'))}-{i+1:04d}"

        pkp = PickupRequest(
            id=uuid.uuid4(),
            business_id=business.id,
            customer_id=cust.id,
            request_number=req_num,
            requester_name=cust.full_name,
            phone_e164=cust.phone_e164,
            pickup_address=cust.address or "Jl. Kemang Raya No. 12, Jakarta Selatan",
            requested_date=req_date,
            requested_time_start=time(9, 0),
            requested_time_end=time(12, 0),
            status=status_choice,
            notes=random.choice(["Tolong ambil pagi sebelum jam 10", "Titip di pos satpam bila tidak ada orang", None]),
            created_at=now - timedelta(days=random.randint(1, 5)),
        )
        db.add(pkp)
        pickup_requests.append(pkp)
    db.flush()
    counts["pickup_requests"] = len(pickup_requests)

    # -------------------------------------------------------------
    # 8. orders (Table 8) & 9. order_items (Table 9) & 10. order_status_history (Table 10)
    # -------------------------------------------------------------
    print(f"[+] 8-10. Seeding {order_count} orders, items, and status progression...")
    orders: list[Order] = []
    order_items_total = 0
    status_history_total = 0

    order_status_distribution = [
        ("RECEIVED", 5),
        ("QUEUED", 5),
        ("WASHING", 6),
        ("DRYING", 6),
        ("IRONING", 6),
        ("QC_PACKING", 6),
        ("READY", 8),
        ("COMPLETED", 6),
        ("CANCELLED", 2),
    ]

    expanded_statuses: list[str] = []
    for st, count in order_status_distribution:
        expanded_statuses.extend([st] * count)
    random.shuffle(expanded_statuses)

    standard_forward_steps = [
        "RECEIVED",
        "QUEUED",
        "WASHING",
        "DRYING",
        "IRONING",
        "QC_PACKING",
        "READY",
        "COMPLETED",
    ]

    for idx in range(order_count):
        cust = random.choice(customers)
        cashier = random.choice(cashiers)
        target_status = expanded_statuses[idx % len(expanded_statuses)]

        intake_method = "PICKUP" if idx < 12 else "DROP_OFF"
        return_method = "DELIVERY" if idx % 3 == 0 else "SELF_PICKUP"

        linked_pickup_id = None
        if intake_method == "PICKUP" and idx < len(pickup_requests):
            pkp_candidate = pickup_requests[idx]
            if pkp_candidate.status == PickupStatus.CONVERTED.value:
                linked_pickup_id = pkp_candidate.id

        order_num = f"ORD-{(now - timedelta(days=idx // 8)).strftime('%Y%m%d')}-{idx+1:04d}"
        created_time = now - timedelta(days=random.randint(1, 14), hours=random.randint(1, 10))
        estimated_finish = created_time + timedelta(hours=48)

        order_entity = Order(
            id=uuid.uuid4(),
            business_id=business.id,
            order_number=order_num,
            customer_id=cust.id,
            pickup_request_id=linked_pickup_id,
            created_by=cashier.id,
            operational_status=target_status,
            intake_method=intake_method,
            return_method=return_method,
            subtotal_amount=0,
            extra_charge_amount=0,
            delivery_fee_amount=10000 if return_method == "DELIVERY" else 0,
            total_amount=0,
            estimated_completion_at=estimated_finish,
            customer_notes=cust.notes,
            internal_notes="Proses sesuai SOP kebersihan standar" if idx % 4 == 0 else None,
            version=1,
            created_at=created_time,
            updated_at=created_time,
        )

        if target_status == "COMPLETED":
            order_entity.completed_at = created_time + timedelta(hours=40)
        elif target_status == "CANCELLED":
            order_entity.cancelled_at = created_time + timedelta(hours=2)
            order_entity.cancellation_reason = "Batal mencuci atas permintaan pelanggan (perubahan rencana perjalanan)."

        db.add(order_entity)
        db.flush()

        item_count = random.randint(1, 3)
        chosen_services = random.sample(services, item_count)
        order_subtotal = 0

        for srv in chosen_services:
            if srv.pricing_type == "PER_KG":
                raw_weight = Decimal(str(round(random.uniform(2.5, 7.8), 2)))
                line_res = PricingEngine.calculate_line_item(
                    pricing_type="PER_KG",
                    quantity=raw_weight,
                    unit_price=srv.unit_price,
                )
                item_qty = line_res.billable_quantity
                item_line_total = line_res.line_total
            elif srv.pricing_type == "PER_METER":
                item_qty = Decimal(str(random.randint(3, 10)))
                item_line_total = int(item_qty * srv.unit_price)
            else:  # PER_ITEM
                item_qty = Decimal(str(random.randint(1, 3)))
                item_line_total = int(item_qty * srv.unit_price)

            order_subtotal += item_line_total
            order_item = OrderItem(
                id=uuid.uuid4(),
                order_id=order_entity.id,
                service_id=srv.id,
                service_name_snapshot=srv.name,
                pricing_type_snapshot=srv.pricing_type,
                unit_snapshot=srv.unit,
                quantity=item_qty,
                unit_price_snapshot=srv.unit_price,
                line_total_amount=item_line_total,
                requires_ironing_snapshot=srv.requires_ironing,
                created_at=created_time,
            )
            db.add(order_item)
            order_items_total += 1

        order_entity.subtotal_amount = order_subtotal
        order_entity.total_amount = order_subtotal + order_entity.delivery_fee_amount

        if target_status == "CANCELLED":
            db.add(
                OrderStatusHistory(
                    id=uuid.uuid4(),
                    order_id=order_entity.id,
                    from_status=None,
                    to_status="RECEIVED",
                    changed_by=cashier.id,
                    reason="Pesanan diterima di kasir",
                    created_at=created_time,
                )
            )
            status_history_total += 1
            db.add(
                OrderStatusHistory(
                    id=uuid.uuid4(),
                    order_id=order_entity.id,
                    from_status="RECEIVED",
                    to_status="CANCELLED",
                    changed_by=cashier.id,
                    reason=order_entity.cancellation_reason,
                    created_at=created_time + timedelta(hours=2),
                )
            )
            status_history_total += 1
        else:
            target_idx = standard_forward_steps.index(target_status)
            for s_idx in range(target_idx + 1):
                st_name = standard_forward_steps[s_idx]
                prev_st = standard_forward_steps[s_idx - 1] if s_idx > 0 else None
                history_entry = OrderStatusHistory(
                    id=uuid.uuid4(),
                    order_id=order_entity.id,
                    from_status=prev_st,
                    to_status=st_name,
                    changed_by=cashier.id,
                    reason=f"Status diperbarui ke {st_name}",
                    created_at=created_time + timedelta(hours=s_idx * 4),
                )
                db.add(history_entry)
                status_history_total += 1

        orders.append(order_entity)

    db.flush()
    counts["orders"] = len(orders)
    counts["order_items"] = order_items_total
    counts["order_status_history"] = status_history_total

    # -------------------------------------------------------------
    # 11. order_handoffs (Table 11)
    # -------------------------------------------------------------
    print("[+] 11. Seeding order_handoffs...")
    handoff_count = 0
    for ord_obj in orders:
        if ord_obj.operational_status in ("READY", "COMPLETED"):
            handoff = OrderHandoff(
                id=uuid.uuid4(),
                order_id=ord_obj.id,
                delivery_task_id=None,
                handoff_method="DIRECT_CUSTOMER" if ord_obj.return_method == "SELF_PICKUP" else "COURIER_DROP",
                received_by_name=ord_obj.customer.full_name,
                confirmed_by_user_id=random.choice(cashiers).id,
                confirmed_at=ord_obj.created_at + timedelta(hours=38),
                notes="Pakaian diserahkan dalam kondisi rapi dan wangi.",
                created_at=ord_obj.created_at + timedelta(hours=38),
            )
            db.add(handoff)
            handoff_count += 1
    db.flush()
    counts["order_handoffs"] = handoff_count

    # -------------------------------------------------------------
    # 12. delivery_tasks (Table 12) & 13. delivery_status_history (Table 13)
    # -------------------------------------------------------------
    print("[+] 12-13. Seeding delivery_tasks & status history (chk_delivery_tasks_type_target)...")
    delivery_tasks_count = 0
    delivery_history_count = 0

    # 12a. Pickup tasks (task_type = 'PICKUP', order_id IS NULL, pickup_request_id IS NOT NULL)
    for pkp in pickup_requests:
        courier = random.choice(couriers)
        creator = random.choice(cashiers)
        task_st = DeliveryTaskStatus.COMPLETED.value if pkp.status in (PickupStatus.PICKED_UP.value, PickupStatus.CONVERTED.value) else DeliveryTaskStatus.ASSIGNED.value

        dt_pickup = DeliveryTask(
            id=uuid.uuid4(),
            business_id=business.id,
            task_type=DeliveryTaskType.PICKUP.value,
            pickup_request_id=pkp.id,
            order_id=None,  # STRICT invariant
            courier_user_id=courier.id,
            scheduled_start_at=now - timedelta(hours=8),
            scheduled_end_at=now - timedelta(hours=5),
            status=task_st,
            recipient_name=pkp.requester_name,
            destination_address=pkp.pickup_address,
            destination_phone=pkp.phone_e164,
            completed_at=now - timedelta(hours=5) if task_st == DeliveryTaskStatus.COMPLETED.value else None,
            created_by=creator.id,
            created_at=now - timedelta(hours=10),
        )
        db.add(dt_pickup)
        db.flush()
        delivery_tasks_count += 1

        hist_1 = DeliveryStatusHistory(
            id=uuid.uuid4(),
            delivery_task_id=dt_pickup.id,
            from_status=None,
            to_status=DeliveryTaskStatus.ASSIGNED.value,
            reason="Tugas penjemputan ditugaskan ke kurir",
            changed_by=creator.id,
            created_at=dt_pickup.created_at,
        )
        db.add(hist_1)
        delivery_history_count += 1

        if task_st == DeliveryTaskStatus.COMPLETED.value:
            hist_2 = DeliveryStatusHistory(
                id=uuid.uuid4(),
                delivery_task_id=dt_pickup.id,
                from_status=DeliveryTaskStatus.ASSIGNED.value,
                to_status=DeliveryTaskStatus.COMPLETED.value,
                reason="Laundry berhasil diambil dari lokasi pelanggan",
                changed_by=courier.id,
                created_at=dt_pickup.completed_at,
            )
            db.add(hist_2)
            delivery_history_count += 1

    # 12b. Delivery tasks (task_type = 'DELIVERY', pickup_request_id IS NULL, order_id IS NOT NULL)
    delivery_eligible_orders = [o for o in orders if o.return_method == "DELIVERY"]
    for ord_obj in delivery_eligible_orders:
        courier = random.choice(couriers)
        creator = random.choice(cashiers)
        task_st = DeliveryTaskStatus.COMPLETED.value if ord_obj.operational_status == "COMPLETED" else DeliveryTaskStatus.EN_ROUTE.value

        dt_delivery = DeliveryTask(
            id=uuid.uuid4(),
            business_id=business.id,
            task_type=DeliveryTaskType.DELIVERY.value,
            pickup_request_id=None,  # STRICT invariant
            order_id=ord_obj.id,
            courier_user_id=courier.id,
            scheduled_start_at=ord_obj.created_at + timedelta(hours=30),
            scheduled_end_at=ord_obj.created_at + timedelta(hours=34),
            status=task_st,
            recipient_name=ord_obj.customer.full_name,
            destination_address=ord_obj.customer.address or "Alamat Pelanggan",
            destination_phone=ord_obj.customer.phone_e164,
            completed_at=ord_obj.created_at + timedelta(hours=34) if task_st == DeliveryTaskStatus.COMPLETED.value else None,
            created_by=creator.id,
            created_at=ord_obj.created_at + timedelta(hours=28),
        )
        db.add(dt_delivery)
        db.flush()
        delivery_tasks_count += 1

        d_hist = DeliveryStatusHistory(
            id=uuid.uuid4(),
            delivery_task_id=dt_delivery.id,
            from_status=None,
            to_status=task_st,
            reason=f"Pengantaran berstatus {task_st}",
            changed_by=courier.id,
            created_at=dt_delivery.created_at,
        )
        db.add(d_hist)
        delivery_history_count += 1

    db.flush()
    counts["delivery_tasks"] = delivery_tasks_count
    counts["delivery_status_history"] = delivery_history_count

    # -------------------------------------------------------------
    # 14. tracking_tokens (Table 14)
    # -------------------------------------------------------------
    print("[+] 14. Seeding tracking_tokens...")
    tokens_count = 0
    for ord_obj in orders:
        raw_token = f"trk_ord_{secrets.token_urlsafe(24)}"
        t_hash = hashlib.sha256(raw_token.encode()).hexdigest()
        tok = TrackingToken(
            id=uuid.uuid4(),
            order_id=ord_obj.id,
            pickup_request_id=None,
            token_hash=t_hash,
            expires_at=now + timedelta(days=90),
            revoked_at=None,
            created_by=ord_obj.created_by,
            created_at=ord_obj.created_at,
        )
        db.add(tok)
        tokens_count += 1

    for pkp in pickup_requests:
        raw_token = f"trk_pkp_{secrets.token_urlsafe(24)}"
        t_hash = hashlib.sha256(raw_token.encode()).hexdigest()
        tok = TrackingToken(
            id=uuid.uuid4(),
            order_id=None,
            pickup_request_id=pkp.id,
            token_hash=t_hash,
            expires_at=now + timedelta(days=30),
            revoked_at=None,
            created_by=None,
            created_at=pkp.created_at,
        )
        db.add(tok)
        tokens_count += 1

    db.flush()
    counts["tracking_tokens"] = tokens_count

    # -------------------------------------------------------------
    # 15. payments (Table 15) & 16. payment_voids (Table 16)
    # -------------------------------------------------------------
    print("[+] 15-16. Seeding payments & payment voids...")
    payment_methods = ["CASH", "BANK_TRANSFER", "QRIS_MANUAL"]
    payments_count = 0
    voids_count = 0
    payment_to_void: Payment | None = None

    for idx, ord_obj in enumerate(orders):
        if ord_obj.operational_status == "CANCELLED":
            continue

        cashier = random.choice(cashiers)
        method = payment_methods[idx % len(payment_methods)]

        if ord_obj.operational_status == "COMPLETED" or idx % 3 == 0:
            pmt = Payment(
                id=uuid.uuid4(),
                order_id=ord_obj.id,
                amount=ord_obj.total_amount,
                method=method,
                verification_status="VERIFIED",
                payment_time=ord_obj.created_at + timedelta(minutes=10),
                verified_by=cashier.id,
                verified_at=ord_obj.created_at + timedelta(minutes=10),
                reference_note="Pelunasan transaksi di kasir",
            )
            db.add(pmt)
            payments_count += 1
        elif idx % 3 == 1:
            dp_amount = ord_obj.total_amount // 2
            if dp_amount > 0:
                pmt = Payment(
                    id=uuid.uuid4(),
                    order_id=ord_obj.id,
                    amount=dp_amount,
                    method=method,
                    verification_status="VERIFIED",
                    payment_time=ord_obj.created_at + timedelta(minutes=5),
                    verified_by=cashier.id,
                    verified_at=ord_obj.created_at + timedelta(minutes=5),
                    reference_note="Uang muka (DP 50%) saat serah cucian",
                )
                db.add(pmt)
                payments_count += 1

                if payment_to_void is None and idx > 10:
                    payment_to_void = pmt

    db.flush()

    if payment_to_void:
        pv = PaymentVoid(
            id=uuid.uuid4(),
            payment_id=payment_to_void.id,
            reason="Pelanggan membatalkan pembayaran transfer ganda; kasir melakukan koreksi void.",
            voided_by=owner_user.id,
            voided_at=payment_to_void.payment_time + timedelta(minutes=30),
        )
        db.add(pv)
        voids_count += 1

    db.flush()
    counts["payments"] = payments_count
    counts["payment_voids"] = voids_count

    # -------------------------------------------------------------
    # 17. expenses (Table 17)
    # -------------------------------------------------------------
    print("[+] 17. Seeding operational expenses...")
    expense_data = [
        ("SUPPLIES", 320000, "Pembelian Deterjen Cair Matic 20 Liter"),
        ("SUPPLIES", 240000, "Pembelian Softener & Pewangi Sakura 20 Liter"),
        ("SUPPLIES", 110000, "Pembelian Plastik Packing Laundry Kiloan 35x50 (5 Pack)"),
        ("SUPPLIES", 75000, "Pembelian Lakban Bening & Tagging Gun Label"),
        ("SUPPLIES", 85000, "Hanger Kawat Putih Laundry (10 Lusin)"),
        ("UTILITIES", 650000, "Pembayaran Tagihan Listrik PLN Pascabayar Bulanan"),
        ("UTILITIES", 280000, "Pembayaran Tagihan Air Bersih PDAM Outlet"),
        ("UTILITIES", 90000, "Refill Gas LPG 3kg untuk Mesin Dryer (4 tabung)"),
        ("MAINTENANCE", 350000, "Servis Rutin Berkala Mesin Cuci Front Loading"),
        ("MAINTENANCE", 180000, "Penggantian V-Belt & Pembersihan Filter Dryer"),
        ("FUEL", 50000, "Bensin Operasional Motor Kurir Doni (Antar Jemput)"),
        ("FUEL", 50000, "Bensin Operasional Motor Kurir Agus (Antar Jemput)"),
        ("SALARY", 150000, "Uang Makan & Transport Kasir Harian"),
        ("SALARY", 120000, "Insentif Harian Kurir"),
        ("OTHER", 45000, "Kertas Struk Kasir Thermal Roll 58mm (10 Roll)"),
        ("OTHER", 35000, "Kain Lap Microfiber & Pembersih Kaca"),
    ]
    expenses_count = 0
    for cat, amt, desc in expense_data:
        exp = Expense(
            id=uuid.uuid4(),
            business_id=business.id,
            category=cat,
            amount=amt,
            description=desc,
            expense_date=(now - timedelta(days=random.randint(1, 20))).date(),
            created_by=random.choice(cashiers).id,
            created_at=now - timedelta(days=random.randint(1, 20)),
        )
        db.add(exp)
        expenses_count += 1
    db.flush()
    counts["expenses"] = expenses_count

    # -------------------------------------------------------------
    # 18. idempotency_records (Table 18)
    # -------------------------------------------------------------
    print("[+] 18. Seeding idempotency_records...")
    idempotency_count = 0
    for i in range(5):
        key = f"idemp-key-sample-{uuid.uuid4().hex[:16]}"
        rec = IdempotencyRecord(
            id=uuid.uuid4(),
            scope_key=f"tenant:{business.id}:user:{random.choice(cashiers).id}",
            operation="CREATE_PAYMENT",
            idempotency_key_hash=hashlib.sha256(key.encode()).hexdigest(),
            request_hash=hashlib.sha256(f"payload_{i}".encode()).hexdigest(),
            status="COMPLETED",
            response_status_code=201,
            response_reference='{"status":"success","data":{"payment_id":"sample"}}',
            created_at=now - timedelta(hours=i * 6),
            expires_at=now + timedelta(hours=24),
        )
        db.add(rec)
        idempotency_count += 1
    db.flush()
    counts["idempotency_records"] = idempotency_count

    # -------------------------------------------------------------
    # 19. audit_logs (Table 19)
    # -------------------------------------------------------------
    print("[+] 19. Seeding audit_logs (Table 19 complete)...")
    audit_events = [
        ("USER_CREATED", "user", users_dict["kasir_ani"].id, None, {"username": "kasir_ani", "role": "CASHIER"}, "Pembuatan akun kasir Ani"),
        ("USER_CREATED", "user", users_dict["kurir_doni"].id, None, {"username": "kurir_doni", "role": "COURIER"}, "Pembuatan akun kurir Doni"),
        ("SERVICE_CREATED", "service", services[0].id, None, {"name": services[0].name, "price": 8000}, "Penambahan layanan Cuci Komplit"),
        ("SERVICE_CREATED", "service", services[1].id, None, {"name": services[1].name, "price": 6000}, "Penambahan layanan Cuci Kering Lipat"),
        ("ORDER_CANCELLED", "order", orders[0].id, {"status": "RECEIVED"}, {"status": "CANCELLED"}, "Pembatalan order atas permintaan customer"),
    ]
    if payment_to_void:
        audit_events.append(
            ("PAYMENT_VOIDED", "payment", payment_to_void.id, {"is_voided": False}, {"is_voided": True}, "Void pembayaran salah input")
        )

    audit_logs_count = 0
    for action, r_type, r_id, b_data, a_data, rsn in audit_events:
        alog = AuditLog(
            id=uuid.uuid4(),
            actor_user_id=owner_user.id,
            action=action,
            resource_type=r_type,
            resource_id=r_id,
            request_id=f"req-seed-{uuid.uuid4().hex[:8]}",
            before_data=b_data,
            after_data=a_data,
            reason=rsn,
            created_at=now - timedelta(hours=random.randint(1, 48)),
        )
        db.add(alog)
        audit_logs_count += 1
    db.flush()
    counts["audit_logs"] = audit_logs_count

    db.commit()
    return counts


def main() -> None:
    parser = argparse.ArgumentParser(description="Seed E-Laundry 2.0 with authentic Indonesian dummy data across all 19 tables.")
    parser.add_argument("--clean", action="store_true", help="Purge all existing rows before seeding")
    parser.add_argument("--sqlite", action="store_true", help="Use local SQLite database file (dev_laundry.db) instead of PostgreSQL")
    parser.add_argument("--db-url", type=str, default=None, help="Custom database URL override")
    parser.add_argument("--customers", type=int, default=30, help="Number of customer records (default: 30)")
    parser.add_argument("--orders", type=int, default=50, help="Number of order records (default: 50)")

    args = parser.parse_args()

    if args.sqlite:
        db_url = "sqlite:///dev_laundry.db"
    elif args.db_url:
        db_url = args.db_url
    else:
        db_url = settings.DATABASE_URL

    print("=" * 70)
    print("=== E-LAUNDRY 2.0 DUMMY DATA SEEDER (19 CORE TABLES) ===")
    print(f"Target Database: {db_url}")
    print("=" * 70)

    connect_args = {"check_same_thread": False} if db_url.startswith("sqlite") else {}
    engine = create_engine(db_url, connect_args=connect_args)

    if db_url.startswith("sqlite"):
        @event.listens_for(engine, "connect")
        def register_sqlite_functions(dbapi_connection, connection_record):
            dbapi_connection.create_function(
                "num_nonnulls",
                -1,
                lambda *args: sum(1 for a in args if a is not None),
            )

    # Ensure schema tables exist
    print("[*] Ensuring all 19 database tables exist in target schema...")
    Base.metadata.create_all(bind=engine)

    SessionFactory = sessionmaker(bind=engine, autocommit=False, autoflush=False)
    db = SessionFactory()

    try:
        if args.clean:
            clean_existing_data(db, engine)

        # Check if already seeded
        biz_exists = db.scalar(select(Business).limit(1))
        if biz_exists and not args.clean:
            print("[!] Database already contains business data.")
            print("    Pass '--clean' if you want to purge and re-seed from scratch.")
            return

        counts = seed_database(db, customer_count=args.customers, order_count=args.orders)

        print("\n" + "=" * 70)
        print("[DONE] SEEDING COMPLETED SUCCESSFULLY! SUMMARY OF 19 TABLES:")
        print("=" * 70)
        total_rows = 0
        for table_name, count in counts.items():
            print(f"   [+] {table_name:<26} : {count:>5} rows")
            total_rows += count
        print("-" * 70)
        print(f"   TOTAL ROWS INSERTED ACROSS 19 TABLES : {total_rows:>5} rows")
        print("=" * 70)
        print("Demo User Credentials:")
        print("   - Owner:    owner       / Owner123!")
        print("   - Cashier:  kasir_ani   / Kasir123!")
        print("   - Cashier:  kasir_budi  / Kasir123!")
        print("   - Courier:  kurir_doni  / Kurir123!")
        print("   - Courier:  kurir_agus  / Kurir123!")
        print("=" * 70)

    except Exception as exc:
        db.rollback()
        print(f"\n[!] Seeding failed with error: {exc}", file=sys.stderr)
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()
