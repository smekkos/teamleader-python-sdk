"""Generate ``teamleader/_generated/enums.py`` from the OpenAPI spec.

Walks ``spec["components"]["schemas"]`` and emits a ``str, Enum``
subclass for every schema where ``type == "string"`` and ``enum`` is
present.
"""

from __future__ import annotations

import keyword
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

OUTPUT_PATH = Path(__file__).parent.parent / "teamleader" / "_generated" / "enums.py"

_FILE_HEADER = """\
# ============================================================
# AUTO-GENERATED — DO NOT EDIT BY HAND
# Run `python codegen/generate.py` to regenerate.
# Spec version: {version}
# Generated at: {timestamp}
# ============================================================

from __future__ import annotations

from enum import Enum

"""


def _to_class_name(schema_name: str) -> str:
    """Convert a schema key to a PascalCase Python class name.

    Examples::

        "Order"            → "Order"
        "contacts.status"  → "ContactsStatus"
    """
    cleaned = re.sub(r"[.\-]", " ", schema_name)
    return "".join(w.capitalize() for w in cleaned.split())


def _to_member_name(value: str) -> str:
    """Convert an enum string value to a valid SCREAMING_SNAKE_CASE identifier."""
    s = re.sub(r"[^a-zA-Z0-9]", "_", str(value)).upper()
    # Strip leading/trailing underscores BEFORE the digit-prefix guard so that
    # values like "#00B2B2" → "_00B2B2" → "00B2B2" are correctly prefixed.
    s = s.strip("_")
    if not s:
        s = "UNKNOWN"
    if s[0].isdigit():
        s = "VALUE_" + s
    # Avoid Python keywords (unlikely in UPPER but be safe)
    if keyword.iskeyword(s.lower()):
        s += "_"
    return s


def generate_enums(spec: dict[str, Any], version: str) -> None:
    """Write enum classes to ``teamleader/_generated/enums.py``."""
    schemas: dict[str, Any] = spec.get("components", {}).get("schemas", {})

    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    lines: list[str] = [_FILE_HEADER.format(version=version, timestamp=timestamp)]

    enum_count = 0
    for schema_name in sorted(schemas):
        schema = schemas[schema_name]
        if schema.get("type") != "string" or "enum" not in schema:
            continue

        class_name = _to_class_name(schema_name)
        raw_values: list[Any] = schema["enum"]

        lines.append(f'class {class_name}(str, Enum):')
        title = schema.get("title", schema_name)
        lines.append(f'    """Auto-generated from schema: {title}"""')
        lines.append("")

        seen: set[str] = set()
        for raw in raw_values:
            if raw is None:
                continue
            member = _to_member_name(str(raw))
            # Deduplicate collisions
            suffix = 0
            original = member
            while member in seen:
                suffix += 1
                member = f"{original}_{suffix}"
            seen.add(member)
            lines.append(f"    {member} = {str(raw)!r}")

        lines.append("")
        lines.append("")
        enum_count += 1

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text("\n".join(lines), encoding="utf-8")
    print(f"  Wrote {enum_count} enum classes → {OUTPUT_PATH.name}")
