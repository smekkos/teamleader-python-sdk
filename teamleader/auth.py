"""OAuth2 Authorization Code flow with refresh token rotation.

Implements:
- Token          — dataclass holding an access/refresh token pair + expiry
- TokenBackend   — abstract storage interface
- MemoryTokenBackend — in-process backend for tests and non-Django use
- OAuth2Handler  — full OAuth2 lifecycle (authorize → exchange → refresh)
"""

from __future__ import annotations

import urllib.parse
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Any

import requests

from teamleader.constants import (
    AUTHORIZATION_URL,
    TOKEN_EXPIRY_MARGIN_SECONDS,
    TOKEN_URL,
)
from teamleader.exceptions import TeamleaderAuthError, TeamleaderAuthExpiredError


# ---------------------------------------------------------------------------
# Token dataclass
# ---------------------------------------------------------------------------


@dataclass
class Token:
    """Holds a Teamleader OAuth2 token pair and its expiry time."""

    access_token: str
    refresh_token: str
    expires_at: datetime

    @property
    def is_expired(self) -> bool:
        """Return True if the token expires within the safety margin.

        The safety margin (``TOKEN_EXPIRY_MARGIN_SECONDS``) means a token is
        considered expired 60 seconds *before* its actual expiry so that
        in-flight requests are never rejected mid-call.
        """
        now = datetime.now(tz=timezone.utc)
        # Normalise expires_at: if it is naive, assume UTC
        expires_at = self.expires_at
        if expires_at.tzinfo is None:
            expires_at = expires_at.replace(tzinfo=timezone.utc)

        remaining = (expires_at - now).total_seconds()
        return remaining < TOKEN_EXPIRY_MARGIN_SECONDS


# ---------------------------------------------------------------------------
# TokenBackend ABC
# ---------------------------------------------------------------------------


class TokenBackend(ABC):
    """Abstract storage backend for a single Token instance."""

    @abstractmethod
    def get(self) -> Token | None:
        """Return the stored token, or None if none exists."""

    @abstractmethod
    def save(self, token: Token) -> None:
        """Persist *token* to the backend."""

    @abstractmethod
    def clear(self) -> None:
        """Delete any stored token."""


# ---------------------------------------------------------------------------
# MemoryTokenBackend — in-process implementation
# ---------------------------------------------------------------------------


class MemoryTokenBackend(TokenBackend):
    """In-process token store — suitable for tests and non-Django use."""

    def __init__(self) -> None:
        self._token: Token | None = None

    def get(self) -> Token | None:
        return self._token

    def save(self, token: Token) -> None:
        self._token = token

    def clear(self) -> None:
        self._token = None


# ---------------------------------------------------------------------------
# OAuth2Handler
# ---------------------------------------------------------------------------


class OAuth2Handler:
    """Manages the full OAuth2 lifecycle for a Teamleader application.

    Usage::

        backend = MemoryTokenBackend()
        handler = OAuth2Handler(
            client_id="...",
            client_secret="...",
            redirect_uri="http://localhost:9999/callback",
            token_backend=backend,
            scopes=["contacts", "deals"],
        )

        # Step 1 — send the user to Teamleader
        url = handler.get_authorization_url()

        # Step 2 — Teamleader redirects back with ?code=...
        handler.exchange_code(request.GET["code"])

        # Step 3 — use in every API call
        access_token = handler.get_valid_token()
    """

    def __init__(
        self,
        client_id: str,
        client_secret: str,
        redirect_uri: str,
        token_backend: TokenBackend,
        scopes: list[str] | None = None,
    ) -> None:
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.token_backend = token_backend
        self.scopes = scopes or []

    # ------------------------------------------------------------------
    # Public interface
    # ------------------------------------------------------------------

    def get_authorization_url(self) -> str:
        """Build the Teamleader OAuth authorisation URL.

        Returns a fully-qualified URL the user must open in a browser.
        """
        params: dict[str, str] = {
            "client_id": self.client_id,
            "response_type": "code",
            "redirect_uri": self.redirect_uri,
        }
        if self.scopes:
            params["scope"] = " ".join(self.scopes)

        return f"{AUTHORIZATION_URL}?{urllib.parse.urlencode(params)}"

    def exchange_code(self, code: str) -> Token:
        """Exchange an authorisation *code* for tokens and persist them.

        Raises:
            TeamleaderAuthError: if the token endpoint returns a non-2xx
                response or the response body is unexpected.
        """
        payload: dict[str, str] = {
            "grant_type": "authorization_code",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "redirect_uri": self.redirect_uri,
            "code": code,
        }
        token = self._request_token(payload)
        self.token_backend.save(token)
        return token

    def get_valid_token(self) -> str:
        """Return a valid access token, refreshing if necessary.

        Raises:
            TeamleaderAuthError: if no token is stored (authorisation has
                never been performed).
            TeamleaderAuthExpiredError: if the refresh token has been
                revoked and the user must re-authorise.
        """
        token = self.token_backend.get()
        if token is None:
            raise TeamleaderAuthError(
                "No token stored. Run `python manage.py teamleader_setup` to "
                "authorise this application with Teamleader.",
            )

        if token.is_expired:
            token = self._refresh(token)

        return token.access_token

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _refresh(self, token: Token) -> Token:
        """Use the refresh token to obtain a new access/refresh token pair.

        Persists the new token via the backend on success.

        Raises:
            TeamleaderAuthExpiredError: if Teamleader rejects the refresh
                token (revoked or expired).
        """
        payload: dict[str, str] = {
            "grant_type": "refresh_token",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "refresh_token": token.refresh_token,
        }
        try:
            new_token = self._request_token(payload)
        except TeamleaderAuthError as exc:
            raise TeamleaderAuthExpiredError(
                "The Teamleader refresh token has been revoked or has expired. "
                "Re-authorise by running `python manage.py teamleader_setup`.",
                status_code=exc.status_code,
                raw_response=exc.raw_response,
            ) from exc

        self.token_backend.save(new_token)
        return new_token

    def _request_token(self, payload: dict[str, Any]) -> Token:
        """POST *payload* to TOKEN_URL and parse the response into a Token.

        Raises:
            TeamleaderAuthError: on any non-2xx HTTP response.
        """
        response = requests.post(TOKEN_URL, data=payload, timeout=30)

        if not response.ok:
            raise TeamleaderAuthError(
                f"Token request failed: {response.status_code} {response.text}",
                status_code=response.status_code,
                raw_response=response,
            )

        data: dict[str, Any] = response.json()

        try:
            access_token: str = data["access_token"]
            refresh_token: str = data["refresh_token"]
            expires_in: int = int(data["expires_in"])
        except (KeyError, TypeError, ValueError) as exc:
            raise TeamleaderAuthError(
                f"Unexpected token response format: {data!r}",
                raw_response=response,
            ) from exc

        expires_at = (
            datetime.now(tz=timezone.utc).replace(microsecond=0)
            + timedelta(seconds=expires_in)
        )

        return Token(
            access_token=access_token,
            refresh_token=refresh_token,
            expires_at=expires_at,
        )
