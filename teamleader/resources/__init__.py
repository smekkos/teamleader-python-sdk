"""Resource classes for the Teamleader SDK.

Each resource corresponds to a Teamleader API domain object and exposes
CRUD operations plus domain-specific actions.

Full implementation in Phases 7 and 9.
"""

from teamleader.resources.companies import CompaniesResource
from teamleader.resources.contacts import ContactsResource
from teamleader.resources.deals import DealsResource
from teamleader.resources.invoices import InvoicesResource
from teamleader.resources.quotations import QuotationsResource

__all__ = [
    "CompaniesResource",
    "ContactsResource",
    "DealsResource",
    "InvoicesResource",
    "QuotationsResource",
]
