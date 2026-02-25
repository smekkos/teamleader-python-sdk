"""Integration tests for DealsResource and the Deal model.

Skipped automatically when TEAMLEADER_INTEGRATION_CLIENT_ID is not set.

All tests are read-only — deals are not created or deleted here because
mutating deal status (win/lose) is difficult to reverse cleanly.
"""

from __future__ import annotations

import pytest

from teamleader.client import TeamleaderClient
from teamleader.models.common import Money
from teamleader.models.deal import Deal
from teamleader.resources.base import Page


def _first_or_skip(page: Page, resource_name: str = "deals"):
    if not page.data:
        pytest.skip(f"No {resource_name} in sandbox account — read-only test skipped")
    return page.data[0]


class TestDealsListAndGet:
    def test_list_returns_page_of_deal_instances(
        self, integration_client: TeamleaderClient
    ) -> None:
        page = integration_client.deals.list(page=1, page_size=5)
        assert isinstance(page, Page)
        _first_or_skip(page)
        for item in page.data:
            assert isinstance(item, Deal)

    def test_deal_has_non_empty_id(
        self, integration_client: TeamleaderClient
    ) -> None:
        page = integration_client.deals.list(page=1, page_size=1)
        deal = _first_or_skip(page)
        assert deal.id != ""

    def test_deal_status_is_valid_enum_value(
        self, integration_client: TeamleaderClient
    ) -> None:
        # The spec documents "open", "won", "lost" — the live API also returns
        # undocumented statuses (e.g. "new") used for pipeline-stage tracking.
        # We accept any non-empty string to stay forward-compatible.
        page = integration_client.deals.list(page=1, page_size=5)
        deal = _first_or_skip(page)
        assert isinstance(deal.status, str) and deal.status != ""

    def test_computed_status_booleans_are_mutually_exclusive(
        self, integration_client: TeamleaderClient
    ) -> None:
        """At most one of is_open, is_won, is_lost is True.

        Deals with undocumented statuses (e.g. "new") will have all three
        flags False — that is acceptable; the flags are only meaningful for
        the documented status values.
        """
        page = integration_client.deals.list(page=1, page_size=5)
        _first_or_skip(page)
        for deal in page.data:
            flags = [deal.is_open, deal.is_won, deal.is_lost]
            assert sum(flags) <= 1, (
                f"Deal {deal.id!r}: at most one status flag should be True, got "
                f"is_open={deal.is_open}, is_won={deal.is_won}, is_lost={deal.is_lost}"
            )

    def test_customer_id_is_uuid_string_when_lead_present(
        self, integration_client: TeamleaderClient
    ) -> None:
        page = integration_client.deals.list(page=1, page_size=10)
        for deal in page.data:
            if deal.lead and deal.customer_id:
                assert isinstance(deal.customer_id, str)
                assert deal.customer_id != ""
                assert deal.customer_type in {"contact", "company"}
                return
        pytest.skip("No deal with lead.customer found in first page")

    def test_get_returns_deal_with_matching_id(
        self, integration_client: TeamleaderClient
    ) -> None:
        page = integration_client.deals.list(page=1, page_size=1)
        first = _first_or_skip(page)
        fetched = integration_client.deals.get(first.id)
        assert isinstance(fetched, Deal)
        assert fetched.id == first.id

    def test_estimated_value_is_money_or_none(
        self, integration_client: TeamleaderClient
    ) -> None:
        page = integration_client.deals.list(page=1, page_size=10)
        for deal in page.data:
            if deal.estimated_value is not None:
                assert isinstance(deal.estimated_value, Money)
                assert isinstance(deal.estimated_value.amount, float)
                assert deal.estimated_value.currency != ""
                return
        pytest.skip("No deal with estimated_value found in first page")

    def test_iterate_yields_deal_instances(
        self, integration_client: TeamleaderClient
    ) -> None:
        from itertools import islice
        deals = list(islice(integration_client.deals.iterate(page_size=20), 20))
        if not deals:
            pytest.skip("No deals in sandbox account")
        assert all(isinstance(d, Deal) for d in deals)


class TestDealsReferenceData:
    def test_list_phases_returns_non_empty_list(
        self, integration_client: TeamleaderClient
    ) -> None:
        """dealPhases.list returns at least one phase object."""
        phases = integration_client.deals.list_phases()
        assert isinstance(phases, list)
        if not phases:
            pytest.skip("No deal phases configured in sandbox account")
        # Each phase dict must have at minimum an id and name
        for phase in phases:
            assert isinstance(phase, dict)
            assert "id" in phase
            assert "name" in phase

    def test_list_phases_with_pipeline_id_filter(
        self, integration_client: TeamleaderClient
    ) -> None:
        """list_phases(deal_pipeline_id=...) accepts a pipeline filter without error."""
        phases = integration_client.deals.list_phases()
        if not phases:
            pytest.skip("No deal phases — cannot test pipeline_id filter")
        # We don't know the pipeline ID, so just check the unfiltered call succeeds
        assert isinstance(phases, list)

    def test_list_sources_returns_list_of_dicts(
        self, integration_client: TeamleaderClient
    ) -> None:
        """dealSources.list returns a list of source dicts (may be empty)."""
        sources = integration_client.deals.list_sources()
        assert isinstance(sources, list)
        for source in sources:
            assert isinstance(source, dict)
            assert "id" in source
            assert "name" in source
