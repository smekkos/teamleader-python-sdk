"""Generate ``teamleader/_generated/models.py`` from the OpenAPI spec.

Walks ``spec["components"]["schemas"]`` for object-type schemas and
emits a ``@dataclass`` named ``_<ModelName>Base`` for each one.

Field-ordering rule (required by Python dataclasses):
  1. Required, non-nullable, non-array fields  — no default
  2. Required, nullable fields                  — ``| None``  (no default,
     callers must pass None explicitly)
  3. Optional fields (absent from ``required``) — ``| None = None``
  4. Array fields                               — ``list[Any] = field(default_factory=list)``

``allOf`` / ``oneOf`` in a property fall back to ``dict[str, Any]``.
Schemas that are only ``oneOf`` at the top level are skipped.
"""

from __future__ import annotations

import keyword
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

OUTPUT_PATH = Path(__file__).parent.parent / "teamleader" / "_generated" / "models.py"

_FILE_HEADER = """\
# ============================================================
# AUTO-GENERATED — DO NOT EDIT BY HAND
# Run `python codegen/generate.py` to regenerate.
# Spec version: {version}
# Generated at: {timestamp}
# ============================================================

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

"""


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _schema_to_class_name(schema_name: str) -> str:
    """Convert a schema key to a PascalCase class name prefix.

    Examples::

        "AddressResponse"     → "AddressResponse"
        "contacts.addrequest" → "ContactsAddrequest"
    """
    cleaned = re.sub(r"[.\-]", " ", schema_name)
    return "".join(w.capitalize() for w in cleaned.split())


def _safe_field_name(name: str) -> str:
    """Return *name* as a safe Python identifier.

    Appends ``_`` for Python keywords.  Replaces hyphens with underscores.
    """
    s = re.sub(r"-", "_", name)
    if keyword.iskeyword(s):
        s += "_"
    return s


def _prop_base_type(prop: dict[str, Any]) -> str:
    """Return the base Python type string for *prop*, ignoring nullability.

    ``allOf`` / ``oneOf`` collapse to ``dict[str, Any]``.
    """
    if "allOf" in prop or "oneOf" in prop:
        return "dict[str, Any]"

    ptype = prop.get("type", "")

    if ptype == "string":
        return "str"
    if ptype == "integer":
        return "int"
    if ptype == "number":
        return "float"
    if ptype == "boolean":
        return "bool"
    if ptype == "array":
        items = prop.get("items", {})
        item_type = _prop_base_type(items)
        return f"list[{item_type}]"
    if ptype == "object":
        return "dict[str, Any]"

    # No type hint — fall back
    return "Any"


def _is_array(prop: dict[str, Any]) -> bool:
    return prop.get("type") == "array"


def _is_nullable(prop: dict[str, Any]) -> bool:
    return bool(prop.get("nullable", False))


# ---------------------------------------------------------------------------
# Main generator
# ---------------------------------------------------------------------------


def generate_models(spec: dict[str, Any], version: str) -> None:
    """Write model base dataclasses to ``teamleader/_generated/models.py``."""
    schemas: dict[str, Any] = spec.get("components", {}).get("schemas", {})

    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    lines: list[str] = [_FILE_HEADER.format(version=version, timestamp=timestamp)]

    model_count = 0
    for schema_name in sorted(schemas):
        schema = schemas[schema_name]

        # Only process object schemas that have properties
        if schema.get("type") != "object":
            continue
        props: dict[str, Any] = schema.get("properties", {})
        if not props:
            continue
        # Skip top-level oneOf (discriminated unions — too complex to flatten)
        if "oneOf" in schema:
            continue

        class_name = f"_{_schema_to_class_name(schema_name)}Base"
        required_keys: set[str] = set(schema.get("required", []))

        # Partition fields into four buckets to satisfy dataclass ordering
        req_plain: list[tuple[str, str]] = []       # no default
        req_nullable: list[tuple[str, str]] = []    # | None, no default
        opt_scalar: list[tuple[str, str]] = []      # | None = None
        opt_array: list[tuple[str, str]] = []       # list[...] = field(...)

        for prop_name, prop_schema in props.items():
            field_name = _safe_field_name(prop_name)
            base = _prop_base_type(prop_schema)
            is_req = prop_name in required_keys
            nullable = _is_nullable(prop_schema)
            is_arr = _is_array(prop_schema)

            if is_arr:
                # Arrays always get default_factory — go last regardless of required
                opt_array.append((field_name, base))
            elif is_req and not nullable:
                req_plain.append((field_name, base))
            elif is_req and nullable:
                req_nullable.append((field_name, f"{base} | None"))
            else:
                opt_scalar.append((field_name, f"{base} | None"))

        lines.append("@dataclass")
        lines.append(f"class {class_name}:")
        title = schema.get("title", schema_name)
        lines.append(f'    """Auto-generated from schema: {title}"""')
        lines.append("")

        for fname, ftype in req_plain:
            lines.append(f"    {fname}: {ftype}")
        for fname, ftype in req_nullable:
            lines.append(f"    {fname}: {ftype}")
        for fname, ftype in opt_scalar:
            lines.append(f"    {fname}: {ftype} = None")
        for fname, ftype in opt_array:
            lines.append(f"    {fname}: {ftype} = field(default_factory=list)")

        # If all fields have defaults (no required plain/nullable), add sentinel
        if not req_plain and not req_nullable and not opt_scalar and not opt_array:
            lines.append("    pass")

        lines.append("")
        lines.append("")
        model_count += 1

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text("\n".join(lines), encoding="utf-8")
    print(f"  Wrote {model_count} model base classes → {OUTPUT_PATH.name}")
