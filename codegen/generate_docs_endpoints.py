"""MkDocs hook + standalone script: generate docs/api-reference/generated-endpoints.md.

When used as a mkdocs hook (hooks: entry in mkdocs.yml), MkDocs calls
``on_pre_build(config)`` before building the site.  The same file can be run
directly::

    python codegen/generate_docs_endpoints.py

The output is ``docs/api-reference/generated-endpoints.md`` — a grouped
reference table of every endpoint in the Teamleader Focus API spec, organised
by the tag that Teamleader uses (contacts, deals, invoices, …).
"""

from __future__ import annotations

import os
from pathlib import Path

import yaml

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

_REPO_ROOT = Path(__file__).resolve().parent.parent
_SPEC_PATH = _REPO_ROOT / "codegen" / "spec" / "api.yaml"
_OUT_PATH = _REPO_ROOT / "docs" / "api-reference" / "generated-endpoints.md"

# ---------------------------------------------------------------------------
# Tag display-name overrides (x-displayName from spec, hand-curated subset)
# ---------------------------------------------------------------------------

_TAG_DISPLAY: dict[str, str] = {}  # populated from spec x-displayName


# ---------------------------------------------------------------------------
# Core generator
# ---------------------------------------------------------------------------


def generate(spec_path: Path = _SPEC_PATH, out_path: Path = _OUT_PATH) -> None:
    """Read *spec_path* and write the grouped endpoint reference to *out_path*."""

    with spec_path.open(encoding="utf-8") as fh:
        spec: dict = yaml.safe_load(fh)

    version: str = spec.get("info", {}).get("version", "unknown")

    # Build tag → display-name map from spec tags list
    tag_display: dict[str, str] = {}
    for tag_entry in spec.get("tags", []):
        name = tag_entry.get("name", "")
        display = tag_entry.get("x-displayName") or name.replace("_", " ").title()
        tag_display[name] = display

    # Collect endpoints: tag → list of (path, summary, description)
    tag_endpoints: dict[str, list[tuple[str, str, str]]] = {}
    for path, path_item in spec.get("paths", {}).items():
        for _method, operation in path_item.items():
            tags: list[str] = operation.get("tags", ["other"])
            summary: str = operation.get("summary", path.lstrip("/"))
            description: str = (operation.get("description") or "").strip()
            # Only first sentence for brevity
            first_sentence = description.split("\n")[0].strip().rstrip(".")
            for tag in tags:
                tag_endpoints.setdefault(tag, []).append(
                    (path, summary, first_sentence)
                )

    # Build markdown
    lines: list[str] = [
        "# Generated API Endpoint Reference",
        "",
        "!!! note",
        f'    Auto-generated from `codegen/spec/api.yaml` (spec **v{version}**).',
        "    Run `python codegen/generate_docs_endpoints.py` to refresh after a spec update.",
        "",
        "Every Teamleader Focus API endpoint is a **POST** request.  The table below",
        "groups endpoints by the resource tag used in the official Teamleader documentation.",
        "",
        "---",
        "",
        "## Calling endpoints via `client.call()`",
        "",
        "Every endpoint listed here can be called through",
        "[`TeamleaderClient.call()`](client.md#teamleader.client.TeamleaderClient.call)",
        "using the **operation ID** shown in the table (the `• client.call()` column):",
        "",
        "```python",
        "# Example — list activity types (no required params)",
        'result = client.call("activityTypes.list", page={"size": 20, "number": 1})',
        'for item in result["data"]:',
        '    print(item["name"])',
        "",
        "# Example — fetch a department by ID (id is required)",
        'dept = client.call("departments.info", id="67c576e7-7e6f-465d-b6ab-a864f6e5e95b")',
        'print(dept["data"]["name"])',
        "```",
        "",
        "!!! tip",
        '    `call()` validates required parameters **before** making the HTTP request',
        "    and raises `ValueError` with a helpful message if any are missing.",
        "    The response is a raw `dict` — no model deserialisation.",
        "",
        "---",
        "",
    ]

    for tag in spec.get("tags", []):
        tag_name: str = tag.get("name", "")
        if tag_name not in tag_endpoints:
            continue
        display = tag_display.get(tag_name, tag_name.replace("_", " ").title())
        tag_desc: str = (tag.get("description") or "").strip()
        # Only first line of tag description
        tag_desc_short = tag_desc.split("\n")[0].strip() if tag_desc else ""

        lines.append(f"## {display}")
        lines.append("")
        if tag_desc_short:
            # Strip RST-style required-scopes lines that won't render nicely
            if "Required scopes" not in tag_desc_short:
                lines.append(tag_desc_short)
                lines.append("")

        lines.append("| Endpoint | Summary | Description | `client.call()` |")
        lines.append("|---|---|---|---|")
        for path, summary, desc in sorted(
            tag_endpoints[tag_name], key=lambda x: x[0]
        ):
            # Escape pipes in description
            desc_esc = desc.replace("|", "\\|")
            # operation_id is the path without the leading slash
            operation_id = path.lstrip("/")
            lines.append(
                f"| `{path}` | `{summary}` | {desc_esc} | `client.call({operation_id!r})` |"
            )
        lines.append("")
        lines.append("---")
        lines.append("")

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"[generate_docs_endpoints] wrote {out_path.relative_to(_REPO_ROOT)}")


# ---------------------------------------------------------------------------
# MkDocs hook entry point
# ---------------------------------------------------------------------------


def on_pre_build(config: object) -> None:  # noqa: ARG001
    """Called by MkDocs before the site build starts."""
    generate()


# ---------------------------------------------------------------------------
# Standalone entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    generate()
