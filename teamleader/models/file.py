"""File model — curated layer over the Teamleader Focus files API."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Self


@dataclass
class File:
    """Represents a Teamleader Focus file (attachment).

    Fields
    ------
    id:
        Teamleader file UUID.
    name:
        Filename including extension (e.g. ``"report.pdf"``).
    mime_type:
        MIME type (e.g. ``"application/pdf"``).
    size:
        File size in bytes.
    updated_at:
        ISO 8601 datetime of last modification.
    subject:
        Entity the file is attached to (nullable).
        Shape: ``{"type": "deal", "id": "<uuid>"}``.
    uploaded_by:
        User who uploaded the file (nullable).
        Shape: ``{"type": "user", "id": "<uuid>"}``.
    folder:
        Folder name (nullable, e.g. ``"Documents"``).
    """

    id: str = ""
    name: str = ""
    mime_type: str = ""
    size: int = 0
    updated_at: str = ""
    subject: dict[str, Any] | None = None
    uploaded_by: dict[str, Any] | None = None
    folder: str | None = None

    # ------------------------------------------------------------------
    # Serialisation
    # ------------------------------------------------------------------

    @classmethod
    def from_api(cls, data: dict[str, Any]) -> Self:
        """Deserialise from a ``files.info`` or ``files.list`` payload.

        Accepts both the full response wrapper ``{"data": {...}}`` and a bare
        data dict, so it can be called consistently from both
        :meth:`~teamleader.resources.files.FilesResource.get` and
        :meth:`~teamleader.resources.files.FilesResource.list`.
        """
        d = data.get("data", data)
        return cls(
            id=d.get("id", ""),
            name=d.get("name", ""),
            mime_type=d.get("mime_type", ""),
            size=d.get("size", 0),
            updated_at=d.get("updated_at", ""),
            subject=d.get("subject"),
            uploaded_by=d.get("uploaded_by"),
            folder=d.get("folder"),
        )
