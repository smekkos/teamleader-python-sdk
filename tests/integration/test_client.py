"""Integration tests for TeamleaderClient — Phase 6.

These tests hit the REAL Teamleader API and are skipped automatically when
TEAMLEADER_INTEGRATION_CLIENT_ID is absent (handled by conftest.py).

Required environment variables (same set as test_auth.py):
    TEAMLEADER_INTEGRATION_CLIENT_ID
    TEAMLEADER_INTEGRATION_CLIENT_SECRET
    TEAMLEADER_INTEGRATION_REDIRECT_URI
    TEAMLEADER_INTEGRATION_ACCESS_TOKEN
    TEAMLEADER_INTEGRATION_REFRESH_TOKEN
    TEAMLEADER_INTEGRATION_EXPIRES_AT   — ISO-8601 UTC string

What these tests prove beyond the unit tests
---------------------------------------------
Unit tests mock HTTP with the ``responses`` library using synthetic payloads.
These tests verify against the real API that:

1. ``_post`` with a valid list endpoint returns a dict with the expected keys —
   proving the Content-Type, session wiring, and response parsing work together.

2. A well-formed request for a non-existent resource raises
   ``TeamleaderNotFoundError`` with a non-empty message — proving
   ``_extract_message`` correctly parses real Teamleader 404 bodies.

3. A POST with a missing required field raises ``TeamleaderValidationError``
   with a non-empty message — proving real 422 body shape is handled.

4. A client call with a manually expired token transparently refreshes and
   still succeeds — exercising the ``_auth_headers()`` → ``get_valid_token()``
   → ``_refresh()`` seam under real network conditions.

Note on token rotation (test 4)
---------------------------------
``test_expired_token_is_transparently_refreshed`` force-expires the stored
token and performs a real refresh.  After the test the new token pair is
persisted back to ``.env`` via ``_persist_tokens_to_env()`` so subsequent
sessions do not start with a stale refresh token.  Run this test *last* if
you want to preserve the current token pair for other test runs.
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone

import pytest

from teamleader.auth import MemoryTokenBackend, OAuth2Handler, Token
from teamleader.client import TeamleaderClient
from teamleader.exceptions import TeamleaderNotFoundError, TeamleaderValidationError


def _persist_tokens_to_env(token: Token) -> None:
    """Rewrite updated token values back to the project .env file.

    Called after a successful token rotation so the next test session starts
    with valid credentials rather than a stale refresh token.
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


class TestIntegrationClient:
    def test_post_contacts_list_returns_data_dict(
        self,
        integration_client: TeamleaderClient,
    ) -> None:
        """_post with a real list endpoint returns a dict containing 'data' and 'meta'.

        This is the primary smoke test for the POST transport path: it proves
        that the Authorization header, Content-Type, and response parsing all
        work correctly against the live API.
        """
        result = integration_client._post(
            "contacts.list",
            {"page": {"size": 1, "number": 1}},
        )

        assert isinstance(result, dict), "Response should be a dict"
        assert "data" in result, "'data' key must be present in list response"
        assert "meta" in result, "'meta' key must be present in list response"

    def test_nonexistent_id_raises_not_found_with_message(
        self,
        integration_client: TeamleaderClient,
    ) -> None:
        """Requesting a UUID that does not exist raises TeamleaderNotFoundError.

        The nil UUID (all-zeros) is guaranteed not to exist in any Teamleader
        account.  This test proves that the real 404 response body shape is
        parseable by _extract_message and that the exception carries a
        non-empty human-readable message.
        """
        with pytest.raises(TeamleaderNotFoundError) as exc_info:
            integration_client._post(
                "contacts.info",
                {"id": "00000000-0000-0000-0000-000000000000"},
            )

        err = exc_info.value
        assert err.status_code == 404
        assert err.message, "Exception message should be non-empty"

    def test_invalid_body_raises_validation_error_with_message(
        self,
        integration_client: TeamleaderClient,
    ) -> None:
        """POSTing an empty body to contacts.add raises TeamleaderValidationError.

        contacts.add requires at minimum a first or last name.  An empty dict
        triggers a 422 Unprocessable Entity response.  This test proves that
        the real validation error body shape is handled correctly by
        _extract_message.
        """
        with pytest.raises(TeamleaderValidationError) as exc_info:
            integration_client._post("contacts.add", {})

        err = exc_info.value
        assert err.status_code == 422
        assert err.message, "Exception message should be non-empty"

    def test_expired_token_is_transparently_refreshed(
        self,
        integration_backend: MemoryTokenBackend,
        integration_handler: OAuth2Handler,
    ) -> None:
        """A client call with an expired token transparently refreshes and succeeds.

        This exercises the _auth_headers() → get_valid_token() → _refresh()
        seam under real network conditions — something the unit tests cannot
        prove.  The rotated token is persisted back to .env so subsequent
        sessions stay valid.
        """
        stored = integration_backend.get()
        assert stored is not None, "Backend must have a token pre-loaded"

        # Force the token to look expired
        backdated = Token(
            access_token=stored.access_token,
            refresh_token=stored.refresh_token,
            expires_at=datetime.now(tz=timezone.utc) - timedelta(seconds=10),
        )
        integration_backend.save(backdated)

        # Build the client AFTER back-dating so it starts with an expired token
        client = TeamleaderClient(integration_handler)

        # This must succeed — the client should refresh transparently
        result = client._get("users.me")

        assert isinstance(result, dict)
        assert "data" in result, "Refreshed call to users.me should return data"

        # The backend must now hold a new (different) access token
        rotated = integration_backend.get()
        assert rotated is not None
        assert rotated.access_token != stored.access_token, (
            "Access token should have been rotated after transparent refresh"
        )

        # Persist updated tokens so subsequent test sessions stay valid
        _persist_tokens_to_env(rotated)
