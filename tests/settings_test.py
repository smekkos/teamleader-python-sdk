"""Minimal Django settings used by pytest-django.

Includes a valid TEAMLEADER dict so that TeamleaderConfig.ready()
passes on startup — individual tests may override it via
``@override_settings(TEAMLEADER=...)``.

Not for production use.
"""

SECRET_KEY = "django-insecure-test-key-not-for-production"  # noqa: S105

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}

INSTALLED_APPS = [
    "django.contrib.contenttypes",
    "django.contrib.auth",
    "teamleader.django",
]

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Disable migrations for teamleader_django so pytest-django creates the table
# directly from the model definition (no migration files required).
MIGRATION_MODULES: dict[str, None] = {
    "teamleader_django": None,
}

# Store datetimes in UTC.
USE_TZ = True

# Minimal valid TEAMLEADER config so TeamleaderConfig.ready() passes at startup.
# Individual tests override this via @override_settings(TEAMLEADER=...).
TEAMLEADER = {
    "CLIENT_ID": "test-client-id",
    "CLIENT_SECRET": "test-client-secret",
    "REDIRECT_URI": "http://localhost:9999/callback",
    "SCOPES": ["contacts", "deals"],
}
