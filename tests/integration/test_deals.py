"""Integration tests against a real Teamleader sandbox account.

Full implementation in Phase 11.

Requires environment variables from .env (see .env.example):
- TEAMLEADER_INTEGRATION_CLIENT_ID
- TEAMLEADER_INTEGRATION_CLIENT_SECRET
- TEAMLEADER_INTEGRATION_ACCESS_TOKEN
- TEAMLEADER_INTEGRATION_REFRESH_TOKEN

Tests are read-only where possible; create+delete cycles are used
only when a list/get is insufficient.
"""

from __future__ import annotations
