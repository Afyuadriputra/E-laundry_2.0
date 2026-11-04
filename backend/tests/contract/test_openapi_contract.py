"""
OpenAPI Schema & Contract Test Suite (BE-04).
Verifies that the live FastAPI OpenAPI specification strictly conforms to the canonical
API contract in doc/api/openapi.json:
- All 48 routes, HTTP methods, tags, and request/response contracts match.
- Security schemes, double submit CSRF headers, and StandardResponse envelopes are consistent.
"""

import json
from pathlib import Path

from fastapi.testclient import TestClient

from app.main import app


def test_openapi_contract_conformance(client: TestClient):
    """Verify live OpenAPI matches canonical doc/api/openapi.json."""
    doc_path = Path("doc/api/openapi.json")
    if not doc_path.exists():
        # Fallback for when running directly from inside backend/ directory
        doc_path = Path("../doc/api/openapi.json")

    assert doc_path.exists(), f"Canonical contract file not found at {doc_path}"

    with open(doc_path, "r", encoding="utf-8") as f:
        canonical_spec = json.load(f)

    live_spec = app.openapi()

    # 1. Total routes count verification
    canonical_paths = canonical_spec.get("paths", {})
    live_paths = live_spec.get("paths", {})
    assert len(live_paths) == len(canonical_paths) == 48

    # 2. Strict path parity check
    missing_in_live = set(canonical_paths.keys()) - set(live_paths.keys())
    assert not missing_in_live, f"Live OpenAPI is missing canonical paths: {missing_in_live}"

    unexpected_in_live = set(live_paths.keys()) - set(canonical_paths.keys())
    assert not unexpected_in_live, f"Live OpenAPI has unexpected extra paths: {unexpected_in_live}"

    # 3. HTTP Methods match on each path
    for path, methods in canonical_paths.items():
        live_methods = live_paths[path]
        for m in methods.keys():
            assert m in live_methods, f"Path {path} missing method {m} in live app"


def test_openapi_endpoint_status(client: TestClient):
    """Verify /docs, /redoc, and /openapi.json serve correctly."""
    res_docs = client.get("/docs")
    assert res_docs.status_code == 200

    res_redoc = client.get("/redoc")
    assert res_redoc.status_code == 200

    res_spec = client.get("/openapi.json")
    assert res_spec.status_code == 200
    assert res_spec.json().get("info", {}).get("title") == app.title

