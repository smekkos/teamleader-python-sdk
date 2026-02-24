"""Unit tests for resource classes and pagination.

Full implementation in Phase 11.

Covers:
- list() returns a Page with correct data and metadata
- get() returns a deserialised model
- create() POSTs and returns the new object
- update() PATCHes and re-fetches
- delete() sends DELETE and returns None
- Page.has_next is True when more pages exist
- iterate() transparently fetches multiple pages
"""

from __future__ import annotations
