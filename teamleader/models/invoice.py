"""Invoice model — curated layer over the Teamleader Focus invoices API."""

from __future__ import annotations

import datetime
from dataclasses import dataclass, field
from typing import Any, Self

from teamleader.models.common import CustomField, Money, PaymentTerm, TypeAndId


@dataclass
class Invoice:
    """Represents a Teamleader Focus invoice.

    All date/datetime fields are ISO 8601 strings as returned by the API.
    Use the computed properties for convenient access to common values.
    """

    id: str = ""
    department: TypeAndId | None = None
    invoice_number: str | None = None
    invoice_date: str | None = None             # ISO 8601 date ("2016-02-04")
    status: str = "draft"                       # "draft" | "outstanding" | "matched"
    due_on: str | None = None                   # ISO 8601 date ("2016-03-03")
    paid: bool = False
    paid_at: str | None = None                  # ISO 8601 datetime
    sent: bool = False
    purchase_order_number: str | None = None
    invoicee: dict[str, Any] | None = None      # name, vat_number, customer TypeAndId, email, …
    discounts: list[dict[str, Any]] = field(default_factory=list)   # CommercialDiscount list
    grouped_lines: list[dict[str, Any]] = field(default_factory=list)
    total: dict[str, Any] | None = None         # tax_exclusive, tax_inclusive, payable, due, …
    payment_term: PaymentTerm | None = None
    payments: list[dict[str, Any]] = field(default_factory=list)
    payment_reference: str | None = None
    note: str | None = None                     # plaintext
    currency: str | None = None                 # ISO 4217
    currency_exchange_rate: dict[str, Any] | None = None
    deal: TypeAndId | None = None
    custom_fields: list[CustomField] = field(default_factory=list)
    created_at: str | None = None               # ISO 8601 datetime
    updated_at: str | None = None               # ISO 8601 datetime
    delivery_date: str | None = None            # ISO 8601 date

    # ------------------------------------------------------------------
    # Computed properties
    # ------------------------------------------------------------------

    @property
    def is_paid(self) -> bool:
        """Return ``True`` when the invoice has been marked paid."""
        return self.paid

    @property
    def is_draft(self) -> bool:
        """Return ``True`` when the invoice is still a draft."""
        return self.status == "draft"

    @property
    def is_overdue(self) -> bool:
        """Return ``True`` if the due date is in the past and the invoice is not paid.

        Returns ``False`` if no ``due_on`` date is set or if it cannot be parsed.
        """
        if self.paid or not self.due_on:
            return False
        try:
            due = datetime.date.fromisoformat(self.due_on)
        except ValueError:
            return False
        return due < datetime.date.today()

    @property
    def total_due(self) -> Money | None:
        """Return the outstanding ``due`` amount from the totals block, or ``None``."""
        if self.total and isinstance(self.total.get("due"), dict):
            return Money.from_api(self.total["due"])
        return None

    @property
    def customer_name(self) -> str | None:
        """Return the invoicee name, or ``None`` if no invoicee is set."""
        if self.invoicee:
            return self.invoicee.get("name")
        return None

    # ------------------------------------------------------------------
    # Serialisation
    # ------------------------------------------------------------------

    @classmethod
    def from_api(cls, data: dict[str, Any]) -> Self:
        """Deserialise from an ``invoices.info`` or ``invoices.list`` payload.

        Accepts both the full response wrapper ``{"data": {...}}`` and a bare
        data dict.
        """
        d = data.get("data", data)

        dept_raw = d.get("department")
        department = TypeAndId.from_api(dept_raw) if dept_raw else None

        pt_raw = d.get("payment_term")
        payment_term = PaymentTerm.from_api(pt_raw) if pt_raw else None

        deal_raw = d.get("deal")
        deal = TypeAndId.from_api(deal_raw) if deal_raw else None

        return cls(
            id=d.get("id", ""),
            department=department,
            invoice_number=d.get("invoice_number"),
            invoice_date=d.get("invoice_date"),
            status=d.get("status", "draft"),
            due_on=d.get("due_on"),
            paid=bool(d.get("paid", False)),
            paid_at=d.get("paid_at"),
            sent=bool(d.get("sent", False)),
            purchase_order_number=d.get("purchase_order_number"),
            invoicee=d.get("invoicee"),
            discounts=d.get("discounts", []),
            grouped_lines=d.get("grouped_lines", []),
            total=d.get("total"),
            payment_term=payment_term,
            payments=d.get("payments", []),
            payment_reference=d.get("payment_reference"),
            note=d.get("note"),
            currency=d.get("currency"),
            currency_exchange_rate=d.get("currency_exchange_rate"),
            deal=deal,
            custom_fields=[CustomField.from_api(cf) for cf in d.get("custom_fields", [])],
            created_at=d.get("created_at"),
            updated_at=d.get("updated_at"),
            delivery_date=d.get("delivery_date"),
        )

    def to_dict(self) -> dict[str, Any]:
        """Serialise to the shape expected by invoice write endpoints."""
        out: dict[str, Any] = {
            "id": self.id,
            "status": self.status,
            "paid": self.paid,
            "sent": self.sent,
            "custom_fields": [cf.to_dict() for cf in self.custom_fields],
        }
        if self.department is not None:
            out["department"] = self.department.to_dict()
        if self.invoice_number is not None:
            out["invoice_number"] = self.invoice_number
        if self.invoice_date is not None:
            out["invoice_date"] = self.invoice_date
        if self.due_on is not None:
            out["due_on"] = self.due_on
        if self.purchase_order_number is not None:
            out["purchase_order_number"] = self.purchase_order_number
        if self.invoicee is not None:
            out["invoicee"] = self.invoicee
        if self.discounts:
            out["discounts"] = self.discounts
        if self.grouped_lines:
            out["grouped_lines"] = self.grouped_lines
        if self.payment_term is not None:
            out["payment_term"] = self.payment_term.to_dict()
        if self.payment_reference is not None:
            out["payment_reference"] = self.payment_reference
        if self.note is not None:
            out["note"] = self.note
        if self.currency is not None:
            out["currency"] = self.currency
        if self.deal is not None:
            out["deal"] = self.deal.to_dict()
        if self.delivery_date is not None:
            out["delivery_date"] = self.delivery_date
        return out
