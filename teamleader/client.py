"""Teamleader HTTP client.

``TeamleaderClient`` is the entry point for all API interactions.  It owns an
:class:`~teamleader.auth.OAuth2Handler` for token management and exposes a
typed resource attribute for every supported Teamleader resource.

Usage (non-Django)::

    from teamleader import TeamleaderClient
    from teamleader.auth import OAuth2Handler, MemoryTokenBackend

    backend = MemoryTokenBackend()
    backend.save(my_token)
    handler = OAuth2Handler(CLIENT_ID, CLIENT_SECRET, REDIRECT_URI, backend)
    client = TeamleaderClient(handler)

    deal = client.deals.get("some-uuid")

Usage (Django)::

    from teamleader.django import get_client

    client = get_client()
    for contact in client.contacts.iterate():
        print(contact.full_name)
"""

from __future__ import annotations

from typing import Any

import requests

from teamleader._generated.endpoints import ENDPOINTS
from teamleader.auth import OAuth2Handler
from teamleader.constants import BASE_URL, DEFAULT_TIMEOUT
from teamleader.exceptions import (
    TeamleaderAPIError,
    TeamleaderAuthError,
    TeamleaderNotFoundError,
    TeamleaderPermissionError,
    TeamleaderRateLimitError,
    TeamleaderServerError,
    TeamleaderValidationError,
)
from teamleader.resources.companies import CompaniesResource
from teamleader.resources.contacts import ContactsResource
from teamleader.resources.deals import DealsResource
from teamleader.resources.invoices import InvoicesResource
from teamleader.resources.quotations import QuotationsResource


class TeamleaderClient:
    """Entry point for all Teamleader API interactions.

    Parameters
    ----------
    auth_handler:
        Fully configured :class:`~teamleader.auth.OAuth2Handler`.  The handler
        is responsible for obtaining and refreshing access tokens; the client
        calls :meth:`~teamleader.auth.OAuth2Handler.get_valid_token` before
        every request so tokens are transparently refreshed as needed.
    timeout:
        HTTP request timeout in seconds.  Defaults to
        :data:`~teamleader.constants.DEFAULT_TIMEOUT` (30 s).
    """

    def __init__(
        self,
        auth_handler: OAuth2Handler,
        *,
        timeout: int = DEFAULT_TIMEOUT,
    ) -> None:
        self._auth = auth_handler
        self._timeout = timeout
        self._session = requests.Session()

        # Typed resource attributes — available immediately after construction.
        # Concrete methods raise NotImplementedError until Phase 7/9.
        self.contacts: ContactsResource = ContactsResource(self)
        self.companies: CompaniesResource = CompaniesResource(self)
        self.deals: DealsResource = DealsResource(self)
        self.invoices: InvoicesResource = InvoicesResource(self)
        self.quotations: QuotationsResource = QuotationsResource(self)

    # ------------------------------------------------------------------
    # Public generic caller
    # ------------------------------------------------------------------

    def call(self, operation_id: str, **kwargs: Any) -> dict[str, Any]:
        """Call any Teamleader API endpoint by its operation ID.

        Uses the generated :data:`~teamleader._generated.endpoints.ENDPOINTS`
        registry to look up the request path and validate required parameters
        **before** the HTTP request is sent.

        Parameters
        ----------
        operation_id:
            The Teamleader API operation ID exactly as it appears in
            :data:`~teamleader._generated.endpoints.ENDPOINTS`, e.g.
            ``"tickets.list"``, ``"activityTypes.list"``, ``"users.me"``.
        **kwargs:
            Request body parameters forwarded directly to the API as JSON.
            Required parameters for the chosen endpoint are validated; a
            ``ValueError`` is raised if any are missing.

        Returns
        -------
        dict[str, Any]:
            Raw response dictionary from the API.  Unlike curated resource
            methods (e.g. :meth:`~teamleader.resources.contacts.ContactsResource.get`),
            this does **not** deserialise into a typed model — the caller
            receives the JSON body as-is.

        Raises
        ------
        ValueError
            If *operation_id* is not in ``ENDPOINTS``, or if one or more
            required parameters are absent from *kwargs*.
        TeamleaderError
            Any HTTP-level error raised by the underlying transport layer
            (same exceptions as the curated resources).

        Examples
        --------
        List activity types (no required params):

        .. code-block:: python

            result = client.call("activityTypes.list", page={"size": 20, "number": 1})
            for item in result["data"]:
                print(item["name"])

        Fetch a single department (``id`` is required):

        .. code-block:: python

            dept = client.call("departments.info", id="67c576e7-7e6f-465d-b6ab-a864f6e5e95b")
            print(dept["data"]["name"])
        """
        endpoint = ENDPOINTS.get(operation_id)
        if endpoint is None:
            raise ValueError(
                f"Unknown operation_id {operation_id!r}. "
                f"See teamleader._generated.endpoints.ENDPOINTS.keys() for the "
                f"full list of {len(ENDPOINTS)} available operation IDs."
            )

        missing = [p for p in endpoint.required_params if p not in kwargs]
        if missing:
            raise ValueError(
                f"Missing required parameter(s) for {operation_id!r}: "
                f"{missing}. "
                f"Required: {list(endpoint.required_params)}, "
                f"optional: {list(endpoint.optional_params)}."
            )

        # endpoint.path is "/contacts.list"; _post expects "contacts.list"
        return self._post(endpoint.path.lstrip("/"), kwargs if kwargs else None)

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _auth_headers(self) -> dict[str, str]:
        """Return an ``Authorization`` header with a fresh Bearer token.

        Calls :meth:`~teamleader.auth.OAuth2Handler.get_valid_token`, which
        transparently refreshes the token if it is within the expiry margin.
        """
        token = self._auth.get_valid_token()
        return {"Authorization": f"Bearer {token}"}

    # ------------------------------------------------------------------
    # Internal HTTP helpers
    # ------------------------------------------------------------------

    def _get(
        self,
        path: str,
        params: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Make an authenticated GET request and return the parsed JSON body.

        Parameters
        ----------
        path:
            API path segment, e.g. ``"users.me"``.  Appended to
            :data:`~teamleader.constants.BASE_URL` with a ``/`` separator.
        params:
            Optional query-string parameters.
        """
        response = self._session.get(
            f"{BASE_URL}/{path}",
            headers=self._auth_headers(),
            params=params,
            timeout=self._timeout,
        )
        return self._handle_response(response)

    def _post(
        self,
        path: str,
        json: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Make an authenticated POST request and return the parsed JSON body.

        Parameters
        ----------
        path:
            API path segment, e.g. ``"contacts.list"``.  Appended to
            :data:`~teamleader.constants.BASE_URL` with a ``/`` separator.
        json:
            Request body serialised as JSON.  Pass ``None`` for endpoints
            that take no body.
        """
        response = self._session.post(
            f"{BASE_URL}/{path}",
            headers=self._auth_headers(),
            json=json,
            timeout=self._timeout,
        )
        return self._handle_response(response)

    def _handle_response(self, response: requests.Response) -> dict[str, Any]:
        """Map HTTP status codes to SDK exceptions; return the body on success.

        Success path (2xx):
            Returns the parsed JSON dict, or an empty dict for empty bodies
            (e.g. 204 No Content).

        Error path:
            Raises the most specific :exc:`~teamleader.exceptions.TeamleaderError`
            subclass that matches the status code.

        Status mapping
        --------------
        - 401 → :exc:`~teamleader.exceptions.TeamleaderAuthError`
        - 403 → :exc:`~teamleader.exceptions.TeamleaderPermissionError`
        - 404 → :exc:`~teamleader.exceptions.TeamleaderNotFoundError`
        - 422 → :exc:`~teamleader.exceptions.TeamleaderValidationError`
        - 429 → :exc:`~teamleader.exceptions.TeamleaderRateLimitError`
          (``retry_after`` populated from the ``Retry-After`` response header)
        - 5xx → :exc:`~teamleader.exceptions.TeamleaderServerError`
        - other 4xx → :exc:`~teamleader.exceptions.TeamleaderAPIError`
        """
        status = response.status_code

        # ---- success -------------------------------------------------
        if status < 300:
            if not response.content:
                return {}
            return response.json()  # type: ignore[no-any-return]

        # ---- error — shared keyword args ----------------------------
        message = self._extract_message(response)
        err_kwargs: dict[str, Any] = {
            "status_code": status,
            "raw_response": response,
        }

        if status == 401:
            raise TeamleaderAuthError(message, **err_kwargs)
        if status == 403:
            raise TeamleaderPermissionError(message, **err_kwargs)
        if status == 404:
            raise TeamleaderNotFoundError(message, **err_kwargs)
        if status == 422:
            raise TeamleaderValidationError(message, **err_kwargs)
        if status == 429:
            retry_after_raw = response.headers.get("Retry-After")
            retry_after = int(retry_after_raw) if retry_after_raw is not None else None
            raise TeamleaderRateLimitError(
                message,
                retry_after=retry_after,
                **err_kwargs,
            )
        if status >= 500:
            raise TeamleaderServerError(message, **err_kwargs)

        # Unexpected 4xx (e.g. 400, 409)
        raise TeamleaderAPIError(message, **err_kwargs)

    @staticmethod
    def _extract_message(response: requests.Response) -> str:
        """Best-effort extraction of an error message from the response body.

        Understands two common Teamleader error shapes:

        JSON:API (most endpoints)::

            {"errors": [{"title": "The contact was not found."}, ...]}

        OAuth-style (token endpoint)::

            {"error": "invalid_grant", "error_description": "Token expired."}

        Falls back to the raw response text, or ``"HTTP <status>"`` if the
        body is empty.
        """
        try:
            body: dict[str, Any] = response.json()
        except ValueError:
            return response.text or f"HTTP {response.status_code}"

        # JSON:API error array
        errors = body.get("errors")
        if isinstance(errors, list) and errors:
            titles = [
                e.get("title", "")
                for e in errors
                if isinstance(e, dict)
            ]
            joined = "; ".join(t for t in titles if t)
            return joined or response.text or f"HTTP {response.status_code}"

        # OAuth / generic single-message shapes
        for key in ("error_description", "message", "error"):
            value = body.get(key)
            if isinstance(value, str) and value:
                return value

        return response.text or f"HTTP {response.status_code}"
