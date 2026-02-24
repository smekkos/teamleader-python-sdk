"""Curated model classes for the Teamleader SDK.

Import them directly from here or from ``teamleader`` top-level:

    from teamleader.models.deal import Deal
    from teamleader import Deal  # same thing
"""

from teamleader.models.common import Address, CustomField, Email, Money, Telephone, WebLink
from teamleader.models.company import Company
from teamleader.models.contact import Contact
from teamleader.models.deal import Deal
from teamleader.models.invoice import Invoice
from teamleader.models.quotation import Quotation

__all__ = [
    "Address",
    "CustomField",
    "Email",
    "Money",
    "Telephone",
    "WebLink",
    "Company",
    "Contact",
    "Deal",
    "Invoice",
    "Quotation",
]
