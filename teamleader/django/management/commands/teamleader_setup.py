"""Management command: python manage.py teamleader_setup

Walks the user through the OAuth2 authorization flow:

1. Reads settings.TEAMLEADER to build the authorization URL.
2. Prints the URL and instructs the user to open it in a browser.
3. Starts a temporary local HTTP server on OAUTH_CALLBACK_PORT (default 9999).
4. Waits for Teamleader to redirect back with ``?code=...``.
5. Exchanges the code for tokens via OAuth2Handler.
6. Persists the tokens with DatabaseTokenBackend.
7. Prints a confirmation with the access-token expiry time.
8. Shuts down the temporary server.
"""

from __future__ import annotations

import threading
import urllib.parse
from http.server import BaseHTTPRequestHandler, HTTPServer

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from teamleader.auth import OAuth2Handler
from teamleader.constants import DEFAULT_OAUTH_CALLBACK_PORT
from teamleader.django.token_store import DatabaseTokenBackend


class _CallbackHandler(BaseHTTPRequestHandler):
    """Minimal HTTP handler that captures the ``?code=`` query parameter."""

    # Set by the Command before the server starts.
    captured_code: str | None = None

    def do_GET(self) -> None:  # noqa: N802
        parsed = urllib.parse.urlparse(self.path)
        params = urllib.parse.parse_qs(parsed.query)
        code_values = params.get("code")

        if code_values:
            _CallbackHandler.captured_code = code_values[0]
            body = (
                b"<html><body>"
                b"<h2>Teamleader authorization successful!</h2>"
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

    def log_message(self, *args: object) -> None:  # noqa: ANN002
        """Suppress default access-log output to keep the terminal clean."""


class Command(BaseCommand):
    help = (
        "Authorize the Teamleader SDK via OAuth2 and save tokens to the database. "
        "Run this once per environment after initial deployment."
    )

    def handle(self, *args: object, **options: object) -> None:
        conf: dict = getattr(settings, "TEAMLEADER", {})

        for required in ("CLIENT_ID", "CLIENT_SECRET", "REDIRECT_URI", "SCOPES"):
            if not conf.get(required):
                raise CommandError(
                    f"settings.TEAMLEADER['{required}'] is required but not set."
                )

        port: int = conf.get("OAUTH_CALLBACK_PORT", DEFAULT_OAUTH_CALLBACK_PORT)

        backend = DatabaseTokenBackend()
        handler = OAuth2Handler(
            client_id=conf["CLIENT_ID"],
            client_secret=conf["CLIENT_SECRET"],
            redirect_uri=conf["REDIRECT_URI"],
            token_backend=backend,
            scopes=conf["SCOPES"],
        )

        auth_url = handler.get_authorization_url()

        self.stdout.write(self.style.SUCCESS("\n=== Teamleader OAuth2 Setup ===\n"))
        self.stdout.write(
            "Open the following URL in your browser to authorize this application:\n"
        )
        self.stdout.write(f"\n  {auth_url}\n")
        self.stdout.write(
            f"\nWaiting for Teamleader to redirect to http://localhost:{port}/callback …\n"
        )

        # Reset captured code from any previous run.
        _CallbackHandler.captured_code = None

        server = HTTPServer(("localhost", port), _CallbackHandler)

        # Serve requests in a background thread so we can poll captured_code.
        server_thread = threading.Thread(target=server.serve_forever, daemon=True)
        server_thread.start()

        # Block until the callback handler captures the code.
        import time

        while _CallbackHandler.captured_code is None:
            time.sleep(0.25)

        server.shutdown()

        code = _CallbackHandler.captured_code
        self.stdout.write("\nAuthorization code received. Exchanging for tokens …\n")

        try:
            token = handler.exchange_code(code)
        except Exception as exc:  # noqa: BLE001
            raise CommandError(f"Token exchange failed: {exc}") from exc

        self.stdout.write(
            self.style.SUCCESS(
                f"\nSuccess! Access token stored in the database.\n"
                f"Token expires at: {token.expires_at.isoformat()}\n"
            )
        )
