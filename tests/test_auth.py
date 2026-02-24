"""Unit tests for the auth layer (teamleader/auth.py).

Coverage targets:
- Token.is_expired             — boundary conditions, naive datetime normalisation
- MemoryTokenBackend           — get / save / clear / overwrite
- OAuth2Handler.get_authorization_url()
- OAuth2Handler.exchange_code()
- OAuth2Handler.get_valid_token()
- OAuth2Handler._refresh()
"""

from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone

import pytest
import responses
from freezegun import freeze_time

from teamleader.auth import MemoryTokenBackend, OAuth2Handler, Token
from teamleader.constants import AUTHORIZATION_URL, TOKEN_URL
from teamleader.exceptions import TeamleaderAuthError, TeamleaderAuthExpiredError
from tests.conftest import FROZEN_NOW, token_response_body


# ===========================================================================
# Token.is_expired
# ===========================================================================


class TestTokenIsExpired:
    """Tests for the is_expired property using a frozen reference point."""

    def _token(self, delta_seconds: int, *, naive: bool = False) -> Token:
        expires_at = FROZEN_NOW + timedelta(seconds=delta_seconds)
        if naive:
            expires_at = expires_at.replace(tzinfo=None)
        return Token("a", "r", expires_at)

    @freeze_time(FROZEN_NOW)
    def test_not_expired_far_future(self) -> None:
        """Token expiring in 120 s is not expired (well outside 60 s margin)."""
        assert self._token(120).is_expired is False

    @freeze_time(FROZEN_NOW)
    def test_expired_within_margin(self) -> None:
        """Token expiring in 30 s is considered expired (< 60 s margin)."""
        assert self._token(30).is_expired is True

    @freeze_time(FROZEN_NOW)
    def test_expired_in_past(self) -> None:
        """Token whose expires_at is already past is expired."""
        assert self._token(-1).is_expired is True

    @freeze_time(FROZEN_NOW)
    def test_exactly_at_margin_boundary(self) -> None:
        """Token expiring in exactly 60 s is NOT expired (boundary: remaining == 60, not < 60)."""
        assert self._token(60).is_expired is False

    @freeze_time(FROZEN_NOW)
    def test_naive_datetime_treated_as_utc(self) -> None:
        """Naive expires_at is treated as UTC; a future naive datetime is not expired."""
        assert self._token(120, naive=True).is_expired is False

    @freeze_time(FROZEN_NOW)
    def test_naive_expired_datetime_treated_as_utc(self) -> None:
        """Naive expires_at in the past is expired even without tzinfo."""
        assert self._token(-1, naive=True).is_expired is True


# ===========================================================================
# MemoryTokenBackend
# ===========================================================================


class TestMemoryTokenBackend:
    def test_get_returns_none_initially(self, backend: MemoryTokenBackend) -> None:
        assert backend.get() is None

    def test_save_and_get(self, backend: MemoryTokenBackend, valid_token: Token) -> None:
        # valid_token fixture already called backend.save(); just verify
        assert backend.get() is valid_token

    def test_clear(self, backend: MemoryTokenBackend, valid_token: Token) -> None:
        backend.clear()
        assert backend.get() is None

    def test_overwrite(self, backend: MemoryTokenBackend) -> None:
        token_a = Token("a_acc", "a_ref", FROZEN_NOW + timedelta(seconds=300))
        token_b = Token("b_acc", "b_ref", FROZEN_NOW + timedelta(seconds=300))
        backend.save(token_a)
        backend.save(token_b)
        assert backend.get() is token_b

    def test_clear_then_save(self, backend: MemoryTokenBackend) -> None:
        token = Token("acc", "ref", FROZEN_NOW + timedelta(seconds=300))
        backend.save(token)
        backend.clear()
        backend.save(token)
        assert backend.get() is token


# ===========================================================================
# OAuth2Handler.get_authorization_url()
# ===========================================================================


class TestGetAuthorizationUrl:
    def test_starts_with_authorization_url(self, handler: OAuth2Handler) -> None:
        assert handler.get_authorization_url().startswith(AUTHORIZATION_URL)

    def test_contains_client_id(self, handler: OAuth2Handler) -> None:
        assert "client_id=test_client_id" in handler.get_authorization_url()

    def test_contains_redirect_uri(self, handler: OAuth2Handler) -> None:
        url = handler.get_authorization_url()
        # encoded or literal — the value must appear in some form
        assert "localhost" in url and "9999" in url

    def test_contains_scopes(self, handler: OAuth2Handler) -> None:
        url = handler.get_authorization_url()
        assert "scope=" in url
        assert "contacts" in url
        assert "deals" in url

    def test_response_type_code(self, handler: OAuth2Handler) -> None:
        assert "response_type=code" in handler.get_authorization_url()

    def test_no_scope_param_when_empty(self, backend: MemoryTokenBackend) -> None:
        h = OAuth2Handler("cid", "csec", "http://cb", backend, scopes=[])
        assert "scope=" not in h.get_authorization_url()


# ===========================================================================
# OAuth2Handler.exchange_code()
# ===========================================================================


class TestExchangeCode:
    @responses.activate
    def test_happy_path_returns_token(self, handler: OAuth2Handler, backend: MemoryTokenBackend) -> None:
        responses.add(
            responses.POST,
            TOKEN_URL,
            body=token_response_body(access_token="acc_new", refresh_token="ref_new"),
            content_type="application/json",
            status=200,
        )
        token = handler.exchange_code("auth_code_123")
        assert token.access_token == "acc_new"
        assert token.refresh_token == "ref_new"

    @responses.activate
    def test_saves_to_backend(self, handler: OAuth2Handler, backend: MemoryTokenBackend) -> None:
        responses.add(
            responses.POST,
            TOKEN_URL,
            body=token_response_body(),
            content_type="application/json",
            status=200,
        )
        handler.exchange_code("code")
        assert backend.get() is not None
        assert backend.get().access_token == "acc_new"  # type: ignore[union-attr]

    @responses.activate
    def test_http_error_raises_auth_error(self, handler: OAuth2Handler) -> None:
        responses.add(responses.POST, TOKEN_URL, status=400, body="Bad request")
        with pytest.raises(TeamleaderAuthError) as exc_info:
            handler.exchange_code("bad_code")
        assert exc_info.value.status_code == 400
        # Must NOT be the Expired subclass — it's a plain auth error
        assert not isinstance(exc_info.value, TeamleaderAuthExpiredError)

    @responses.activate
    def test_malformed_json_raises_auth_error(self, handler: OAuth2Handler) -> None:
        responses.add(
            responses.POST,
            TOKEN_URL,
            body=json.dumps({"token_type": "Bearer"}),  # missing access_token
            content_type="application/json",
            status=200,
        )
        with pytest.raises(TeamleaderAuthError):
            handler.exchange_code("code")

    @responses.activate
    def test_expires_at_is_utc_aware(self, handler: OAuth2Handler) -> None:
        responses.add(
            responses.POST,
            TOKEN_URL,
            body=token_response_body(expires_in=3600),
            content_type="application/json",
            status=200,
        )
        token = handler.exchange_code("code")
        assert token.expires_at.tzinfo is not None


# ===========================================================================
# OAuth2Handler.get_valid_token()
# ===========================================================================


class TestGetValidToken:
    def test_no_token_stored_raises_auth_error(
        self, handler: OAuth2Handler, backend: MemoryTokenBackend
    ) -> None:
        # backend is empty (no valid_token fixture loaded)
        with pytest.raises(TeamleaderAuthError) as exc_info:
            handler.get_valid_token()
        # Must be the base auth error, not the Expired subclass
        assert not isinstance(exc_info.value, TeamleaderAuthExpiredError)

    @freeze_time(FROZEN_NOW)
    def test_valid_token_returned_without_http(
        self, handler: OAuth2Handler, valid_token: Token
    ) -> None:
        """A non-expired token is returned directly; no HTTP call should be made."""
        result = handler.get_valid_token()
        assert result == "acc_valid"

    @responses.activate
    @freeze_time(FROZEN_NOW)
    def test_expired_token_triggers_refresh(
        self, handler: OAuth2Handler, expired_token: Token, backend: MemoryTokenBackend
    ) -> None:
        responses.add(
            responses.POST,
            TOKEN_URL,
            body=token_response_body(access_token="acc_refreshed"),
            content_type="application/json",
            status=200,
        )
        result = handler.get_valid_token()
        assert result == "acc_refreshed"
        assert backend.get().access_token == "acc_refreshed"  # type: ignore[union-attr]

    @responses.activate
    @freeze_time(FROZEN_NOW)
    def test_expired_token_refresh_fails_raises_expired(
        self, handler: OAuth2Handler, expired_token: Token
    ) -> None:
        responses.add(responses.POST, TOKEN_URL, status=401, body="Unauthorized")
        with pytest.raises(TeamleaderAuthExpiredError):
            handler.get_valid_token()


# ===========================================================================
# OAuth2Handler._refresh()
# ===========================================================================


class TestRefresh:
    @responses.activate
    def test_happy_path_returns_new_token(
        self, handler: OAuth2Handler, expired_token: Token, backend: MemoryTokenBackend
    ) -> None:
        responses.add(
            responses.POST,
            TOKEN_URL,
            body=token_response_body(access_token="acc_r", refresh_token="ref_r"),
            content_type="application/json",
            status=200,
        )
        new_token = handler._refresh(expired_token)
        assert new_token.access_token == "acc_r"
        assert new_token.refresh_token == "ref_r"

    @responses.activate
    def test_refresh_updates_backend(
        self, handler: OAuth2Handler, expired_token: Token, backend: MemoryTokenBackend
    ) -> None:
        responses.add(
            responses.POST,
            TOKEN_URL,
            body=token_response_body(access_token="acc_updated"),
            content_type="application/json",
            status=200,
        )
        handler._refresh(expired_token)
        assert backend.get().access_token == "acc_updated"  # type: ignore[union-attr]

    @responses.activate
    def test_refresh_sends_refresh_token_to_endpoint(
        self, handler: OAuth2Handler, expired_token: Token
    ) -> None:
        responses.add(
            responses.POST,
            TOKEN_URL,
            body=token_response_body(),
            content_type="application/json",
            status=200,
        )
        handler._refresh(expired_token)
        request_body = responses.calls[0].request.body
        assert "refresh_token" in request_body
        assert expired_token.refresh_token in request_body

    @responses.activate
    def test_refresh_401_raises_auth_expired(
        self, handler: OAuth2Handler, expired_token: Token
    ) -> None:
        responses.add(responses.POST, TOKEN_URL, status=401, body="Unauthorized")
        with pytest.raises(TeamleaderAuthExpiredError):
            handler._refresh(expired_token)

    @responses.activate
    def test_refresh_500_raises_auth_expired(
        self, handler: OAuth2Handler, expired_token: Token
    ) -> None:
        responses.add(responses.POST, TOKEN_URL, status=500, body="Server Error")
        with pytest.raises(TeamleaderAuthExpiredError):
            handler._refresh(expired_token)

    @responses.activate
    def test_refresh_expired_error_is_subclass_of_auth_error(
        self, handler: OAuth2Handler, expired_token: Token
    ) -> None:
        """TeamleaderAuthExpiredError must be catchable as TeamleaderAuthError."""
        responses.add(responses.POST, TOKEN_URL, status=401, body="Unauthorized")
        with pytest.raises(TeamleaderAuthError):
            handler._refresh(expired_token)
