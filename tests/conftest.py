"""Shared pytest fixtures for unit tests.

Full implementation in Phase 11.
"""

from __future__ import annotations

# Fixtures will include:
#   - client: TeamleaderClient with MemoryTokenBackend pre-loaded with a valid token
#   - expired_client: TeamleaderClient with an expired access token
#   - mock_responses: responses library activation context
