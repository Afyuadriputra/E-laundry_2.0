import uuid
from datetime import UTC, datetime
from decimal import Decimal

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.modules.businesses.models import Business
from app.modules.customers.models import Customer
from app.modules.orders.models import Order, OrderItem
from app.modules.payments.models import Payment
from app.modules.users.models import User, UserRole


def _login(client: TestClient, username: str, password: str) -> dict[str, str]:
    res = client.post("/api/v1/auth/login", json={"username": username, "password": password})
    assert res.status_code == 200
    csrf = res.headers.get("X-CSRF-Token", "")
    return {"X-CSRF-Token": csrf}


def test_invoices_and_whatsapp_flow(client: TestClient, db_session: Session):
    business_id = uuid.uuid4()
    business = Business(
        id=business_id,
        name="Laundry Bersih Wangi",
        phone_e164="+6281211112222",
        address="Jl. Gajah Mada No. 8",
        timezone="Asia/Jakarta",
        is_active=True,
    )
    db_session.add(business)

    cashier = User(
        id=uuid.uuid4(),
        business_id=business_id,
        username="kasir_nota",
        full_name="Kasir Nota",
        password_hash=hash_password("KasirNota123!"),
        role=UserRole.CASHIER.value,
        is_active=True,
    )
    customer = Customer(
        id=uuid.uuid4(),
        business_id=business_id,
        full_name="Ibu Dewi Sartika",
        phone_e164="+6281234567777",
        address="Jl. Melati 99",
        is_active=True,
    )
    db_session.add_all([cashier, customer])
    db_session.commit()

    order_id = uuid.uuid4()
    order = Order(
        id=order_id,
        business_id=business_id,
        order_number="ORD-20261103-NOTA",
        customer_id=customer.id,
        created_by=cashier.id,
        operational_status="RECEIVED",
        intake_method="DROP_OFF",
        return_method="SELF_PICKUP",
        subtotal_amount=30000,
        extra_charge_amount=0,
        delivery_fee_amount=0,
        total_amount=30000,
        estimated_completion_at=datetime.now(UTC),
        version=1,
    )
    db_session.add(order)
    db_session.flush()

    item = OrderItem(
        id=uuid.uuid4(),
        order_id=order_id,
        service_id=uuid.uuid4(),
        service_name_snapshot="Cuci Kering Lipat",
        pricing_type_snapshot="PER_KG",
        unit_snapshot="KG",
        quantity=Decimal("3.0"),
        unit_price_snapshot=10000,
        line_total_amount=30000,
        requires_ironing_snapshot=False,
    )
    db_session.add(item)

    payment = Payment(
        id=uuid.uuid4(),
        order_id=order_id,
        amount=30000,
        method="CASH",
        verification_status="VERIFIED",
        payment_time=datetime.now(UTC),
        verified_by=cashier.id,
        verified_at=datetime.now(UTC),
        created_at=datetime.now(UTC),
    )
    db_session.add(payment)
    db_session.commit()

    # Login as Cashier
    headers = _login(client, "kasir_nota", "KasirNota123!")

    # 1. Digital Invoice JSON API
    res = client.get(f"/api/v1/invoices/{order_id}", headers=headers)
    assert res.status_code == 200
    inv = res.json()["data"]
    assert inv["order_number"] == "ORD-20261103-NOTA"
    assert inv["business_name"] == "Laundry Bersih Wangi"
    assert inv["customer_name"] == "Ibu Dewi Sartika"
    assert inv["total_amount"] == 30000
    assert inv["total_paid"] == 30000
    assert inv["remaining_amount"] == 0
    assert inv["payment_status"] == "PAID"
    assert "https://wa.me/6281234567777" in inv["whatsapp_share_url"]
    assert "ORD-20261103-NOTA" in inv["whatsapp_share_text"]

    # 2. Thermal 58mm text format
    res_thermal = client.get(f"/api/v1/invoices/{order_id}/thermal", headers=headers)
    assert res_thermal.status_code == 200
    assert "text/plain" in res_thermal.headers["content-type"]
    assert "ORD-20261103-NOTA" in res_thermal.text
    assert "TOTAL" in res_thermal.text

    # 3. HTML printable format
    res_html = client.get(f"/api/v1/invoices/{order_id}/html", headers=headers)
    assert res_html.status_code == 200
    assert "text/html" in res_html.headers["content-type"]
    assert "<!DOCTYPE html>" in res_html.text
    assert "Laundry Bersih Wangi" in res_html.text
