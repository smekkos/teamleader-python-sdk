"""Shared pytest fixtures for unit tests."""

from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone

import pytest
import responses as responses_lib

from teamleader.auth import MemoryTokenBackend, OAuth2Handler, Token
from teamleader.constants import TOKEN_URL


# ---------------------------------------------------------------------------
# Token fixtures
# ---------------------------------------------------------------------------

FROZEN_NOW = datetime(2024, 6, 1, 12, 0, 0, tzinfo=timezone.utc)


def _make_token(
    *,
    access_token: str = "acc_valid",
    refresh_token: str = "ref_valid",
    delta_seconds: int = 300,
) -> Token:
    return Token(
        access_token=access_token,
        refresh_token=refresh_token,
        expires_at=FROZEN_NOW + timedelta(seconds=delta_seconds),
    )


@pytest.fixture()
def backend() -> MemoryTokenBackend:
    """A fresh, empty MemoryTokenBackend."""
    return MemoryTokenBackend()


@pytest.fixture()
def valid_token(backend: MemoryTokenBackend) -> Token:
    """A Token expiring in 300 s (well outside the 60 s margin), pre-loaded."""
    token = _make_token(delta_seconds=300)
    backend.save(token)
    return token


@pytest.fixture()
def expired_token(backend: MemoryTokenBackend) -> Token:
    """A Token whose expires_at is 10 s in the past, pre-loaded."""
    token = _make_token(access_token="acc_expired", delta_seconds=-10)
    backend.save(token)
    return token


@pytest.fixture()
def handler(backend: MemoryTokenBackend) -> OAuth2Handler:
    """An OAuth2Handler wired to the shared MemoryTokenBackend fixture."""
    return OAuth2Handler(
        client_id="test_client_id",
        client_secret="test_client_secret",
        redirect_uri="http://localhost:9999/callback",
        token_backend=backend,
        scopes=["contacts", "deals"],
    )


# ---------------------------------------------------------------------------
# Helpers used by multiple test modules
# ---------------------------------------------------------------------------

def token_response_body(
    *,
    access_token: str = "acc_new",
    refresh_token: str = "ref_new",
    expires_in: int = 3600,
) -> str:
    """Return a JSON string matching the Teamleader token endpoint format."""
    return json.dumps(
        {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "Bearer",
            "expires_in": expires_in,
        }
    )
