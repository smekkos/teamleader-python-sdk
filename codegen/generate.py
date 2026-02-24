"""Master code generation entry point.

Usage::

    python codegen/generate.py

Fetches the latest ``@teamleader/focus-api-specification`` from npm,
regenerates all three ``_generated/`` files, and prints a summary.

After running, review changes and run tests before committing::

    git diff teamleader/_generated/
    pytest
"""

from __future__ import annotations

import sys
import time
from pathlib import Path

# Make the repo root importable when run as a script
sys.path.insert(0, str(Path(__file__).parent.parent))

from codegen.fetch_spec import fetch_spec
from codegen.generate_endpoints import generate_endpoints
from codegen.generate_enums import generate_enums
from codegen.generate_models import generate_models


def main() -> None:
    print("=" * 60)
    print("Teamleader SDK — code generator")
    print("=" * 60)

    t0 = time.monotonic()

    spec, version = fetch_spec()

    print(f"\nGenerating from spec v{version} …")
    generate_enums(spec, version)
    generate_models(spec, version)
    generate_endpoints(spec, version)

    elapsed = time.monotonic() - t0
    print(f"\nDone in {elapsed:.1f}s")
    print()
    print("Next steps:")
    print("  1. git diff teamleader/_generated/   ← review what changed")
    print("  2. pytest                             ← confirm nothing broke")
    print("  3. Fix any curated code broken by schema changes")
    print("  4. Commit _generated/ + fixes together with the version in the message")


if __name__ == "__main__":
    main()
