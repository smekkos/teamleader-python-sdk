"""Contacts resource.

Full implementation in Phase 9.
"""

from __future__ import annotations

from typing import Any

from teamleader.models.contact import Contact
from teamleader.resources.base import CrudResource


class ContactsResource(CrudResource[Contact]):
    """CRUD + extra actions for Teamleader contacts."""

    prefix = "contacts"
    model = Contact

    def link_to_company(self, contact_id: str, company_id: str, **kwargs: Any) -> None:
        raise NotImplementedError  # Phase 9

    def unlink_from_company(self, contact_id: str, company_id: str) -> None:
        raise NotImplementedError  # Phase 9

    def tag(self, contact_id: str, tags: list[str]) -> None:
        raise NotImplementedError  # Phase 9

    def untag(self, contact_id: str, tags: list[str]) -> None:
        raise NotImplementedError  # Phase 9
