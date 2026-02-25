# Non-Django Usage

The core SDK has no Django dependency.  Use it in FastAPI services, Celery workers,
CLI scripts, or any other Python environment.

---

## 1. Obtain credentials

Run the standalone helper once on a dev machine to get an initial token pair:

```bash
python get_tokens.py
```

The script opens the Teamleader OAuth flow in a browser, captures the callback on
`localhost:9999`, exchanges the code, and prints a `.env` block:

```
TEAMLEADER_ACCESS_TOKEN=eyJhbGci...
TEAMLEADER_REFRESH_TOKEN=def5020...
TEAMLEADER_EXPIRES_AT=2025-06-01T12:00:00+00:00
```

Save this to a `.env` file (already in `.gitignore`).

---

## 2. Build the client

```python
from datetime import datetime, timezone
from teamleader import TeamleaderClient, OAuth2Handler, MemoryTokenBackend, Token

# 1. Create a backend and load the stored token
backend = MemoryTokenBackend()
backend.save(Token(
    access_token="<access-token>",
    refresh_token="<refresh-token>",
    expires_at=datetime(2025, 12, 31, tzinfo=timezone.utc),
))

# 2. Create an auth handler
handler = OAuth2Handler(
    client_id="your-client-id",
    client_secret="your-client-secret",
    redirect_uri="http://localhost:9999/callback",
    token_backend=backend,
)

# 3. Create the client
client = TeamleaderClient(handler)

# 4. Use it
invoice = client.invoices.get("e540fe7e-dce2-459e-bf7e-24e605fc18b3")
print(invoice.invoice_number, invoice.is_overdue)
```

---

## 3. Loading tokens from environment variables

```python
import os
from datetime import datetime, timezone
from dotenv import load_dotenv
from teamleader import TeamleaderClient, OAuth2Handler, MemoryTokenBackend, Token

load_dotenv()  # reads .env file

backend = MemoryTokenBackend()
backend.save(Token(
    access_token=os.environ["TEAMLEADER_ACCESS_TOKEN"],
    refresh_token=os.environ["TEAMLEADER_REFRESH_TOKEN"],
    expires_at=datetime.fromisoformat(os.environ["TEAMLEADER_EXPIRES_AT"]),
))

handler = OAuth2Handler(
    client_id=os.environ["TEAMLEADER_CLIENT_ID"],
    client_secret=os.environ["TEAMLEADER_CLIENT_SECRET"],
    redirect_uri=os.environ["TEAMLEADER_REDIRECT_URI"],
    token_backend=backend,
)

client = TeamleaderClient(handler)
```

---

## 4. Custom token backend

Implement `TokenBackend` to persist tokens in Redis, a file, or any other store:

```python
from teamleader.auth import TokenBackend, Token
import json, pathlib

class FileTokenBackend(TokenBackend):
    def __init__(self, path: str) -> None:
        self._path = pathlib.Path(path)

    def get(self) -> Token | None:
        if not self._path.exists():
            return None
        data = json.loads(self._path.read_text())
        from datetime import datetime
        return Token(
            access_token=data["access_token"],
            refresh_token=data["refresh_token"],
            expires_at=datetime.fromisoformat(data["expires_at"]),
        )

    def save(self, token: Token) -> None:
        self._path.write_text(json.dumps({
            "access_token":  token.access_token,
            "refresh_token": token.refresh_token,
            "expires_at":    token.expires_at.isoformat(),
        }))

    def clear(self) -> None:
        self._path.unlink(missing_ok=True)
```

Pass it to `OAuth2Handler` the same way as `MemoryTokenBackend`.

---

## Token refresh behaviour

`TeamleaderClient` calls `OAuth2Handler.get_valid_token()` before every request.
If the stored `Token.is_expired` returns `True`, the handler transparently issues a
refresh-token grant and saves the new pair via the backend.  The original request then
proceeds with the fresh access token — **no manual refresh logic required**.

A safety margin of 60 seconds is applied: tokens are considered expired 60 s before
their actual `expires_at` so in-flight requests are never rejected mid-call.

!!! warning "Refresh token revocation"
    If Teamleader revokes the refresh token (app re-authorised, long inactivity),
    `TeamleaderAuthExpiredError` is raised.  Re-run `get_tokens.py` to obtain a new pair.
