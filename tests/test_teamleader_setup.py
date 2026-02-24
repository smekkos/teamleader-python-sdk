"""Unit tests for the _CallbackHandler used by the teamleader_setup command.

Tests start a real HTTPServer on an OS-assigned ephemeral port and make
actual HTTP requests against it, so no mocking is required.

Run with:
    .venv/bin/python -m pytest tests/test_teamleader_setup.py -v
"""

from __future__ import annotations

import http.client
import threading
from http.server import HTTPServer

import pytest

from teamleader.django.management.commands.teamleader_setup import _CallbackHandler

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _start_server() -> tuple[HTTPServer, int]:
    """Start an HTTPServer on an OS-assigned ephemeral port.

    Returns the server instance and the bound port number.
    The server runs in a daemon thread so it is automatically cleaned up
    when the test process exits.
    """
    server = HTTPServer(("localhost", 0), _CallbackHandler)
    port = server.server_address[1]
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return server, port


def _get(port: int, path: str) -> http.client.HTTPResponse:
    """Issue a GET request and return the response (body not yet read)."""
    conn = http.client.HTTPConnection("localhost", port, timeout=5)
    conn.request("GET", path)
    return conn.getresponse()


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture(autouse=True)
def _reset_captured_code() -> None:
    """Ensure _CallbackHandler.captured_code is cleared before every test."""
    _CallbackHandler.captured_code = None


# ---------------------------------------------------------------------------
# Tests — code capture
# ---------------------------------------------------------------------------


class TestCallbackHandlerCodeCapture:
    def test_captures_code_from_query_string(self) -> None:
        server, port = _start_server()
        try:
            _get(port, "/callback?code=abc123")
        finally:
            server.shutdown()
        assert _CallbackHandler.captured_code == "abc123"

    def test_captured_code_is_none_when_no_code_param(self) -> None:
        server, port = _start_server()
        try:
            _get(port, "/callback?state=xyz&foo=bar")
        finally:
            server.shutdown()
        assert _CallbackHandler.captured_code is None

    def test_captures_code_when_multiple_params_present(self) -> None:
        """?state=…&code=…&scope=… — the code param must be extracted correctly."""
        server, port = _start_server()
        try:
            _get(port, "/callback?state=random_state&code=token123&scope=read")
        finally:
            server.shutdown()
        assert _CallbackHandler.captured_code == "token123"

    def test_captures_code_with_special_characters(self) -> None:
        """URL-encoded code values must be captured as decoded strings."""
        server, port = _start_server()
        try:
            _get(port, "/callback?code=abc%2Fdef%2B123")
        finally:
            server.shutdown()
        # parse_qs decodes percent-encoding automatically
        assert _CallbackHandler.captured_code == "abc/def+123"


# ---------------------------------------------------------------------------
# Tests — HTTP status codes
# ---------------------------------------------------------------------------


class TestCallbackHandlerHttpStatus:
    def test_returns_200_when_code_present(self) -> None:
        server, port = _start_server()
        try:
            response = _get(port, "/callback?code=abc123")
            status = response.status
        finally:
            server.shutdown()
        assert status == 200

    def test_returns_400_when_code_missing(self) -> None:
        server, port = _start_server()
        try:
            response = _get(port, "/callback?state=xyz")
            status = response.status
        finally:
            server.shutdown()
        assert status == 400

    def test_returns_400_for_root_path_with_no_params(self) -> None:
        server, port = _start_server()
        try:
            response = _get(port, "/")
            status = response.status
        finally:
            server.shutdown()
        assert status == 400


# ---------------------------------------------------------------------------
# Tests — response body
# ---------------------------------------------------------------------------


class TestCallbackHandlerResponseBody:
    def test_success_body_contains_authorization_successful(self) -> None:
        server, port = _start_server()
        try:
            response = _get(port, "/callback?code=abc123")
            body = response.read().decode()
        finally:
            server.shutdown()
        assert "successful" in body.lower()

    def test_success_body_is_html(self) -> None:
        server, port = _start_server()
        try:
            response = _get(port, "/callback?code=abc123")
            content_type = response.getheader("Content-Type", "")
            response.read()  # drain
        finally:
            server.shutdown()
        assert "text/html" in content_type
