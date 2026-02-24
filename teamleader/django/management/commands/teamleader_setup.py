"""Management command: python manage.py teamleader_setup

Walks the user through the OAuth2 authorization flow, starts a
temporary local HTTP server to capture the redirect, exchanges the
authorization code for tokens, and persists them via
DatabaseTokenBackend.

Full implementation in Phase 5.
"""

from __future__ import annotations

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = (
        "Authorize the Teamleader SDK via OAuth2 and save tokens to the database. "
        "Run this once per environment after initial deployment."
    )

    def handle(self, *args: object, **options: object) -> None:
        """Full implementation in Phase 5."""
        raise NotImplementedError  # Phase 5
