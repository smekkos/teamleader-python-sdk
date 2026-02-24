#!/usr/bin/env python
"""Standalone OAuth2 token-fetching helper.

Run this script once on your dev machine to obtain the access/refresh
tokens needed to populate ``.env`` for integration tests.

Usage::

    python get_tokens.py

The script will:
1. Ask for your CLIENT_ID and CLIENT_SECRET (or read from env / .env).
2. Print the Teamleader authorization URL — open it in your browser.
3. Start a local HTTP server on port 9999 to capture the redirect.
4. Exchange the authorization code for tokens automatically.
5. Print the ready-to-paste .env block.

Prerequisites
-------------
- Your Teamleader Marketplace app must have ``http://localhost:9999/callback``
  as an allowed redirect URI.
- This script must be run from the project root so that ``teamleader``
  is importable (i.e. ``pip install -e .`` has been done, or the venv
  contains the package).
"""

from __future__ import annotations

import os
import sys
import threading
import time
import urllib.parse
from http.server import BaseHTTPRequestHandler, HTTPServer

# ---------------------------------------------------------------------------
# Load .env if it exists (no hard dependency on python-dotenv)
# ---------------------------------------------------------------------------
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # python-dotenv not installed — rely on real env vars

# ---------------------------------------------------------------------------
# Ensure the SDK is importable when run from the project root without install
# ---------------------------------------------------------------------------
sys.path.insert(0, os.path.dirname(__file__))

from teamleader.auth import MemoryTokenBackend, OAuth2Handler  # noqa: E402
from teamleader.constants import DEFAULT_OAUTH_CALLBACK_PORT  # noqa: E402

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
PORT = int(os.environ.get("TEAMLEADER_OAUTH_CALLBACK_PORT", DEFAULT_OAUTH_CALLBACK_PORT))
REDIRECT_URI = os.environ.get(
    "TEAMLEADER_REDIRECT_URI",
    f"http://localhost:{PORT}/callback",
)
# Teamleader Focus scopes are configured at the app level in the Marketplace.
# Leave TEAMLEADER_SCOPES unset (empty) to omit the scope parameter from the
# authorization URL, which lets Teamleader grant all permissions the app is
# configured for.  Set it only if you need to request a specific subset.
SCOPES = os.environ.get("TEAMLEADER_SCOPES", "")


def _prompt(label: str, env_key: str, secret: bool = False) -> str:
    """Return the env var value, or interactively prompt for it."""
    value = os.environ.get(env_key, "").strip()
    if value:
        masked = ("*" * 8) if secret else value
        print(f"  {label}: {masked}  (from environment)")
        return value
    value = input(f"  {label}: ").strip()
    if not value:
        print(f"ERROR: {label} is required.", file=sys.stderr)
        sys.exit(1)
    return value


# ---------------------------------------------------------------------------
# Minimal HTTP callback server
# ---------------------------------------------------------------------------
class _CallbackHandler(BaseHTTPRequestHandler):
    captured_code: str | None = None

    def do_GET(self) -> None:  # noqa: N802
        parsed = urllib.parse.urlparse(self.path)
        params = urllib.parse.parse_qs(parsed.query)
        code_values = params.get("code")

        if code_values:
            _CallbackHandler.captured_code = code_values[0]
            body = (
                b"<html><body>"
                b"<h2>Authorization successful!</h2>"
                b"<p>You can close this tab and return to the terminal.</p>"
                b"</body></html>"
            )
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
        else:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b"Missing ?code= parameter.")

    def log_message(self, *args: object) -> None:  # silence access log
        pass


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main() -> None:
    print("\n=== Teamleader OAuth2 Token Fetcher ===\n")
    print("Enter your Teamleader app credentials")
    print("(or set TEAMLEADER_CLIENT_ID / TEAMLEADER_CLIENT_SECRET in the environment)\n")

    client_id = _prompt("CLIENT_ID", "TEAMLEADER_CLIENT_ID")
    client_secret = _prompt("CLIENT_SECRET", "TEAMLEADER_CLIENT_SECRET", secret=True)

    backend = MemoryTokenBackend()
    handler = OAuth2Handler(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=REDIRECT_URI,
        token_backend=backend,
        scopes=SCOPES.split(),
    )

    auth_url = handler.get_authorization_url()

    print(f"\nOpen this URL in your browser:\n\n  {auth_url}\n")
    print(f"Waiting for Teamleader to redirect to {REDIRECT_URI} …\n")

    # Reset captured code from any previous run.
    _CallbackHandler.captured_code = None

    server = HTTPServer(("localhost", PORT), _CallbackHandler)
    server_thread = threading.Thread(target=server.serve_forever, daemon=True)
    server_thread.start()

    # Poll until the callback handler captures the authorization code.
    while _CallbackHandler.captured_code is None:
        time.sleep(0.25)

    server.shutdown()

    code = _CallbackHandler.captured_code
    print("Authorization code received. Exchanging for tokens …\n")

    try:
        token = handler.exchange_code(code)
    except Exception as exc:  # noqa: BLE001
        print(f"ERROR: Token exchange failed: {exc}", file=sys.stderr)
        sys.exit(1)

    print("=" * 60)
    print("SUCCESS! Add the following block to your .env file:\n")
    print(f"TEAMLEADER_INTEGRATION_CLIENT_ID={client_id}")
    print(f"TEAMLEADER_INTEGRATION_CLIENT_SECRET={client_secret}")
    print(f"TEAMLEADER_INTEGRATION_REDIRECT_URI={REDIRECT_URI}")
    print(f"TEAMLEADER_INTEGRATION_ACCESS_TOKEN={token.access_token}")
    print(f"TEAMLEADER_INTEGRATION_REFRESH_TOKEN={token.refresh_token}")
    print(f"TEAMLEADER_INTEGRATION_EXPIRES_AT={token.expires_at.isoformat()}")
    print("=" * 60)
    print(
        "\nToken expires at:", token.expires_at.isoformat(),
        "\nRun the integration tests with:\n"
        "  python -m pytest tests/integration/test_auth.py -v\n"
    )


if __name__ == "__main__":
    main()
