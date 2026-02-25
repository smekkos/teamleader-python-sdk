"""Integration tests for ContactsResource and the Contact model.

Skipped automatically when TEAMLEADER_INTEGRATION_CLIENT_ID is not set.

Read-only tests use whatever contacts exist in the sandbox account.
Write tests follow a create → assert → delete pattern with try/finally
cleanup so no dangling test data is left behind.
"""

from __future__ import annotations

import pytest

from teamleader.client import TeamleaderClient
from teamleader.models.common import AddressEntry, CustomField, Money
from teamleader.models.contact import Contact
from teamleader.resources.base import Page


# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------


def _first_or_skip(page: Page, resource_name: str = "contacts"):
    """Return page.data[0] or skip the test if the sandbox has no data."""
    if not page.data:
        pytest.skip(f"No {resource_name} in sandbox account — read-only test skipped")
    return page.data[0]


# ---------------------------------------------------------------------------
# Read-only tests
# ---------------------------------------------------------------------------


class TestContactsListAndGet:
    def test_list_returns_page_of_contact_instances(
        self, integration_client: TeamleaderClient
    ) -> None:
        """list() returns a Page whose items are Contact dataclass instances."""
        page = integration_client.contacts.list(page=1, page_size=5)
        assert isinstance(page, Page)
        _first_or_skip(page)
        for item in page.data:
            assert isinstance(item, Contact)

    def test_contact_has_non_empty_id(
        self, integration_client: TeamleaderClient
    ) -> None:
        page = integration_client.contacts.list(page=1, page_size=1)
        contact = _first_or_skip(page)
        assert contact.id != ""

    def test_contact_status_is_valid_enum_value(
        self, integration_client: TeamleaderClient
    ) -> None:
        """API status field maps to one of the known enum values."""
        page = integration_client.contacts.list(page=1, page_size=5)
        contact = _first_or_skip(page)
        assert contact.status in {"active", "deactivated"}

    def test_is_active_matches_status_field(
        self, integration_client: TeamleaderClient
    ) -> None:
        page = integration_client.contacts.list(page=1, page_size=5)
        contact = _first_or_skip(page)
        assert contact.is_active == (contact.status == "active")

    def test_full_name_is_non_empty_string(
        self, integration_client: TeamleaderClient
    ) -> None:
        page = integration_client.contacts.list(page=1, page_size=5)
        contact = _first_or_skip(page)
        assert isinstance(contact.full_name, str)
        assert contact.full_name.strip() != ""

    def test_primary_email_returns_string_or_none(
        self, integration_client: TeamleaderClient
    ) -> None:
        """primary_email must never raise — returns str or None."""
        page = integration_client.contacts.list(page=1, page_size=5)
        contact = _first_or_skip(page)
        result = contact.primary_email
        assert result is None or isinstance(result, str)

    def test_primary_email_prefers_primary_type(
        self, integration_client: TeamleaderClient
    ) -> None:
        """When a primary-typed email exists, primary_email returns its address."""
        page = integration_client.contacts.list(page=1, page_size=20)
        # Find a contact that has a primary-typed email
        for contact in page.data:
            primary = [e for e in contact.emails if e.type == "primary"]
            if primary:
                assert contact.primary_email == primary[0].email
                return
        pytest.skip("No contact with type='primary' email found in first page")

    def test_get_returns_contact_with_matching_id(
        self, integration_client: TeamleaderClient
    ) -> None:
        page = integration_client.contacts.list(page=1, page_size=1)
        first = _first_or_skip(page)
        fetched = integration_client.contacts.get(first.id)
        assert isinstance(fetched, Contact)
        assert fetched.id == first.id

    def test_addresses_deserialise_to_address_entry_instances(
        self, integration_client: TeamleaderClient
    ) -> None:
        """AddressEntry objects should be returned, not raw dicts."""
        page = integration_client.contacts.list(page=1, page_size=20)
        for contact in page.data:
            if contact.addresses:
                entry = contact.addresses[0]
                assert isinstance(entry, AddressEntry)
                # type must be a string (e.g. "primary", "invoicing")
                if entry.type is not None:
                    assert isinstance(entry.type, str)
                return
        pytest.skip("No contact with addresses found in first page")

    def test_custom_fields_deserialise_with_non_empty_id(
        self, integration_client: TeamleaderClient
    ) -> None:
        page = integration_client.contacts.list(page=1, page_size=20)
        for contact in page.data:
            if contact.custom_fields:
                cf = contact.custom_fields[0]
                assert isinstance(cf, CustomField)
                assert cf.id != ""
                return
        pytest.skip("No contact with custom_fields found in first page")

    def test_iterate_yields_at_least_one_contact(
        self, integration_client: TeamleaderClient
    ) -> None:
        # islice caps consumption to one page — avoids hundreds of API calls
        # and rate-limit errors on accounts with large contact lists.
        from itertools import islice
        contacts = list(islice(integration_client.contacts.iterate(page_size=20), 20))
        if not contacts:
            pytest.skip("No contacts in sandbox account")
        assert all(isinstance(c, Contact) for c in contacts)


# ---------------------------------------------------------------------------
# Write tests — create → assert → delete with try/finally cleanup
# ---------------------------------------------------------------------------


class TestContactsMutations:
    def test_tag_untag_cycle(self, integration_client: TeamleaderClient) -> None:
        """Create a contact, tag it, untag it, then delete."""
        contact = integration_client.contacts.create(
            first_name="SDK",
            last_name="TestContact",
            emails=[{"type": "primary", "email": "sdk.test.contact@example.invalid"}],
        )
        try:
            integration_client.contacts.tag(contact.id, ["tl_sdk_test"])
            refreshed = integration_client.contacts.get(contact.id)
            assert "tl_sdk_test" in refreshed.tags

            integration_client.contacts.untag(contact.id, ["tl_sdk_test"])
            refreshed = integration_client.contacts.get(contact.id)
            assert "tl_sdk_test" not in refreshed.tags
        finally:
            integration_client.contacts.delete(contact.id)

    def test_link_unlink_company_cycle(
        self, integration_client: TeamleaderClient
    ) -> None:
        """Create a contact and a company, link them, unlink, then delete both."""
        contact = integration_client.contacts.create(
            first_name="SDK",
            last_name="LinkedContact",
            emails=[{"type": "primary", "email": "sdk.linked@example.invalid"}],
        )
        company = integration_client.companies.create(name="SDK Test Company")
        try:
            integration_client.contacts.link_to_company(
                contact.id, company.id, position="Tester"
            )
            refreshed = integration_client.contacts.get(contact.id)
            linked_ids = [c["company"]["id"] for c in refreshed.companies]
            assert company.id in linked_ids

            integration_client.contacts.unlink_from_company(contact.id, company.id)
            refreshed = integration_client.contacts.get(contact.id)
            linked_ids = [c["company"]["id"] for c in refreshed.companies]
            assert company.id not in linked_ids
        finally:
            integration_client.contacts.delete(contact.id)
            integration_client.companies.delete(company.id)
