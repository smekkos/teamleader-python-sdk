"""Unit tests for TeamleaderConfig.ready() settings validation — Phase 10.

Uses ``@override_settings`` to control the TEAMLEADER dict without
touching the shared test settings file.  No network I/O; no migrations.

Coverage
--------
- ready() raises ImproperlyConfigured when TEAMLEADER is absent
- ready() raises ImproperlyConfigured when TEAMLEADER is not a dict
- ready() raises ImproperlyConfigured when one required key is missing
- ready() raises ImproperlyConfigured when multiple required keys are missing
- Error message names the missing key(s)
- ready() returns normally when all required keys are present
- ready() accepts extra (non-required) keys without raising
"""

from __future__ import annotations

import pytest
from django.core.exceptions import ImproperlyConfigured
from django.test import override_settings

from teamleader.django.apps import REQUIRED_SETTINGS_KEYS, TeamleaderConfig


_VALID_TEAMLEADER = {
    "CLIENT_ID": "test-client-id",
    "CLIENT_SECRET": "test-client-secret",
    "REDIRECT_URI": "http://localhost:9999/callback",
    "SCOPES": ["contacts", "deals"],
}


def _call_ready() -> None:
    """Instantiate a fresh TeamleaderConfig and call ready()."""
    app = TeamleaderConfig("teamleader.django", __import__("teamleader.django"))
    app.ready()


# ---------------------------------------------------------------------------
# TEAMLEADER setting absent / wrong type
# ---------------------------------------------------------------------------


class TestReadyMissingOrInvalidSetting:
    @override_settings()
    def test_raises_when_teamleader_absent(self) -> None:
        """TEAMLEADER not set at all → ImproperlyConfigured."""
        # Remove TEAMLEADER from settings entirely (it's not in settings_test.py
        # so this is already the default, but be explicit with delattr guard).
        from django.conf import settings as dj_settings
        if hasattr(dj_settings, "TEAMLEADER"):
            del dj_settings.TEAMLEADER  # type: ignore[attr-defined]

        with pytest.raises(ImproperlyConfigured, match="missing or is not a dict"):
            _call_ready()

    @override_settings(TEAMLEADER=None)
    def test_raises_when_teamleader_is_none(self) -> None:
        with pytest.raises(ImproperlyConfigured, match="missing or is not a dict"):
            _call_ready()

    @override_settings(TEAMLEADER="bad-value")
    def test_raises_when_teamleader_is_string(self) -> None:
        with pytest.raises(ImproperlyConfigured, match="missing or is not a dict"):
            _call_ready()

    @override_settings(TEAMLEADER=42)
    def test_raises_when_teamleader_is_int(self) -> None:
        with pytest.raises(ImproperlyConfigured, match="missing or is not a dict"):
            _call_ready()

    @override_settings(TEAMLEADER=[])
    def test_raises_when_teamleader_is_list(self) -> None:
        with pytest.raises(ImproperlyConfigured, match="missing or is not a dict"):
            _call_ready()


# ---------------------------------------------------------------------------
# Required keys missing
# ---------------------------------------------------------------------------


class TestReadyMissingKeys:
    @override_settings(TEAMLEADER={})
    def test_raises_when_all_keys_missing(self) -> None:
        with pytest.raises(ImproperlyConfigured, match="missing required key"):
            _call_ready()

    @override_settings(TEAMLEADER={k: "x" for k in REQUIRED_SETTINGS_KEYS - {"CLIENT_SECRET"}})
    def test_raises_when_client_secret_missing(self) -> None:
        with pytest.raises(ImproperlyConfigured, match="CLIENT_SECRET"):
            _call_ready()

    @override_settings(TEAMLEADER={k: "x" for k in REQUIRED_SETTINGS_KEYS - {"CLIENT_ID"}})
    def test_raises_when_client_id_missing(self) -> None:
        with pytest.raises(ImproperlyConfigured, match="CLIENT_ID"):
            _call_ready()

    @override_settings(TEAMLEADER={k: "x" for k in REQUIRED_SETTINGS_KEYS - {"REDIRECT_URI"}})
    def test_raises_when_redirect_uri_missing(self) -> None:
        with pytest.raises(ImproperlyConfigured, match="REDIRECT_URI"):
            _call_ready()

    @override_settings(TEAMLEADER={k: "x" for k in REQUIRED_SETTINGS_KEYS - {"SCOPES"}})
    def test_raises_when_scopes_missing(self) -> None:
        with pytest.raises(ImproperlyConfigured, match="SCOPES"):
            _call_ready()

    @override_settings(TEAMLEADER={"CLIENT_ID": "x"})
    def test_error_message_lists_all_missing_keys(self) -> None:
        """When multiple keys are absent the error names them all."""
        with pytest.raises(ImproperlyConfigured) as exc_info:
            _call_ready()
        msg = str(exc_info.value)
        for key in ("CLIENT_SECRET", "REDIRECT_URI", "SCOPES"):
            assert key in msg


# ---------------------------------------------------------------------------
# Happy path
# ---------------------------------------------------------------------------


class TestReadyValid:
    @override_settings(TEAMLEADER=_VALID_TEAMLEADER)
    def test_ready_returns_none_with_all_required_keys(self) -> None:
        assert _call_ready() is None

    @override_settings(TEAMLEADER={**_VALID_TEAMLEADER, "EXTRA_KEY": "value", "TIMEOUT": 60})
    def test_ready_accepts_extra_keys(self) -> None:
        """Non-required keys must not trigger an error."""
        assert _call_ready() is None

    @override_settings(TEAMLEADER={**_VALID_TEAMLEADER, "TOKEN_BACKEND": "my.module.Backend"})
    def test_ready_accepts_optional_token_backend(self) -> None:
        assert _call_ready() is None


# ---------------------------------------------------------------------------
# REQUIRED_SETTINGS_KEYS constant
# ---------------------------------------------------------------------------


class TestRequiredSettingsKeys:
    def test_contains_all_four_required_keys(self) -> None:
        assert REQUIRED_SETTINGS_KEYS == {"CLIENT_ID", "CLIENT_SECRET", "REDIRECT_URI", "SCOPES"}

    def test_is_frozenset(self) -> None:
        assert isinstance(REQUIRED_SETTINGS_KEYS, frozenset)
