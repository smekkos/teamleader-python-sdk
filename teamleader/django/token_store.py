"""DatabaseTokenBackend — Django ORM implementation of TokenBackend.

Stores and retrieves the OAuth2 token from the ``TeamleaderToken``
singleton model.  All writes go through ``transaction.atomic()`` with
``select_for_update()`` to prevent double-saves in multi-worker
deployments (e.g. gunicorn with multiple workers).
"""

from __future__ import annotations

from teamleader.auth import Token, TokenBackend


class DatabaseTokenBackend(TokenBackend):
    """Stores the OAuth2 token in the ``TeamleaderToken`` Django model.

    Uses ``select_for_update()`` inside ``transaction.atomic()`` to
    prevent race conditions in multi-worker deployments.
    """

    def get(self) -> Token | None:
        """Return the stored token, or ``None`` if no row exists yet."""
        # Import here to avoid Django app-registry issues at module load time.
        from teamleader.django.models import TeamleaderToken

        try:
            obj = TeamleaderToken.objects.get(pk=1)
        except TeamleaderToken.DoesNotExist:
            return None

        return Token(
            access_token=obj.access_token,
            refresh_token=obj.refresh_token,
            expires_at=obj.expires_at,
        )

    def save(self, token: Token) -> None:
        """Upsert the singleton row inside a serialisable transaction."""
        from django.db import transaction

        from teamleader.django.models import TeamleaderToken

        with transaction.atomic():
            # Lock the row (or the gap) so concurrent workers don't race.
            obj = TeamleaderToken.objects.select_for_update().filter(pk=1).first()
            if obj is None:
                obj = TeamleaderToken(pk=1)
            obj.access_token = token.access_token
            obj.refresh_token = token.refresh_token
            obj.expires_at = token.expires_at
            obj.save()

    def clear(self) -> None:
        """Delete the singleton row (no-op if it does not exist)."""
        from teamleader.django.models import TeamleaderToken

        TeamleaderToken.objects.filter(pk=1).delete()
