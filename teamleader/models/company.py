"""Company model — curated layer over the Teamleader Focus companies API."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Self

from teamleader.models.common import (
    AddressEntry,
    CustomField,
    Email,
    PaymentTerm,
    Telephone,
    TypeAndId,
)


@dataclass
class Company:
    """Represents a Teamleader Focus company.

    All datetime fields are ISO 8601 strings as returned by the API.
    Use the computed properties for convenient access to common values.
    """

    id: str = ""
    name: str = ""
    status: str = "active"                          # "active" | "deactivated"
    business_type: TypeAndId | None = None
    vat_number: str | None = None
    national_identification_number: str | None = None
    emails: list[Email] = field(default_factory=list)
    telephones: list[Telephone] = field(default_factory=list)
    website: str | None = None                      # single URL string (spec: `website`)
    addresses: list[AddressEntry] = field(default_factory=list)
    iban: str | None = None
    bic: str | None = None
    language: str | None = None                     # ISO 639-1
    preferred_currency: str | None = None           # ISO 4217
    payment_term: PaymentTerm | None = None
    responsible_user: TypeAndId | None = None
    remarks: str | None = None                      # Markdown
    tags: list[str] = field(default_factory=list)
    custom_fields: list[CustomField] = field(default_factory=list)
    marketing_mails_consent: bool | None = None
    added_at: str | None = None                     # ISO 8601 datetime
    updated_at: str | None = None                   # ISO 8601 datetime
    web_url: str | None = None
    # Only present when requested via `includes=related_companies`
    related_companies: list[TypeAndId] = field(default_factory=list)
    # Only present when requested via `includes=related_contacts`
    related_contacts: list[dict[str, Any]] = field(default_factory=list)

    # ------------------------------------------------------------------
    # Computed properties
    # ------------------------------------------------------------------

    @property
    def is_active(self) -> bool:
        """Return ``True`` when ``status == "active"``."""
        return self.status == "active"

    @property
    def primary_email(self) -> str | None:
        """Return the address marked ``type="primary"``, else the first email, else ``None``."""
        for e in self.emails:
            if e.type == "primary":
                return e.email
        return self.emails[0].email if self.emails else None

    @property
    def primary_phone(self) -> str | None:
        """Return the first telephone number, or ``None`` if none recorded."""
        return self.telephones[0].number if self.telephones else None

    # ------------------------------------------------------------------
    # Serialisation
    # ------------------------------------------------------------------

    @classmethod
    def from_api(cls, data: dict[str, Any]) -> Self:
        """Deserialise from a ``companies.info`` or ``companies.list`` payload.

        Accepts both the full response wrapper ``{"data": {...}}`` and a bare
        data dict.
        """
        d = data.get("data", data)

        bt_raw = d.get("business_type")
        business_type = TypeAndId.from_api(bt_raw) if bt_raw else None

        ru_raw = d.get("responsible_user")
        responsible_user = TypeAndId.from_api(ru_raw) if ru_raw else None

        pt_raw = d.get("payment_term")
        payment_term = PaymentTerm.from_api(pt_raw) if pt_raw else None

        related_companies = [
            TypeAndId.from_api(rc) for rc in d.get("related_companies", [])
        ]

        return cls(
            id=d.get("id", ""),
            name=d.get("name", ""),
            status=d.get("status", "active"),
            business_type=business_type,
            vat_number=d.get("vat_number"),
            national_identification_number=d.get("national_identification_number"),
            emails=[Email.from_api(e) for e in d.get("emails", [])],
            telephones=[Telephone.from_api(t) for t in d.get("telephones", [])],
            website=d.get("website"),
            addresses=[AddressEntry.from_api(a) for a in d.get("addresses", [])],
            iban=d.get("iban"),
            bic=d.get("bic"),
            language=d.get("language"),
            preferred_currency=d.get("preferred_currency"),
            payment_term=payment_term,
            responsible_user=responsible_user,
            remarks=d.get("remarks"),
            tags=d.get("tags", []),
            custom_fields=[CustomField.from_api(cf) for cf in d.get("custom_fields", [])],
            marketing_mails_consent=d.get("marketing_mails_consent"),
            added_at=d.get("added_at"),
            updated_at=d.get("updated_at"),
            web_url=d.get("web_url"),
            related_companies=related_companies,
            related_contacts=d.get("related_contacts", []),
        )

    def to_dict(self) -> dict[str, Any]:
        """Serialise to the shape expected by ``companies.add`` / ``companies.update``."""
        out: dict[str, Any] = {
            "id": self.id,
            "name": self.name,
            "status": self.status,
            "emails": [e.to_dict() for e in self.emails],
            "telephones": [t.to_dict() for t in self.telephones],
            "addresses": [a.to_dict() for a in self.addresses],
            "tags": self.tags,
            "custom_fields": [cf.to_dict() for cf in self.custom_fields],
        }
        if self.business_type is not None:
            out["business_type"] = self.business_type.to_dict()
        if self.vat_number is not None:
            out["vat_number"] = self.vat_number
        if self.national_identification_number is not None:
            out["national_identification_number"] = self.national_identification_number
        if self.website is not None:
            out["website"] = self.website
        if self.iban is not None:
            out["iban"] = self.iban
        if self.bic is not None:
            out["bic"] = self.bic
        if self.language is not None:
            out["language"] = self.language
        if self.preferred_currency is not None:
            out["preferred_currency"] = self.preferred_currency
        if self.payment_term is not None:
            out["payment_term"] = self.payment_term.to_dict()
        if self.responsible_user is not None:
            out["responsible_user"] = self.responsible_user.to_dict()
        if self.remarks is not None:
            out["remarks"] = self.remarks
        if self.marketing_mails_consent is not None:
            out["marketing_mails_consent"] = self.marketing_mails_consent
        return out
