"""Django ORM model for persisting the Teamleader OAuth2 token.

No migrations are shipped with this package.  After adding
``"teamleader.django"`` to ``INSTALLED_APPS`` run::

    python manage.py makemigrations teamleader_django
    python manage.py migrate
"""

from __future__ import annotations

from django.db import models


class TeamleaderToken(models.Model):
    """Singleton model that stores the active OAuth2 token.

    Only one row ever exists (pk=1).  The singleton constraint is
    enforced in ``save()`` by hard-pinning the primary key to 1 so that
    every subsequent call is an UPDATE rather than an INSERT.
    """

    access_token = models.TextField()
    refresh_token = models.TextField()
    expires_at = models.DateTimeField()
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = "teamleader_django"

    def save(self, *args: object, **kwargs: object) -> None:
        """Enforce the singleton constraint by pinning pk to 1."""
        self.pk = 1
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"TeamleaderToken(expires_at={self.expires_at})"
