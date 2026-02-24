"""Django ORM model for persisting the Teamleader OAuth2 token.

Full implementation in Phase 5.

No migrations are shipped with this package.  After adding
``"teamleader.django"`` to ``INSTALLED_APPS`` run::

    python manage.py makemigrations teamleader_django
    python manage.py migrate
"""

from __future__ import annotations

from django.db import models


class TeamleaderToken(models.Model):
    """Singleton model that stores the active OAuth2 token.

    Only one row should ever exist.  The singleton constraint is
    enforced in ``save()`` — full implementation in Phase 5.
    """

    access_token = models.TextField()
    refresh_token = models.TextField()
    expires_at = models.DateTimeField()
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = "teamleader_django"

    def save(self, *args: object, **kwargs: object) -> None:
        """Enforce the singleton constraint before delegating to super."""
        raise NotImplementedError  # Phase 5

    def __str__(self) -> str:
        return f"TeamleaderToken(expires_at={self.expires_at})"
