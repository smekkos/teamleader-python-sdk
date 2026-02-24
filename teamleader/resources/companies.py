"""Companies resource.

Full implementation in Phase 9.
"""

from __future__ import annotations

from teamleader.models.company import Company
from teamleader.resources.base import CrudResource


class CompaniesResource(CrudResource[Company]):
    """CRUD + extra actions for Teamleader companies."""

    prefix = "companies"
    model = Company

    def tag(self, company_id: str, tags: list[str]) -> None:
        raise NotImplementedError  # Phase 9

    def untag(self, company_id: str, tags: list[str]) -> None:
        raise NotImplementedError  # Phase 9
