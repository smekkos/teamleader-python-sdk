"""Shared sub-models used across multiple Teamleader resources.

Full implementation in Phase 8.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Self


@dataclass
class Address:
    """Postal address."""

    line_1: str | None = None
    postal_code: str | None = None
    city: str | None = None
    country: str | None = None  # ISO 3166-1 alpha-2
    area_level_two_id: str | None = None

    @classmethod
    def from_api(cls, data: dict[str, Any]) -> Self:
        raise NotImplementedError  # Phase 8

    def to_dict(self) -> dict[str, Any]:
        raise NotImplementedError  # Phase 8


@dataclass
class Email:
    """Email contact detail."""

    email: str
    type: str | None = None  # "primary", "invoicing", etc.

    @classmethod
    def from_api(cls, data: dict[str, Any]) -> Self:
        raise NotImplementedError  # Phase 8

    def to_dict(self) -> dict[str, Any]:
        raise NotImplementedError  # Phase 8


@dataclass
class Telephone:
    """Telephone contact detail."""

    number: str
    type: str | None = None

    @classmethod
    def from_api(cls, data: dict[str, Any]) -> Self:
        raise NotImplementedError  # Phase 8

    def to_dict(self) -> dict[str, Any]:
        raise NotImplementedError  # Phase 8


@dataclass
class Money:
    """Monetary amount with currency."""

    amount: float
    currency: str  # ISO 4217 (e.g. "EUR")

    @classmethod
    def from_api(cls, data: dict[str, Any]) -> Self:
        raise NotImplementedError  # Phase 8

    def to_dict(self) -> dict[str, Any]:
        raise NotImplementedError  # Phase 8


@dataclass
class CustomField:
    """A single custom field value attached to a resource."""

    id: str
    value: Any = None

    @classmethod
    def from_api(cls, data: dict[str, Any]) -> Self:
        raise NotImplementedError  # Phase 8

    def to_dict(self) -> dict[str, Any]:
        raise NotImplementedError  # Phase 8


@dataclass
class WebLink:
    """Web URL attached to a resource."""

    url: str
    type: str | None = None

    @classmethod
    def from_api(cls, data: dict[str, Any]) -> Self:
        raise NotImplementedError  # Phase 8

    def to_dict(self) -> dict[str, Any]:
        raise NotImplementedError  # Phase 8
