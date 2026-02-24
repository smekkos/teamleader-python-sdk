"""Invoice model — curated layer over the generated base.

Full implementation in Phase 8.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Self

from teamleader.models.common import CustomField, Money


@dataclass
class Invoice:
    """Represents a Teamleader Focus invoice.

    Full implementation in Phase 8.
    """

    id: str = ""
    invoice_number: str | None = None
    status: str = ""  # will become an enum after Phase 2/8
    due_date: str | None = None  # ISO 8601 date string
    total: Money | None = None
    custom_fields: list[CustomField] = field(default_factory=list)

    @property
    def is_overdue(self) -> bool:
        """Return True if the due date is in the past and status is not paid."""
        raise NotImplementedError  # Phase 8

    @classmethod
    def from_api(cls, data: dict[str, Any]) -> Self:
        raise NotImplementedError  # Phase 8

    def to_dict(self) -> dict[str, Any]:
        raise NotImplementedError  # Phase 8
