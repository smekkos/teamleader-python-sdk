"""Deals resource — CRUD + extra actions."""

from __future__ import annotations

from typing import Any

from teamleader.models.deal import Deal
from teamleader.resources.base import CrudResource


class DealsResource(CrudResource[Deal]):
    """CRUD + extra actions for Teamleader deals.

    Inherits :meth:`list`, :meth:`get`, :meth:`create`, :meth:`update`,
    :meth:`delete`, and :meth:`iterate` from :class:`~teamleader.resources.base.CrudResource`.
    """

    prefix = "deals"
    model = Deal

    # ------------------------------------------------------------------
    # Status transitions
    # ------------------------------------------------------------------

    def move_to_phase(self, deal_id: str, phase_id: str) -> None:
        """Move a deal to a different pipeline phase.

        Calls ``deals.move``.

        Parameters
        ----------
        deal_id:
            UUID of the deal to move.
        phase_id:
            UUID of the target deal phase.
        """
        self._client._post("deals.move", {"id": deal_id, "phase_id": phase_id})

    def win(self, deal_id: str) -> None:
        """Mark a deal as won.

        Calls ``deals.win``.

        Parameters
        ----------
        deal_id:
            UUID of the deal to mark as won.
        """
        self._client._post("deals.win", {"id": deal_id})

    def lose(
        self,
        deal_id: str,
        *,
        reason_id: str | None = None,
        extra_info: str | None = None,
    ) -> None:
        """Mark a deal as lost.

        Calls ``deals.lose``.

        Parameters
        ----------
        deal_id:
            UUID of the deal to mark as lost.
        reason_id:
            Optional UUID of a configured lost-reason.
        extra_info:
            Optional free-text explanation (e.g. ``"Too expensive"``).
        """
        body: dict[str, Any] = {"id": deal_id}
        if reason_id is not None:
            body["reason_id"] = reason_id
        if extra_info is not None:
            body["extra_info"] = extra_info
        self._client._post("deals.lose", body)

    # ------------------------------------------------------------------
    # Reference data
    # ------------------------------------------------------------------

    def list_phases(
        self,
        *,
        deal_pipeline_id: str | None = None,
        ids: list[str] | None = None,
    ) -> list[dict[str, Any]]:
        """Return all deal phases from the ``dealPhases.list`` endpoint.

        Parameters
        ----------
        deal_pipeline_id:
            Optional UUID — filter phases to a specific pipeline.
        ids:
            Optional list of phase UUIDs to retrieve.

        Returns
        -------
        list[dict]
            Raw phase dicts as returned by the API (``id``, ``name``,
            ``actions``, ``expected_duration_in_days``).
        """
        body: dict[str, Any] = {}
        filter_: dict[str, Any] = {}
        if deal_pipeline_id is not None:
            filter_["deal_pipeline_id"] = deal_pipeline_id
        if ids is not None:
            filter_["ids"] = ids
        if filter_:
            body["filter"] = filter_
        resp = self._client._post("dealPhases.list", body)
        return resp.get("data", [])

    def list_sources(
        self,
        *,
        ids: list[str] | None = None,
    ) -> list[dict[str, Any]]:
        """Return all deal sources from the ``dealSources.list`` endpoint.

        Parameters
        ----------
        ids:
            Optional list of source UUIDs to filter by.

        Returns
        -------
        list[dict]
            Raw source dicts as returned by the API (``id``, ``name``).
        """
        body: dict[str, Any] = {}
        if ids is not None:
            body["filter"] = {"ids": ids}
        resp = self._client._post("dealSources.list", body)
        return resp.get("data", [])
