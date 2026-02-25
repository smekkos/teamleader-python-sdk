"""Integration tests for InvoicesResource and the Invoice model.

Skipped automatically when TEAMLEADER_INTEGRATION_CLIENT_ID is not set.

All tests are read-only.  Write operations (book, credit, register_payment,
send) are too high-impact to run against a sandbox without explicit manual
setup, so they are not included here.
"""

from __future__ import annotations

import pytest

from teamleader.client import TeamleaderClient
from teamleader.models.common import Money
from teamleader.models.invoice import Invoice
from teamleader.resources.base import Page


def _first_or_skip(page: Page, resource_name: str = "invoices"):
    if not page.data:
        pytest.skip(f"No {resource_name} in sandbox account — read-only test skipped")
    return page.data[0]


class TestInvoicesListAndGet:
    def test_list_returns_page_of_invoice_instances(
        self, integration_client: TeamleaderClient
    ) -> None:
        page = integration_client.invoices.list(page=1, page_size=5)
        assert isinstance(page, Page)
        _first_or_skip(page)
        for item in page.data:
            assert isinstance(item, Invoice)

    def test_invoice_has_non_empty_id(
        self, integration_client: TeamleaderClient
    ) -> None:
        page = integration_client.invoices.list(page=1, page_size=1)
        invoice = _first_or_skip(page)
        assert invoice.id != ""

    def test_invoice_status_is_valid_enum_value(
        self, integration_client: TeamleaderClient
    ) -> None:
        page = integration_client.invoices.list(page=1, page_size=5)
        invoice = _first_or_skip(page)
        assert invoice.status in {"draft", "outstanding", "matched"}

    def test_is_paid_matches_paid_field(
        self, integration_client: TeamleaderClient
    ) -> None:
        page = integration_client.invoices.list(page=1, page_size=5)
        _first_or_skip(page)
        for invoice in page.data:
            assert invoice.is_paid == invoice.paid

    def test_is_overdue_is_always_a_bool(
        self, integration_client: TeamleaderClient
    ) -> None:
        """is_overdue must never raise — it is always a bool."""
        page = integration_client.invoices.list(page=1, page_size=10)
        _first_or_skip(page)
        for invoice in page.data:
            result = invoice.is_overdue
            assert isinstance(result, bool)

    def test_is_draft_matches_status_field(
        self, integration_client: TeamleaderClient
    ) -> None:
        page = integration_client.invoices.list(page=1, page_size=5)
        _first_or_skip(page)
        for invoice in page.data:
            assert invoice.is_draft == (invoice.status == "draft")

    def test_total_due_is_money_or_none(
        self, integration_client: TeamleaderClient
    ) -> None:
        page = integration_client.invoices.list(page=1, page_size=10)
        for invoice in page.data:
            td = invoice.total_due
            assert td is None or isinstance(td, Money)
            if isinstance(td, Money):
                assert td.currency != ""
                return
        pytest.skip("No invoice with total.due found in first page")

    def test_customer_name_is_string_or_none(
        self, integration_client: TeamleaderClient
    ) -> None:
        """customer_name must never raise."""
        page = integration_client.invoices.list(page=1, page_size=10)
        _first_or_skip(page)
        for invoice in page.data:
            name = invoice.customer_name
            assert name is None or isinstance(name, str)

    def test_get_returns_invoice_with_matching_id(
        self, integration_client: TeamleaderClient
    ) -> None:
        page = integration_client.invoices.list(page=1, page_size=1)
        first = _first_or_skip(page)
        fetched = integration_client.invoices.get(first.id)
        assert isinstance(fetched, Invoice)
        assert fetched.id == first.id

    def test_download_returns_location_url(
        self, integration_client: TeamleaderClient
    ) -> None:
        """download() returns a dict with a 'location' key containing a URL string."""
        page = integration_client.invoices.list(page=1, page_size=5)
        # Only booked invoices can be downloaded — skip if only drafts
        booked = [inv for inv in page.data if inv.status != "draft"]
        if not booked:
            pytest.skip("No booked invoices in first page — download test skipped")
        result = integration_client.invoices.download(booked[0].id)
        assert isinstance(result, dict)
        assert "location" in result
        assert isinstance(result["location"], str)
        assert result["location"].startswith("http")
