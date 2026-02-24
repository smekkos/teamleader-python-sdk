"""Teamleader SDK exception hierarchy.

All exceptions inherit from TeamleaderError so callers can catch the
broadest class they care about:

    try:
        client.deals.get("some-id")
    except TeamleaderNotFoundError:
        ...
    except TeamleaderAuthError:
        ...
    except TeamleaderError:
        # catch-all for any SDK error

Implemented in Phase 3.  Stubs are provided here so the package is
importable before Phase 3 is complete.
"""

from __future__ import annotations

from typing import Any


class TeamleaderError(Exception):
    """Base class for every exception raised by this SDK."""

    def __init__(
        self,
        message: str = "",
        *,
        status_code: int | None = None,
        raw_response: Any = None,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.raw_response = raw_response

    def __repr__(self) -> str:  # pragma: no cover
        return (
            f"{self.__class__.__name__}("
            f"message={self.message!r}, "
            f"status_code={self.status_code!r})"
        )


# ---------------------------------------------------------------------------
# HTTP / network errors
# ---------------------------------------------------------------------------


class TeamleaderAPIError(TeamleaderError):
    """Raised when the Teamleader API returns an unexpected HTTP status."""


class TeamleaderNotFoundError(TeamleaderAPIError):
    """404 — the requested resource does not exist."""


class TeamleaderRateLimitError(TeamleaderAPIError):
    """429 — rate limit exceeded; inspect ``retry_after`` for back-off."""

    def __init__(
        self,
        message: str = "",
        *,
        status_code: int | None = 429,
        raw_response: Any = None,
        retry_after: int | None = None,
    ) -> None:
        super().__init__(message, status_code=status_code, raw_response=raw_response)
        self.retry_after = retry_after


class TeamleaderServerError(TeamleaderAPIError):
    """5xx — the Teamleader server returned an internal error."""


# ---------------------------------------------------------------------------
# Auth errors
# ---------------------------------------------------------------------------


class TeamleaderAuthError(TeamleaderError):
    """401 — request was not authenticated or the token is invalid."""


class TeamleaderAuthExpiredError(TeamleaderAuthError):
    """The refresh token has been revoked or has expired.

    The user must re-authorise via ``python manage.py teamleader_setup``.
    """


# ---------------------------------------------------------------------------
# Request errors
# ---------------------------------------------------------------------------


class TeamleaderValidationError(TeamleaderError):
    """422 — the request body failed server-side validation."""


class TeamleaderPermissionError(TeamleaderError):
    """403 — the OAuth token lacks the required scope for this operation."""
