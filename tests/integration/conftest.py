"""Integration test fixtures.

Full implementation in Phase 11.

Auto-skips all integration tests when TEAMLEADER_INTEGRATION_CLIENT_ID
is not set in the environment, so CI passes without real credentials.
"""

from __future__ import annotations

import os

import pytest


def pytest_collection_modifyitems(items: list[pytest.Item]) -> None:
    """Skip integration tests when credentials are absent."""
    if not os.getenv("TEAMLEADER_INTEGRATION_CLIENT_ID"):
        skip = pytest.mark.skip(reason="Integration credentials not set in environment")
        for item in items:
            if "integration" in str(item.fspath):
                item.add_marker(skip)
