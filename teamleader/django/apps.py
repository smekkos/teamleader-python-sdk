"""Django AppConfig for the Teamleader SDK.

Full implementation in Phase 10 (settings validation in ready()).
Stub is provided here so Django can discover the app.
"""

from __future__ import annotations

from django.apps import AppConfig


class TeamleaderConfig(AppConfig):
    name = "teamleader.django"
    label = "teamleader_django"
    verbose_name = "Teamleader SDK"
    default_auto_field = "django.db.models.BigAutoField"

    def ready(self) -> None:
        """Validate required settings on startup.

        Full implementation in Phase 10.
        """
        pass  # Phase 10


default_app_config = "teamleader.django.apps.TeamleaderConfig"
