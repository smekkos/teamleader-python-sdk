"""Base classes for Teamleader resource objects.

Full implementation in Phase 7.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Generic, Iterator, TYPE_CHECKING, TypeVar

if TYPE_CHECKING:
    from teamleader.client import TeamleaderClient

M = TypeVar("M")


@dataclass
class Page(Generic[M]):
    """A single page of results from a list endpoint.

    Full implementation in Phase 7.
    """

    data: list[M] = field(default_factory=list)
    total_count: int = 0
    current_page: int = 1
    page_size: int = 20

    # Private — set by CrudResource after construction
    _resource: Any = field(default=None, repr=False, compare=False)
    _filters: dict[str, Any] = field(default_factory=dict, repr=False, compare=False)

    @property
    def has_next(self) -> bool:
        """Return True if there is at least one more page after this one."""
        raise NotImplementedError  # Phase 7

    def next(self) -> Page[M]:
        """Fetch and return the next page of results."""
        raise NotImplementedError  # Phase 7


class CrudResource(Generic[M]):
    """Generic CRUD resource base class.

    Subclasses set ``prefix`` and ``model`` at the class level.

    Full implementation in Phase 7.
    """

    prefix: str = ""
    model: type[M]  # type: ignore[misc]

    def __init__(self, client: TeamleaderClient) -> None:
        self._client = client

    def _path(self, operation: str) -> str:
        """Build the API path for *operation*, e.g. ``contacts.list``."""
        return f"{self.prefix}.{operation}"

    def _deserialise(self, data: dict[str, Any]) -> M:
        raise NotImplementedError  # Phase 7

    def list(
        self,
        *,
        page: int = 1,
        page_size: int = 20,
        **filters: Any,
    ) -> Page[M]:
        raise NotImplementedError  # Phase 7

    def get(self, id: str) -> M:
        raise NotImplementedError  # Phase 7

    def create(self, **kwargs: Any) -> M:
        raise NotImplementedError  # Phase 7

    def update(self, id: str, **kwargs: Any) -> M:
        raise NotImplementedError  # Phase 7

    def delete(self, id: str) -> None:
        raise NotImplementedError  # Phase 7

    def iterate(self, page_size: int = 20, **filters: Any) -> Iterator[M]:
        """Yield every matching object, fetching additional pages as needed."""
        raise NotImplementedError  # Phase 7
