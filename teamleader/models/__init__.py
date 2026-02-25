"""Curated model classes for the Teamleader SDK.

Import them directly from here or from the ``teamleader`` top-level package:

    from teamleader.models import Deal, Invoice
    from teamleader import Deal  # same thing
"""

from teamleader.models.common import (
    Address,
    AddressEntry,
    CustomField,
    Email,
    Money,
    PaymentTerm,
    Telephone,
    TypeAndId,
    WebLink,
)
from teamleader.models.company import Company
from teamleader.models.contact import Contact
from teamleader.models.deal import Deal
from teamleader.models.invoice import Invoice
from teamleader.models.quotation import Quotation

__all__ = [
    # common sub-models
    "Address",
    "AddressEntry",
    "CustomField",
    "Email",
    "Money",
    "PaymentTerm",
    "Telephone",
    "TypeAndId",
    "WebLink",
    # resource models
    "Company",
    "Contact",
    "Deal",
    "Invoice",
    "Quotation",
]
