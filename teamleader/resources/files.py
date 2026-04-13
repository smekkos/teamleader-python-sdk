"""Files resource — upload, download, list, get, delete."""

from __future__ import annotations

from typing import Any, Iterator

import requests as _requests

from teamleader.constants import DEFAULT_PAGE_SIZE
from teamleader.models.file import File
from teamleader.resources.base import CrudResource, Page


class FilesResource(CrudResource[File]):
    """File management for Teamleader Focus.

    Unlike contacts / companies / deals, files do not follow the standard
    add/update CRUD pattern.  This resource exposes five API operations:

    - :meth:`upload` — request a signed upload URL (step 1 of 2).
    - :meth:`upload_content` — full two-step convenience wrapper.
    - :meth:`download` — request a temporary download URL.
    - :meth:`list` — list files attached to an entity (returns :class:`~teamleader.resources.base.Page`).
    - :meth:`get` — get full details for a single file (inherited from :class:`~teamleader.resources.base.CrudResource`).
    - :meth:`delete` — permanently delete a file (inherited from :class:`~teamleader.resources.base.CrudResource`).

    .. note::
        ``create()``, ``update()``, and ``iterate()`` are **not** supported
        for files and raise :exc:`NotImplementedError` if called.  Use
        :meth:`upload_content` to add a file, and loop over :meth:`list`
        pages manually when you need to consume many pages.
    """

    prefix = "files"
    model = File

    # ------------------------------------------------------------------
    # Upload
    # ------------------------------------------------------------------

    def upload(
        self,
        name: str,
        subject: dict[str, Any],
        *,
        folder: str | None = None,
    ) -> dict[str, Any]:
        """Request a pre-signed upload URL (step 1 of the upload flow).

        Calls ``files.upload``.  The returned ``location`` is a short-lived
        signed URL (~2 minutes); PUT the raw file bytes to it to complete the
        upload (see :meth:`upload_content` for a one-call convenience wrapper).

        Parameters
        ----------
        name:
            Filename including extension (e.g. ``"report.pdf"``).
        subject:
            Entity to attach the file to — dict with ``type`` and ``id``.

            Supported types: ``company``, ``contact``, ``deal``, ``invoice``,
            ``creditNote``, ``nextgenProject``, ``ticket``.

            Pass ``{"type": "temporary"}`` to upload without linking
            (file is auto-deleted after 24 hours if never linked).
        folder:
            Optional Teamleader folder name.  Defaults to the account's
            *General* folder when omitted.

        Returns
        -------
        dict
            ``{"id": "<file-uuid>", "location": "<signed-url>", "expires_at": "<iso-datetime>"}``
        """
        body: dict[str, Any] = {"name": name, "subject": subject}
        if folder is not None:
            body["folder"] = folder
        resp = self._client._post("files.upload", body)
        return resp.get("data", {})

    def upload_content(
        self,
        name: str,
        content: bytes,
        subject: dict[str, Any],
        *,
        content_type: str = "application/octet-stream",
        folder: str | None = None,
        timeout: int = 30,
    ) -> str:
        """Upload raw file content in a single call (steps 1 + 2).

        Requests a pre-signed URL via :meth:`upload`, then PUTs the raw bytes
        to that URL.  The file UUID is taken from the step-1 response — cloud
        storage signed-URL endpoints return an empty body, not a JSON payload.

        Parameters
        ----------
        name:
            Filename including extension.
        content:
            Raw file bytes.
        subject:
            Entity to attach the file to; see :meth:`upload` for valid types.
        content_type:
            ``Content-Type`` header for the PUT request.  Defaults to
            ``"application/octet-stream"``.
        folder:
            Optional Teamleader folder name.
        timeout:
            HTTP timeout in seconds for the PUT request.  Defaults to ``30``.

        Returns
        -------
        str
            The Teamleader file UUID assigned at upload time.

        Raises
        ------
        requests.HTTPError
            If the PUT to the signed URL fails (non-2xx status).
        """
        upload_info = self.upload(name, subject, folder=folder)
        location: str = upload_info["location"]

        # Step 2: POST the binary content to the Teamleader-hosted upload URL.
        # The spec says POST (not PUT), and the response body returns the file UUID.
        resp = _requests.post(
            location,
            data=content,
            headers={"Content-Type": content_type},
            timeout=timeout,
        )
        resp.raise_for_status()
        return resp.json()["data"]["id"]

    # ------------------------------------------------------------------
    # Download
    # ------------------------------------------------------------------

    def download(self, id: str) -> dict[str, str]:
        """Request a temporary download URL for a file.

        Calls ``files.download``.  The returned URL is valid for a short
        period (typically a few minutes).

        Parameters
        ----------
        id:
            Teamleader file UUID.

        Returns
        -------
        dict
            ``{"location": "<cdn-url>", "expires_at": "<iso-datetime>"}``
        """
        resp = self._client._post("files.download", {"id": id})
        return resp.get("data", {})

    # ------------------------------------------------------------------
    # List  (override — `filter` is mandatory for files.list)
    # ------------------------------------------------------------------

    def list(  # type: ignore[override]
        self,
        filter: dict[str, Any],
        *,
        page: int = 1,
        page_size: int = DEFAULT_PAGE_SIZE,
        sort: list[dict[str, Any]] | None = None,
    ) -> Page[File]:
        """Return a page of files matching *filter*.

        Calls ``files.list``.  Unlike other resources, a ``filter`` is
        **required** by the Teamleader API.

        Parameters
        ----------
        filter:
            Required filter dict.
            
            Examples::

                {"subject": {"type": "deal", "id": "<uuid>"}}
                {"subject": {"type": "contact", "id": "<uuid>"}}

        page:
            1-based page number.  Defaults to ``1``.
        page_size:
            Number of items per page.  Defaults to
            :data:`~teamleader.constants.DEFAULT_PAGE_SIZE` (20).
        sort:
            Optional sort specification, e.g.
            ``[{"field": "updated_at", "order": "desc"}]``.

        Returns
        -------
        Page[File]
            A :class:`~teamleader.resources.base.Page` supporting
            :attr:`~teamleader.resources.base.Page.has_next` and
            :meth:`~teamleader.resources.base.Page.next` for forward
            pagination.
        """
        extra: dict[str, Any] = {"filter": filter}
        if sort is not None:
            extra["sort"] = sort
        return super().list(page=page, page_size=page_size, **extra)

    # ------------------------------------------------------------------
    # Unsupported CrudResource operations
    # ------------------------------------------------------------------

    def create(self, **kwargs: Any) -> File:  # type: ignore[override]
        """Not supported — files have no ``files.add`` endpoint.

        Raises
        ------
        NotImplementedError
            Always.  Use :meth:`upload_content` to add a new file.
        """
        raise NotImplementedError(
            "FilesResource does not support create(). "
            "Use upload_content() to upload a file."
        )

    def update(self, id: str, **kwargs: Any) -> File:  # type: ignore[override]
        """Not supported — files have no ``files.update`` endpoint.

        Raises
        ------
        NotImplementedError
            Always.
        """
        raise NotImplementedError(
            "FilesResource does not support update(). "
            "Files cannot be modified after upload."
        )

    def iterate(  # type: ignore[override]
        self, page_size: int = DEFAULT_PAGE_SIZE, **filters: Any
    ) -> Iterator[File]:
        """Not supported — ``files.list`` requires an explicit *filter* dict.

        Raises
        ------
        NotImplementedError
            Always.  Loop over :meth:`list` pages manually instead::

                page = client.files.list(filter={"subject": {...}})
                while True:
                    for f in page.data:
                        process(f)
                    if not page.has_next:
                        break
                    page = page.next()
        """
        raise NotImplementedError(
            "FilesResource does not support iterate(). "
            "Use list() with an explicit filter= argument and paginate via Page.next()."
        )
