"""Invoices resource.

Full implementation in Phase 9.
"""

from __future__ import annotations

from typing import Any

from teamleader.models.invoice import Invoice
from teamleader.resources.base import CrudResource


class InvoicesResource(CrudResource[Invoice]):
    """CRUD + extra actions for Teamleader invoices."""

    prefix = "invoices"
    model = Invoice

    def book(self, invoice_id: str, **kwargs: Any) -> None:
        raise NotImplementedError  # Phase 9

    def credit(self, invoice_id: str, **kwargs: Any) -> Invoice:
        raise NotImplementedError  # Phase 9

    def send(self, invoice_id: str, **kwargs: Any) -> None:
        raise NotImplementedError  # Phase 9

    def register_payment(self, invoice_id: str, **kwargs: Any) -> None:
        raise NotImplementedError  # Phase 9

    def download(self, invoice_id: str) -> bytes:
        """Return the PDF binary for the invoice."""
        raise NotImplementedError  # Phase 9
