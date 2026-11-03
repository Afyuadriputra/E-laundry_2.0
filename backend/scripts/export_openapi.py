"""Export OpenAPI specification from FastAPI application."""

import json
import sys
from pathlib import Path

# Ensure backend root is on sys.path
backend_root = Path(__file__).resolve().parent.parent
if str(backend_root) not in sys.path:
    sys.path.insert(0, str(backend_root))

from app.main import app  # noqa: E402


def export_openapi():
    openapi_schema = app.openapi()
    output_dir = backend_root.parent / "doc" / "api"
    output_dir.mkdir(parents=True, exist_ok=True)

    output_file = output_dir / "openapi.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(openapi_schema, f, indent=2, ensure_ascii=False)

    print(f"OpenAPI schema successfully exported to: {output_file}")


if __name__ == "__main__":
    export_openapi()
