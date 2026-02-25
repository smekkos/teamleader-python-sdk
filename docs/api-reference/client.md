# TeamleaderClient — API Reference

`TeamleaderClient` is the entry point for all API calls.  It handles Bearer token
injection, response parsing, and exposes the five curated resource attributes.

See [Non-Django Usage](../guides/non-django.md) and [Django Integration](../guides/django.md)
for construction examples.

---

## Two ways to call the API

| Approach | How | Returns | When to use |
|---|---|---|---|
| **Curated resources** | `client.contacts.get(id)` | Typed model (`Contact`, `Deal`, …) | The 5 supported resource families |
| **`call()` bridge** | `client.call("tickets.list", …)` | Raw `dict` | Any of the 290 generated endpoints |

The [`call()` method](#teamleader.client.TeamleaderClient.call) accepts any operation ID
from the [Generated Endpoint Reference](generated-endpoints.md) and validates required
parameters before sending the request.

---

::: teamleader.client.TeamleaderClient

---

## Resource attributes

| Attribute | Type | Description |
|---|---|---|
| `contacts` | `ContactsResource` | CRUD + tag/untag/link operations on contacts |
| `companies` | `CompaniesResource` | CRUD + tag/untag operations on companies |
| `deals` | `DealsResource` | CRUD + phase/win/lose/list_phases/list_sources |
| `invoices` | `InvoicesResource` | CRUD + book/credit/register_payment/send/download |
| `quotations` | `QuotationsResource` | CRUD + send/accept |

## HTTP internals

All Teamleader API calls are `POST` requests (per the Teamleader API convention).
`TeamleaderClient` exposes two internal helpers used by resources:

- `_post(path, json)` — POST body, deserialise response
- `_get(path, params)` — GET with query params (used for a small number of endpoints)

Both methods call `_auth_headers()` which transparently refreshes the access token
via `OAuth2Handler.get_valid_token()` if it is expired.
