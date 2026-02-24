"""Integration test fixtures.

Auto-skips all integration tests when TEAMLEADER_INTEGRATION_CLIENT_ID
is not set in the environment (or .env file), so CI passes without
real credentials.

Shared fixtures
---------------
``integration_backend``    — MemoryTokenBackend loaded from env vars
``integration_handler``    — OAuth2Handler wired to that backend
``integration_client``     — TeamleaderClient wrapping the handler

Each test module may define its own local fixtures with the same names to
shadow these conftest versions (e.g. ``test_auth.py`` does this).  That is
intentional — pytest resolves fixtures from the most-local scope first.
"""

from __future__ import annotations

import os
from datetime import datetime, timezone

import pytest

from teamleader.auth import MemoryTokenBackend, OAuth2Handler, Token
from teamleader.client import TeamleaderClient

# Load .env from the project root if python-dotenv is installed.
# This lets developers run integration tests with just a .env file
# rather than having to export every variable into the shell.
try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass  # No python-dotenv — rely on real environment variables.


def _env(key: str) -> str:
    """Return the value of *key* from the environment, or skip the test."""
    value = os.environ.get(key, "")
    if not value:
        pytest.skip(f"Environment variable {key!r} is not set")
    return value


def _persist_tokens_to_env(token: Token) -> None:
    """Rewrite updated token values back to the project .env file.

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


def pytest_collection_modifyitems(items: list[pytest.Item]) -> None:
    """Skip integration tests when credentials are absent."""
    if not os.getenv("TEAMLEADER_INTEGRATION_CLIENT_ID"):
        skip = pytest.mark.skip(reason="Integration credentials not set in environment")
        for item in items:
            if "integration" in str(item.fspath):
                item.add_marker(skip)


# ---------------------------------------------------------------------------
# Shared fixtures — available to all integration test modules
# ---------------------------------------------------------------------------


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
    """OAuth2Handler wired to the shared integration backend."""
    return OAuth2Handler(
        client_id=_env("TEAMLEADER_INTEGRATION_CLIENT_ID"),
        client_secret=_env("TEAMLEADER_INTEGRATION_CLIENT_SECRET"),
        redirect_uri=_env("TEAMLEADER_INTEGRATION_REDIRECT_URI"),
        token_backend=integration_backend,
    )


@pytest.fixture()
def integration_client(integration_handler: OAuth2Handler) -> TeamleaderClient:
    """TeamleaderClient wired to the real Teamleader API via integration credentials."""
    return TeamleaderClient(integration_handler)
