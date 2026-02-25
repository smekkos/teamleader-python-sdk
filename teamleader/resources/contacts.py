"""Contacts resource — CRUD + extra actions."""

from __future__ import annotations

from teamleader.models.contact import Contact
from teamleader.resources.base import CrudResource


class ContactsResource(CrudResource[Contact]):
    """CRUD + extra actions for Teamleader contacts.

    Inherits :meth:`list`, :meth:`get`, :meth:`create`, :meth:`update`,
    :meth:`delete`, and :meth:`iterate` from :class:`~teamleader.resources.base.CrudResource`.
    """

    prefix = "contacts"
    model = Contact

    # ------------------------------------------------------------------
    # Tagging
    # ------------------------------------------------------------------

    def tag(self, contact_id: str, tags: list[str]) -> None:
        """Add one or more tags to a contact.

        Calls ``contacts.tag``.  Tags that already exist on the contact are
        silently ignored by the API.

        Parameters
        ----------
        contact_id:
            UUID of the contact to tag.
        tags:
            List of tag strings (new or existing) to add.
        """
        self._client._post("contacts.tag", {"id": contact_id, "tags": tags})

    def untag(self, contact_id: str, tags: list[str]) -> None:
        """Remove one or more tags from a contact.

        Calls ``contacts.untag``.  Tags that are not present are silently
        ignored by the API.

        Parameters
        ----------
        contact_id:
            UUID of the contact to untag.
        tags:
            List of tag strings to remove.
        """
        self._client._post("contacts.untag", {"id": contact_id, "tags": tags})

    # ------------------------------------------------------------------
    # Company linking
    # ------------------------------------------------------------------

    def link_to_company(
        self,
        contact_id: str,
        company_id: str,
        *,
        position: str | None = None,
        decision_maker: bool | None = None,
    ) -> None:
        """Link a contact to a company.

        Calls ``contacts.linkToCompany``.

        Parameters
        ----------
        contact_id:
            UUID of the contact.
        company_id:
            UUID of the company to link to.
        position:
            Optional job title at the company (e.g. ``"CEO"``).
        decision_maker:
            Optional flag indicating whether this contact is a decision maker
            at the linked company.
        """
        body: dict = {"id": contact_id, "company_id": company_id}
        if position is not None:
            body["position"] = position
        if decision_maker is not None:
            body["decision_maker"] = decision_maker
        self._client._post("contacts.linkToCompany", body)

    def unlink_from_company(self, contact_id: str, company_id: str) -> None:
        """Remove the link between a contact and a company.

        Calls ``contacts.unlinkFromCompany``.

        Parameters
        ----------
        contact_id:
            UUID of the contact.
        company_id:
            UUID of the company to unlink from.
        """
        self._client._post(
            "contacts.unlinkFromCompany",
            {"id": contact_id, "company_id": company_id},
        )
