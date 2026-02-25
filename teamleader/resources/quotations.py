"""Quotations resource — CRUD + extra actions."""

from __future__ import annotations

from typing import Any

from teamleader.models.quotation import Quotation
from teamleader.resources.base import CrudResource


class QuotationsResource(CrudResource[Quotation]):
    """CRUD + extra actions for Teamleader quotations.

    Inherits :meth:`list`, :meth:`get`, :meth:`create`, :meth:`update`,
    :meth:`delete`, and :meth:`iterate` from :class:`~teamleader.resources.base.CrudResource`.
    """

    prefix = "quotations"
    model = Quotation

    def send(
        self,
        quotation_ids: list[str],
        recipients: dict[str, Any],
        subject: str,
        content: str,
        language: str,
        *,
        from_: dict[str, Any] | None = None,
    ) -> None:
        """Send one or more quotations from the same deal via e-mail.

        Calls ``quotations.send``.

        All ``quotation_ids`` must belong to the same deal.

        Parameters
        ----------
        quotation_ids:
            List of quotation UUIDs to send in a single e-mail.
        recipients:
            Recipient dict with a required ``"to"`` key and optional ``"cc"``
            key.  Each entry in the list is
            ``{"email_address": "...", "customer": {...}}``.

            Example::

                {
                    "to": [{"email_address": "client@example.com"}],
                    "cc": [{"email_address": "internal@acme.com"}],
                }

        subject:
            E-mail subject line.
        content:
            E-mail body text (plain-text or Markdown).
        language:
            ISO 639-1 language code for the e-mail (e.g. ``"en"``, ``"nl"``).
        from_:
            Optional sender override::

                {
                    "sender": {"type": "user", "id": "<uuid>"},
                    "email_address": "sender@acme.com",
                }
        """
        body: dict[str, Any] = {
            "quotations": quotation_ids,
            "recipients": recipients,
            "subject": subject,
            "content": content,
            "language": language,
        }
        if from_ is not None:
            body["from"] = from_
        self._client._post("quotations.send", body)

    def accept(self, quotation_id: str) -> None:
        """Mark a quotation as accepted.

        Calls ``quotations.accept``.

        Parameters
        ----------
        quotation_id:
            UUID of the quotation to accept.
        """
        self._client._post("quotations.accept", {"id": quotation_id})
