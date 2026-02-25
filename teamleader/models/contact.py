"""Contact model — curated layer over the Teamleader Focus contacts API."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Self

from teamleader.models.common import (
    AddressEntry,
    CustomField,
    Email,
    PaymentTerm,
    Telephone,
)


@dataclass
class Contact:
    """Represents a Teamleader Focus contact.

    All datetime fields are ISO 8601 strings as returned by the API.
    Use the computed properties for convenient access to common values.
    """

    id: str = ""
    first_name: str = ""
    last_name: str = ""
    status: str = "active"                          # "active" | "deactivated"
    salutation: str | None = None
    vat_number: str | None = None
    emails: list[Email] = field(default_factory=list)
    telephones: list[Telephone] = field(default_factory=list)
    website: str | None = None                      # single URL string (spec: `website`)
    addresses: list[AddressEntry] = field(default_factory=list)
    gender: str | None = None
    birthdate: str | None = None                    # ISO 8601 date
    iban: str | None = None
    bic: str | None = None
    national_identification_number: str | None = None
    companies: list[dict[str, Any]] = field(default_factory=list)
    language: str | None = None                     # ISO 639-1
    payment_term: PaymentTerm | None = None
    remarks: str | None = None                      # Markdown
    tags: list[str] = field(default_factory=list)
    custom_fields: list[CustomField] = field(default_factory=list)
    marketing_mails_consent: bool | None = None
    added_at: str | None = None                     # ISO 8601 datetime
    updated_at: str | None = None                   # ISO 8601 datetime
    web_url: str | None = None

    # ------------------------------------------------------------------
    # Computed properties
    # ------------------------------------------------------------------

    @property
    def full_name(self) -> str:
        """Return ``"First Last"``, stripping extra whitespace."""
        return f"{self.first_name} {self.last_name}".strip()

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

    @property
    def is_active(self) -> bool:
        """Return ``True`` when ``status == "active"``."""
        return self.status == "active"

    # ------------------------------------------------------------------
    # Serialisation
    # ------------------------------------------------------------------

    @classmethod
    def from_api(cls, data: dict[str, Any]) -> Self:
        """Deserialise from a ``contacts.info`` or ``contacts.list`` payload.

        Accepts both the full response wrapper ``{"data": {...}}`` and a bare
        data dict.
        """
        d = data.get("data", data)

        pt_raw = d.get("payment_term")
        payment_term = PaymentTerm.from_api(pt_raw) if pt_raw else None

        return cls(
            id=d.get("id", ""),
            first_name=d.get("first_name", ""),
            last_name=d.get("last_name", ""),
            status=d.get("status", "active"),
            salutation=d.get("salutation"),
            vat_number=d.get("vat_number"),
            emails=[Email.from_api(e) for e in d.get("emails", [])],
            telephones=[Telephone.from_api(t) for t in d.get("telephones", [])],
            website=d.get("website"),
            addresses=[AddressEntry.from_api(a) for a in d.get("addresses", [])],
            gender=d.get("gender"),
            birthdate=d.get("birthdate"),
            iban=d.get("iban"),
            bic=d.get("bic"),
            national_identification_number=d.get("national_identification_number"),
            companies=d.get("companies", []),
            language=d.get("language"),
            payment_term=payment_term,
            remarks=d.get("remarks"),
            tags=d.get("tags", []),
            custom_fields=[CustomField.from_api(cf) for cf in d.get("custom_fields", [])],
            marketing_mails_consent=d.get("marketing_mails_consent"),
            added_at=d.get("added_at"),
            updated_at=d.get("updated_at"),
            web_url=d.get("web_url"),
        )

    def to_dict(self) -> dict[str, Any]:
        """Serialise to the shape expected by ``contacts.add`` / ``contacts.update``."""
        out: dict[str, Any] = {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "status": self.status,
            "emails": [e.to_dict() for e in self.emails],
            "telephones": [t.to_dict() for t in self.telephones],
            "addresses": [a.to_dict() for a in self.addresses],
            "tags": self.tags,
            "custom_fields": [cf.to_dict() for cf in self.custom_fields],
            "companies": self.companies,
        }
        if self.salutation is not None:
            out["salutation"] = self.salutation
        if self.vat_number is not None:
            out["vat_number"] = self.vat_number
        if self.website is not None:
            out["website"] = self.website
        if self.gender is not None:
            out["gender"] = self.gender
        if self.birthdate is not None:
            out["birthdate"] = self.birthdate
        if self.iban is not None:
            out["iban"] = self.iban
        if self.bic is not None:
            out["bic"] = self.bic
        if self.national_identification_number is not None:
            out["national_identification_number"] = self.national_identification_number
        if self.language is not None:
            out["language"] = self.language
        if self.payment_term is not None:
            out["payment_term"] = self.payment_term.to_dict()
        if self.remarks is not None:
            out["remarks"] = self.remarks
        if self.marketing_mails_consent is not None:
            out["marketing_mails_consent"] = self.marketing_mails_consent
        return out
