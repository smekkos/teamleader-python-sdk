"""Base classes for Teamleader resource objects.

Every concrete resource (contacts, deals, …) subclasses :class:`CrudResource`
and sets two class-level attributes::

    class ContactsResource(CrudResource[Contact]):
        prefix = "contacts"
        model = Contact

The :class:`Page` dataclass is returned by :meth:`CrudResource.list` and
exposes lazy forward-pagination via :meth:`Page.next`.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Generic, Iterator, TYPE_CHECKING, TypeVar

from teamleader.constants import DEFAULT_PAGE_SIZE

if TYPE_CHECKING:
    from teamleader.client import TeamleaderClient

M = TypeVar("M")


@dataclass
class Page(Generic[M]):
    """A single page of results from a list endpoint.

    Parameters
    ----------
    data:
        The deserialised model objects on this page.
    total_count:
        Total number of matching objects across **all** pages
        (``meta.matches`` from the API response).
    current_page:
        1-based index of this page.
    page_size:
        Number of items requested per page.

    After construction :class:`CrudResource` sets two private attributes used
    for forward-pagination:

    ``_resource``
        Back-reference to the :class:`CrudResource` that produced this page.
    ``_filters``
        The extra ``**filters`` kwargs that were passed to
        :meth:`CrudResource.list`, forwarded verbatim when fetching the next page.
    """

    data: list[M]
    total_count: int
    current_page: int
    page_size: int

    # Set by CrudResource after construction — not part of the public constructor.
    _resource: Any = field(default=None, init=False, repr=False, compare=False)
    _filters: dict[str, Any] = field(
        default_factory=dict, init=False, repr=False, compare=False
    )

    @property
    def has_next(self) -> bool:
        """``True`` when at least one more page exists after this one.

        Calculated as ``current_page * page_size < total_count``.  This is
        correct even when the last page is partially filled (e.g. 5 items with
        page_size=20 → ``1 * 20 < 5`` is ``False``).
        """
        return self.current_page * self.page_size < self.total_count

    def next(self) -> Page[M]:
        """Fetch and return the next page of results.

        Raises
        ------
        ValueError
            If :attr:`has_next` is ``False`` (caller should check before calling).
        """
        if not self.has_next:
            raise ValueError(
                f"No more pages: page {self.current_page} * size {self.page_size}"
                f" >= total {self.total_count}"
            )
        return self._resource.list(
            page=self.current_page + 1,
            page_size=self.page_size,
            **self._filters,
        )


class CrudResource(Generic[M]):
    """Generic CRUD resource base class.

    Subclasses **must** set two class-level attributes:

    ``prefix``
        The Teamleader API resource prefix, e.g. ``"contacts"``.  Combined with
        an operation name to build the endpoint path: ``contacts.list``,
        ``contacts.info``, etc.

    ``model``
        The model class to deserialise API payloads into.  Must implement a
        ``from_api(dict) -> M`` classmethod.

    All Teamleader API calls use POST; both :meth:`list` and mutating operations
    go through :meth:`~teamleader.client.TeamleaderClient._post`.

    Parameters
    ----------
    client:
        A fully configured :class:`~teamleader.client.TeamleaderClient`.
    """

    prefix: str = ""
    model: type[M]  # type: ignore[misc]

    def __init__(self, client: TeamleaderClient) -> None:
        self._client = client

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _path(self, operation: str) -> str:
        """Build the full operation path, e.g. ``contacts.list``.

        Parameters
        ----------
        operation:
            The operation suffix — ``"list"``, ``"info"``, ``"add"``,
            ``"update"``, ``"delete"``, or any resource-specific action.
        """
        return f"{self.prefix}.{operation}"

    def _deserialise(self, data: dict[str, Any]) -> M:
        """Deserialise a single API object dict into a model instance.

        Delegates to ``model.from_api(data)``.
        """
        return self.model.from_api(data)  # type: ignore[return-value]

    # ------------------------------------------------------------------
    # CRUD operations
    # ------------------------------------------------------------------

    def list(
        self,
        *,
        page: int = 1,
        page_size: int = DEFAULT_PAGE_SIZE,
        **filters: Any,
    ) -> Page[M]:
        """Return a single page of results.

        Parameters
        ----------
        page:
            1-based page number.  Defaults to ``1``.
        page_size:
            Number of items per page.  Defaults to
            :data:`~teamleader.constants.DEFAULT_PAGE_SIZE` (20).
        **filters:
            Extra top-level body parameters forwarded to the API, e.g.
            ``filter={"email": "..."}``, ``sort=[...]``, ``includes=[...]``.
            These are stored on the returned :class:`Page` so that
            :meth:`Page.next` can continue with the same filters.

        Returns
        -------
        Page[M]
            A page whose ``total_count`` reflects ``meta.matches`` from the
            API response — the total across **all** pages, not just this one.
        """
        body: dict[str, Any] = {
            "page": {"size": page_size, "number": page},
            **filters,
        }
        resp = self._client._post(self._path("list"), body)
        items = [self._deserialise(d) for d in resp["data"]]
        page_obj = Page(
            data=items,
            total_count=resp["meta"]["matches"],
            current_page=page,
            page_size=page_size,
        )
        page_obj._resource = self
        page_obj._filters = filters
        return page_obj

    def get(self, id: str) -> M:
        """Fetch a single object by ID.

        Uses the ``{prefix}.info`` endpoint (Teamleader's canonical name for
        single-object retrieval — not ``.get``).

        Parameters
        ----------
        id:
            The UUID of the object to retrieve.
        """
        resp = self._client._post(self._path("info"), {"id": id})
        return self._deserialise(resp["data"])

    def create(self, **kwargs: Any) -> M:
        """Create a new object and return the fully-populated model.

        POSTs ``kwargs`` to the ``{prefix}.add`` endpoint.  The API returns a
        minimal reference ``{"data": {"type": "...", "id": "..."}}``; this
        method re-fetches the full object via :meth:`get` before returning.

        Parameters
        ----------
        **kwargs:
            Fields to set on the new object, as accepted by the ``add``
            endpoint for this resource.
        """
        resp = self._client._post(self._path("add"), kwargs)
        new_id: str = resp["data"]["id"]
        return self.get(new_id)

    def update(self, id: str, **kwargs: Any) -> M:
        """Update an existing object and return the refreshed model.

        POSTs ``{"id": id, **kwargs}`` to the ``{prefix}.update`` endpoint.
        The API returns an empty body on success; this method re-fetches the
        updated object via :meth:`get` before returning.

        Parameters
        ----------
        id:
            The UUID of the object to update.
        **kwargs:
            Fields to change, as accepted by the ``update`` endpoint.
        """
        self._client._post(self._path("update"), {"id": id, **kwargs})
        return self.get(id)

    def delete(self, id: str) -> None:
        """Delete an object by ID.

        POSTs ``{"id": id}`` to the ``{prefix}.delete`` endpoint.  Returns
        ``None`` on success; raises a
        :class:`~teamleader.exceptions.TeamleaderError` subclass on failure.

        Parameters
        ----------
        id:
            The UUID of the object to delete.
        """
        self._client._post(self._path("delete"), {"id": id})

    def iterate(self, page_size: int = DEFAULT_PAGE_SIZE, **filters: Any) -> Iterator[M]:
        """Yield every matching object, transparently fetching additional pages.

        This is the preferred way to consume a full result set without dealing
        with pagination manually::

            for contact in client.contacts.iterate():
                print(contact.full_name)

        Parameters
        ----------
        page_size:
            Items per page for each underlying :meth:`list` call.  Defaults to
            :data:`~teamleader.constants.DEFAULT_PAGE_SIZE` (20).
        **filters:
            Forwarded to every :meth:`list` call (same semantics as
            :meth:`list`'s ``**filters``).
        """
        current = self.list(page=1, page_size=page_size, **filters)
        while True:
            yield from current.data
            if not current.has_next:
                break
            current = current.next()
