# teamleader-sdk

Python SDK for the [Teamleader Focus](https://www.teamleader.eu/) API.

- Generated CRUD layer from the official OpenAPI spec (`@teamleader/focus-api-specification`)
- Curated model classes with computed properties and full type hints
- Optional Django integration: `DatabaseTokenBackend`, `teamleader_setup` management command
- Framework-agnostic core usable from FastAPI, Celery, scripts, etc.
- Python ≥ 3.10 · `requests` · no Pydantic / attrs

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
pip install teamleader-sdk

# With Django integration
pip install teamleader-sdk[django]
```

---

## Quick start

=== "Django"

    ```python
    # After running: python manage.py teamleader_setup
    from teamleader.django import get_client

    client = get_client()
    for deal in client.deals.iterate():
        print(deal.title, deal.is_open)
    ```

=== "Standalone"

    ```python
    from datetime import datetime, timezone
    from teamleader import TeamleaderClient, OAuth2Handler, MemoryTokenBackend, Token

    backend = MemoryTokenBackend()
    backend.save(Token(
        access_token="<access-token>",
        refresh_token="<refresh-token>",
        expires_at=datetime(2025, 12, 31, tzinfo=timezone.utc),
    ))
    handler = OAuth2Handler(
        client_id="your-client-id",
        client_secret="your-client-secret",
        redirect_uri="http://localhost:9999/callback",
        token_backend=backend,
    )
    client = TeamleaderClient(handler)
    contact = client.contacts.get("cde0bc5f-8602-4e12-b5d3-f03436b54c0d")
    print(contact.full_name, contact.primary_email)
    ```

---

## What's in the box

| Module | Contents |
|---|---|
| [`teamleader.models`](api-reference/models.md) | `Contact`, `Company`, `Deal`, `Invoice`, `Quotation` + common sub-models |
| [`teamleader.resources`](api-reference/resources.md) | `CrudResource`, `Page`, `ContactsResource`, `CompaniesResource`, `DealsResource`, `InvoicesResource`, `QuotationsResource` |
| [`teamleader.auth`](api-reference/auth.md) | `Token`, `TokenBackend`, `MemoryTokenBackend`, `OAuth2Handler` |
| [`teamleader.client`](api-reference/client.md) | `TeamleaderClient` |
| [`teamleader.exceptions`](api-reference/exceptions.md) | 9-class exception hierarchy |
| [`teamleader._generated`](api-reference/generated-endpoints.md) | 290 endpoints, 483 base models, 23 enums — auto-generated from spec v1.112.0 |
| [`teamleader.django`](guides/django.md) | `DatabaseTokenBackend`, `TeamleaderToken`, `teamleader_setup` command |
