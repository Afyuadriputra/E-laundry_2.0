from fastapi.testclient import TestClient


def test_root_info(client: TestClient):
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "app" in data
    assert data["docs"] == "/docs"
    assert data["health"] == "/api/v1/health/live"


def test_liveness_returns_200(client: TestClient):
    response = client.get("/api/v1/health/live")
    assert response.status_code == 200
    assert response.json() == {"status": "alive"}


def test_readiness_returns_200_when_db_up(client: TestClient):
    response = client.get("/api/v1/health/ready")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ready"
    assert data["database"] == "connected"


def test_request_id_in_response_header(client: TestClient):
    response = client.get("/api/v1/health/live")
    assert response.status_code == 200
    assert "X-Request-ID" in response.headers
    assert len(response.headers["X-Request-ID"]) > 0


def test_custom_request_id_propagated(client: TestClient):
    custom_id = "test-custom-request-id-12345"
    response = client.get("/api/v1/health/live", headers={"X-Request-ID": custom_id})
    assert response.status_code == 200
    assert response.headers.get("X-Request-ID") == custom_id


def test_security_headers_present(client: TestClient):
    response = client.get("/api/v1/health/live")
    assert response.headers.get("X-Content-Type-Options") == "nosniff"
    assert response.headers.get("X-Frame-Options") == "DENY"
    assert response.headers.get("X-XSS-Protection") == "1; mode=block"
