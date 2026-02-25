"""Django AppConfig for the Teamleader SDK."""

from __future__ import annotations

from django.apps import AppConfig

#: Keys that *must* be present in ``settings.TEAMLEADER``.
REQUIRED_SETTINGS_KEYS: frozenset[str] = frozenset(
    {"CLIENT_ID", "CLIENT_SECRET", "REDIRECT_URI", "SCOPES"}
)


class TeamleaderConfig(AppConfig):
    """AppConfig that validates ``settings.TEAMLEADER`` on startup.

    Add ``"teamleader.django"`` to ``INSTALLED_APPS`` and define a
    ``TEAMLEADER`` dict in your settings file::

        TEAMLEADER = {
            "CLIENT_ID": "...",
            "CLIENT_SECRET": "...",
            "REDIRECT_URI": "http://localhost:9999/callback",
            "SCOPES": ["contacts", "deals"],
        }

    :meth:`ready` will raise
    :class:`django.core.exceptions.ImproperlyConfigured` on startup if
    the dict is absent or any required key is missing, giving a clear,
    actionable error message rather than a late ``KeyError`` at runtime.
    """

    name = "teamleader.django"
    label = "teamleader_django"
    verbose_name = "Teamleader SDK"
    default_auto_field = "django.db.models.BigAutoField"

    def ready(self) -> None:
        """Validate required ``settings.TEAMLEADER`` keys on startup.

        Raises
        ------
        django.core.exceptions.ImproperlyConfigured
            If ``settings.TEAMLEADER`` is absent, is not a ``dict``, or is
            missing one or more of :data:`REQUIRED_SETTINGS_KEYS`.
        """
        from django.conf import settings
        from django.core.exceptions import ImproperlyConfigured

        cfg = getattr(settings, "TEAMLEADER", None)

        if not isinstance(cfg, dict):
            raise ImproperlyConfigured(
                "settings.TEAMLEADER is missing or is not a dict.\n"
                "Add the following to your settings.py:\n\n"
                "    TEAMLEADER = {\n"
                '        "CLIENT_ID": "...",\n'
                '        "CLIENT_SECRET": "...",\n'
                '        "REDIRECT_URI": "http://localhost:9999/callback",\n'
                '        "SCOPES": ["contacts", "deals"],\n'
                "    }\n\n"
                f"Required keys: {sorted(REQUIRED_SETTINGS_KEYS)}"
            )

        missing = REQUIRED_SETTINGS_KEYS - cfg.keys()
        if missing:
            raise ImproperlyConfigured(
                f"settings.TEAMLEADER is missing required key(s): "
                f"{sorted(missing)}\n"
                f"All required keys: {sorted(REQUIRED_SETTINGS_KEYS)}"
            )


default_app_config = "teamleader.django.apps.TeamleaderConfig"
