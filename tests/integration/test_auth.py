"""Integration tests for the auth layer.

These tests hit the REAL Teamleader token endpoint.
They are skipped automatically when TEAMLEADER_INTEGRATION_CLIENT_ID is absent
(handled by tests/integration/conftest.py).

Required environment variables:
    TEAMLEADER_INTEGRATION_CLIENT_ID
    TEAMLEADER_INTEGRATION_CLIENT_SECRET
    TEAMLEADER_INTEGRATION_REDIRECT_URI
    TEAMLEADER_INTEGRATION_ACCESS_TOKEN
    TEAMLEADER_INTEGRATION_REFRESH_TOKEN
    TEAMLEADER_INTEGRATION_EXPIRES_AT   — ISO-8601 UTC string, e.g. 2024-12-31T12:00:00+00:00
"""

from __future__ import annotations

import os
from datetime import datetime, timedelta, timezone

import pytest

from teamleader.auth import MemoryTokenBackend, OAuth2Handler, Token


def _env(key: str) -> str:
    value = os.environ.get(key, "")
    if not value:
        pytest.skip(f"Environment variable {key!r} is not set")
    return value


@pytest.fixture()
def integration_backend() -> MemoryTokenBackend:
    """MemoryTokenBackend pre-loaded from environment variables."""
    access_token = _env("TEAMLEADER_INTEGRATION_ACCESS_TOKEN")
    refresh_token = _env("TEAMLEADER_INTEGRATION_REFRESH_TOKEN")
    raw_expires = _env("TEAMLEADER_INTEGRATION_EXPIRES_AT")
    expires_at = datetime.fromisoformat(raw_expires)
    if expires_at.tzinfo is None:
        expires_at = expires_at.replace(tzinfo=timezone.utc)

    backend = MemoryTokenBackend()
    backend.save(Token(access_token=access_token, refresh_token=refresh_token, expires_at=expires_at))
    return backend


@pytest.fixture()
def integration_handler(integration_backend: MemoryTokenBackend) -> OAuth2Handler:
    return OAuth2Handler(
        client_id=_env("TEAMLEADER_INTEGRATION_CLIENT_ID"),
        client_secret=_env("TEAMLEADER_INTEGRATION_CLIENT_SECRET"),
        redirect_uri=_env("TEAMLEADER_INTEGRATION_REDIRECT_URI"),
        token_backend=integration_backend,
    )


class TestIntegrationAuth:
    def test_get_valid_token_with_stored_credentials(
        self,
        integration_handler: OAuth2Handler,
        integration_backend: MemoryTokenBackend,
    ) -> None:
        """get_valid_token() returns a non-empty string when credentials are valid."""
        token = integration_handler.get_valid_token()
        assert isinstance(token, str)
        assert len(token) > 0

    def test_refresh_token_rotation(
        self,
        integration_handler: OAuth2Handler,
        integration_backend: MemoryTokenBackend,
    ) -> None:
        """Force a refresh by back-dating expires_at; new token must be stored."""
        stored = integration_backend.get()
        assert stored is not None

        # Back-date expires_at so the token looks expired
        backdated = Token(
            access_token=stored.access_token,
            refresh_token=stored.refresh_token,
            expires_at=datetime.now(tz=timezone.utc) - timedelta(seconds=10),
        )
        integration_backend.save(backdated)

        new_access_token = integration_handler.get_valid_token()

        # A new (different) access token should have been issued
        assert isinstance(new_access_token, str)
        assert new_access_token != stored.access_token

        # Backend must now hold the refreshed token
        refreshed = integration_backend.get()
        assert refreshed is not None
        assert refreshed.access_token == new_access_token
