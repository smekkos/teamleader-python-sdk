"""Unit tests for curated model classes.

Full implementation in Phase 11.

Covers:
- from_api() round-trips for each model
- Computed properties: Contact.full_name, Invoice.is_overdue
- to_dict() produces valid API payloads
"""

from __future__ import annotations
