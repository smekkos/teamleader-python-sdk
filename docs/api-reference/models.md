# Models — API Reference

Curated model classes with full type hints, `from_api()` deserialisation, and
computed properties.  All models are pure dataclasses (no Pydantic / attrs).

---

## Common sub-models

These sub-models are shared across multiple resource models.

::: teamleader.models.common.TypeAndId

::: teamleader.models.common.Address

::: teamleader.models.common.AddressEntry

::: teamleader.models.common.Email

::: teamleader.models.common.Telephone

::: teamleader.models.common.Money

::: teamleader.models.common.CustomField

::: teamleader.models.common.PaymentTerm

::: teamleader.models.common.WebLink

---

## Contact

::: teamleader.models.contact.Contact

---

## Company

::: teamleader.models.company.Company

---

## Deal

::: teamleader.models.deal.Deal

---

## Invoice

::: teamleader.models.invoice.Invoice

---

## Quotation

::: teamleader.models.quotation.Quotation

---

## Computed properties cheat-sheet

### Contact

| Property | Returns |
|---|---|
| `full_name` | `"First Last"`, whitespace-stripped |
| `primary_email` | First `type="primary"` email address, else first email, else `None` |
| `primary_phone` | First telephone number, or `None` |
| `is_active` | `True` when `status == "active"` |

### Company

| Property | Returns |
|---|---|
| `is_active` | `True` when `status == "active"` |
| `primary_email` | Same selection logic as Contact |
| `primary_phone` | First telephone number, or `None` |

### Deal

| Property | Returns |
|---|---|
| `is_open` | `status == "open"` |
| `is_won` | `status == "won"` |
| `is_lost` | `status == "lost"` |
| `customer_id` | UUID of the lead's customer |
| `customer_type` | `"contact"` or `"company"` |

!!! note "Deal.status is an open string"
    The Teamleader API may return undocumented status values (e.g. `"new"`) not in the
    spec.  `Deal.status` is therefore `str`, not an enum.  The boolean properties guard
    against forward-compatible reads.

### Invoice

| Property | Returns |
|---|---|
| `is_paid` | `paid == True` |
| `is_draft` | `status == "draft"` |
| `is_overdue` | `due_on < today AND NOT paid` (date-safe, returns `False` when `due_on` is `None`) |
| `total_due` | `Money` extracted from `total["due"]`, or `None` |
| `customer_name` | `invoicee["name"]`, or `None` |

### Quotation

| Property | Returns |
|---|---|
| `is_open` | `status == "open"` |
| `is_accepted` | `status == "accepted"` |
| `is_expired` | `status == "expired"` |
| `total_tax_exclusive` | `Money` from `totals["tax_exclusive"]`, or `None` |
| `total_tax_inclusive` | `Money` from `totals["tax_inclusive"]`, or `None` |
