# Error Handling

All exceptions raised by the SDK inherit from `TeamleaderError`, so you can catch
the broadest class you care about, or handle specific errors individually.

---

## Exception hierarchy

```
TeamleaderError
├── TeamleaderAPIError              non-specific 4xx response
│   ├── TeamleaderNotFoundError     404 — resource not found
│   ├── TeamleaderRateLimitError    429 — rate limit exceeded (adds .retry_after)
│   └── TeamleaderServerError       5xx — server-side error
├── TeamleaderAuthError             401 — access token invalid / missing
│   └── TeamleaderAuthExpiredError  refresh token revoked or expired
├── TeamleaderValidationError       422 — request body failed validation
└── TeamleaderPermissionError       403 — insufficient OAuth scope
```

Every exception carries three attributes:

| Attribute | Type | Description |
|---|---|---|
| `message` | `str` | Human-readable error message extracted from the API response |
| `status_code` | `int \| None` | HTTP status code |
| `raw_response` | `requests.Response \| None` | Full response object for advanced inspection |

`TeamleaderRateLimitError` adds a fourth:

| Attribute | Type | Description |
|---|---|---|
| `retry_after` | `int \| None` | Seconds to wait before retrying (from `Retry-After` header) |

---

## Usage patterns

### Catch specific errors

```python
import time
from teamleader.exceptions import (
    TeamleaderNotFoundError,
    TeamleaderRateLimitError,
    TeamleaderAuthExpiredError,
    TeamleaderPermissionError,
    TeamleaderValidationError,
    TeamleaderError,
)

try:
    deal = client.deals.get("non-existent-uuid")

except TeamleaderNotFoundError:
    print("Deal does not exist")

except TeamleaderRateLimitError as e:
    wait = e.retry_after or 60
    print(f"Rate limited — retrying in {wait}s")
    time.sleep(wait)

except TeamleaderAuthExpiredError:
    # Refresh token has been revoked — must re-authorise
    print("Re-run `python manage.py teamleader_setup` to re-authorise")

except TeamleaderPermissionError:
    # OAuth scope missing — check your SCOPES setting
    print(f"Missing scope: {e.message}")

except TeamleaderValidationError as e:
    print(f"Bad request: {e.message}")

except TeamleaderError as e:
    # Catch-all for any SDK error
    print(f"SDK error {e.status_code}: {e.message}")
```

### Broad catch-all

```python
from teamleader.exceptions import TeamleaderError

try:
    client.invoices.book(invoice_id, on="2025-03-01")
except TeamleaderError as e:
    logger.error("Teamleader API error", extra={
        "status_code": e.status_code,
        "message": e.message,
    })
    raise
```

### Rate-limit retry loop

```python
import time
from teamleader.exceptions import TeamleaderRateLimitError

MAX_RETRIES = 3
attempt = 0

while attempt < MAX_RETRIES:
    try:
        page = client.contacts.list(page=1, page_size=100)
        break
    except TeamleaderRateLimitError as e:
        attempt += 1
        if attempt >= MAX_RETRIES:
            raise
        wait = e.retry_after or (2 ** attempt)
        time.sleep(wait)
```

---

## Auth errors vs. API errors

| Exception | When raised | Action |
|---|---|---|
| `TeamleaderAuthError` | 401 response | Access token invalid — the SDK will attempt a refresh automatically for the *next* request; this is raised when the explicit token fetch fails |
| `TeamleaderAuthExpiredError` | Refresh grant rejected | Re-run `teamleader_setup` or `get_tokens.py` to obtain a new token pair |
| `TeamleaderPermissionError` | 403 response | The OAuth app lacks the required scope — update `SCOPES` in settings and re-authorise |

!!! tip
    Transparent token refresh happens inside `OAuth2Handler.get_valid_token()` — called
    automatically before every request.  You only see `TeamleaderAuthExpiredError` if the
    *refresh* grant itself fails (revoked token, app re-authorised, etc.).
