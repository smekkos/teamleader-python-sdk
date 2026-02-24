"""Deals resource.

Full implementation in Phase 9.
"""

from __future__ import annotations

from typing import Any

from teamleader.models.deal import Deal
from teamleader.resources.base import CrudResource, Page


class DealsResource(CrudResource[Deal]):
    """CRUD + extra actions for Teamleader deals."""

    prefix = "deals"
    model = Deal

    def move_to_phase(self, deal_id: str, phase_id: str) -> None:
        raise NotImplementedError  # Phase 9

    def win(self, deal_id: str) -> None:
        raise NotImplementedError  # Phase 9

    def lose(self, deal_id: str, reason_id: str | None = None) -> None:
        raise NotImplementedError  # Phase 9

    def list_phases(self) -> list[dict[str, Any]]:
        raise NotImplementedError  # Phase 9

    def list_sources(self) -> list[dict[str, Any]]:
        raise NotImplementedError  # Phase 9
