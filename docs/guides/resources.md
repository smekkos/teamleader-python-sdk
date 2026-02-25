# Working with Resources

Every resource on `TeamleaderClient` exposes the same five CRUD methods plus
resource-specific extra actions.  The five curated resources are:

| Attribute | Resource class | Model |
|---|---|---|
| `client.contacts` | `ContactsResource` | `Contact` |
| `client.companies` | `CompaniesResource` | `Company` |
| `client.deals` | `DealsResource` | `Deal` |
| `client.invoices` | `InvoicesResource` | `Invoice` |
| `client.quotations` | `QuotationsResource` | `Quotation` |

---

## CRUD methods

All five resources inherit from `CrudResource[M]` and expose:

```python
# List — returns a Page[M] (see Pagination below)
page = client.contacts.list(page=1, page_size=20, filter={"email": "x@y.com"})

# Get a single object by UUID
contact = client.contacts.get("cde0bc5f-8602-4e12-b5d3-f03436b54c0d")

# Create — POSTs to contacts.add, re-fetches full object via contacts.info
contact = client.contacts.create(
    first_name="Ada",
    last_name="Lovelace",
    emails=[{"type": "primary", "email": "ada@example.com"}],
)

# Update — POSTs to contacts.update, re-fetches via contacts.info
contact = client.contacts.update(
    "cde0bc5f-8602-4e12-b5d3-f03436b54c0d",
    last_name="Lovelace-King",
)

# Delete
client.contacts.delete("cde0bc5f-8602-4e12-b5d3-f03436b54c0d")
```

!!! note "create() and update() always re-fetch"
    Both methods re-fetch the full object via `.info` after the write so the returned
    model always reflects the server state (computed fields, defaults, etc.).

---

## Pagination

`list()` returns a `Page[M]` dataclass:

| Attribute | Type | Description |
|---|---|---|
| `data` | `list[M]` | Deserialised model objects on this page |
| `total_count` | `int` | Total matches across **all** pages |
| `current_page` | `int` | 1-based page index |
| `page_size` | `int` | Items requested per page |
| `has_next` | `bool` | `True` when more pages exist |

### Manual pagination

```python
page = client.deals.list(page=1, page_size=20, filter={"status": "open"})

while True:
    for deal in page.data:
        print(deal.title, deal.status)
    if not page.has_next:
        break
    page = page.next()
```

### `iterate()` — consume all pages automatically

```python
# iterate() uses page_size=20 by default; all extra kwargs are forwarded as filters
for contact in client.contacts.iterate(filter={"tag": "vip"}):
    print(contact.full_name, contact.primary_email)
```

`iterate()` is a generator that fetches pages lazily.  Wrap it with `itertools.islice`
to cap the number of objects without loading all pages:

```python
from itertools import islice

# First 100 contacts only
top_100 = list(islice(client.contacts.iterate(), 100))
```

---

## Extra resource methods

### Contacts

```python
# Add / remove tags (silently ignored if already present / absent)
client.contacts.tag(contact_id, ["vip", "expo-2025"])
client.contacts.untag(contact_id, ["expo-2025"])

# Link / unlink a company (position and decision_maker are optional)
client.contacts.link_to_company(
    contact_id,
    company_id,
    position="CTO",
    decision_maker=True,
)
client.contacts.unlink_from_company(contact_id, company_id)
```

### Companies

```python
client.companies.tag(company_id, ["customer", "enterprise"])
client.companies.untag(company_id, ["prospect"])
```

### Deals

```python
# Move a deal to a different pipeline phase
client.deals.move_to_phase(deal_id, phase_id)

# Mark as won or lost
client.deals.win(deal_id)
client.deals.lose(deal_id, reason_id="reason-uuid", extra_info="Too expensive")

# List available phases for a pipeline
phases = client.deals.list_phases(deal_pipeline_id="pipeline-uuid")

# List all deal sources
sources = client.deals.list_sources()
```

### Invoices

```python
# Book a draft invoice (transitions it from draft → booked)
client.invoices.book(invoice_id, on="2025-03-01")

# Credit an invoice — returns a TypeAndId referencing the new credit note
credit_note_ref = client.invoices.credit(invoice_id, credit_note_date="2025-03-05")

# Register a payment
from teamleader.models import Money
client.invoices.register_payment(
    invoice_id,
    payment=Money(amount=500.0, currency="EUR"),
    paid_at="2025-03-01T12:00:00+00:00",
)

# Send via e-mail
client.invoices.send(
    invoice_id,
    subject="Your invoice #2025-042",
    body="Please find your invoice attached.",
)

# Get a pre-signed download URL
# Returns {"location": "<url>", "expires": "<ISO datetime>"}
download = client.invoices.download(invoice_id, format="pdf")
print(download["location"])
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

# Mark a quotation as accepted
client.quotations.accept(quotation_id)
```

---

## Filter kwargs

Filters are forwarded verbatim as the `filter` key in the POST body.  The available
filter fields per endpoint are documented in the
[Generated Endpoint Reference](../api-reference/generated-endpoints.md).

```python
# Filter contacts by tag
page = client.contacts.list(filter={"tag": "vip"})

# Filter open deals assigned to a specific user
page = client.deals.list(filter={"status": ["open"], "assignee_id": user_uuid})
```
