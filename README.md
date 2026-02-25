# teamleader-sdk

Python SDK for the [Teamleader Focus](https://www.teamleader.eu/) API.

- Generated CRUD layer from the official OpenAPI spec (`@teamleader/focus-api-specification`)
- Curated model classes with computed properties and full type hints
- Optional Django integration: `DatabaseTokenBackend`, `teamleader_setup` management command
- Framework-agnostic core usable from FastAPI, Celery, scripts, etc.
- Python ≥ 3.10 · requests · no Pydantic / attrs

---

## Contents

1. [Requirements](#requirements)
2. [Installation](#installation)
3. [Django setup](#django-setup)
4. [Non-Django usage](#non-django-usage)
5. [Working with resources](#working-with-resources)
6. [Pagination](#pagination)
7. [Extra resource methods](#extra-resource-methods)
8. [Models and computed properties](#models-and-computed-properties)
9. [Error handling](#error-handling)
10. [Codegen — updating the generated layer](#codegen--updating-the-generated-layer)
11. [Documentation — serving and building the docs](#documentation--serving-and-building-the-docs)

---

## Requirements

| Dependency | Version |
|---|---|
| Python | ≥ 3.10 |
| requests | ≥ 2.28 |
| Django *(optional)* | ≥ 4.2 |

---

## Installation

```bash
# Core only (non-Django projects, scripts, Celery workers)
pip install git+https://github.com/smekkos/teamleader-python-sdk.git

# With Django integration
pip install "git+https://github.com/smekkos/teamleader-python-sdk.git#egg=teamleader-sdk[django]"
```

---

## Django setup

### 1. Add to `INSTALLED_APPS`

```python
INSTALLED_APPS = [
    ...
    "teamleader.django",
]
```

### 2. Add `TEAMLEADER` settings dict

```python
# settings.py
TEAMLEADER = {
    # Required
    "CLIENT_ID":      "your-client-id",
    "CLIENT_SECRET":  "your-client-secret",
    "REDIRECT_URI":   "http://localhost:9999/callback",   # must match Marketplace app
    "SCOPES":         ["contacts", "deals"],

    # Optional — defaults shown
    "OAUTH_CALLBACK_PORT": 9999,          # port for the setup HTTP server
    "TOKEN_BACKEND":       "teamleader.django.token_store.DatabaseTokenBackend",
    "TIMEOUT":             30,            # HTTP request timeout in seconds
}
```

`TeamleaderConfig.ready()` validates the required keys on startup and raises
`django.core.exceptions.ImproperlyConfigured` with an actionable message if any
are missing.

### 3. Create the token table

The SDK does **not** ship migrations. Run `makemigrations` once per project:

```bash
python manage.py makemigrations teamleader_django
python manage.py migrate
```

### 4. Obtain OAuth tokens

```bash
python manage.py teamleader_setup
```

This command:
1. Prints an authorization URL — open it in your browser
2. Starts a temporary HTTP server on `OAUTH_CALLBACK_PORT` (default 9999)
3. Captures the OAuth callback code
4. Exchanges it for access + refresh tokens and saves them in the database

### 5. Use the client

```python
from teamleader.django import get_client

client = get_client()

# Iterate all deals
for deal in client.deals.iterate():
    print(deal.title, deal.status)

# Fetch a single contact
contact = client.contacts.get("cde0bc5f-8602-4e12-b5d3-f03436b54c0d")
print(contact.full_name, contact.primary_email)
```

---

## Non-Django usage

```python
from datetime import datetime, timezone
from teamleader import TeamleaderClient, OAuth2Handler, MemoryTokenBackend, Token

# 1. Create a token backend and pre-load a token you obtained earlier
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

### Obtaining an initial token (scripts / dev machines)

```bash
python get_tokens.py
```

Copy the printed `.env` block and save it; then load it into your `MemoryTokenBackend`
or database.

---

## Working with resources

Every resource exposes the same five CRUD methods:

```python
# List — returns a Page object (see Pagination)
page = client.contacts.list(page=1, page_size=20, filter={"email": "x@y.com"})

# Get a single object by UUID
contact = client.contacts.get("cde0bc5f-...")

# Create — POSTs to .add, then re-fetches via .info
contact = client.contacts.create(first_name="Ada", last_name="Lovelace",
                                  emails=[{"type": "primary", "email": "ada@example.com"}])

# Update — POSTs to .update, then re-fetches via .info
contact = client.contacts.update("cde0bc5f-...", last_name="Lovelace-King")

# Delete
client.contacts.delete("cde0bc5f-...")
```

---

## Pagination

`list()` returns a `Page[M]` dataclass:

| Attribute | Type | Description |
|---|---|---|
| `data` | `list[M]` | Deserialised model objects |
| `total_count` | `int` | Total matches across all pages |
| `current_page` | `int` | 1-based page index |
| `page_size` | `int` | Items requested per page |
| `has_next` | `bool` | `True` when more pages exist |

```python
page = client.deals.list(page=1, page_size=20, filter={"status": "open"})
while page.has_next:
    page = page.next()
    for deal in page.data:
        print(deal.title)
```

### `iterate()` — consume all pages automatically

```python
for contact in client.contacts.iterate(filter={"tag": "vip"}):
    print(contact.full_name)
```

---

## Extra resource methods

### Contacts

```python
client.contacts.tag(contact_id, ["vip", "expo"])
client.contacts.untag(contact_id, ["expo"])
client.contacts.link_to_company(contact_id, company_id, position="CTO", decision_maker=True)
client.contacts.unlink_from_company(contact_id, company_id)
```

### Companies

```python
client.companies.tag(company_id, ["customer"])
client.companies.untag(company_id, ["prospect"])
```

### Deals

```python
client.deals.move_to_phase(deal_id, phase_id)
client.deals.win(deal_id)
client.deals.lose(deal_id, reason_id="r-uuid", extra_info="Too expensive")

phases  = client.deals.list_phases(deal_pipeline_id="pipe-uuid")
sources = client.deals.list_sources()
```

### Invoices

```python
# Book a draft invoice
client.invoices.book(invoice_id, on="2025-03-01")

# Credit an invoice — returns TypeAndId referencing the new credit note
credit_note_ref = client.invoices.credit(invoice_id, credit_note_date="2025-03-05")

# Register a payment
from teamleader.models import Money
client.invoices.register_payment(
    invoice_id,
    payment=Money(amount=500.0, currency="EUR"),
    paid_at="2025-03-01T12:00:00+00:00",
)

# Send via e-mail
client.invoices.send(invoice_id, subject="Your invoice", body="Please find your invoice attached.")

# Download — returns {"location": "<pre-signed URL>", "expires": "<ISO datetime>"}
download = client.invoices.download(invoice_id, format="pdf")
```

### Quotations

```python
# Send one or more quotations from the same deal
client.quotations.send(
    quotation_ids=["q-uuid-1"],
    recipients={"to": [{"email_address": "client@example.com"}]},
    subject="Quotation for your project",
    content="Please find your quotation attached.",
    language="en",
)

# Mark as accepted
client.quotations.accept(quotation_id)
```

---

## Models and computed properties

### Contact

| Property | Returns |
|---|---|
| `full_name` | `"First Last"` |
| `primary_email` | First `type="primary"` email address, else first email, else `None` |
| `primary_phone` | First telephone number, else `None` |
| `is_active` | `status == "active"` |

### Company

| Property | Returns |
|---|---|
| `is_active` | `status == "active"` |
| `primary_email` | Same logic as Contact |
| `primary_phone` | First telephone number |

### Deal

| Property | Returns |
|---|---|
| `is_open` | `status == "open"` |
| `is_won` | `status == "won"` |
| `is_lost` | `status == "lost"` |
| `customer_id` | UUID of the lead's customer |
| `customer_type` | `"contact"` or `"company"` |

### Invoice

| Property | Returns |
|---|---|
| `is_paid` | `paid == True` |
| `is_draft` | `status == "draft"` |
| `is_overdue` | `due_on < today AND NOT paid` (date-safe) |
| `total_due` | `Money` from `total["due"]`, or `None` |
| `customer_name` | `invoicee["name"]`, or `None` |

### Quotation

| Property | Returns |
|---|---|
| `is_open` | `status == "open"` |
| `is_accepted` | `status == "accepted"` |
| `is_expired` | `status == "expired"` |
| `total_tax_exclusive` | `Money` from totals, or `None` |
| `total_tax_inclusive` | `Money` from totals, or `None` |

---

## Error handling

```python
from teamleader.exceptions import (
    TeamleaderError,           # base
    TeamleaderAPIError,        # non-specific 4xx
    TeamleaderAuthError,       # 401 — token invalid
    TeamleaderAuthExpiredError,# refresh token revoked
    TeamleaderNotFoundError,   # 404
    TeamleaderPermissionError, # 403
    TeamleaderValidationError, # 422 — bad request body
    TeamleaderRateLimitError,  # 429 — adds .retry_after (int | None)
    TeamleaderServerError,     # 5xx
)

try:
    deal = client.deals.get("non-existent-uuid")
except TeamleaderNotFoundError:
    print("Deal not found")
except TeamleaderRateLimitError as e:
    if e.retry_after:
        time.sleep(e.retry_after)
except TeamleaderAuthExpiredError:
    print("Refresh token revoked — re-run teamleader_setup")
```

---

## Codegen — updating the generated layer

The SDK is partially generated from the npm spec snapshot `codegen/spec/api.yaml`.

```bash
# Fetch latest spec and regenerate _generated/
python codegen/generate.py

# Review what changed
git diff teamleader/_generated/

# Run the full test suite — curated code may need updating
pytest

# Commit both the generated files and any curated fixes
git add teamleader/_generated/ teamleader/models/ teamleader/resources/
git commit -m "chore: update generated layer to spec vX.Y.Z"
```

The committed `codegen/spec/api.yaml` serves as a canonical snapshot for diffing against
future spec versions.

---

## Documentation — serving and building the docs

The docs are built with [MkDocs Material](https://squidfunk.github.io/mkdocs-material/) and
[mkdocstrings](https://mkdocstrings.github.io/). All required tools are included in the `dev`
extras.

### Install doc dependencies

```bash
pip install -e ".[dev]"
```

### Serve locally (live-reload)

```bash
mkdocs serve
```

Open <http://127.0.0.1:8000> in your browser. Pages and docstrings reload automatically on
every save. The [`codegen/generate_docs_endpoints.py`](codegen/generate_docs_endpoints.py)
build hook runs automatically so the generated API-reference page is always up to date.

### Build static site

```bash
mkdocs build
```

Output is written to the `site/` directory (excluded from the package via
`.gitignore`/`MANIFEST`).
