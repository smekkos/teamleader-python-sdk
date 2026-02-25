"""Companies resource — CRUD + extra actions."""

from __future__ import annotations

from teamleader.models.company import Company
from teamleader.resources.base import CrudResource


class CompaniesResource(CrudResource[Company]):
    """CRUD + extra actions for Teamleader companies.

    Inherits :meth:`list`, :meth:`get`, :meth:`create`, :meth:`update`,
    :meth:`delete`, and :meth:`iterate` from :class:`~teamleader.resources.base.CrudResource`.
    """

    prefix = "companies"
    model = Company

    def tag(self, company_id: str, tags: list[str]) -> None:
        """Add one or more tags to a company.

        Calls ``companies.tag``.  Tags that already exist on the company are
        silently ignored by the API.

        Parameters
        ----------
        company_id:
            UUID of the company to tag.
        tags:
            List of tag strings (new or existing) to add.
        """
        self._client._post("companies.tag", {"id": company_id, "tags": tags})

    def untag(self, company_id: str, tags: list[str]) -> None:
        """Remove one or more tags from a company.

        Calls ``companies.untag``.  Tags that are not present are silently
        ignored by the API.

        Parameters
        ----------
        company_id:
            UUID of the company to untag.
        tags:
            List of tag strings to remove.
        """
        self._client._post("companies.untag", {"id": company_id, "tags": tags})
