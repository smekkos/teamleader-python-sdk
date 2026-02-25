# Generated API Endpoint Reference

!!! note
    Auto-generated from `codegen/spec/api.yaml` (spec **v1.112.0**).
    Run `python codegen/generate_docs_endpoints.py` to refresh after a spec update.

Every Teamleader Focus API endpoint is a **POST** request.  The table below
groups endpoints by the resource tag used in the official Teamleader documentation.

---

## Calling endpoints via `client.call()`

Every endpoint listed here can be called through
[`TeamleaderClient.call()`](client.md#teamleader.client.TeamleaderClient.call)
using the **operation ID** shown in the table (the `• client.call()` column):

```python
# Example — list activity types (no required params)
result = client.call("activityTypes.list", page={"size": 20, "number": 1})
for item in result["data"]:
    print(item["name"])

# Example — fetch a department by ID (id is required)
dept = client.call("departments.info", id="67c576e7-7e6f-465d-b6ab-a864f6e5e95b")
print(dept["data"]["name"])
```

!!! tip
    `call()` validates required parameters **before** making the HTTP request
    and raises `ValueError` with a helpful message if any are missing.
    The response is a raw `dict` — no model deserialisation.

---

## Departments

Departments are used to split quotations and invoices for different legal entities or within one organisation.

| Endpoint | Summary | Description | `client.call()` |
|---|---|---|---|
| `/departments.info` | `departments.info` | Get details for a single department | `client.call('departments.info')` |
| `/departments.list` | `departments.list` | Get a list of departments | `client.call('departments.list')` |

---

## Users

Users are co-workers in a Teamleader account.

| Endpoint | Summary | Description | `client.call()` |
|---|---|---|---|
| `/users.getWeekSchedule` | `users.getWeekSchedule` | Returns information about week schedule of a user. Only available with the *Weekly working schedule* feature | `client.call('users.getWeekSchedule')` |
| `/users.info` | `users.info` | Get details for a single user | `client.call('users.info')` |
| `/users.list` | `users.list` | Get a list of all users | `client.call('users.list')` |
| `/users.listDaysOff` | `users.listDaysOff` | Returns information about days off of a given user | `client.call('users.listDaysOff')` |
| `/users.me` | `users.me` | Get the current authenticated user | `client.call('users.me')` |

---

## Teams

| Endpoint | Summary | Description | `client.call()` |
|---|---|---|---|
| `/teams.list` | `teams.list` | Gets a list of all teams | `client.call('teams.list')` |

---

## Custom Fields

Custom fields are used to add additional data/properties to entities within Teamleader.

| Endpoint | Summary | Description | `client.call()` |
|---|---|---|---|
| `/customFieldDefinitions.create` | `customFieldDefinitions.create` | Create a custom field definition | `client.call('customFieldDefinitions.create')` |
| `/customFieldDefinitions.info` | `customFieldDefinitions.info` | Get info about a specific custom field definition | `client.call('customFieldDefinitions.info')` |
| `/customFieldDefinitions.list` | `customFieldDefinitions.list` | Get a list of all the definitions of custom fields | `client.call('customFieldDefinitions.list')` |

---

## Work Types

Work types define the type of work for events or time tracking. Hourly rates can be added to work types, so that the work can be billed to a customer.

| Endpoint | Summary | Description | `client.call()` |
|---|---|---|---|
| `/workTypes.list` | `workTypes.list` | Get a list of all work types, sorted alphabetically (on their name) | `client.call('workTypes.list')` |

---

## Document Templates

Document Templates

| Endpoint | Summary | Description | `client.call()` |
|---|---|---|---|
| `/documentTemplates.list` | `documentTemplates.list` | Get a list of all document templates | `client.call('documentTemplates.list')` |

---

## Currencies

Currencies

| Endpoint | Summary | Description | `client.call()` |
|---|---|---|---|
| `/currencies.exchangeRates` | `currencies.exchangeRates` | Get a list of exchange rates for a provided currency | `client.call('currencies.exchangeRates')` |

---

## Notes

Notes

| Endpoint | Summary | Description | `client.call()` |
|---|---|---|---|
| `/notes.create` | `notes.create` | Create a new note | `client.call('notes.create')` |
| `/notes.list` | `notes.list` | Get a list of all notes | `client.call('notes.list')` |
| `/notes.update` | `notes.update` | Update an existing note | `client.call('notes.update')` |

---

## Email Tracking

Email Tracking

| Endpoint | Summary | Description | `client.call()` |
|---|---|---|---|
| `/emailTracking.create` | `emailTracking.create` | Create a new email tracking | `client.call('emailTracking.create')` |
| `/emailTracking.list` | `emailTracking.list` | Get a list of all email tracking | `client.call('emailTracking.list')` |

---

## Closing Days

Closing Days

| Endpoint | Summary | Description | `client.call()` |
|---|---|---|---|
| `/closingDays.add` | `closingDays.add` | Adds a closing day for the account | `client.call('closingDays.add')` |
| `/closingDays.delete` | `closingDays.delete` | Removes a closing day for the account | `client.call('closingDays.delete')` |
| `/closingDays.list` | `closingDays.list` | Returns information about closing days of the account | `client.call('closingDays.list')` |

---

## Day Off Types

Day Off Types

| Endpoint | Summary | Description | `client.call()` |
|---|---|---|---|
| `/dayOffTypes.create` | `dayOffTypes.create` | Create a new day off type | `client.call('dayOffTypes.create')` |
| `/dayOffTypes.delete` | `dayOffTypes.delete` | Delete a day off type | `client.call('dayOffTypes.delete')` |
| `/dayOffTypes.list` | `dayOffTypes.list` | Returns a list of day off types for the account | `client.call('dayOffTypes.list')` |
| `/dayOffTypes.update` | `dayOffTypes.update` | Update a day off type | `client.call('dayOffTypes.update')` |

---

## Days Off

Days Off

| Endpoint | Summary | Description | `client.call()` |
|---|---|---|---|
| `/daysOff.bulkDelete` | `daysOff.bulkDelete` | Deletes a list of days off for the given user | `client.call('daysOff.bulkDelete')` |
| `/daysOff.import` | `daysOff.import` | Imports a list of days off for the given user | `client.call('daysOff.import')` |

---

## Contacts

Contacts are physical entities who are added to your CRM database. Contacts might be linked to one or more companies.

| Endpoint | Summary | Description | `client.call()` |
|---|---|---|---|
| `/contacts.add` | `contacts.add` | Add a new contact | `client.call('contacts.add')` |
| `/contacts.delete` | `contacts.delete` | Delete a contact | `client.call('contacts.delete')` |
| `/contacts.info` | `contacts.info` | Get details for a single contact | `client.call('contacts.info')` |
| `/contacts.linkToCompany` | `contacts.linkToCompany` | Link a contact to a company | `client.call('contacts.linkToCompany')` |
| `/contacts.list` | `contacts.list` | Get a list of contacts | `client.call('contacts.list')` |
| `/contacts.tag` | `contacts.tag` | Add a new or existing tag to a contact | `client.call('contacts.tag')` |
| `/contacts.unlinkFromCompany` | `contacts.unlinkFromCompany` | Unlink a contact from a company | `client.call('contacts.unlinkFromCompany')` |
| `/contacts.untag` | `contacts.untag` | Remove a tag from a contact | `client.call('contacts.untag')` |
| `/contacts.update` | `contacts.update` | Update a contact | `client.call('contacts.update')` |
| `/contacts.updateCompanyLink` | `contacts.updateCompanyLink` | Update contact to company link | `client.call('contacts.updateCompanyLink')` |
| `/contacts.uploadAvatar` | `contacts.uploadAvatar` | Update the avatar of a contact | `client.call('contacts.uploadAvatar')` |

---

## Companies

Companies are legal entities, usually linked to a VAT and/or local business number.

| Endpoint | Summary | Description | `client.call()` |
|---|---|---|---|
| `/companies.add` | `companies.add` | Add a new company | `client.call('companies.add')` |
| `/companies.delete` | `companies.delete` | Delete a company | `client.call('companies.delete')` |
| `/companies.info` | `companies.info` | Get details for a single company | `client.call('companies.info')` |
| `/companies.list` | `companies.list` | Get a list of companies | `client.call('companies.list')` |
| `/companies.tag` | `companies.tag` | Add a new or existing tag to a company | `client.call('companies.tag')` |
| `/companies.untag` | `companies.untag` | Remove a tag from a company | `client.call('companies.untag')` |
| `/companies.update` | `companies.update` | Update a company | `client.call('companies.update')` |
| `/companies.uploadLogo` | `companies.uploadLogo` | Update the logo of a company | `client.call('companies.uploadLogo')` |

---

## Business Types

Each country has a specific set of business types or range of legal entities. You can specify the business type when adding or updating a company.

| Endpoint | Summary | Description | `client.call()` |
|---|---|---|---|
| `/businessTypes.list` | `businessTypes.list` | Get the names of business types (legal structures) a company can have within a certain country, sorted alphabetically | `client.call('businessTypes.list')` |

---

## Tags

Tags are used to label contacts or companies, so that they can easily be filtered or grouped into segments.

| Endpoint | Summary | Description | `client.call()` |
|---|---|---|---|
| `/tags.list` | `tags.list` | Get a list of tags | `client.call('tags.list')` |

---

## Addresses

We provide a set of data which can be used to build addresses.

| Endpoint | Summary | Description | `client.call()` |
|---|---|---|---|
| `/levelTwoAreas.list` | `levelTwoAreas.list` | Get a list of level two areas (which correspond to provinces, departments or states in most countries) | `client.call('levelTwoAreas.list')` |

---

## Deals

Deals are sale opportunities, which need to be followed up by their responsible user. A deal can move through specific deal phases, and be marked as won or lost.

| Endpoint | Summary | Description | `client.call()` |
|---|---|---|---|
| `/deals.create` | `deals.create` | Create a new deal for a customer | `client.call('deals.create')` |
| `/deals.delete` | `deals.delete` | Delete a deal | `client.call('deals.delete')` |
| `/deals.info` | `deals.info` | Get details for a single deal | `client.call('deals.info')` |
| `/deals.list` | `deals.list` | Get a list of deals | `client.call('deals.list')` |
| `/deals.lose` | `deals.lose` | Mark a deal as lost | `client.call('deals.lose')` |
| `/deals.move` | `deals.move` | Move the deal to a different phase | `client.call('deals.move')` |
| `/deals.update` | `deals.update` | Update a deal | `client.call('deals.update')` |
| `/deals.win` | `deals.win` | Mark a deal as won | `client.call('deals.win')` |
| `/lostReasons.list` | `lostReasons.list` | Get a list of lost reasons for deals | `client.call('lostReasons.list')` |

---

## Deal Pipelines

Each deal belongs to a specific pipeline, in which it goes through the different deal phases.

| Endpoint | Summary | Description | `client.call()` |
|---|---|---|---|
| `/dealPipelines.create` | `dealPipelines.create` | Create a new deal pipeline | `client.call('dealPipelines.create')` |
| `/dealPipelines.delete` | `dealPipelines.delete` | Delete a deal pipeline | `client.call('dealPipelines.delete')` |
| `/dealPipelines.duplicate` | `dealPipelines.duplicate` | Create a new deal pipeline by duplicating an existing one | `client.call('dealPipelines.duplicate')` |
| `/dealPipelines.list` | `dealPipelines.list` | Get a list of all deal pipelines | `client.call('dealPipelines.list')` |
| `/dealPipelines.markAsDefault` | `dealPipelines.markAsDefault` | Mark a pipeline as default | `client.call('dealPipelines.markAsDefault')` |
| `/dealPipelines.update` | `dealPipelines.update` | Update a single deal pipeline | `client.call('dealPipelines.update')` |

---

## Deal Phases

Deal phases are the different phases a deal typically goes through. A deal can be moved to either a next or previous phase. A deal can be marked as won or lost independently from the deal phase.

| Endpoint | Summary | Description | `client.call()` |
|---|---|---|---|
| `/dealPhases.create` | `dealPhases.create` | Create a new deal phase | `client.call('dealPhases.create')` |
| `/dealPhases.delete` | `dealPhases.delete` | Delete a phase | `client.call('dealPhases.delete')` |
| `/dealPhases.duplicate` | `dealPhases.duplicate` | Create a new deal phase by duplicating an existing one | `client.call('dealPhases.duplicate')` |
| `/dealPhases.list` | `dealPhases.list` | Get a list of all phases a deal can go through, sorted by their order in the flow | `client.call('dealPhases.list')` |
| `/dealPhases.move` | `dealPhases.move` | Move a phase to a new position in the pipeline | `client.call('dealPhases.move')` |
| `/dealPhases.update` | `dealPhases.update` | Update a deal phase | `client.call('dealPhases.update')` |

---

## Deal Sources

Deal sources are used to track the origin of a deal.

| Endpoint | Summary | Description | `client.call()` |
|---|---|---|---|
| `/dealSources.list` | `dealSources.list` | Get a list of all deal sources, sorted alphabetically (on name) | `client.call('dealSources.list')` |

---

## Quotations

A quotation is a sales offer for a specific customer. It is always attached to a deal. Quotations can be signed online via Cloudsign.

| Endpoint | Summary | Description | `client.call()` |
|---|---|---|---|
| `/quotations.accept` | `quotations.accept` | Mark a quotation as accepted | `client.call('quotations.accept')` |
| `/quotations.create` | `quotations.create` | Create a quotation | `client.call('quotations.create')` |
| `/quotations.delete` | `quotations.delete` | Delete a quotation | `client.call('quotations.delete')` |
| `/quotations.download` | `quotations.download` | Download a quotation in a specific format | `client.call('quotations.download')` |
| `/quotations.info` | `quotations.info` | Get a quotation | `client.call('quotations.info')` |
| `/quotations.list` | `quotations.list` | Get a list of quotations | `client.call('quotations.list')` |
| `/quotations.send` | `quotations.send` | Send a quotation | `client.call('quotations.send')` |
| `/quotations.update` | `quotations.update` | Update a quotation | `client.call('quotations.update')` |

---

## Orders

| Endpoint | Summary | Description | `client.call()` |
|---|---|---|---|
| `/orders.info` | `orders.info` | Get details for a single order | `client.call('orders.info')` |
| `/orders.list` | `orders.list` | Get a list of orders | `client.call('orders.list')` |

---

## Meetings

Meetings

| Endpoint | Summary | Description | `client.call()` |
|---|---|---|---|
| `/meetings.complete` | `meetings.complete` | Mark a meeting as complete | `client.call('meetings.complete')` |
| `/meetings.createReport` | `meetings.createReport` | Creates a report for a meeting | `client.call('meetings.createReport')` |
| `/meetings.delete` | `meetings.delete` | Deletes a meeting | `client.call('meetings.delete')` |
| `/meetings.info` | `meetings.info` | Get information about a meeting | `client.call('meetings.info')` |
| `/meetings.list` | `meetings.list` | Get a list of meetings | `client.call('meetings.list')` |
| `/meetings.schedule` | `meetings.schedule` | Schedule a meeting | `client.call('meetings.schedule')` |
| `/meetings.update` | `meetings.update` | Update a meeting | `client.call('meetings.update')` |

---

## Calls

Calls

| Endpoint | Summary | Description | `client.call()` |
|---|---|---|---|
| `/calls.add` | `calls.add` | Add a new call | `client.call('calls.add')` |
| `/calls.complete` | `calls.complete` | Mark a call as complete | `client.call('calls.complete')` |
| `/calls.info` | `calls.info` | Get information about a call | `client.call('calls.info')` |
| `/calls.list` | `calls.list` | Get a list of calls | `client.call('calls.list')` |
| `/calls.update` | `calls.update` | Update a new call | `client.call('calls.update')` |

---

## Call Outcomes

Call Outcomes

| Endpoint | Summary | Description | `client.call()` |
|---|---|---|---|
| `/callOutcomes.list` | `callOutcomes.list` | Get a list of call outcomes | `client.call('callOutcomes.list')` |

---

## Calendar events

Calendar events are scheduled events in your calendar. A calendar event involves a particular activity type: a task, meeting or call.

| Endpoint | Summary | Description | `client.call()` |
|---|---|---|---|
| `/events.cancel` | `events.cancel` | Cancel a calendar event (for all attendees) | `client.call('events.cancel')` |
| `/events.create` | `events.create` | Create a new calendar event | `client.call('events.create')` |
| `/events.info` | `events.info` | Get details for a single calendar event | `client.call('events.info')` |
| `/events.list` | `events.list` | Get a list of calendar events | `client.call('events.list')` |
| `/events.update` | `events.update` | Update a calendar event | `client.call('events.update')` |

---

## Activity Types

Activity types identify the different types of events that take place within your organisation.

| Endpoint | Summary | Description | `client.call()` |
|---|---|---|---|
| `/activityTypes.list` | `activityTypes.list` | Get a list of all activity types | `client.call('activityTypes.list')` |

---

## Invoices

Teamleader provides a whole set of endpoints to make it easy to develop

| Endpoint | Summary | Description | `client.call()` |
|---|---|---|---|
| `/invoices.book` | `invoices.book` | Book a draft invoice | `client.call('invoices.book')` |
| `/invoices.copy` | `invoices.copy` | Creates a new draft invoice based on another invoice | `client.call('invoices.copy')` |
| `/invoices.credit` | `invoices.credit` | Credit an invoice completely | `client.call('invoices.credit')` |
| `/invoices.creditPartially` | `invoices.creditPartially` | Credit an invoice partially | `client.call('invoices.creditPartially')` |
| `/invoices.delete` | `invoices.delete` | Delete an existing invoice. Only possible for draft invoices or the last booked invoice | `client.call('invoices.delete')` |
| `/invoices.download` | `invoices.download` | Download an invoice in a specific format | `client.call('invoices.download')` |
| `/invoices.draft` | `invoices.draft` | Draft a new invoice | `client.call('invoices.draft')` |
| `/invoices.info` | `invoices.info` | Get details for a single invoice | `client.call('invoices.info')` |
| `/invoices.list` | `invoices.list` | Get a list of invoices | `client.call('invoices.list')` |
| `/invoices.registerPayment` | `invoices.registerPayment` | Register a payment for an invoice | `client.call('invoices.registerPayment')` |
| `/invoices.removePayments` | `invoices.removePayments` | Marks an invoice as unpaid and removes all linked payments. This will also trigger a re-rendering of the invoice PDF | `client.call('invoices.removePayments')` |
| `/invoices.send` | `invoices.send` | Send an invoice via e-mail | `client.call('invoices.send')` |
| `/invoices.sendViaPeppol` | `invoices.sendViaPeppol` | Send an invoice via the Peppol network | `client.call('invoices.sendViaPeppol')` |
| `/invoices.update` | `invoices.update` | Update a draft invoice. Booked invoices cannot be updated | `client.call('invoices.update')` |
| `/invoices.updateBooked` | `invoices.updateBooked` | Update a booked invoice. Only available when editing booked invoices is allowed through the settings | `client.call('invoices.updateBooked')` |

---

## Credit Notes

Credit notes are created when certain products or services are not delivered

| Endpoint | Summary | Description | `client.call()` |
|---|---|---|---|
| `/creditNotes.download` | `creditNotes.download` | Download a credit note in a specific format | `client.call('creditNotes.download')` |
| `/creditNotes.info` | `creditNotes.info` | Get details for a single credit note | `client.call('creditNotes.info')` |
| `/creditNotes.list` | `creditNotes.list` | List credit notes | `client.call('creditNotes.list')` |
| `/creditNotes.sendViaPeppol` | `creditNotes.sendViaPeppol` | Send a credit note via the Peppol network | `client.call('creditNotes.sendViaPeppol')` |

---

## Subscriptions

Subscriptions

| Endpoint | Summary | Description | `client.call()` |
|---|---|---|---|
| `/subscriptions.create` | `subscriptions.create` | Create a new subscription | `client.call('subscriptions.create')` |
| `/subscriptions.deactivate` | `subscriptions.deactivate` | Deactivate a subscription | `client.call('subscriptions.deactivate')` |
| `/subscriptions.info` | `subscriptions.info` | Get details for a single subscription | `client.call('subscriptions.info')` |
| `/subscriptions.list` | `subscriptions.list` | Get a list of subscriptions | `client.call('subscriptions.list')` |
| `/subscriptions.update` | `subscriptions.update` | Update a subscription | `client.call('subscriptions.update')` |

---

## Tax Rates

Tax rates provide an overview of different taxation rates used to bill

| Endpoint | Summary | Description | `client.call()` |
|---|---|---|---|
| `/taxRates.list` | `taxRates.list` | Get a list of available tax rates | `client.call('taxRates.list')` |

---

## Payment Terms

Payment terms are the conditions under which an invoice need to be paid.

| Endpoint | Summary | Description | `client.call()` |
|---|---|---|---|
| `/paymentTerms.list` | `paymentTerms.list` | Get a list of available payment terms | `client.call('paymentTerms.list')` |

---

## Withholding Tax Rates

Withholding tax rates provide an overview of different taxation rates used

| Endpoint | Summary | Description | `client.call()` |
|---|---|---|---|
| `/withholdingTaxRates.list` | `withholdingTaxRates.list` | Get a list of available withholding tax rates | `client.call('withholdingTaxRates.list')` |

---

## Commercial Discounts

Commercial Discounts

| Endpoint | Summary | Description | `client.call()` |
|---|---|---|---|
| `/commercialDiscounts.list` | `commercialDiscounts.list` | Get a list of commercial discounts | `client.call('commercialDiscounts.list')` |

---

## Payment Methods

Payment Methods

| Endpoint | Summary | Description | `client.call()` |
|---|---|---|---|
| `/paymentMethods.list` | `paymentMethods.list` | Get a list of payment methods | `client.call('paymentMethods.list')` |

---

## Expenses

Expenses

| Endpoint | Summary | Description | `client.call()` |
|---|---|---|---|
| `/expenses.list` | `expenses.list` | Get a list of all expenses | `client.call('expenses.list')` |

---

## Bookkeeping Submissions

Bookkeeping Submissions

| Endpoint | Summary | Description | `client.call()` |
|---|---|---|---|
| `/bookkeepingSubmissions.list` | `bookkeepingSubmissions.list` | List all bookkeeping submissions belonging to a specific financial document id and type | `client.call('bookkeepingSubmissions.list')` |

---

## Incoming Credit Notes

Incoming credit notes are credit notes received from your suppliers. They

| Endpoint | Summary | Description | `client.call()` |
|---|---|---|---|
| `/incomingCreditNotes.add` | `incomingCreditNotes.add` | Adds an incoming credit note | `client.call('incomingCreditNotes.add')` |
| `/incomingCreditNotes.approve` | `incomingCreditNotes.approve` | Approve an incoming credit note | `client.call('incomingCreditNotes.approve')` |
| `/incomingCreditNotes.delete` | `incomingCreditNotes.delete` | Deletes an incoming credit note | `client.call('incomingCreditNotes.delete')` |
| `/incomingCreditNotes.info` | `incomingCreditNotes.info` | Get details for a single incoming credit note | `client.call('incomingCreditNotes.info')` |
| `/incomingCreditNotes.listPayments` | `incomingCreditNotes.listPayments` | List payments for an incoming credit note | `client.call('incomingCreditNotes.listPayments')` |
| `/incomingCreditNotes.markAsPendingReview` | `incomingCreditNotes.markAsPendingReview` | Mark an incoming credit note as pending review | `client.call('incomingCreditNotes.markAsPendingReview')` |
| `/incomingCreditNotes.refuse` | `incomingCreditNotes.refuse` | Refuse an incoming credit note | `client.call('incomingCreditNotes.refuse')` |
| `/incomingCreditNotes.registerPayment` | `incomingCreditNotes.registerPayment` | Register a payment for an incoming credit note | `client.call('incomingCreditNotes.registerPayment')` |
| `/incomingCreditNotes.removePayment` | `incomingCreditNotes.removePayment` | Remove a payment from an incoming credit note | `client.call('incomingCreditNotes.removePayment')` |
| `/incomingCreditNotes.sendToBookkeeping` | `incomingCreditNotes.sendToBookkeeping` | Send an incoming credit note to bookkeeping | `client.call('incomingCreditNotes.sendToBookkeeping')` |
| `/incomingCreditNotes.update` | `incomingCreditNotes.update` | Updates an incoming credit note | `client.call('incomingCreditNotes.update')` |
| `/incomingCreditNotes.updatePayment` | `incomingCreditNotes.updatePayment` | Update a payment for an incoming credit note | `client.call('incomingCreditNotes.updatePayment')` |

---

## Incoming Invoices

Incoming invoices are invoices received from your suppliers. They can be

| Endpoint | Summary | Description | `client.call()` |
|---|---|---|---|
| `/incomingInvoices.add` | `incomingInvoices.add` | Adds an incoming invoice | `client.call('incomingInvoices.add')` |
| `/incomingInvoices.approve` | `incomingInvoices.approve` | Approve an incoming invoice | `client.call('incomingInvoices.approve')` |
| `/incomingInvoices.delete` | `incomingInvoices.delete` | Deletes an incoming invoice | `client.call('incomingInvoices.delete')` |
| `/incomingInvoices.info` | `incomingInvoices.info` | Get details for a single incoming invoice | `client.call('incomingInvoices.info')` |
| `/incomingInvoices.listPayments` | `incomingInvoices.listPayments` | List payments for an incoming invoice | `client.call('incomingInvoices.listPayments')` |
| `/incomingInvoices.markAsPendingReview` | `incomingInvoices.markAsPendingReview` | Mark an incoming invoice as pending review | `client.call('incomingInvoices.markAsPendingReview')` |
| `/incomingInvoices.refuse` | `incomingInvoices.refuse` | Refuse an incoming invoice | `client.call('incomingInvoices.refuse')` |
| `/incomingInvoices.registerPayment` | `incomingInvoices.registerPayment` | Register a payment for an incoming invoice | `client.call('incomingInvoices.registerPayment')` |
| `/incomingInvoices.removePayment` | `incomingInvoices.removePayment` | Remove a payment from an incoming invoice | `client.call('incomingInvoices.removePayment')` |
| `/incomingInvoices.sendToBookkeeping` | `incomingInvoices.sendToBookkeeping` | Send an incoming invoice to bookkeeping | `client.call('incomingInvoices.sendToBookkeeping')` |
| `/incomingInvoices.update` | `incomingInvoices.update` | Updates an incoming invoice | `client.call('incomingInvoices.update')` |
| `/incomingInvoices.updatePayment` | `incomingInvoices.updatePayment` | Update a payment for an incoming invoice | `client.call('incomingInvoices.updatePayment')` |

---

## Receipts

Receipts are expenses for which you have a receipt, but no invoice. They can

| Endpoint | Summary | Description | `client.call()` |
|---|---|---|---|
| `/receipts.add` | `receipts.add` | Adds a receipt | `client.call('receipts.add')` |
| `/receipts.approve` | `receipts.approve` | Approve a receipt | `client.call('receipts.approve')` |
| `/receipts.delete` | `receipts.delete` | Deletes a receipt | `client.call('receipts.delete')` |
| `/receipts.info` | `receipts.info` | Get details for a single receipt | `client.call('receipts.info')` |
| `/receipts.listPayments` | `receipts.listPayments` | List payments for a(n incoming) receipt | `client.call('receipts.listPayments')` |
| `/receipts.markAsPendingReview` | `receipts.markAsPendingReview` | Mark a receipts as pending review | `client.call('receipts.markAsPendingReview')` |
| `/receipts.refuse` | `receipts.refuse` | Refuse a receipts | `client.call('receipts.refuse')` |
| `/receipts.registerPayment` | `receipts.registerPayment` | Register a payment for a(n incoming) receipt | `client.call('receipts.registerPayment')` |
| `/receipts.removePayment` | `receipts.removePayment` | Remove a payment from a receipt | `client.call('receipts.removePayment')` |
| `/receipts.sendToBookkeeping` | `receipts.sendToBookkeeping` | Send a receipt to bookkeeping for processing | `client.call('receipts.sendToBookkeeping')` |
| `/receipts.update` | `receipts.update` | Updates a receipt | `client.call('receipts.update')` |
| `/receipts.updatePayment` | `receipts.updatePayment` | Update a payment for a(n incoming) receipt | `client.call('receipts.updatePayment')` |

---

## Product Categories

Product categories are used to group specific products. They can be linked

| Endpoint | Summary | Description | `client.call()` |
|---|---|---|---|
| `/productCategories.list` | `productCategories.list` | Get a list of product categories | `client.call('productCategories.list')` |

---

## Products

| Endpoint | Summary | Description | `client.call()` |
|---|---|---|---|
| `/products.add` | `products.add` | Add a new product | `client.call('products.add')` |
| `/products.delete` | `products.delete` | Delete a product | `client.call('products.delete')` |
| `/products.info` | `products.info` | Get details for a single product | `client.call('products.info')` |
| `/products.list` | `products.list` | Get a list of products | `client.call('products.list')` |
| `/products.update` | `products.update` | Update a product | `client.call('products.update')` |

---

## Units of Measure

Units of Measure

| Endpoint | Summary | Description | `client.call()` |
|---|---|---|---|
| `/unitsOfMeasure.list` | `unitsOfMeasure.list` | Get a list of units of measure | `client.call('unitsOfMeasure.list')` |

---

## Price Lists

Price Lists

| Endpoint | Summary | Description | `client.call()` |
|---|---|---|---|
| `/priceLists.list` | `priceLists.list` | Get a list of priceLists | `client.call('priceLists.list')` |

---

## Legacy Projects

Projects allow users to work together as a team on a single project. They

| Endpoint | Summary | Description | `client.call()` |
|---|---|---|---|
| `/projects.addParticipant` | `projects.addParticipant` | Add a participant to a project | `client.call('projects.addParticipant')` |
| `/projects.close` | `projects.close` | Closes a project, all its phases, and all tasks within each phase (but not meetings) | `client.call('projects.close')` |
| `/projects.create` | `projects.create` | Create a new project | `client.call('projects.create')` |
| `/projects.delete` | `projects.delete` | Delete a project | `client.call('projects.delete')` |
| `/projects.info` | `projects.info` | Get details for a single project | `client.call('projects.info')` |
| `/projects.list` | `projects.list` | Get a list of projects | `client.call('projects.list')` |
| `/projects.reopen` | `projects.reopen` | Reopens a project, changing its status to "active" | `client.call('projects.reopen')` |
| `/projects.update` | `projects.update` | Update a project | `client.call('projects.update')` |
| `/projects.updateParticipant` | `projects.updateParticipant` | Update a participant's role for a project | `client.call('projects.updateParticipant')` |

---

## Legacy Milestones

Every projects consists of one or more milestones which are limited in time

| Endpoint | Summary | Description | `client.call()` |
|---|---|---|---|
| `/milestones.close` | `milestones.close` | Close a milestone. All open tasks will be closed, open meetings will remain open. Closing the last open milestone will also close the project | `client.call('milestones.close')` |
| `/milestones.create` | `milestones.create` | Create a new milestone | `client.call('milestones.create')` |
| `/milestones.delete` | `milestones.delete` | Delete a milestone | `client.call('milestones.delete')` |
| `/milestones.info` | `milestones.info` | Get details for a single milestone | `client.call('milestones.info')` |
| `/milestones.list` | `milestones.list` | Get a list of project milestones | `client.call('milestones.list')` |
| `/milestones.open` | `milestones.open` | (Re)open a milestone. If the milestone's project is closed, the project will be reopened | `client.call('milestones.open')` |
| `/milestones.update` | `milestones.update` | Update a milestone | `client.call('milestones.update')` |

---

## Projects

> _This is the documentation of the new projects module. See the **Legacy

| Endpoint | Summary | Description | `client.call()` |
|---|---|---|---|
| `/projects-v2/projects.addCustomer` | `projects.addCustomer` | Add a customer to the project. Doesn't fail if the customer was already added | `client.call('projects-v2/projects.addCustomer')` |
| `/projects-v2/projects.addDeal` | `projects.addDeal` | Add a deal to the project. Doesn't fail if the deal was already added | `client.call('projects-v2/projects.addDeal')` |
| `/projects-v2/projects.addOwner` | `projects.addOwner` | Add a user as owner. Doesn't fail if the user was already added | `client.call('projects-v2/projects.addOwner')` |
| `/projects-v2/projects.addQuotation` | `projects.addQuotation` | Add a quotation to the project. Doesn't fail if the quotation was already added | `client.call('projects-v2/projects.addQuotation')` |
| `/projects-v2/projects.assign` | `projects.assign` | Assign a user or a team to a project | `client.call('projects-v2/projects.assign')` |
| `/projects-v2/projects.close` | `projects.close` | Mark a project as closed | `client.call('projects-v2/projects.close')` |
| `/projects-v2/projects.create` | `projects.create` | Create a new project. Only `title` is required. All the other fields are optional | `client.call('projects-v2/projects.create')` |
| `/projects-v2/projects.delete` | `projects.delete` | Delete a project | `client.call('projects-v2/projects.delete')` |
| `/projects-v2/projects.duplicate` | `projects.duplicate` | Duplicate a project | `client.call('projects-v2/projects.duplicate')` |
| `/projects-v2/projects.info` | `projects.info` | Returns all the information of a single project | `client.call('projects-v2/projects.info')` |
| `/projects-v2/projects.list` | `projects.list` | Lists all projects that match the optional filters provided | `client.call('projects-v2/projects.list')` |
| `/projects-v2/projects.removeCustomer` | `projects.removeCustomer` | Remove a customer from the project. Doesn't fail if the customer was not added | `client.call('projects-v2/projects.removeCustomer')` |
| `/projects-v2/projects.removeDeal` | `projects.removeDeal` | Remove a deal from the project. Doesn't fail if the deal was already removed | `client.call('projects-v2/projects.removeDeal')` |
| `/projects-v2/projects.removeOwner` | `projects.removeOwner` | Remove a user as owner. Doesn't fail if the user wasn't linked | `client.call('projects-v2/projects.removeOwner')` |
| `/projects-v2/projects.removeQuotation` | `projects.removeQuotation` | Remove a quotation from the project. Doesn't fail if the quotation was already removed | `client.call('projects-v2/projects.removeQuotation')` |
| `/projects-v2/projects.reopen` | `projects.reopen` | Reopen a closed project | `client.call('projects-v2/projects.reopen')` |
| `/projects-v2/projects.unassign` | `projects.unassign` | Unassign a user or a team from a project | `client.call('projects-v2/projects.unassign')` |
| `/projects-v2/projects.update` | `projects.update` | Update a project. All attributes except for `id` are optional. Providing `null` will clear that value from the project (for properties that are nullable) | `client.call('projects-v2/projects.update')` |

---

## External parties

> An external party is a contact or company that is added to a project with an optional function and/or sub function.

| Endpoint | Summary | Description | `client.call()` |
|---|---|---|---|
| `/projects-v2/externalParties.addToProject` | `externalParties.addToProject` | Add an external party to a project | `client.call('projects-v2/externalParties.addToProject')` |
| `/projects-v2/externalParties.delete` | `externalParties.delete` | Delete an external party | `client.call('projects-v2/externalParties.delete')` |
| `/projects-v2/externalParties.update` | `externalParties.update` | Update an external party | `client.call('projects-v2/externalParties.update')` |

---

## Project lines

> A project line can be a group, a task, or a material.

| Endpoint | Summary | Description | `client.call()` |
|---|---|---|---|
| `/projects-v2/projectLines.addToGroup` | `projectLines.addToGroup` | Add an existing task or material to a group | `client.call('projects-v2/projectLines.addToGroup')` |
| `/projects-v2/projectLines.list` | `projectLines.list` | All line types (tasks, materials, groups) can be side-loaded | `client.call('projects-v2/projectLines.list')` |
| `/projects-v2/projectLines.removeFromGroup` | `projectLines.removeFromGroup` | Remove a task or material from the group it is currently in | `client.call('projects-v2/projectLines.removeFromGroup')` |

---

## Groups

| Endpoint | Summary | Description | `client.call()` |
|---|---|---|---|
| `/projects-v2/projectGroups.assign` | `projectGroups.assign` | Assign a user or a team to a group | `client.call('projects-v2/projectGroups.assign')` |
| `/projects-v2/projectGroups.create` | `projectGroups.create` | Create a group. All properties except for `title` and `project_id` are optional | `client.call('projects-v2/projectGroups.create')` |
| `/projects-v2/projectGroups.delete` | `projectGroups.delete` | Delete a group | `client.call('projects-v2/projectGroups.delete')` |
| `/projects-v2/projectGroups.duplicate` | `projectGroups.duplicate` | Duplicate a group and its entities, without any time trackings | `client.call('projects-v2/projectGroups.duplicate')` |
| `/projects-v2/projectGroups.info` | `projectGroups.info` | Returns all the information for one group | `client.call('projects-v2/projectGroups.info')` |
| `/projects-v2/projectGroups.list` | `projectGroups.list` | Lists all the groups that match the optional filters provided | `client.call('projects-v2/projectGroups.list')` |
| `/projects-v2/projectGroups.unassign` | `projectGroups.unassign` | Unassign a user or a team from a group | `client.call('projects-v2/projectGroups.unassign')` |
| `/projects-v2/projectGroups.update` | `projectGroups.update` | Update a group. All attributes except for `id` are optional. Providing `null` will clear that value from the project (for properties that are nullable) | `client.call('projects-v2/projectGroups.update')` |

---

## Tasks

> _These endpoints are for (new) project tasks. For documentation on

| Endpoint | Summary | Description | `client.call()` |
|---|---|---|---|
| `/projects-v2/tasks.assign` | `tasks.assign` | Assign a user or a team to a task | `client.call('projects-v2/tasks.assign')` |
| `/projects-v2/tasks.create` | `tasks.create` | Create a task. All properties except for `title` and `project_id` are optional | `client.call('projects-v2/tasks.create')` |
| `/projects-v2/tasks.delete` | `tasks.delete` | Delete a task | `client.call('projects-v2/tasks.delete')` |
| `/projects-v2/tasks.duplicate` | `tasks.duplicate` | Duplicate a task, without its time trackings | `client.call('projects-v2/tasks.duplicate')` |
| `/projects-v2/tasks.info` | `tasks.info` | Returns all the information for one task | `client.call('projects-v2/tasks.info')` |
| `/projects-v2/tasks.list` | `tasks.list` | Lists all the tasks that match the optional filters provided | `client.call('projects-v2/tasks.list')` |
| `/projects-v2/tasks.unassign` | `tasks.unassign` | Unassign a user or a team from a task | `client.call('projects-v2/tasks.unassign')` |
| `/projects-v2/tasks.update` | `tasks.update` | Update a task. All attributes except for `id` are optional. Providing `null` will clear that value from the project (for properties that are nullable) | `client.call('projects-v2/tasks.update')` |

---

## Materials

| Endpoint | Summary | Description | `client.call()` |
|---|---|---|---|
| `/projects-v2/materials.assign` | `materials.assign` | Assign a user or a team to a material | `client.call('projects-v2/materials.assign')` |
| `/projects-v2/materials.create` | `materials.create` | Create a material. All properties except for `title` and `project_id` are optional | `client.call('projects-v2/materials.create')` |
| `/projects-v2/materials.delete` | `materials.delete` | Delete a material | `client.call('projects-v2/materials.delete')` |
| `/projects-v2/materials.duplicate` | `materials.duplicate` | Duplicate a material | `client.call('projects-v2/materials.duplicate')` |
| `/projects-v2/materials.info` | `materials.info` | Returns all the information for one material | `client.call('projects-v2/materials.info')` |
| `/projects-v2/materials.list` | `materials.list` | Lists all the materials that match the optional filters provided | `client.call('projects-v2/materials.list')` |
| `/projects-v2/materials.unassign` | `materials.unassign` | Unassign a user or a team from a material | `client.call('projects-v2/materials.unassign')` |
| `/projects-v2/materials.update` | `materials.update` | Update a material. All attributes except for `id` are optional. Providing `null` will clear that value from the project (for properties that are nullable) | `client.call('projects-v2/materials.update')` |

---

## Tasks

Tasks

| Endpoint | Summary | Description | `client.call()` |
|---|---|---|---|
| `/tasks.complete` | `tasks.complete` | Mark a task as complete | `client.call('tasks.complete')` |
| `/tasks.create` | `tasks.create` | Create a new task | `client.call('tasks.create')` |
| `/tasks.delete` | `tasks.delete` | Delete a task | `client.call('tasks.delete')` |
| `/tasks.info` | `tasks.info` | Get information about a task | `client.call('tasks.info')` |
| `/tasks.list` | `tasks.list` | Get a list of tasks | `client.call('tasks.list')` |
| `/tasks.reopen` | `tasks.reopen` | Reopen a task that had been marked as complete | `client.call('tasks.reopen')` |
| `/tasks.schedule` | `tasks.schedule` | Schedule a task in your calendar | `client.call('tasks.schedule')` |
| `/tasks.update` | `tasks.update` | Update a task | `client.call('tasks.update')` |

---

## Time Tracking

Time tracking allows users to record time spent on tasks or projects and the

| Endpoint | Summary | Description | `client.call()` |
|---|---|---|---|
| `/timeTracking.add` | `timeTracking.add` | Add tracked time | `client.call('timeTracking.add')` |
| `/timeTracking.delete` | `timeTracking.delete` | Delete a tracked time | `client.call('timeTracking.delete')` |
| `/timeTracking.info` | `timeTracking.info` | Get information about tracked time | `client.call('timeTracking.info')` |
| `/timeTracking.list` | `timeTracking.list` | Get a list of tracked time | `client.call('timeTracking.list')` |
| `/timeTracking.resume` | `timeTracking.resume` | Start a new timer based on previously tracked time | `client.call('timeTracking.resume')` |
| `/timeTracking.update` | `timeTracking.update` | Update tracked time | `client.call('timeTracking.update')` |

---

## Timers

Timers are an easy way to track time. You can start, stop or resume a timer

| Endpoint | Summary | Description | `client.call()` |
|---|---|---|---|
| `/timers.current` | `timers.current` | Get the current running timer | `client.call('timers.current')` |
| `/timers.start` | `timers.start` | Start a new timer | `client.call('timers.start')` |
| `/timers.stop` | `timers.stop` | Stop the current timer. This will add a new time tracking in the background | `client.call('timers.stop')` |
| `/timers.update` | `timers.update` | Update the current timer. Only possible if there is a timer running | `client.call('timers.update')` |

---

## Tickets

| Endpoint | Summary | Description | `client.call()` |
|---|---|---|---|
| `/tickets.addInternalMessage` | `tickets.addInternalMessage` | Adds an internal message to a ticket | `client.call('tickets.addInternalMessage')` |
| `/tickets.addReply` | `tickets.addReply` | Adds a message to a ticket | `client.call('tickets.addReply')` |
| `/tickets.create` | `tickets.create` | Create a ticket | `client.call('tickets.create')` |
| `/tickets.getMessage` | `tickets.getMessage` | Gets the ticket message | `client.call('tickets.getMessage')` |
| `/tickets.importMessage` | `tickets.importMessage` | Imports an existing message to a ticket | `client.call('tickets.importMessage')` |
| `/tickets.info` | `tickets.info` | Get details for a single ticket | `client.call('tickets.info')` |
| `/tickets.list` | `tickets.list` | Get a list of tickets | `client.call('tickets.list')` |
| `/tickets.listMessages` | `tickets.listMessages` | Lists messages of a ticket | `client.call('tickets.listMessages')` |
| `/tickets.update` | `tickets.update` | Update a ticket | `client.call('tickets.update')` |

---

## Ticket Status

Ticket Status

| Endpoint | Summary | Description | `client.call()` |
|---|---|---|---|
| `/ticketStatus.list` | `ticketStatus.list` | Get a list of ticket statuses | `client.call('ticketStatus.list')` |

---

## Files

Files

| Endpoint | Summary | Description | `client.call()` |
|---|---|---|---|
| `/files.delete` | `files.delete` | Delete a file | `client.call('files.delete')` |
| `/files.download` | `files.download` | Request the download link for a file | `client.call('files.download')` |
| `/files.info` | `files.info` | Get details for a single file | `client.call('files.info')` |
| `/files.list` | `files.list` | Get a list of files | `client.call('files.list')` |
| `/files.upload` | `files.upload` | Request the upload link for a file | `client.call('files.upload')` |

---

## Mail Templates

Mail Templates

| Endpoint | Summary | Description | `client.call()` |
|---|---|---|---|
| `/mailTemplates.list` | `mailTemplates.list` | Get a list of all mail templates | `client.call('mailTemplates.list')` |

---

## Migrating

⚠️ WARNING! These endpoints are not guaranteed to stay backwards compatible.

| Endpoint | Summary | Description | `client.call()` |
|---|---|---|---|
| `/migrate.activityType` | `migrate.activityType` | Translates `meeting`, `call` and `task` into their respective activity type UUID | `client.call('migrate.activityType')` |
| `/migrate.id` | `migrate.id` | Translates an ID from the deprecated API into a new UUID | `client.call('migrate.id')` |
| `/migrate.taxRate` | `migrate.taxRate` | Translates tax rates from the deprecated API into a new UUID tax rate | `client.call('migrate.taxRate')` |

---

## Webhooks

Webhooks

| Endpoint | Summary | Description | `client.call()` |
|---|---|---|---|
| `/webhooks.list` | `webhooks.list` | List registered webhooks ordered by URL | `client.call('webhooks.list')` |
| `/webhooks.register` | `webhooks.register` | Register a new webhook | `client.call('webhooks.register')` |
| `/webhooks.unregister` | `webhooks.unregister` | Unregister a webhook | `client.call('webhooks.unregister')` |

---

## Cloud Platforms

Cloud Platforms

| Endpoint | Summary | Description | `client.call()` |
|---|---|---|---|
| `/cloudPlatforms.url` | `cloudPlatforms.url` | Fetch cloudPlatform url for type and id | `client.call('cloudPlatforms.url')` |

---

## Accounts

Accounts

| Endpoint | Summary | Description | `client.call()` |
|---|---|---|---|
| `/accounts.projects-v2-status` | `accounts.projects-v2-status` | Fetch which version of Projects the account is using | `client.call('accounts.projects-v2-status')` |

---

## Plannable items

Plannable items

| Endpoint | Summary | Description | `client.call()` |
|---|---|---|---|
| `/plannableItems.info` | `plannableItems.info` | Returns the info for a single plannable item, either by ID or source if the ID is unknown | `client.call('plannableItems.info')` |
| `/plannableItems.list` | `plannableItems.list` | Lists all plannable items that match the optional filters provided | `client.call('plannableItems.list')` |

---

## Reservations

Reservations

| Endpoint | Summary | Description | `client.call()` |
|---|---|---|---|
| `/reservations.create` | `reservations.create` | Create a new reservation | `client.call('reservations.create')` |
| `/reservations.delete` | `reservations.delete` | Delete a reservation | `client.call('reservations.delete')` |
| `/reservations.list` | `reservations.list` | Lists all reservations that match the optional filters provided | `client.call('reservations.list')` |
| `/reservations.update` | `reservations.update` | Update an existing reservation | `client.call('reservations.update')` |

---

## User availability

User availability

| Endpoint | Summary | Description | `client.call()` |
|---|---|---|---|
| `/userAvailability.daily` | `userAvailability.daily` | Returns the daily availability for all users | `client.call('userAvailability.daily')` |
| `/userAvailability.total` | `userAvailability.total` | Returns the total availability for all users | `client.call('userAvailability.total')` |

---
