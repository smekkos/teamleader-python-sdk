"""Deal model — curated layer over the Teamleader Focus deals API."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Self

from teamleader.models.common import CustomField, Money, TypeAndId


@dataclass
class Deal:
    """Represents a Teamleader Focus deal.

    All datetime fields are ISO 8601 strings as returned by the API.
    Use the computed properties for convenient access to common values.
    """

    id: str = ""
    title: str = ""
    summary: str | None = None
    reference: str | None = None
    status: str = "open"                        # "open" | "won" | "lost"
    lead: dict[str, Any] | None = None          # {customer: TypeAndId, contact_person: TypeAndId}
    department: TypeAndId | None = None
    estimated_value: Money | None = None
    estimated_closing_date: str | None = None   # ISO 8601 date
    estimated_probability: float | None = None  # 0.0 – 1.0
    weighted_value: Money | None = None
    purchase_order_number: str | None = None
    current_phase: TypeAndId | None = None
    responsible_user: TypeAndId | None = None
    closed_at: str | None = None                # ISO 8601 datetime
    source: TypeAndId | None = None
    phase_history: list[dict[str, Any]] = field(default_factory=list)
    quotations: list[TypeAndId] = field(default_factory=list)
    lost_reason: dict[str, Any] | None = None
    pipeline: TypeAndId | None = None
    custom_fields: list[CustomField] = field(default_factory=list)
    created_at: str | None = None               # ISO 8601 datetime
    updated_at: str | None = None               # ISO 8601 datetime
    web_url: str | None = None

    # ------------------------------------------------------------------
    # Computed properties
    # ------------------------------------------------------------------

    @property
    def is_open(self) -> bool:
        """Return ``True`` when the deal is still open."""
        return self.status == "open"

    @property
    def is_won(self) -> bool:
        """Return ``True`` when the deal has been won."""
        return self.status == "won"

    @property
    def is_lost(self) -> bool:
        """Return ``True`` when the deal has been lost."""
        return self.status == "lost"

    @property
    def customer_id(self) -> str | None:
        """Return the UUID of the lead's customer, or ``None`` if no lead."""
        if self.lead and isinstance(self.lead.get("customer"), dict):
            return self.lead["customer"].get("id")
        return None

    @property
    def customer_type(self) -> str | None:
        """Return the resource type of the lead's customer (``"contact"`` or ``"company"``).

        Returns ``None`` if no lead is set.
        """
        if self.lead and isinstance(self.lead.get("customer"), dict):
            return self.lead["customer"].get("type")
        return None

    # ------------------------------------------------------------------
    # Serialisation
    # ------------------------------------------------------------------

    @classmethod
    def from_api(cls, data: dict[str, Any]) -> Self:
        """Deserialise from a ``deals.info`` or ``deals.list`` payload.

        Accepts both the full response wrapper ``{"data": {...}}`` and a bare
        data dict.
        """
        d = data.get("data", data)

        dept_raw = d.get("department")
        department = TypeAndId.from_api(dept_raw) if dept_raw else None

        ev_raw = d.get("estimated_value")
        estimated_value = Money.from_api(ev_raw) if ev_raw else None

        wv_raw = d.get("weighted_value")
        weighted_value = Money.from_api(wv_raw) if wv_raw else None

        cp_raw = d.get("current_phase")
        current_phase = TypeAndId.from_api(cp_raw) if cp_raw else None

        ru_raw = d.get("responsible_user")
        responsible_user = TypeAndId.from_api(ru_raw) if ru_raw else None

        src_raw = d.get("source")
        source = TypeAndId.from_api(src_raw) if src_raw else None

        pl_raw = d.get("pipeline")
        pipeline = TypeAndId.from_api(pl_raw) if pl_raw else None

        quotations = [
            TypeAndId.from_api(q) for q in d.get("quotations", [])
        ]

        return cls(
            id=d.get("id", ""),
            title=d.get("title", ""),
            summary=d.get("summary"),
            reference=d.get("reference"),
            status=d.get("status", "open"),
            lead=d.get("lead"),
            department=department,
            estimated_value=estimated_value,
            estimated_closing_date=d.get("estimated_closing_date"),
            estimated_probability=d.get("estimated_probability"),
            weighted_value=weighted_value,
            purchase_order_number=d.get("purchase_order_number"),
            current_phase=current_phase,
            responsible_user=responsible_user,
            closed_at=d.get("closed_at"),
            source=source,
            phase_history=d.get("phase_history", []),
            quotations=quotations,
            lost_reason=d.get("lost_reason"),
            pipeline=pipeline,
            custom_fields=[CustomField.from_api(cf) for cf in d.get("custom_fields", [])],
            created_at=d.get("created_at"),
            updated_at=d.get("updated_at"),
            web_url=d.get("web_url"),
        )

    def to_dict(self) -> dict[str, Any]:
        """Serialise to the shape expected by ``deals.create`` / ``deals.update``."""
        out: dict[str, Any] = {
            "id": self.id,
            "title": self.title,
            "status": self.status,
            "custom_fields": [cf.to_dict() for cf in self.custom_fields],
        }
        if self.summary is not None:
            out["summary"] = self.summary
        if self.reference is not None:
            out["reference"] = self.reference
        if self.lead is not None:
            out["lead"] = self.lead
        if self.department is not None:
            out["department"] = self.department.to_dict()
        if self.estimated_value is not None:
            out["estimated_value"] = self.estimated_value.to_dict()
        if self.estimated_closing_date is not None:
            out["estimated_closing_date"] = self.estimated_closing_date
        if self.estimated_probability is not None:
            out["estimated_probability"] = self.estimated_probability
        if self.purchase_order_number is not None:
            out["purchase_order_number"] = self.purchase_order_number
        if self.current_phase is not None:
            out["current_phase"] = self.current_phase.to_dict()
        if self.responsible_user is not None:
            out["responsible_user"] = self.responsible_user.to_dict()
        if self.source is not None:
            out["source"] = self.source.to_dict()
        return out
