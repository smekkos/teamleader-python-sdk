"""OAuth2 Authorization Code flow with refresh token rotation.

Full implementation in Phase 4.  Stubs are provided here so the
package is importable during the scaffold phase.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    pass


@dataclass
class Token:
    """Holds a Teamleader OAuth2 token pair and its expiry time."""

    access_token: str
    refresh_token: str
    expires_at: datetime

    @property
    def is_expired(self) -> bool:
        """Return True if the token expires within the safety margin."""
        raise NotImplementedError  # Phase 4


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


class OAuth2Handler:
    """Manages the full OAuth2 lifecycle for a Teamleader application.

    Full implementation in Phase 4.
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

    def get_authorization_url(self) -> str:
        """Build the Teamleader OAuth authorisation URL."""
        raise NotImplementedError  # Phase 4

    def exchange_code(self, code: str) -> Token:
        """Exchange an authorisation code for tokens and persist them."""
        raise NotImplementedError  # Phase 4

    def get_valid_token(self) -> str:
        """Return a valid access token, refreshing if necessary."""
        raise NotImplementedError  # Phase 4

    def _refresh(self, token: Token) -> Token:
        """Use the refresh token to obtain a new access token."""
        raise NotImplementedError  # Phase 4
