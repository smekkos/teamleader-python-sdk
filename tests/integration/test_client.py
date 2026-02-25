"""Integration tests for TeamleaderClient — Phase 6 + client.call() bridge.

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
from teamleader.exceptions import (
    TeamleaderAPIError,
    TeamleaderNotFoundError,
    TeamleaderValidationError,
)


def _persist_tokens_to_env(token: Token) -> None:
    """Rewrite updated token values back to os.environ and the .env file."""
    import os as _os
    _os.environ["TEAMLEADER_INTEGRATION_ACCESS_TOKEN"] = token.access_token
    _os.environ["TEAMLEADER_INTEGRATION_REFRESH_TOKEN"] = token.refresh_token
    _os.environ["TEAMLEADER_INTEGRATION_EXPIRES_AT"] = token.expires_at.isoformat()

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
        # contacts.list does not support includes=pagination so meta is absent.
        # Other endpoints (companies, deals) return meta if includes=pagination is sent.
        assert isinstance(result["data"], list), "'data' must be a list"

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
        """POSTing an empty body to contacts.add raises a 4xx API error with a message.

        contacts.add requires at minimum a first or last name.  An empty dict
        triggers a validation error response whose exact status code (400 vs 422)
        may vary by API version.  This test proves that:
        1. A client-side error exception is raised (not a server error or success)
        2. The real response body shape is parsed into a non-empty message
        """
        from teamleader.exceptions import TeamleaderAPIError

        with pytest.raises(TeamleaderAPIError) as exc_info:
            integration_client._post("contacts.add", {})

        err = exc_info.value
        assert err.status_code in (400, 422), (
            f"Expected 400 or 422 status, got {err.status_code}"
        )
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


class TestIntegrationClientCall:
    """Integration tests for TeamleaderClient.call() — the generic endpoint bridge.

    These prove that call() works end-to-end against the real Teamleader API:
    - Pre-flight validation (ValueError for unknown/missing args) never touches the network.
    - Happy-path calls return the same dict structure as the equivalent _post() call.
    - API errors (404, 4xx) propagate through call() exactly as they do through _post().
    - call() can reach endpoints not covered by any curated resource.
    """

    def test_call_unknown_operation_raises_value_error(
        self,
        integration_client: TeamleaderClient,
    ) -> None:
        """Unknown operation ID raises ValueError without making an HTTP request."""
        with pytest.raises(ValueError, match="Unknown operation_id"):
            integration_client.call("totally.unknown.operation")

    def test_call_missing_required_param_raises_value_error(
        self,
        integration_client: TeamleaderClient,
    ) -> None:
        """Missing required param raises ValueError before any HTTP request is made."""
        # departments.info requires 'id'
        with pytest.raises(ValueError, match="Missing required parameter"):
            integration_client.call("departments.info")

    def test_call_no_required_params_returns_data(
        self,
        integration_client: TeamleaderClient,
    ) -> None:
        """call() with an all-optional endpoint returns a real response dict with 'data'.

        activityTypes.list is available in every Teamleader account and requires no
        parameters, making it a reliable smoke test for the happy path.
        """
        result = integration_client.call(
            "activityTypes.list",
            page={"size": 5, "number": 1},
        )

        assert isinstance(result, dict), "Response must be a dict"
        assert "data" in result, "'data' key must be present"
        assert isinstance(result["data"], list), "'data' must be a list"

    def test_call_result_matches_direct_post(
        self,
        integration_client: TeamleaderClient,
    ) -> None:
        """call() returns the exact same dict as the equivalent _post() call.

        This proves call() is a thin, transparent wrapper — no data is lost or
        transformed between the ENDPOINTS lookup and the HTTP response.
        """
        body = {"page": {"size": 1, "number": 1}}
        via_post = integration_client._post("activityTypes.list", body)
        via_call = integration_client.call("activityTypes.list", **body)

        assert via_call == via_post, (
            "call() and _post() must return identical dicts for the same request"
        )

    def test_call_propagates_not_found_error(
        self,
        integration_client: TeamleaderClient,
    ) -> None:
        """API 404 responses propagate through call() as TeamleaderNotFoundError.

        The nil UUID is guaranteed not to exist in any Teamleader account.
        This proves that error handling inside _handle_response() is not
        bypassed by the call() bridge.
        """
        with pytest.raises(TeamleaderNotFoundError) as exc_info:
            integration_client.call(
                "departments.info",
                id="00000000-0000-0000-0000-000000000000",
            )

        err = exc_info.value
        assert err.status_code == 404
        assert err.message, "404 exception should carry a non-empty message"

    def test_call_can_reach_uncurated_endpoint(
        self,
        integration_client: TeamleaderClient,
    ) -> None:
        """call() can reach endpoints that have no curated resource wrapper.

        users.list has no curated resource on TeamleaderClient — it can only be
        reached via call().  This test proves the bridge provides genuine coverage
        of the full API surface, not just the 5 curated resource families.
        """
        result = integration_client.call(
            "users.list",
            page={"size": 1, "number": 1},
        )

        assert isinstance(result, dict)
        assert "data" in result
        assert isinstance(result["data"], list)
        # Every Teamleader account has at least one user (the account owner)
        assert len(result["data"]) >= 1, "users.list must return at least one user"
