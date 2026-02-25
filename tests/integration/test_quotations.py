"""Integration tests for QuotationsResource and the Quotation model.

Skipped automatically when TEAMLEADER_INTEGRATION_CLIENT_ID is not set.

All tests are read-only.  Sending and accepting quotations are intentionally
excluded as they mutate deal state in ways that are difficult to reverse.
"""

from __future__ import annotations

import pytest

from teamleader.client import TeamleaderClient
from teamleader.models.common import Money
from teamleader.models.quotation import Quotation
from teamleader.resources.base import Page


def _first_or_skip(page: Page, resource_name: str = "quotations"):
    if not page.data:
        pytest.skip(f"No {resource_name} in sandbox account — read-only test skipped")
    return page.data[0]


class TestQuotationsListAndGet:
    def test_list_returns_page_of_quotation_instances(
        self, integration_client: TeamleaderClient
    ) -> None:
        page = integration_client.quotations.list(page=1, page_size=5)
        assert isinstance(page, Page)
        _first_or_skip(page)
        for item in page.data:
            assert isinstance(item, Quotation)

    def test_quotation_has_non_empty_id(
        self, integration_client: TeamleaderClient
    ) -> None:
        page = integration_client.quotations.list(page=1, page_size=1)
        q = _first_or_skip(page)
        assert q.id != ""

    def test_quotation_status_is_valid_enum_value(
        self, integration_client: TeamleaderClient
    ) -> None:
        page = integration_client.quotations.list(page=1, page_size=5)
        q = _first_or_skip(page)
        assert q.status in {"open", "accepted", "expired", "rejected", "closed"}

    def test_computed_status_properties_match_status_field(
        self, integration_client: TeamleaderClient
    ) -> None:
        page = integration_client.quotations.list(page=1, page_size=10)
        _first_or_skip(page)
        for q in page.data:
            assert q.is_open == (q.status == "open")
            assert q.is_accepted == (q.status == "accepted")
            assert q.is_expired == (q.status == "expired")

    def test_get_returns_quotation_with_matching_id(
        self, integration_client: TeamleaderClient
    ) -> None:
        page = integration_client.quotations.list(page=1, page_size=1)
        first = _first_or_skip(page)
        fetched = integration_client.quotations.get(first.id)
        assert isinstance(fetched, Quotation)
        assert fetched.id == first.id

    def test_total_tax_exclusive_is_money_or_none(
        self, integration_client: TeamleaderClient
    ) -> None:
        """total_tax_exclusive must never raise — returns Money or None."""
        page = integration_client.quotations.list(page=1, page_size=10)
        for q in page.data:
            te = q.total_tax_exclusive
            assert te is None or isinstance(te, Money)
            if isinstance(te, Money):
                assert te.currency != ""
                return
        pytest.skip("No quotation with total.tax_exclusive found in first page")

    def test_total_tax_inclusive_is_money_or_none(
        self, integration_client: TeamleaderClient
    ) -> None:
        page = integration_client.quotations.list(page=1, page_size=10)
        for q in page.data:
            ti = q.total_tax_inclusive
            assert ti is None or isinstance(ti, Money)
        # If we get here without skipping, the property never raised — that's the test.
