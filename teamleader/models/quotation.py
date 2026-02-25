"""Quotation model — curated layer over the Teamleader Focus quotations API."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Self

from teamleader.models.common import CustomField, Money, TypeAndId


@dataclass
class Quotation:
    """Represents a Teamleader Focus quotation.

    All datetime fields are ISO 8601 strings as returned by the API.
    Use the computed properties for convenient access to common values.
    """

    id: str = ""
    deal: TypeAndId | None = None
    grouped_lines: list[dict[str, Any]] = field(default_factory=list)
    currency: str | None = None                 # ISO 4217
    currency_exchange_rate: dict[str, Any] | None = None
    text: str | None = None                     # Markdown
    total: dict[str, Any] | None = None         # tax_exclusive, tax_inclusive, taxes, …
    discounts: list[dict[str, Any]] = field(default_factory=list)   # CommercialDiscount list
    status: str = "open"                        # "open" | "accepted" | "expired" | "rejected" | "closed"
    name: str | None = None
    document_template: TypeAndId | None = None
    custom_fields: list[CustomField] = field(default_factory=list)
    created_at: str | None = None               # ISO 8601 datetime
    updated_at: str | None = None               # ISO 8601 datetime

    # ------------------------------------------------------------------
    # Computed properties
    # ------------------------------------------------------------------

    @property
    def is_open(self) -> bool:
        """Return ``True`` when the quotation is still awaiting a response."""
        return self.status == "open"

    @property
    def is_accepted(self) -> bool:
        """Return ``True`` when the quotation has been accepted."""
        return self.status == "accepted"

    @property
    def is_expired(self) -> bool:
        """Return ``True`` when the quotation has expired."""
        return self.status == "expired"

    @property
    def total_tax_exclusive(self) -> Money | None:
        """Return the tax-exclusive total amount, or ``None`` if totals not present."""
        if self.total and isinstance(self.total.get("tax_exclusive"), dict):
            return Money.from_api(self.total["tax_exclusive"])
        return None

    @property
    def total_tax_inclusive(self) -> Money | None:
        """Return the tax-inclusive total amount, or ``None`` if totals not present."""
        if self.total and isinstance(self.total.get("tax_inclusive"), dict):
            return Money.from_api(self.total["tax_inclusive"])
        return None

    # ------------------------------------------------------------------
    # Serialisation
    # ------------------------------------------------------------------

    @classmethod
    def from_api(cls, data: dict[str, Any]) -> Self:
        """Deserialise from a ``quotations.info`` or ``quotations.list`` payload.

        Accepts both the full response wrapper ``{"data": {...}}`` and a bare
        data dict.
        """
        d = data.get("data", data)

        deal_raw = d.get("deal")
        deal = TypeAndId.from_api(deal_raw) if deal_raw else None

        dt_raw = d.get("document_template")
        document_template = TypeAndId.from_api(dt_raw) if dt_raw else None

        return cls(
            id=d.get("id", ""),
            deal=deal,
            grouped_lines=d.get("grouped_lines", []),
            currency=d.get("currency"),
            currency_exchange_rate=d.get("currency_exchange_rate"),
            text=d.get("text"),
            total=d.get("total"),
            discounts=d.get("discounts", []),
            status=d.get("status", "open"),
            name=d.get("name"),
            document_template=document_template,
            custom_fields=[CustomField.from_api(cf) for cf in d.get("custom_fields", [])],
            created_at=d.get("created_at"),
            updated_at=d.get("updated_at"),
        )

    def to_dict(self) -> dict[str, Any]:
        """Serialise to the shape expected by quotation write endpoints."""
        out: dict[str, Any] = {
            "id": self.id,
            "status": self.status,
            "custom_fields": [cf.to_dict() for cf in self.custom_fields],
        }
        if self.deal is not None:
            out["deal"] = self.deal.to_dict()
        if self.grouped_lines:
            out["grouped_lines"] = self.grouped_lines
        if self.currency is not None:
            out["currency"] = self.currency
        if self.text is not None:
            out["text"] = self.text
        if self.discounts:
            out["discounts"] = self.discounts
        if self.name is not None:
            out["name"] = self.name
        if self.document_template is not None:
            out["document_template"] = self.document_template.to_dict()
        return out
