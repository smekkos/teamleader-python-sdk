"""Invoices resource — CRUD + extra actions."""

from __future__ import annotations

from typing import Any

from teamleader.models.common import Money, TypeAndId
from teamleader.models.invoice import Invoice
from teamleader.resources.base import CrudResource


class InvoicesResource(CrudResource[Invoice]):
    """CRUD + extra actions for Teamleader invoices.

    Inherits :meth:`list`, :meth:`get`, :meth:`create`, :meth:`update`,
    :meth:`delete`, and :meth:`iterate` from :class:`~teamleader.resources.base.CrudResource`.
    """

    prefix = "invoices"
    model = Invoice

    def book(self, invoice_id: str, on: str) -> None:
        """Book a draft invoice, turning it into a numbered invoice.

        Calls ``invoices.book``.

        Parameters
        ----------
        invoice_id:
            UUID of the draft invoice to book.
        on:
            Invoice date as an ISO 8601 date string (``"YYYY-MM-DD"``).
            This becomes the ``invoice_date`` on the booked invoice.
        """
        self._client._post("invoices.book", {"id": invoice_id, "on": on})

    def credit(
        self,
        invoice_id: str,
        *,
        credit_note_date: str | None = None,
    ) -> TypeAndId:
        """Credit an invoice completely, creating a credit note.

        Calls ``invoices.credit``.  Returns a :class:`~teamleader.models.common.TypeAndId`
        reference to the newly created credit note (``type="creditNote"``).

        Parameters
        ----------
        invoice_id:
            UUID of the booked invoice to credit.
        credit_note_date:
            Optional ISO 8601 date string for the credit note.  Defaults to
            the current date when omitted.

        Returns
        -------
        TypeAndId
            Reference to the credit note created by the API.
        """
        body: dict[str, Any] = {"id": invoice_id}
        if credit_note_date is not None:
            body["credit_note_date"] = credit_note_date
        resp = self._client._post("invoices.credit", body)
        return TypeAndId.from_api(resp["data"])

    def register_payment(
        self,
        invoice_id: str,
        payment: Money,
        paid_at: str,
        *,
        payment_method_id: str | None = None,
    ) -> None:
        """Register a payment against an invoice.

        Calls ``invoices.registerPayment``.

        Parameters
        ----------
        invoice_id:
            UUID of the invoice being paid.
        payment:
            The amount paid as a :class:`~teamleader.models.common.Money` object.
        paid_at:
            ISO 8601 datetime at which the payment was received
            (e.g. ``"2016-03-03T16:44:33+00:00"``).
        payment_method_id:
            Optional UUID of a configured payment method.
        """
        body: dict[str, Any] = {
            "id": invoice_id,
            "payment": payment.to_dict(),
            "paid_at": paid_at,
        }
        if payment_method_id is not None:
            body["payment_method_id"] = payment_method_id
        self._client._post("invoices.registerPayment", body)

    def send(
        self,
        invoice_id: str,
        subject: str,
        body: str,
        *,
        mail_template_id: str | None = None,
        recipients: dict[str, Any] | None = None,
    ) -> None:
        """Send an invoice to the invoicee via e-mail.

        Calls ``invoices.send``.

        Parameters
        ----------
        invoice_id:
            UUID of the invoice to send.
        subject:
            E-mail subject line.
        body:
            E-mail body text.
        mail_template_id:
            Optional UUID of a mail template to use.
        recipients:
            Optional ``{"to": [...], "cc": [...]}`` dict overriding the default
            recipients.  Each entry is ``{"email": "...", "customer": {...}}``.
        """
        content: dict[str, Any] = {"subject": subject, "body": body}
        if mail_template_id is not None:
            content["mail_template_id"] = mail_template_id

        payload: dict[str, Any] = {"id": invoice_id, "content": content}
        if recipients is not None:
            payload["recipients"] = recipients
        self._client._post("invoices.send", payload)

    def download(
        self,
        invoice_id: str,
        format: str = "pdf",
    ) -> dict[str, str]:
        """Request a download URL for an invoice document.

        Calls ``invoices.download``.  The API returns a pre-signed URL that
        expires after a short time.

        Parameters
        ----------
        invoice_id:
            UUID of the invoice to download.
        format:
            Document format — ``"pdf"`` (default), ``"ubl/e-fff"``, or
            ``"ubl/peppol_bis_3"``.

        Returns
        -------
        dict
            ``{"location": "<pre-signed URL>", "expires": "<ISO datetime>"}``
        """
        resp = self._client._post(
            "invoices.download", {"id": invoice_id, "format": format}
        )
        return resp["data"]
