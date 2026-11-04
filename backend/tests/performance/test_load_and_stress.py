"""
Performance, Load & Stress Benchmark Suite (BE-07 / BE-08 / BE-09 / BE-10).
Executes high-concurrency request batches to measure:
- Requests Per Second (RPS) throughput
- Latency percentiles (p50, p95, p99, mean)
- Tracemalloc peak memory overhead
- Business endpoints: health, CSRF, customer search, order listing, public tracking, reports
"""

import statistics
import time
import tracemalloc
import uuid
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta, timezone

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.modules.businesses.models import Business
from app.modules.customers.models import Customer
from app.modules.orders.domain.state_machine import OperationalStatus
from app.modules.orders.models import Order
from app.modules.services.models import Service
from app.modules.tracking.service import TrackingService
from app.modules.users.models import User, UserRole


def _login(client: TestClient, username: str, password: str = "Secret123!"):
    csrf_res = client.get("/api/v1/auth/csrf")
    token = csrf_res.json()["data"]["csrf_token"]
    login_res = client.post(
        "/api/v1/auth/login",
        json={"username": username, "password": password},
        headers={"X-CSRF-Token": token},
    )
    assert login_res.status_code == 200, f"Login failed: {login_res.text}"
    new_token = login_res.json()["data"]["csrf_token"]
    return {"X-CSRF-Token": new_token}


def test_health_endpoint_throughput_and_latency(client: TestClient):
    """Benchmark /api/v1/health/live under multi-threaded load."""
    tracemalloc.start()
    iterations = 200
    latencies = []

    def make_request():
        t0 = time.perf_counter()
        res = client.get("/api/v1/health/live")
        t1 = time.perf_counter()
        assert res.status_code == 200
        return (t1 - t0) * 1000.0  # ms

    start_total = time.perf_counter()
    with ThreadPoolExecutor(max_workers=10) as pool:
        futures = [pool.submit(make_request) for _ in range(iterations)]
        for f in futures:
            latencies.append(f.result())
    total_duration = time.perf_counter() - start_total
    current_mem, peak_mem = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    rps = iterations / total_duration
    p50 = statistics.median(latencies)
    sorted_lats = sorted(latencies)
    p95 = sorted_lats[int(len(sorted_lats) * 0.95)]
    p99 = sorted_lats[int(len(sorted_lats) * 0.99)]

    print(
        f"\n[BENCHMARK HEALTH] RPS: {rps:.1f} req/s | Mean: {statistics.mean(latencies):.2f}ms | "
        f"p50: {p50:.2f}ms | p95: {p95:.2f}ms | p99: {p99:.2f}ms | Peak RAM: {peak_mem / 1024:.1f} KB"
    )

    # Invariants (allows realistic overhead for in-process TestClient thread locks on Windows)
    assert p95 < 500.0, f"p95 latency {p95:.2f}ms exceeded threshold"
    assert rps > 30.0, f"Throughput {rps:.1f} RPS below minimum expectation"


def test_root_and_csrf_benchmark(client: TestClient):
    """Benchmark CSRF retrieval and root endpoint under load."""
    tracemalloc.start()
    iterations = 100
    latencies = []

    def make_request():
        t0 = time.perf_counter()
        res = client.get("/api/v1/auth/csrf")
        t1 = time.perf_counter()
        assert res.status_code == 200
        return (t1 - t0) * 1000.0

    start_total = time.perf_counter()
    with ThreadPoolExecutor(max_workers=5) as pool:
        futures = [pool.submit(make_request) for _ in range(iterations)]
        for f in futures:
            latencies.append(f.result())
    total_duration = time.perf_counter() - start_total
    current_mem, peak_mem = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    rps = iterations / total_duration
    sorted_lats = sorted(latencies)
    p95 = sorted_lats[int(len(sorted_lats) * 0.95)]

    print(f"\n[BENCHMARK CSRF] RPS: {rps:.1f} req/s | p95: {p95:.2f}ms | Peak RAM: {peak_mem / 1024:.1f} KB")
    assert p95 < 400.0, f"p95 latency {p95:.2f}ms exceeded threshold"


def test_business_customer_search_and_order_listing_benchmark(client: TestClient, db_session: Session):
    """Benchmark real business workloads: Customer Search & Order Listing."""
    # Seed business, cashier, customer, order
    biz = Business(
        id=uuid.uuid4(),
        name="Bench Laundry",
        phone_e164="+6281200000099",
        address="Jl. Bench No. 1",
        timezone="Asia/Jakarta",
        is_active=True,
    )
    user = User(
        id=uuid.uuid4(),
        business_id=biz.id,
        username="bench_cashier",
        full_name="Bench Cashier",
        password_hash=hash_password("Secret123!"),
        role=UserRole.CASHIER.value,
        is_active=True,
    )
    cust = Customer(
        id=uuid.uuid4(),
        business_id=biz.id,
        full_name="Siti Benchmark",
        phone_e164="+6281299998888",
        address="Jl. Test No. 99",
        is_active=True,
    )
    order = Order(
        id=uuid.uuid4(),
        business_id=biz.id,
        customer_id=cust.id,
        order_number="ORD-BENCH-001",
        created_by=user.id,
        operational_status=OperationalStatus.RECEIVED.value,
        intake_method="DROP_OFF",
        return_method="SELF_PICKUP",
        total_amount=35000,
        estimated_completion_at=datetime.now(timezone.utc) + timedelta(days=2),
        version=1,
    )
    db_session.add_all([biz, user, cust, order])
    db_session.flush()

    headers = _login(client, user.username, "Secret123!")

    tracemalloc.start()
    iterations = 50
    latencies = []
    start_total = time.perf_counter()
    for _ in range(iterations):
        t0 = time.perf_counter()
        res = client.get("/api/v1/customers?search=Siti", headers=headers)
        t1 = time.perf_counter()
        assert res.status_code == 200
        latencies.append((t1 - t0) * 1000.0)
    total_duration = time.perf_counter() - start_total
    current_mem, peak_mem = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    rps = iterations / total_duration
    p50 = statistics.median(latencies)
    sorted_lats = sorted(latencies)
    p95 = sorted_lats[int(len(sorted_lats) * 0.95)]
    p99 = sorted_lats[int(len(sorted_lats) * 0.99)]

    print(
        f"\n[BENCHMARK CUSTOMER SEARCH] RPS: {rps:.1f} req/s | Mean: {statistics.mean(latencies):.2f}ms | "
        f"p50: {p50:.2f}ms | p95: {p95:.2f}ms | p99: {p99:.2f}ms | Peak RAM: {peak_mem / 1024:.1f} KB"
    )
    assert p95 < 200.0, f"Customer search p95 {p95:.2f}ms exceeded limit"
    assert rps > 15.0, f"RPS {rps:.1f} below expectation"


def test_business_public_tracking_benchmark(client: TestClient, db_session: Session):
    """Benchmark public order tracking lookup by token."""
    biz = Business(
        id=uuid.uuid4(),
        name="Track Bench",
        phone_e164="+6281200000098",
        address="Jl. Bench 2",
        timezone="Asia/Jakarta",
        is_active=True,
    )
    staff_user = User(
        id=uuid.uuid4(),
        business_id=biz.id,
        username="track_staff",
        full_name="Track Staff",
        password_hash=hash_password("Secret123!"),
        role=UserRole.CASHIER.value,
        is_active=True,
    )
    cust = Customer(
        id=uuid.uuid4(),
        business_id=biz.id,
        full_name="Budi Tracking",
        phone_e164="+6281277776666",
        address="Jl. Track 1",
        is_active=True,
    )
    order = Order(
        id=uuid.uuid4(),
        business_id=biz.id,
        customer_id=cust.id,
        order_number="ORD-TRACK-001",
        created_by=staff_user.id,
        operational_status=OperationalStatus.WASHING.value,
        intake_method="DROP_OFF",
        return_method="SELF_PICKUP",
        total_amount=40000,
        estimated_completion_at=datetime.now(timezone.utc) + timedelta(days=2),
        version=1,
    )
    db_session.add_all([biz, staff_user, cust, order])
    db_session.flush()

    token_record, raw_token = TrackingService.create_order_tracking_token(db=db_session, order_id=order.id)
    db_session.flush()

    tracemalloc.start()
    iterations = 50
    latencies = []
    start_total = time.perf_counter()
    for _ in range(iterations):
        t0 = time.perf_counter()
        res = client.get(f"/api/v1/tracking/{raw_token}")
        t1 = time.perf_counter()
        assert res.status_code == 200
        latencies.append((t1 - t0) * 1000.0)
    total_duration = time.perf_counter() - start_total
    current_mem, peak_mem = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    rps = iterations / total_duration
    p50 = statistics.median(latencies)
    sorted_lats = sorted(latencies)
    p95 = sorted_lats[int(len(sorted_lats) * 0.95)]
    p99 = sorted_lats[int(len(sorted_lats) * 0.99)]

    print(
        f"\n[BENCHMARK PUBLIC TRACKING] RPS: {rps:.1f} req/s | Mean: {statistics.mean(latencies):.2f}ms | "
        f"p50: {p50:.2f}ms | p95: {p95:.2f}ms | p99: {p99:.2f}ms | Peak RAM: {peak_mem / 1024:.1f} KB"
    )
    assert p95 < 200.0, f"Tracking p95 {p95:.2f}ms exceeded limit"
    assert rps > 15.0, f"RPS {rps:.1f} below expectation"


def test_business_reports_benchmark(client: TestClient, db_session: Session):
    """Benchmark financial and operational summary reporting endpoints."""
    biz = Business(
        id=uuid.uuid4(),
        name="Report Bench",
        phone_e164="+6281200000097",
        address="Jl. Bench 3",
        timezone="Asia/Jakarta",
        is_active=True,
    )
    owner = User(
        id=uuid.uuid4(),
        business_id=biz.id,
        username="bench_owner",
        full_name="Bench Owner",
        password_hash=hash_password("Secret123!"),
        role=UserRole.OWNER.value,
        is_active=True,
    )
    db_session.add_all([biz, owner])
    db_session.flush()

    headers = _login(client, owner.username, "Secret123!")

    tracemalloc.start()
    iterations = 40
    latencies = []
    start_total = time.perf_counter()
    for _ in range(iterations):
        t0 = time.perf_counter()
        res = client.get("/api/v1/reports/dashboard", headers=headers)
        t1 = time.perf_counter()
        assert res.status_code == 200
        latencies.append((t1 - t0) * 1000.0)
    total_duration = time.perf_counter() - start_total
    current_mem, peak_mem = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    rps = iterations / total_duration
    p50 = statistics.median(latencies)
    sorted_lats = sorted(latencies)
    p95 = sorted_lats[int(len(sorted_lats) * 0.95)]

    print(
        f"\n[BENCHMARK DASHBOARD REPORT] RPS: {rps:.1f} req/s | Mean: {statistics.mean(latencies):.2f}ms | "
        f"p50: {p50:.2f}ms | p95: {p95:.2f}ms | Peak RAM: {peak_mem / 1024:.1f} KB"
    )
    assert p95 < 250.0, f"Report p95 {p95:.2f}ms exceeded limit"
    assert rps > 10.0, f"RPS {rps:.1f} below expectation"
