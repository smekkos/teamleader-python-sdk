"""Unit tests for curated model classes — Phase 8.

Covers:
- ``from_api()`` round-trips for every model (bare dict + wrapped ``{"data": {...}}``)
- Computed properties: full_name, primary_email, primary_phone, is_active,
  is_open / is_won / is_lost, is_overdue / is_paid / is_draft, customer_id,
  customer_name, total_due, total_tax_exclusive / total_tax_inclusive
- ``to_dict()`` shape and optional-field omission
- Common sub-models: TypeAndId, Address, AddressEntry, Email, Telephone,
  Money, CustomField, PaymentTerm, WebLink
"""

from __future__ import annotations

import datetime

import pytest
from freezegun import freeze_time

from teamleader.models import (
    Address,
    AddressEntry,
    Company,
    Contact,
    CustomField,
    Deal,
    Email,
    Invoice,
    Money,
    PaymentTerm,
    Quotation,
    Telephone,
    TypeAndId,
    WebLink,
)

# ---------------------------------------------------------------------------
# Shared sample payloads (trimmed to fields touched by from_api)
# ---------------------------------------------------------------------------

CONTACT_DATA = {
    "id": "cde0bc5f-8602-4e12-b5d3-f03436b54c0d",
    "first_name": "Erlich",
    "last_name": "Bachman",
    "status": "active",
    "salutation": "Mr",
    "vat_number": "BE0899623034",
    "emails": [{"type": "primary", "email": "info@piedpiper.eu"}],
    "telephones": [{"type": "phone", "number": "092980615"}],
    "website": "https://piedpiper.com",
    "addresses": [
        {
            "type": "invoicing",
            "address": {
                "addressee": "Teamleader HQ",
                "line_1": "Dok Noord 3A 101",
                "postal_code": "9000",
                "city": "Ghent",
                "country": "BE",
            },
        }
    ],
    "gender": "male",
    "birthdate": "1987-04-25",
    "iban": "BE12123412341234",
    "bic": "BICBANK",
    "national_identification_number": "00051730-A",
    "companies": [{"position": "Developer", "company": {"type": "company", "id": "abc"}}],
    "language": "en",
    "payment_term": {"type": "after_invoice_date", "days": 30},
    "remarks": "First contact at expo",
    "tags": ["vip", "partner"],
    "custom_fields": [{"definition": {"type": "customFieldDefinition", "id": "cf-1"}, "value": "foo"}],
    "marketing_mails_consent": False,
    "added_at": "2016-02-04T16:44:33+00:00",
    "updated_at": "2016-02-05T16:44:33+00:00",
    "web_url": "https://focus.teamleader.eu/contact_detail.php?id=cde0bc5f",
}

COMPANY_DATA = {
    "id": "e8d31ae7-8258-4fcd-9b2d-78f41b0aa5d5",
    "name": "Pied Piper",
    "status": "active",
    "business_type": {"type": "businessType", "id": "fd48d4a3-b9dc-4eac-8071-5889c9f21e5d"},
    "vat_number": "BE0899623035",
    "national_identification_number": "63326426",
    "emails": [
        {"type": "primary", "email": "info@piedpiper.eu"},
        {"type": "invoicing", "email": "billing@piedpiper.eu"},
    ],
    "telephones": [{"type": "phone", "number": "092980615"}],
    "website": "https://piedpiper.com",
    "addresses": [],
    "iban": "BE12123412341234",
    "bic": "BICBANK",
    "language": "nl",
    "preferred_currency": "EUR",
    "payment_term": {"type": "end_of_month"},
    "responsible_user": {"type": "user", "id": "user-1"},
    "tags": ["customer"],
    "custom_fields": [],
    "marketing_mails_consent": True,
    "added_at": "2016-02-04T16:44:33+00:00",
    "updated_at": "2016-02-05T16:44:33+00:00",
    "web_url": "https://focus.teamleader.eu/company_detail.php?id=e8d31ae7",
    "related_companies": [{"type": "company", "id": "rel-1"}],
    "related_contacts": [{"type": "contact", "id": "rel-2"}],
}

DEAL_DATA = {
    "id": "f6871b06-6513-4750-b5e6-ff3503b5a029",
    "title": "Interesting deal",
    "summary": "Additional information",
    "reference": "2017/2",
    "status": "won",
    "lead": {
        "customer": {"type": "company", "id": "2659dc4d-444b-4ced-b51c-b87591f604d7"},
        "contact_person": {"type": "contact", "id": "74c6769e-815a-4774-87d7-dfab9b1a0abb"},
    },
    "department": {"type": "department", "id": "dept-1"},
    "estimated_value": {"amount": 123.3, "currency": "EUR"},
    "estimated_closing_date": "2017-05-09",
    "estimated_probability": 0.5,
    "weighted_value": {"amount": 61.65, "currency": "EUR"},
    "purchase_order_number": "000023",
    "current_phase": {"type": "dealPhase", "id": "phase-1"},
    "responsible_user": {"type": "user", "id": "user-1"},
    "closed_at": "2017-05-09T11:31:30+00:00",
    "source": {"type": "dealSource", "id": "source-1"},
    "phase_history": [],
    "quotations": [{"type": "quotation", "id": "quot-1"}],
    "lost_reason": None,
    "pipeline": {"type": "dealPipeline", "id": "pipe-1"},
    "custom_fields": [],
    "created_at": "2017-05-09T11:25:11+00:00",
    "updated_at": "2017-05-09T11:30:58+00:00",
    "web_url": "https://focus.teamleader.eu/sale_detail.php?id=f6871b06",
}

INVOICE_DATA = {
    "id": "e540fe7e-dce2-459e-bf7e-24e605fc18b3",
    "department": {"type": "department", "id": "dept-1"},
    "invoice_number": "2017 / 5",
    "invoice_date": "2016-02-04",
    "status": "outstanding",
    "due_on": "2016-03-03",
    "paid": False,
    "paid_at": None,
    "sent": True,
    "purchase_order_number": "000023",
    "invoicee": {"name": "De Rode Duivels", "vat_number": "BE0899623035"},
    "discounts": [],
    "grouped_lines": [],
    "total": {
        "tax_exclusive": {"amount": 100.0, "currency": "EUR"},
        "tax_inclusive": {"amount": 121.0, "currency": "EUR"},
        "due": {"amount": 121.0, "currency": "EUR"},
    },
    "payment_term": {"type": "after_invoice_date", "days": 30},
    "payments": [],
    "payment_reference": "+++084/2613/66074+++",
    "note": "Some extra remarks",
    "currency": "EUR",
    "currency_exchange_rate": None,
    "deal": {"type": "deal", "id": "deal-1"},
    "custom_fields": [],
    "created_at": "2016-02-04T16:44:33+00:00",
    "updated_at": "2016-02-05T16:44:33+00:00",
    "delivery_date": "2025-12-08",
}

QUOTATION_DATA = {
    "id": "e7a3fe2b-2c75-480f-87b9-121816b5257b",
    "deal": {"type": "deal", "id": "deal-1"},
    "grouped_lines": [],
    "currency": "EUR",
    "currency_exchange_rate": None,
    "text": "Quotation text",
    "total": {
        "tax_exclusive": {"amount": 100.0, "currency": "EUR"},
        "tax_inclusive": {"amount": 121.0, "currency": "EUR"},
    },
    "discounts": [],
    "status": "open",
    "name": "Webdevelopment",
    "document_template": {"type": "documentTemplate", "id": "tmpl-1"},
    "custom_fields": [],
    "created_at": "2017-05-09T11:25:11+00:00",
    "updated_at": "2017-05-09T11:30:58+00:00",
}


# ===========================================================================
# Common sub-models
# ===========================================================================


class TestTypeAndId:
    def test_from_api_basic(self):
        obj = TypeAndId.from_api({"id": "abc", "type": "deal"})
        assert obj.id == "abc"
        assert obj.type == "deal"

    def test_from_api_missing_fields(self):
        obj = TypeAndId.from_api({})
        assert obj.id == ""
        assert obj.type == ""

    def test_to_dict_roundtrip(self):
        obj = TypeAndId(id="abc", type="deal")
        assert obj.to_dict() == {"id": "abc", "type": "deal"}


class TestAddress:
    def test_from_api_full(self):
        data = {
            "line_1": "Dok Noord 3A 101",
            "postal_code": "9000",
            "city": "Ghent",
            "country": "BE",
            "area_level_two": {"id": "area-1", "type": "areaLevelTwo"},
        }
        addr = Address.from_api(data)
        assert addr.line_1 == "Dok Noord 3A 101"
        assert addr.postal_code == "9000"
        assert addr.city == "Ghent"
        assert addr.country == "BE"
        assert addr.area_level_two == {"id": "area-1", "type": "areaLevelTwo"}

    def test_from_api_minimal(self):
        addr = Address.from_api({"country": "BE"})
        assert addr.country == "BE"
        assert addr.line_1 is None
        assert addr.area_level_two is None

    def test_to_dict_excludes_none(self):
        addr = Address(city="Ghent", country="BE")
        d = addr.to_dict()
        assert "city" in d
        assert "country" in d
        assert "line_1" not in d
        assert "postal_code" not in d


class TestAddressEntry:
    def test_from_api_full(self):
        data = {
            "type": "invoicing",
            "address": {
                "addressee": "Teamleader HQ",
                "line_1": "Dok Noord 3A 101",
                "city": "Ghent",
                "country": "BE",
            },
        }
        entry = AddressEntry.from_api(data)
        assert entry.type == "invoicing"
        assert entry.addressee == "Teamleader HQ"
        assert entry.address is not None
        assert entry.address.city == "Ghent"

    def test_from_api_addressee_extracted(self):
        """addressee lives inside the nested address dict in the API response."""
        data = {"type": "primary", "address": {"addressee": "HQ", "country": "BE"}}
        entry = AddressEntry.from_api(data)
        assert entry.addressee == "HQ"
        assert entry.address.country == "BE"

    def test_to_dict_merges_addressee(self):
        entry = AddressEntry(
            type="primary",
            address=Address(city="Ghent", country="BE"),
            addressee="HQ",
        )
        d = entry.to_dict()
        assert d["type"] == "primary"
        assert d["address"]["city"] == "Ghent"
        assert d["address"]["addressee"] == "HQ"

    def test_to_dict_empty_address(self):
        entry = AddressEntry(type="primary")
        d = entry.to_dict()
        assert "address" not in d  # no address dict emitted when Address is None


class TestEmail:
    def test_from_api(self):
        e = Email.from_api({"email": "a@b.com", "type": "primary"})
        assert e.email == "a@b.com"
        assert e.type == "primary"

    def test_to_dict_with_type(self):
        assert Email(email="a@b.com", type="invoicing").to_dict() == {
            "email": "a@b.com",
            "type": "invoicing",
        }

    def test_to_dict_without_type(self):
        d = Email(email="a@b.com").to_dict()
        assert "type" not in d


class TestTelephone:
    def test_from_api(self):
        t = Telephone.from_api({"number": "0123456789", "type": "mobile"})
        assert t.number == "0123456789"
        assert t.type == "mobile"

    def test_to_dict_with_type(self):
        assert Telephone(number="0123", type="fax").to_dict() == {
            "number": "0123",
            "type": "fax",
        }

    def test_to_dict_without_type(self):
        d = Telephone(number="0123").to_dict()
        assert "type" not in d


class TestMoney:
    def test_from_api(self):
        m = Money.from_api({"amount": 123.3, "currency": "EUR"})
        assert m.amount == 123.3
        assert m.currency == "EUR"

    def test_to_dict(self):
        assert Money(amount=99.5, currency="USD").to_dict() == {
            "amount": 99.5,
            "currency": "USD",
        }


class TestCustomField:
    def test_from_api_flattens_definition_id(self):
        cf = CustomField.from_api(
            {"definition": {"type": "customFieldDefinition", "id": "cf-1"}, "value": "foo"}
        )
        assert cf.id == "cf-1"
        assert cf.value == "foo"
        assert cf.definition["type"] == "customFieldDefinition"

    def test_from_api_no_definition(self):
        cf = CustomField.from_api({"value": 42})
        assert cf.id == ""
        assert cf.value == 42

    def test_to_dict_uses_definition(self):
        cf = CustomField(id="cf-1", value="bar", definition={"type": "customFieldDefinition", "id": "cf-1"})
        d = cf.to_dict()
        assert d["definition"]["id"] == "cf-1"
        assert d["value"] == "bar"

    def test_to_dict_falls_back_to_id(self):
        """When definition dict is empty, to_dict builds one from the id."""
        cf = CustomField(id="cf-2", value=5)
        d = cf.to_dict()
        assert d["definition"]["id"] == "cf-2"


class TestPaymentTerm:
    def test_from_api_with_days(self):
        pt = PaymentTerm.from_api({"type": "after_invoice_date", "days": 30})
        assert pt.type == "after_invoice_date"
        assert pt.days == 30

    def test_from_api_cash_no_days(self):
        pt = PaymentTerm.from_api({"type": "cash"})
        assert pt.type == "cash"
        assert pt.days is None

    def test_to_dict_with_days(self):
        assert PaymentTerm(type="after_invoice_date", days=30).to_dict() == {
            "type": "after_invoice_date",
            "days": 30,
        }

    def test_to_dict_without_days(self):
        d = PaymentTerm(type="cash").to_dict()
        assert "days" not in d


class TestWebLink:
    def test_from_api(self):
        wl = WebLink.from_api({"url": "https://example.com", "type": "website"})
        assert wl.url == "https://example.com"
        assert wl.type == "website"

    def test_to_dict_without_type(self):
        d = WebLink(url="https://example.com").to_dict()
        assert d == {"url": "https://example.com"}


# ===========================================================================
# Contact
# ===========================================================================


class TestContactFromApi:
    def test_bare_dict(self):
        c = Contact.from_api(CONTACT_DATA)
        assert c.id == "cde0bc5f-8602-4e12-b5d3-f03436b54c0d"
        assert c.first_name == "Erlich"
        assert c.last_name == "Bachman"
        assert c.status == "active"
        assert c.salutation == "Mr"
        assert c.vat_number == "BE0899623034"

    def test_wrapped_dict(self):
        c = Contact.from_api({"data": CONTACT_DATA})
        assert c.id == "cde0bc5f-8602-4e12-b5d3-f03436b54c0d"

    def test_emails_deserialised(self):
        c = Contact.from_api(CONTACT_DATA)
        assert len(c.emails) == 1
        assert isinstance(c.emails[0], Email)
        assert c.emails[0].email == "info@piedpiper.eu"

    def test_telephones_deserialised(self):
        c = Contact.from_api(CONTACT_DATA)
        assert len(c.telephones) == 1
        assert isinstance(c.telephones[0], Telephone)
        assert c.telephones[0].number == "092980615"

    def test_addresses_deserialised(self):
        c = Contact.from_api(CONTACT_DATA)
        assert len(c.addresses) == 1
        assert isinstance(c.addresses[0], AddressEntry)
        assert c.addresses[0].type == "invoicing"
        assert c.addresses[0].addressee == "Teamleader HQ"

    def test_payment_term_deserialised(self):
        c = Contact.from_api(CONTACT_DATA)
        assert isinstance(c.payment_term, PaymentTerm)
        assert c.payment_term.type == "after_invoice_date"
        assert c.payment_term.days == 30

    def test_custom_fields_deserialised(self):
        c = Contact.from_api(CONTACT_DATA)
        assert len(c.custom_fields) == 1
        assert isinstance(c.custom_fields[0], CustomField)
        assert c.custom_fields[0].id == "cf-1"

    def test_tags(self):
        c = Contact.from_api(CONTACT_DATA)
        assert c.tags == ["vip", "partner"]

    def test_website_is_string(self):
        c = Contact.from_api(CONTACT_DATA)
        assert c.website == "https://piedpiper.com"

    def test_missing_optional_fields_default_to_none(self):
        c = Contact.from_api({"id": "x", "first_name": "A", "last_name": "B"})
        assert c.salutation is None
        assert c.payment_term is None
        assert c.tags == []


class TestContactComputedProperties:
    def test_full_name(self):
        c = Contact(first_name="Erlich", last_name="Bachman")
        assert c.full_name == "Erlich Bachman"

    def test_full_name_strips_whitespace(self):
        assert Contact(first_name="", last_name="Bachman").full_name == "Bachman"
        assert Contact(first_name="Erlich", last_name="").full_name == "Erlich"

    def test_is_active_true(self):
        assert Contact(status="active").is_active is True

    def test_is_active_false(self):
        assert Contact(status="deactivated").is_active is False

    def test_primary_email_prefers_type_primary(self):
        c = Contact(emails=[
            Email(email="other@x.com", type="invoicing"),
            Email(email="main@x.com", type="primary"),
        ])
        assert c.primary_email == "main@x.com"

    def test_primary_email_falls_back_to_first(self):
        c = Contact(emails=[Email(email="first@x.com", type="invoicing")])
        assert c.primary_email == "first@x.com"

    def test_primary_email_none_when_empty(self):
        assert Contact().primary_email is None

    def test_primary_phone(self):
        c = Contact(telephones=[Telephone(number="0123"), Telephone(number="0456")])
        assert c.primary_phone == "0123"

    def test_primary_phone_none_when_empty(self):
        assert Contact().primary_phone is None


class TestContactToDict:
    def test_required_keys_always_present(self):
        c = Contact(id="x", first_name="A", last_name="B")
        d = c.to_dict()
        for key in ("id", "first_name", "last_name", "status", "emails", "telephones", "addresses", "tags"):
            assert key in d

    def test_none_fields_omitted(self):
        c = Contact(id="x", first_name="A", last_name="B")
        d = c.to_dict()
        assert "salutation" not in d
        assert "vat_number" not in d
        assert "payment_term" not in d

    def test_payment_term_included_when_set(self):
        c = Contact(payment_term=PaymentTerm(type="cash"))
        d = c.to_dict()
        assert d["payment_term"] == {"type": "cash"}

    def test_emails_serialised(self):
        c = Contact(emails=[Email(email="a@b.com", type="primary")])
        d = c.to_dict()
        assert d["emails"] == [{"email": "a@b.com", "type": "primary"}]


# ===========================================================================
# Company
# ===========================================================================


class TestCompanyFromApi:
    def test_basic_fields(self):
        co = Company.from_api(COMPANY_DATA)
        assert co.id == "e8d31ae7-8258-4fcd-9b2d-78f41b0aa5d5"
        assert co.name == "Pied Piper"
        assert co.status == "active"
        assert co.vat_number == "BE0899623035"

    def test_wrapped_dict(self):
        co = Company.from_api({"data": COMPANY_DATA})
        assert co.name == "Pied Piper"

    def test_business_type(self):
        co = Company.from_api(COMPANY_DATA)
        assert isinstance(co.business_type, TypeAndId)
        assert co.business_type.type == "businessType"

    def test_responsible_user(self):
        co = Company.from_api(COMPANY_DATA)
        assert isinstance(co.responsible_user, TypeAndId)
        assert co.responsible_user.id == "user-1"

    def test_payment_term_no_days(self):
        co = Company.from_api(COMPANY_DATA)
        assert isinstance(co.payment_term, PaymentTerm)
        assert co.payment_term.type == "end_of_month"
        assert co.payment_term.days is None

    def test_related_companies(self):
        co = Company.from_api(COMPANY_DATA)
        assert len(co.related_companies) == 1
        assert isinstance(co.related_companies[0], TypeAndId)
        assert co.related_companies[0].id == "rel-1"

    def test_related_contacts_raw(self):
        co = Company.from_api(COMPANY_DATA)
        assert co.related_contacts == [{"type": "contact", "id": "rel-2"}]

    def test_multiple_emails(self):
        co = Company.from_api(COMPANY_DATA)
        assert len(co.emails) == 2


class TestCompanyComputedProperties:
    def test_is_active(self):
        assert Company(status="active").is_active is True
        assert Company(status="deactivated").is_active is False

    def test_primary_email_picks_primary_type(self):
        co = Company(emails=[
            Email(email="billing@x.com", type="invoicing"),
            Email(email="main@x.com", type="primary"),
        ])
        assert co.primary_email == "main@x.com"

    def test_primary_email_first_when_no_primary(self):
        co = Company(emails=[Email(email="first@x.com", type="invoicing")])
        assert co.primary_email == "first@x.com"

    def test_primary_phone(self):
        co = Company(telephones=[Telephone(number="555")])
        assert co.primary_phone == "555"


# ===========================================================================
# Deal
# ===========================================================================


class TestDealFromApi:
    def test_basic_fields(self):
        d = Deal.from_api(DEAL_DATA)
        assert d.id == "f6871b06-6513-4750-b5e6-ff3503b5a029"
        assert d.title == "Interesting deal"
        assert d.status == "won"
        assert d.reference == "2017/2"
        assert d.purchase_order_number == "000023"

    def test_wrapped_dict(self):
        d = Deal.from_api({"data": DEAL_DATA})
        assert d.title == "Interesting deal"

    def test_money_fields(self):
        d = Deal.from_api(DEAL_DATA)
        assert isinstance(d.estimated_value, Money)
        assert d.estimated_value.amount == 123.3
        assert isinstance(d.weighted_value, Money)
        assert d.weighted_value.amount == 61.65

    def test_type_and_id_fields(self):
        d = Deal.from_api(DEAL_DATA)
        assert isinstance(d.department, TypeAndId)
        assert isinstance(d.current_phase, TypeAndId)
        assert isinstance(d.responsible_user, TypeAndId)
        assert isinstance(d.source, TypeAndId)
        assert isinstance(d.pipeline, TypeAndId)

    def test_quotations_list(self):
        d = Deal.from_api(DEAL_DATA)
        assert len(d.quotations) == 1
        assert isinstance(d.quotations[0], TypeAndId)
        assert d.quotations[0].type == "quotation"

    def test_lead_raw(self):
        d = Deal.from_api(DEAL_DATA)
        assert d.lead["customer"]["type"] == "company"

    def test_missing_optional_fields(self):
        d = Deal.from_api({"id": "x", "title": "T"})
        assert d.estimated_value is None
        assert d.current_phase is None
        assert d.quotations == []


class TestDealComputedProperties:
    def test_is_open(self):
        assert Deal(status="open").is_open is True
        assert Deal(status="won").is_open is False

    def test_is_won(self):
        assert Deal(status="won").is_won is True
        assert Deal(status="lost").is_won is False

    def test_is_lost(self):
        assert Deal(status="lost").is_lost is True
        assert Deal(status="open").is_lost is False

    def test_customer_id_and_type(self):
        d = Deal.from_api(DEAL_DATA)
        assert d.customer_id == "2659dc4d-444b-4ced-b51c-b87591f604d7"
        assert d.customer_type == "company"

    def test_customer_id_none_when_no_lead(self):
        d = Deal()
        assert d.customer_id is None
        assert d.customer_type is None


# ===========================================================================
# Invoice
# ===========================================================================


class TestInvoiceFromApi:
    def test_basic_fields(self):
        inv = Invoice.from_api(INVOICE_DATA)
        assert inv.id == "e540fe7e-dce2-459e-bf7e-24e605fc18b3"
        assert inv.invoice_number == "2017 / 5"
        assert inv.status == "outstanding"
        assert inv.due_on == "2016-03-03"
        assert inv.paid is False
        assert inv.sent is True

    def test_wrapped_dict(self):
        inv = Invoice.from_api({"data": INVOICE_DATA})
        assert inv.invoice_number == "2017 / 5"

    def test_department(self):
        inv = Invoice.from_api(INVOICE_DATA)
        assert isinstance(inv.department, TypeAndId)
        assert inv.department.type == "department"

    def test_payment_term(self):
        inv = Invoice.from_api(INVOICE_DATA)
        assert isinstance(inv.payment_term, PaymentTerm)
        assert inv.payment_term.days == 30

    def test_deal(self):
        inv = Invoice.from_api(INVOICE_DATA)
        assert isinstance(inv.deal, TypeAndId)
        assert inv.deal.type == "deal"

    def test_total_raw(self):
        inv = Invoice.from_api(INVOICE_DATA)
        assert inv.total["tax_exclusive"]["amount"] == 100.0

    def test_missing_optional_fields(self):
        inv = Invoice.from_api({"id": "x"})
        assert inv.department is None
        assert inv.paid is False
        assert inv.sent is False


class TestInvoiceComputedProperties:
    def test_is_paid_true(self):
        inv = Invoice(paid=True)
        assert inv.is_paid is True

    def test_is_paid_false(self):
        assert Invoice(paid=False).is_paid is False

    def test_is_draft(self):
        assert Invoice(status="draft").is_draft is True
        assert Invoice(status="outstanding").is_draft is False

    @freeze_time("2020-06-15")
    def test_is_overdue_past_due_unpaid(self):
        inv = Invoice(due_on="2020-06-01", paid=False)
        assert inv.is_overdue is True

    @freeze_time("2020-06-15")
    def test_is_overdue_future_due_date(self):
        inv = Invoice(due_on="2020-12-31", paid=False)
        assert inv.is_overdue is False

    @freeze_time("2020-06-15")
    def test_is_overdue_paid_ignores_past_date(self):
        inv = Invoice(due_on="2020-01-01", paid=True)
        assert inv.is_overdue is False

    def test_is_overdue_no_due_date(self):
        assert Invoice(due_on=None, paid=False).is_overdue is False

    def test_is_overdue_bad_date_string(self):
        assert Invoice(due_on="not-a-date", paid=False).is_overdue is False

    def test_total_due(self):
        inv = Invoice.from_api(INVOICE_DATA)
        td = inv.total_due
        assert isinstance(td, Money)
        assert td.amount == 121.0
        assert td.currency == "EUR"

    def test_total_due_none_when_no_total(self):
        assert Invoice().total_due is None

    def test_customer_name(self):
        inv = Invoice.from_api(INVOICE_DATA)
        assert inv.customer_name == "De Rode Duivels"

    def test_customer_name_none_when_no_invoicee(self):
        assert Invoice().customer_name is None


class TestInvoiceToDict:
    def test_required_keys(self):
        inv = Invoice(id="x", status="draft")
        d = inv.to_dict()
        assert d["id"] == "x"
        assert d["status"] == "draft"
        assert d["paid"] is False
        assert d["sent"] is False

    def test_optional_fields_omitted_when_none(self):
        d = Invoice(id="x").to_dict()
        assert "due_on" not in d
        assert "payment_reference" not in d


# ===========================================================================
# Quotation
# ===========================================================================


class TestQuotationFromApi:
    def test_basic_fields(self):
        q = Quotation.from_api(QUOTATION_DATA)
        assert q.id == "e7a3fe2b-2c75-480f-87b9-121816b5257b"
        assert q.status == "open"
        assert q.name == "Webdevelopment"
        assert q.currency == "EUR"
        assert q.text == "Quotation text"

    def test_wrapped_dict(self):
        q = Quotation.from_api({"data": QUOTATION_DATA})
        assert q.name == "Webdevelopment"

    def test_deal(self):
        q = Quotation.from_api(QUOTATION_DATA)
        assert isinstance(q.deal, TypeAndId)
        assert q.deal.type == "deal"

    def test_document_template(self):
        q = Quotation.from_api(QUOTATION_DATA)
        assert isinstance(q.document_template, TypeAndId)
        assert q.document_template.type == "documentTemplate"

    def test_missing_optional_fields(self):
        q = Quotation.from_api({"id": "x"})
        assert q.deal is None
        assert q.document_template is None
        assert q.grouped_lines == []


class TestQuotationComputedProperties:
    def test_is_open(self):
        assert Quotation(status="open").is_open is True
        assert Quotation(status="accepted").is_open is False

    def test_is_accepted(self):
        assert Quotation(status="accepted").is_accepted is True
        assert Quotation(status="open").is_accepted is False

    def test_is_expired(self):
        assert Quotation(status="expired").is_expired is True
        assert Quotation(status="rejected").is_expired is False

    def test_total_tax_exclusive(self):
        q = Quotation.from_api(QUOTATION_DATA)
        te = q.total_tax_exclusive
        assert isinstance(te, Money)
        assert te.amount == 100.0

    def test_total_tax_inclusive(self):
        q = Quotation.from_api(QUOTATION_DATA)
        ti = q.total_tax_inclusive
        assert isinstance(ti, Money)
        assert ti.amount == 121.0

    def test_total_tax_exclusive_none_when_no_total(self):
        assert Quotation().total_tax_exclusive is None

    def test_total_tax_inclusive_none_when_no_total(self):
        assert Quotation().total_tax_inclusive is None


class TestQuotationToDict:
    def test_required_keys(self):
        q = Quotation(id="x", status="accepted")
        d = q.to_dict()
        assert d["id"] == "x"
        assert d["status"] == "accepted"

    def test_optional_keys_omitted_when_none(self):
        d = Quotation(id="x").to_dict()
        assert "deal" not in d
        assert "document_template" not in d
        assert "text" not in d

    def test_deal_included_when_set(self):
        q = Quotation(deal=TypeAndId(id="d1", type="deal"))
        d = q.to_dict()
        assert d["deal"] == {"id": "d1", "type": "deal"}
