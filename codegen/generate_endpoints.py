"""Generate ``teamleader/_generated/endpoints.py`` from the OpenAPI spec.

Walks ``spec["paths"]`` and emits:

- A frozen ``@dataclass`` called ``Endpoint`` describing a single operation.
- A module-level ``ENDPOINTS: dict[str, Endpoint]`` mapping ``operationId``
  to its ``Endpoint``.

All Teamleader Focus API paths use POST.  Parameters live in the request
body (``requestBody.content.application/json.schema``), which is either a
direct object schema or wrapped in ``allOf[0]``.
"""

from __future__ import annotations

import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

OUTPUT_PATH = (
    Path(__file__).parent.parent / "teamleader" / "_generated" / "endpoints.py"
)

_FILE_HEADER = """\
# ============================================================
# AUTO-GENERATED — DO NOT EDIT BY HAND
# Run `python codegen/generate.py` to regenerate.
# Spec version: {version}
# Generated at: {timestamp}
# ============================================================

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Endpoint:
    \"\"\"Metadata for a single Teamleader Focus API operation.\"\"\"

    operation_id: str
    method: str
    path: str
    tag: str
    required_params: tuple[str, ...]
    optional_params: tuple[str, ...]
    description: str = ""


# fmt: off
ENDPOINTS: dict[str, Endpoint] = {{
"""

_FILE_FOOTER = """\
}
# fmt: on
"""


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _extract_body_schema(operation: dict[str, Any]) -> dict[str, Any] | None:
    """Return the innermost request-body object schema, or None."""
    rb = operation.get("requestBody", {})
    content = rb.get("content", {})
    app_json = content.get("application/json", {})
    schema = app_json.get("schema", {})

    if not schema:
        return None

    # The spec wraps schemas in allOf — unwrap one level
    if "allOf" in schema:
        parts = schema["allOf"]
        if parts:
            schema = parts[0]

    return schema if schema.get("type") == "object" or "properties" in schema else None


def _safe_repr(s: str) -> str:
    return repr(s)


# ---------------------------------------------------------------------------
# Main generator
# ---------------------------------------------------------------------------


def generate_endpoints(spec: dict[str, Any], version: str) -> None:
    """Write endpoint definitions to ``teamleader/_generated/endpoints.py``."""
    paths: dict[str, Any] = spec.get("paths", {})

    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    lines: list[str] = [_FILE_HEADER.format(version=version, timestamp=timestamp)]

    endpoint_count = 0
    for path in sorted(paths):
        path_item = paths[path]
        for http_method, operation in path_item.items():
            if not isinstance(operation, dict):
                continue

            operation_id: str = operation.get("operationId", "")
            if not operation_id:
                continue

            tags: list[str] = operation.get("tags", [])
            tag = tags[0] if tags else ""
            description: str = operation.get("description", "").strip()
            # Escape description for repr
            description = description.replace("\\", "\\\\").replace('"', '\\"')

            # Extract required / optional params from body schema
            body_schema = _extract_body_schema(operation)
            required_params: list[str] = []
            optional_params: list[str] = []

            if body_schema:
                required_set: set[str] = set(body_schema.get("required", []))
                props: dict[str, Any] = body_schema.get("properties", {})
                for param_name in sorted(props):
                    if param_name in required_set:
                        required_params.append(param_name)
                    else:
                        optional_params.append(param_name)

            req_tuple = "(" + ", ".join(_safe_repr(p) for p in required_params)
            req_tuple += ("," if len(required_params) == 1 else "") + ")"
            opt_tuple = "(" + ", ".join(_safe_repr(p) for p in optional_params)
            opt_tuple += ("," if len(optional_params) == 1 else "") + ")"

            lines.append(f"    {_safe_repr(operation_id)}: Endpoint(")
            lines.append(f"        operation_id={_safe_repr(operation_id)},")
            lines.append(f"        method={_safe_repr(http_method.upper())},")
            lines.append(f"        path={_safe_repr(path)},")
            lines.append(f"        tag={_safe_repr(tag)},")
            lines.append(f"        required_params={req_tuple},")
            lines.append(f"        optional_params={opt_tuple},")
            lines.append(f"        description={_safe_repr(description)},")
            lines.append("    ),")

            endpoint_count += 1

    lines.append(_FILE_FOOTER)

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text("\n".join(lines), encoding="utf-8")
    print(f"  Wrote {endpoint_count} endpoints → {OUTPUT_PATH.name}")
