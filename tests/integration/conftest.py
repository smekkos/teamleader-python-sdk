"""Integration test fixtures.

Auto-skips all integration tests when TEAMLEADER_INTEGRATION_CLIENT_ID
is not set in the environment (or .env file), so CI passes without
real credentials.

Full resource fixtures live in Phase 11.
"""

from __future__ import annotations

import os

import pytest

# Load .env from the project root if python-dotenv is installed.
# This lets developers run integration tests with just a .env file
# rather than having to export every variable into the shell.
try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass  # No python-dotenv — rely on real environment variables.


def pytest_collection_modifyitems(items: list[pytest.Item]) -> None:
    """Skip integration tests when credentials are absent."""
    if not os.getenv("TEAMLEADER_INTEGRATION_CLIENT_ID"):
        skip = pytest.mark.skip(reason="Integration credentials not set in environment")
        for item in items:
            if "integration" in str(item.fspath):
                item.add_marker(skip)
