"""Shared sub-models used across multiple Teamleader resources."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Self


@dataclass
class TypeAndId:
    """A lightweight reference: a resource type string plus a UUID."""

    id: str = ""
    type: str = ""

    @classmethod
    def from_api(cls, data: dict[str, Any]) -> Self:
        return cls(
            id=data.get("id", ""),
            type=data.get("type", ""),
        )

    def to_dict(self) -> dict[str, Any]:
        return {"id": self.id, "type": self.type}


@dataclass
class Address:
    """Postal address (leaf object — no type/addressee here)."""

    line_1: str | None = None
    postal_code: str | None = None
    city: str | None = None
    country: str | None = None  # ISO 3166-1 alpha-2
    area_level_two: dict[str, Any] | None = None  # TypeAndId ref (id + type)

    @classmethod
    def from_api(cls, data: dict[str, Any]) -> Self:
        area = data.get("area_level_two")
        return cls(
            line_1=data.get("line_1"),
            postal_code=data.get("postal_code"),
            city=data.get("city"),
            country=data.get("country"),
            area_level_two=area if area else None,
        )

    def to_dict(self) -> dict[str, Any]:
        out: dict[str, Any] = {}
        if self.line_1 is not None:
            out["line_1"] = self.line_1
        if self.postal_code is not None:
            out["postal_code"] = self.postal_code
        if self.city is not None:
            out["city"] = self.city
        if self.country is not None:
            out["country"] = self.country
        if self.area_level_two is not None:
            out["area_level_two"] = self.area_level_two
        return out


@dataclass
class AddressEntry:
    """Typed address wrapper — role (e.g. "primary") + address + optional addressee."""

    type: str | None = None       # "primary" | "invoicing" | "delivery" | "visiting"
    address: Address | None = None
    addressee: str | None = None

    @classmethod
    def from_api(cls, data: dict[str, Any]) -> Self:
        raw_addr = data.get("address") or {}
        addressee = raw_addr.get("addressee")
        addr = Address.from_api(raw_addr) if raw_addr else None
        return cls(
            type=data.get("type"),
            address=addr,
            addressee=addressee,
        )

    def to_dict(self) -> dict[str, Any]:
        out: dict[str, Any] = {}
        if self.type is not None:
            out["type"] = self.type
        addr_dict: dict[str, Any] = self.address.to_dict() if self.address else {}
        if self.addressee is not None:
            addr_dict["addressee"] = self.addressee
        if addr_dict:
            out["address"] = addr_dict
        return out


@dataclass
class Email:
    """Email contact detail."""

    email: str = ""
    type: str | None = None  # "primary" | "invoicing"

    @classmethod
    def from_api(cls, data: dict[str, Any]) -> Self:
        return cls(
            email=data.get("email", ""),
            type=data.get("type"),
        )

    def to_dict(self) -> dict[str, Any]:
        out: dict[str, Any] = {"email": self.email}
        if self.type is not None:
            out["type"] = self.type
        return out


@dataclass
class Telephone:
    """Telephone contact detail."""

    number: str = ""
    type: str | None = None  # "phone" | "mobile" | "fax"

    @classmethod
    def from_api(cls, data: dict[str, Any]) -> Self:
        return cls(
            number=data.get("number", ""),
            type=data.get("type"),
        )

    def to_dict(self) -> dict[str, Any]:
        out: dict[str, Any] = {"number": self.number}
        if self.type is not None:
            out["type"] = self.type
        return out


@dataclass
class Money:
    """Monetary amount with ISO 4217 currency code."""

    amount: float = 0.0
    currency: str = ""  # e.g. "EUR"

    @classmethod
    def from_api(cls, data: dict[str, Any]) -> Self:
        return cls(
            amount=float(data.get("amount", 0.0)),
            currency=data.get("currency", ""),
        )

    def to_dict(self) -> dict[str, Any]:
        return {"amount": self.amount, "currency": self.currency}


@dataclass
class CustomField:
    """A single custom field value attached to a resource.

    ``id`` is the custom-field *definition* UUID (shortcut to ``definition["id"]``).
    """

    id: str = ""
    value: Any = None
    definition: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_api(cls, data: dict[str, Any]) -> Self:
        definition = data.get("definition") or {}
        return cls(
            id=definition.get("id", ""),
            value=data.get("value"),
            definition=definition,
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "definition": self.definition or {"id": self.id, "type": "customFieldDefinition"},
            "value": self.value,
        }


@dataclass
class PaymentTerm:
    """Payment term attached to a contact or company."""

    type: str = ""  # "cash" | "end_of_month" | "after_invoice_date"
    days: int | None = None

    @classmethod
    def from_api(cls, data: dict[str, Any]) -> Self:
        return cls(
            type=data.get("type", ""),
            days=int(data["days"]) if data.get("days") is not None else None,
        )

    def to_dict(self) -> dict[str, Any]:
        out: dict[str, Any] = {"type": self.type}
        if self.days is not None:
            out["days"] = self.days
        return out


@dataclass
class WebLink:
    """Web URL attached to a resource (kept for backward compatibility)."""

    url: str = ""
    type: str | None = None

    @classmethod
    def from_api(cls, data: dict[str, Any]) -> Self:
        return cls(
            url=data.get("url", ""),
            type=data.get("type"),
        )

    def to_dict(self) -> dict[str, Any]:
        out: dict[str, Any] = {"url": self.url}
        if self.type is not None:
            out["type"] = self.type
        return out
