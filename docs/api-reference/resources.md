# Resources — API Reference

Resource classes expose CRUD operations and resource-specific actions on top of
`TeamleaderClient`.  See the [Working with Resources](../guides/resources.md) guide
for usage examples.

---

## Base classes

### Page

`Page[M]` is returned by every `CrudResource.list()` call.

::: teamleader.resources.base.Page

---

### CrudResource

`CrudResource[M]` is the base class for all five curated resources.

::: teamleader.resources.base.CrudResource

---

## Contacts

::: teamleader.resources.contacts.ContactsResource

---

## Companies

::: teamleader.resources.companies.CompaniesResource

---

## Deals

::: teamleader.resources.deals.DealsResource

---

## Invoices

::: teamleader.resources.invoices.InvoicesResource

---

## Quotations

::: teamleader.resources.quotations.QuotationsResource
