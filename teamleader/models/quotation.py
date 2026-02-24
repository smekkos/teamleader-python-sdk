"""Quotation model — curated layer over the generated base.

Full implementation in Phase 8.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Self

from teamleader.models.common import CustomField, Money


@dataclass
class Quotation:
    """Represents a Teamleader Focus quotation.

    Full implementation in Phase 8.
    """

    id: str = ""
    title: str = ""
    status: str = ""  # will become an enum after Phase 2/8
    total: Money | None = None
    custom_fields: list[CustomField] = field(default_factory=list)

    @classmethod
    def from_api(cls, data: dict[str, Any]) -> Self:
        raise NotImplementedError  # Phase 8

    def to_dict(self) -> dict[str, Any]:
        raise NotImplementedError  # Phase 8
