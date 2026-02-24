"""Unit tests for DatabaseTokenBackend.

These tests hit a real in-memory SQLite database (configured in
tests/settings_test.py) so Django's ORM is fully exercised.

Marks:
    @pytest.mark.django_db  — required for any test that touches the database.

Run with:
    .venv/bin/python -m pytest tests/test_django_token_store.py -v
"""

from __future__ import annotations

from datetime import datetime, timezone

import pytest

from teamleader.auth import Token
from teamleader.django.token_store import DatabaseTokenBackend

# ---------------------------------------------------------------------------
# Fixtures / shared data
# ---------------------------------------------------------------------------

_TOKEN_A = Token(
    access_token="access_aaa",
    refresh_token="refresh_aaa",
    expires_at=datetime(2030, 1, 1, 12, 0, 0, tzinfo=timezone.utc),
)

_TOKEN_B = Token(
    access_token="access_bbb",
    refresh_token="refresh_bbb",
    expires_at=datetime(2030, 6, 1, 0, 0, 0, tzinfo=timezone.utc),
)


@pytest.fixture()
def backend() -> DatabaseTokenBackend:
    return DatabaseTokenBackend()


# ---------------------------------------------------------------------------
# get()
# ---------------------------------------------------------------------------


class TestDatabaseTokenBackendGet:
    @pytest.mark.django_db
    def test_returns_none_when_table_is_empty(self, backend: DatabaseTokenBackend) -> None:
        assert backend.get() is None

    @pytest.mark.django_db
    def test_returns_token_after_save(self, backend: DatabaseTokenBackend) -> None:
        backend.save(_TOKEN_A)
        result = backend.get()
        assert result is not None
        assert result.access_token == _TOKEN_A.access_token
        assert result.refresh_token == _TOKEN_A.refresh_token
        assert result.expires_at == _TOKEN_A.expires_at

    @pytest.mark.django_db
    def test_expires_at_is_timezone_aware(self, backend: DatabaseTokenBackend) -> None:
        """Round-trip must preserve timezone awareness (USE_TZ=True guards this)."""
        backend.save(_TOKEN_A)
        result = backend.get()
        assert result is not None
        assert result.expires_at.tzinfo is not None


# ---------------------------------------------------------------------------
# save()
# ---------------------------------------------------------------------------


class TestDatabaseTokenBackendSave:
    @pytest.mark.django_db
    def test_save_creates_exactly_one_row(self, backend: DatabaseTokenBackend) -> None:
        from teamleader.django.models import TeamleaderToken

        backend.save(_TOKEN_A)
        assert TeamleaderToken.objects.count() == 1

    @pytest.mark.django_db
    def test_save_uses_pk_one(self, backend: DatabaseTokenBackend) -> None:
        from teamleader.django.models import TeamleaderToken

        backend.save(_TOKEN_A)
        assert TeamleaderToken.objects.filter(pk=1).exists()

    @pytest.mark.django_db
    def test_second_save_does_not_create_new_row(self, backend: DatabaseTokenBackend) -> None:
        from teamleader.django.models import TeamleaderToken

        backend.save(_TOKEN_A)
        backend.save(_TOKEN_B)
        assert TeamleaderToken.objects.count() == 1

    @pytest.mark.django_db
    def test_second_save_overwrites_values(self, backend: DatabaseTokenBackend) -> None:
        backend.save(_TOKEN_A)
        backend.save(_TOKEN_B)
        result = backend.get()
        assert result is not None
        assert result.access_token == _TOKEN_B.access_token
        assert result.refresh_token == _TOKEN_B.refresh_token
        assert result.expires_at == _TOKEN_B.expires_at


# ---------------------------------------------------------------------------
# clear()
# ---------------------------------------------------------------------------


class TestDatabaseTokenBackendClear:
    @pytest.mark.django_db
    def test_clear_removes_row(self, backend: DatabaseTokenBackend) -> None:
        backend.save(_TOKEN_A)
        backend.clear()
        assert backend.get() is None

    @pytest.mark.django_db
    def test_clear_on_empty_table_is_noop(self, backend: DatabaseTokenBackend) -> None:
        """clear() must not raise when the table is empty."""
        backend.clear()  # Should not raise

    @pytest.mark.django_db
    def test_save_after_clear_creates_row_again(self, backend: DatabaseTokenBackend) -> None:
        backend.save(_TOKEN_A)
        backend.clear()
        backend.save(_TOKEN_B)
        result = backend.get()
        assert result is not None
        assert result.access_token == _TOKEN_B.access_token

    @pytest.mark.django_db
    def test_clear_is_idempotent(self, backend: DatabaseTokenBackend) -> None:
        """Calling clear() twice must not raise."""
        backend.save(_TOKEN_A)
        backend.clear()
        backend.clear()  # Second clear — no row exists, must not raise


# ---------------------------------------------------------------------------
# Full lifecycle
# ---------------------------------------------------------------------------


class TestDatabaseTokenBackendLifecycle:
    @pytest.mark.django_db
    def test_full_save_get_overwrite_get_clear_cycle(
        self, backend: DatabaseTokenBackend
    ) -> None:
        assert backend.get() is None

        backend.save(_TOKEN_A)
        first = backend.get()
        assert first is not None
        assert first.access_token == _TOKEN_A.access_token

        backend.save(_TOKEN_B)
        second = backend.get()
        assert second is not None
        assert second.access_token == _TOKEN_B.access_token

        backend.clear()
        assert backend.get() is None
