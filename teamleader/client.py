"""Teamleader HTTP client.

Full implementation in Phase 6.  Stubs are provided here so the
package is importable during the scaffold phase.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from teamleader.auth import OAuth2Handler


class TeamleaderClient:
    """Entry point for all Teamleader API interactions.

    Instantiate via ``teamleader.django.get_client()`` in Django projects,
    or construct directly with an :class:`~teamleader.auth.OAuth2Handler`
    for framework-agnostic use.

    Example (non-Django)::

        from teamleader import TeamleaderClient
        from teamleader.auth import OAuth2Handler, MemoryTokenBackend

        backend = MemoryTokenBackend()
        backend.save(my_token)
        handler = OAuth2Handler(CLIENT_ID, CLIENT_SECRET, REDIRECT_URI, backend)
        client = TeamleaderClient(handler)

        deal = client.deals.get("some-uuid")
    """

    def __init__(self, auth_handler: OAuth2Handler) -> None:
        self._auth = auth_handler

        # Resource attributes — assigned in Phase 6 after resource classes exist
        # self.contacts = ContactsResource(self)
        # self.companies = CompaniesResource(self)
        # self.deals = DealsResource(self)
        # self.invoices = InvoicesResource(self)
        # self.quotations = QuotationsResource(self)

    # ------------------------------------------------------------------
    # Internal HTTP helpers — implemented in Phase 6
    # ------------------------------------------------------------------

    def _get(self, path: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        raise NotImplementedError  # Phase 6

    def _post(self, path: str, json: dict[str, Any] | None = None) -> dict[str, Any]:
        raise NotImplementedError  # Phase 6

    def _handle_response(self, response: Any) -> dict[str, Any]:
        raise NotImplementedError  # Phase 6
