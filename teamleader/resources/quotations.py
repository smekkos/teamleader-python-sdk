"""Quotations resource.

Full implementation in Phase 9.
"""

from __future__ import annotations

from typing import Any

from teamleader.models.quotation import Quotation
from teamleader.resources.base import CrudResource


class QuotationsResource(CrudResource[Quotation]):
    """CRUD + extra actions for Teamleader quotations."""

    prefix = "quotations"
    model = Quotation

    def send(self, quotation_id: str, **kwargs: Any) -> None:
        raise NotImplementedError  # Phase 9

    def accept(self, quotation_id: str) -> None:
        raise NotImplementedError  # Phase 9

    def decline(self, quotation_id: str) -> None:
        raise NotImplementedError  # Phase 9
