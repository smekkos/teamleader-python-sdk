"""Minimal Django settings used by pytest-django when running
tests/test_django_token_store.py.

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
