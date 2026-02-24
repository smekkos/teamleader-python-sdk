"""Integration tests for the auth layer.

These tests hit the REAL Teamleader token endpoint and API.
They are skipped automatically when TEAMLEADER_INTEGRATION_CLIENT_ID is absent
(handled by tests/integration/conftest.py).

Required environment variables:
    TEAMLEADER_INTEGRATION_CLIENT_ID
    TEAMLEADER_INTEGRATION_CLIENT_SECRET
    TEAMLEADER_INTEGRATION_REDIRECT_URI
    TEAMLEADER_INTEGRATION_ACCESS_TOKEN
    TEAMLEADER_INTEGRATION_REFRESH_TOKEN
    TEAMLEADER_INTEGRATION_EXPIRES_AT   — ISO-8601 UTC string, e.g. 2024-12-31T12:00:00+00:00

Note on refresh token rotation:
    test_refresh_token_rotation consumes (and rotates) the refresh token stored
    in .env.  Re-run `python get_tokens.py` to refresh .env before the next
    integration test session.  test_stored_access_token_is_accepted_by_api
    does NOT consume the refresh token — run it first if you want to preserve
    the stored token for later.
"""

from __future__ import annotations

import os
from datetime import datetime, timedelta, timezone

import pytest
import requests as http_requests

from teamleader.auth import MemoryTokenBackend, OAuth2Handler, Token
from teamleader.constants import BASE_URL


def _persist_tokens_to_env(token: Token) -> None:
    """Write updated token values back to the project .env file.

    Called after a successful token rotation so the next test session
    starts with valid credentials rather than a stale refresh token.
    No-op if python-dotenv is not installed or no .env file is found.
    """
    try:
        from dotenv import find_dotenv, set_key  # type: ignore[import]
    except ImportError:
        return

    dotenv_path = find_dotenv(usecwd=True)
    if not dotenv_path:
        return

    set_key(dotenv_path, "TEAMLEADER_INTEGRATION_ACCESS_TOKEN", token.access_token)
    set_key(dotenv_path, "TEAMLEADER_INTEGRATION_REFRESH_TOKEN", token.refresh_token)
    set_key(dotenv_path, "TEAMLEADER_INTEGRATION_EXPIRES_AT", token.expires_at.isoformat())


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

        # Persist the new token pair to .env so the next test session has
        # valid credentials and does not fail with "Token has been revoked".
        _persist_tokens_to_env(refreshed)

    def test_stored_access_token_is_accepted_by_api(
        self,
        integration_handler: OAuth2Handler,
    ) -> None:
        """The access token from get_valid_token() must be accepted by the real API.

        Calls GET /users.me — a read-only endpoint that requires a valid
        access token.  This verifies the full auth chain end-to-end:
        credentials in .env → OAuth2Handler → real Teamleader API.

        Note: this test does NOT force a refresh, so it does not consume
        the refresh token and can be run repeatedly without re-running
        get_tokens.py.
        """
        access_token = integration_handler.get_valid_token()

        response = http_requests.get(
            f"{BASE_URL}/users.me",
            headers={"Authorization": f"Bearer {access_token}"},
            timeout=10,
        )

        assert response.status_code == 200, (
            f"Teamleader API rejected the access token: "
            f"{response.status_code} {response.text}"
        )
        data = response.json()
        assert "data" in data, f"Unexpected response shape: {data!r}"
