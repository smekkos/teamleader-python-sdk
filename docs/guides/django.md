# Django Integration

The `teamleader.django` sub-package provides a `DatabaseTokenBackend` that stores
OAuth2 tokens in your Django database, and a `teamleader_setup` management command
that automates the initial OAuth handshake.

---

## 1. Install the Django extra

```bash
pip install teamleader-sdk[django]
```

---

## 2. Add to `INSTALLED_APPS`

```python
# settings.py
INSTALLED_APPS = [
    ...
    "teamleader.django",
]
```

`TeamleaderConfig.ready()` validates all required settings keys on startup and raises
`django.core.exceptions.ImproperlyConfigured` with an actionable message if any are
missing.

---

## 3. Configure the `TEAMLEADER` settings dict

```python
# settings.py
TEAMLEADER = {
    # Required
    "CLIENT_ID":     "your-client-id",
    "CLIENT_SECRET": "your-client-secret",
    "REDIRECT_URI":  "http://localhost:9999/callback",  # must match your Marketplace app
    "SCOPES":        ["contacts", "deals"],

    # Optional — defaults shown
    "OAUTH_CALLBACK_PORT": 9999,   # port for the setup command's local HTTP server
    "TOKEN_BACKEND":       "teamleader.django.token_store.DatabaseTokenBackend",
    "TIMEOUT":             30,     # HTTP request timeout in seconds
}
```

### Required keys

| Key | Description |
|---|---|
| `CLIENT_ID` | OAuth2 client ID from Teamleader Marketplace |
| `CLIENT_SECRET` | OAuth2 client secret |
| `REDIRECT_URI` | Must exactly match the Redirect URI configured in the Marketplace app |
| `SCOPES` | List of OAuth scope strings your app needs |

### Optional keys

| Key | Default | Description |
|---|---|---|
| `OAUTH_CALLBACK_PORT` | `9999` | Port for the `teamleader_setup` local HTTP server |
| `TOKEN_BACKEND` | `DatabaseTokenBackend` (dotted path) | Custom token storage backend |
| `TIMEOUT` | `30` | HTTP request timeout in seconds |

---

## 4. Create the token table

The SDK does **not** ship migrations.  Run `makemigrations` once per downstream project:

```bash
python manage.py makemigrations teamleader_django
python manage.py migrate
```

This creates the `TeamleaderToken` singleton table that `DatabaseTokenBackend` uses.

---

## 5. Obtain OAuth tokens

```bash
python manage.py teamleader_setup
```

The command:

1. Validates your `TEAMLEADER` settings dict
2. Builds the authorization URL via `OAuth2Handler.get_authorization_url()`
3. Prints the URL — open it in a browser and authorise the app
4. Starts a temporary HTTP server on `OAUTH_CALLBACK_PORT` (default 9999)
5. Captures the `?code=…` callback
6. Exchanges the code for an access + refresh token pair
7. Saves both tokens in the database via `DatabaseTokenBackend`
8. Prints a confirmation with the access-token expiry time

---

## 6. Use the client in your code

```python
from teamleader.django import get_client

client = get_client()

# The client automatically refreshes expired access tokens using the stored
# refresh token — no manual token management needed.

# Iterate over all contacts
for contact in client.contacts.iterate():
    print(contact.full_name, contact.primary_email)

# Fetch a single deal by UUID
deal = client.deals.get("c3dea2c8-dad9-4834-8a49-e16b5c5f1dde")
print(deal.title, deal.is_won)
```

`get_client()` reads `settings.TEAMLEADER`, constructs a `DatabaseTokenBackend` and
`OAuth2Handler`, and returns a fully configured `TeamleaderClient`.

---

## Token storage details

`DatabaseTokenBackend` uses `select_for_update()` inside `transaction.atomic()` on
every `save()` to prevent race conditions in multi-worker/multi-process deployments
(gunicorn, uWSGI, Celery, etc.).

The `TeamleaderToken` model enforces a singleton by pinning `pk = 1` before every
`save()`.  There is always at most one token row in the database.

---

## Token rotation

Teamleader uses refresh-token rotation: every successful token refresh invalidates the
old refresh token and issues a new pair.  `DatabaseTokenBackend.save()` updates both
`access_token` and `refresh_token` atomically on each refresh, so subsequent requests
in the same process always see the latest credentials.

!!! warning "Re-run `teamleader_setup` if the refresh token is revoked"
    If the refresh token is revoked (e.g. the Marketplace app is re-authorised),
    `TeamleaderAuthExpiredError` will be raised.  Re-run `teamleader_setup` to obtain
    a fresh token pair.
