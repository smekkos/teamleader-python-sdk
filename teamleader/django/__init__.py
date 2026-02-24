"""Teamleader SDK — Django integration.

Import guard: raises a clear error if Django is not installed so that
non-Django users get an actionable message rather than an AttributeError.

Usage in Django projects::

    # settings.py
    INSTALLED_APPS = [
        ...
        "teamleader.django",
    ]

    TEAMLEADER = {
        "CLIENT_ID": "...",
        "CLIENT_SECRET": "...",
        "REDIRECT_URI": "http://localhost:9999/callback",
        "SCOPES": ["contacts", "deals"],
    }

    # anywhere in your code
    from teamleader.django import get_client

    client = get_client()
    deal = client.deals.get("some-uuid")

Full implementation in Phase 5.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

# ---------------------------------------------------------------------------
# Django availability guard — must run before any django import elsewhere
# in this subpackage.  The check is intentionally simple: if `import django`
# fails the user gets an actionable message instead of a bare ImportError.
# ---------------------------------------------------------------------------
try:
    import django  # noqa: F401
except ImportError as _exc:
    raise ImportError(
        "teamleader.django requires Django to be installed.\n"
        "Install it with:  pip install teamleader-sdk[django]\n"
        "Or add django>=4.2 to your project's dependencies."
    ) from _exc

if TYPE_CHECKING:
    from teamleader.client import TeamleaderClient


def get_client() -> TeamleaderClient:
    """Return a configured :class:`~teamleader.client.TeamleaderClient`.

    Reads ``settings.TEAMLEADER``, constructs a
    :class:`~teamleader.django.token_store.DatabaseTokenBackend`, and
    returns a ready-to-use client.

    Example::

        from teamleader.django import get_client

        client = get_client()
        deals = client.deals.list()
    """
    from django.conf import settings

    from teamleader.auth import OAuth2Handler
    from teamleader.client import TeamleaderClient
    from teamleader.django.token_store import DatabaseTokenBackend

    conf: dict = getattr(settings, "TEAMLEADER", {})

    backend = DatabaseTokenBackend()
    auth_handler = OAuth2Handler(
        client_id=conf["CLIENT_ID"],
        client_secret=conf["CLIENT_SECRET"],
        redirect_uri=conf["REDIRECT_URI"],
        token_backend=backend,
        scopes=conf.get("SCOPES", []),
    )
    return TeamleaderClient(auth_handler=auth_handler)
