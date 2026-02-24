"""Contact model — curated layer over the generated base.

Full implementation in Phase 8.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Self

from teamleader.models.common import Address, CustomField, Email, Telephone, WebLink


@dataclass
class Contact:
    """Represents a Teamleader Focus contact.

    Inherits fields from ``_ContactBase`` (generated) and adds
    deserialization, serialisation, and computed properties.

    Full implementation in Phase 8.
    """

    id: str = ""
    first_name: str = ""
    last_name: str = ""
    emails: list[Email] = field(default_factory=list)
    telephones: list[Telephone] = field(default_factory=list)
    addresses: list[Address] = field(default_factory=list)
    websites: list[WebLink] = field(default_factory=list)
    custom_fields: list[CustomField] = field(default_factory=list)

    @property
    def full_name(self) -> str:
        """Return ``"First Last"``."""
        return f"{self.first_name} {self.last_name}".strip()

    @classmethod
    def from_api(cls, data: dict[str, Any]) -> Self:
        raise NotImplementedError  # Phase 8

    def to_dict(self) -> dict[str, Any]:
        raise NotImplementedError  # Phase 8
