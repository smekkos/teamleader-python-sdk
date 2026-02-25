"""Integration tests for CompaniesResource and the Company model.

Skipped automatically when TEAMLEADER_INTEGRATION_CLIENT_ID is not set.
"""

from __future__ import annotations

import pytest

from teamleader.client import TeamleaderClient
from teamleader.models.common import CustomField
from teamleader.models.company import Company
from teamleader.resources.base import Page


def _first_or_skip(page: Page, resource_name: str = "companies"):
    if not page.data:
        pytest.skip(f"No {resource_name} in sandbox account — read-only test skipped")
    return page.data[0]


class TestCompaniesListAndGet:
    def test_list_returns_page_of_company_instances(
        self, integration_client: TeamleaderClient
    ) -> None:
        page = integration_client.companies.list(page=1, page_size=5)
        assert isinstance(page, Page)
        _first_or_skip(page)
        for item in page.data:
            assert isinstance(item, Company)

    def test_company_has_non_empty_id(
        self, integration_client: TeamleaderClient
    ) -> None:
        page = integration_client.companies.list(page=1, page_size=1)
        company = _first_or_skip(page)
        assert company.id != ""

    def test_company_name_is_non_empty_string(
        self, integration_client: TeamleaderClient
    ) -> None:
        page = integration_client.companies.list(page=1, page_size=1)
        company = _first_or_skip(page)
        assert isinstance(company.name, str)
        assert company.name.strip() != ""

    def test_company_status_is_valid_enum_value(
        self, integration_client: TeamleaderClient
    ) -> None:
        page = integration_client.companies.list(page=1, page_size=5)
        company = _first_or_skip(page)
        assert company.status in {"active", "deactivated"}

    def test_is_active_matches_status_field(
        self, integration_client: TeamleaderClient
    ) -> None:
        page = integration_client.companies.list(page=1, page_size=5)
        company = _first_or_skip(page)
        assert company.is_active == (company.status == "active")

    def test_get_returns_company_with_matching_id(
        self, integration_client: TeamleaderClient
    ) -> None:
        page = integration_client.companies.list(page=1, page_size=1)
        first = _first_or_skip(page)
        fetched = integration_client.companies.get(first.id)
        assert isinstance(fetched, Company)
        assert fetched.id == first.id

    def test_iterate_yields_company_instances(
        self, integration_client: TeamleaderClient
    ) -> None:
        from itertools import islice
        companies = list(islice(integration_client.companies.iterate(page_size=20), 20))
        if not companies:
            pytest.skip("No companies in sandbox account")
        assert all(isinstance(c, Company) for c in companies)

    def test_primary_email_returns_string_or_none(
        self, integration_client: TeamleaderClient
    ) -> None:
        page = integration_client.companies.list(page=1, page_size=5)
        company = _first_or_skip(page)
        result = company.primary_email
        assert result is None or isinstance(result, str)

    def test_custom_fields_deserialise_with_non_empty_id(
        self, integration_client: TeamleaderClient
    ) -> None:
        page = integration_client.companies.list(page=1, page_size=20)
        for company in page.data:
            if company.custom_fields:
                cf = company.custom_fields[0]
                assert isinstance(cf, CustomField)
                assert cf.id != ""
                return
        pytest.skip("No company with custom_fields found in first page")


class TestCompaniesMutations:
    def test_tag_untag_cycle(self, integration_client: TeamleaderClient) -> None:
        """Create a company, tag it, untag it, then delete."""
        company = integration_client.companies.create(name="SDK Test Company Tag Cycle")
        try:
            integration_client.companies.tag(company.id, ["tl_sdk_test"])
            refreshed = integration_client.companies.get(company.id)
            assert "tl_sdk_test" in refreshed.tags

            integration_client.companies.untag(company.id, ["tl_sdk_test"])
            refreshed = integration_client.companies.get(company.id)
            assert "tl_sdk_test" not in refreshed.tags
        finally:
            integration_client.companies.delete(company.id)
