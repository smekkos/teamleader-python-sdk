"""Teamleader Focus Python SDK.

Quick-start (non-Django)::

    from teamleader import TeamleaderClient
    from teamleader.auth import OAuth2Handler, MemoryTokenBackend

    backend = MemoryTokenBackend()
    backend.save(my_token)
    handler = OAuth2Handler(CLIENT_ID, CLIENT_SECRET, REDIRECT_URI, backend)
    client = TeamleaderClient(handler)

    for deal in client.deals.iterate():
        print(deal.title)

Quick-start (Django)::

    # pip install teamleader-sdk[django]
    from teamleader.django import get_client

    client = get_client()
    contact = client.contacts.get("some-uuid")
"""

__version__ = "0.1.0"

from teamleader.auth import MemoryTokenBackend, OAuth2Handler, Token, TokenBackend
from teamleader.client import TeamleaderClient
from teamleader.exceptions import (
    TeamleaderAPIError,
    TeamleaderAuthError,
    TeamleaderAuthExpiredError,
    TeamleaderError,
    TeamleaderNotFoundError,
    TeamleaderPermissionError,
    TeamleaderRateLimitError,
    TeamleaderServerError,
    TeamleaderValidationError,
)
from teamleader.models.company import Company
from teamleader.models.contact import Contact
from teamleader.models.deal import Deal
from teamleader.models.invoice import Invoice
from teamleader.models.quotation import Quotation

__all__ = [
    # Client
    "TeamleaderClient",
    # Auth
    "OAuth2Handler",
    "Token",
    "TokenBackend",
    "MemoryTokenBackend",
    # Exceptions
    "TeamleaderError",
    "TeamleaderAPIError",
    "TeamleaderAuthError",
    "TeamleaderAuthExpiredError",
    "TeamleaderNotFoundError",
    "TeamleaderPermissionError",
    "TeamleaderRateLimitError",
    "TeamleaderServerError",
    "TeamleaderValidationError",
    # Models
    "Company",
    "Contact",
    "Deal",
    "Invoice",
    "Quotation",
]
