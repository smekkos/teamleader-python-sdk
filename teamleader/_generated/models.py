# ============================================================
# AUTO-GENERATED — DO NOT EDIT BY HAND
# Run `python codegen/generate.py` to regenerate.
# Spec version: 1.112.0
# Generated at: 2026-02-24T13:41:23Z
# ============================================================

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class _AddressrequestBase:
    """Auto-generated from schema: AddressRequest"""

    country: str
    line_1: str | None
    postal_code: str | None
    city: str | None
    area_level_two_id: str | None = None


@dataclass
class _AddressresponseBase:
    """Auto-generated from schema: AddressResponse"""

    line_1: str | None = None
    postal_code: str | None = None
    city: str | None = None
    country: str | None = None
    area_level_two: dict[str, Any] | None = None


@dataclass
class _AddressesrequestBase:
    """Auto-generated from schema: AddressesRequest"""

    type: str | None = None
    address: dict[str, Any] | None = None


@dataclass
class _AddressesresponseBase:
    """Auto-generated from schema: AddressesResponse"""

    type: str | None = None
    address: dict[str, Any] | None = None


@dataclass
class _AmountwithtaxBase:
    """Auto-generated from schema: AmountWithTax"""

    amount: float
    tax: str


@dataclass
class _AssigneeBase:
    """Auto-generated from schema: Assignee"""

    type: str | None = None
    id: str | None = None


@dataclass
class _AssigneesBase:
    """Auto-generated from schema: Assignees"""

    assignee: dict[str, Any] | None = None
    assign_type: str | None = None


@dataclass
class _AttendeeBase:
    """Auto-generated from schema: Attendee"""

    type: str
    id: str


@dataclass
class _AttendeesBase:
    """Auto-generated from schema: Attendees"""

    type: str | None = None
    id: str | None = None


@dataclass
class _BillingcycleBase:
    """Auto-generated from schema: BillingCycle"""

    periodicity: dict[str, Any] | None = None
    days_in_advance: int | None = None


@dataclass
class _BillinginfoBase:
    """Auto-generated from schema: BillingInfo"""

    type: str | None = None
    invoice: dict[str, Any] | None = None


@dataclass
class _BillingmethodBase:
    """Auto-generated from schema: BillingMethod"""

    value: str
    update_strategy: str


@dataclass
class _CcemailBase:
    """Auto-generated from schema: CcEmail"""

    email: str
    customer: dict[str, Any] | None = None


@dataclass
class _CcemailaddressBase:
    """Auto-generated from schema: CcEmailAddress"""

    email_address: str
    customer: dict[str, Any] | None = None


@dataclass
class _CommercialdiscountBase:
    """Auto-generated from schema: CommercialDiscount"""

    type: str | None = None
    value: float | None = None
    description: str | None = None


@dataclass
class _CompanycustomerBase:
    """Auto-generated from schema: CompanyCustomer"""

    type: str
    id: str


@dataclass
class _CompanytelephoneBase:
    """Auto-generated from schema: CompanyTelephone"""

    type: str
    number: str


@dataclass
class _CreditnotesgroupedlinesresponseBase:
    """Auto-generated from schema: CreditNotesGroupedLinesResponse"""

    section: dict[str, Any] | None = None
    line_items: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class _CreditnoteslistinvoiceeBase:
    """Auto-generated from schema: CreditNotesListInvoicee"""

    name: str | None = None
    vat_number: str | None = None
    customer: dict[str, Any] | None = None


@dataclass
class _CreditnotesresponseinvoiceeBase:
    """Auto-generated from schema: CreditNotesResponseInvoicee"""

    name: str | None = None
    vat_number: str | None = None
    customer: dict[str, Any] | None = None
    email: str | None = None
    national_identification_number: str | None = None


@dataclass
class _CurrencyBase:
    """Auto-generated from schema: Currency"""

    code: str
    exchange_rate: float | None = None


@dataclass
class _CurrencyexchangerateBase:
    """Auto-generated from schema: CurrencyExchangeRate"""

    from_: dict[str, Any] | None = None
    to: dict[str, Any] | None = None
    rate: float | None = None


@dataclass
class _CurrencywithrequiredexchangerateBase:
    """Auto-generated from schema: CurrencyWithRequiredExchangeRate"""

    code: str
    exchange_rate: float


@dataclass
class _CustomfieldsrequestBase:
    """Auto-generated from schema: CustomFieldsRequest"""

    id: str | None = None
    value: dict[str, Any] | None = None


@dataclass
class _CustomfieldsresponseBase:
    """Auto-generated from schema: CustomFieldsResponse"""

    definition: dict[str, Any] | None = None
    value: dict[str, Any] | None = None


@dataclass
class _CustomerBase:
    """Auto-generated from schema: Customer"""

    type: str
    id: str


@dataclass
class _DatevalidityBase:
    """Auto-generated from schema: DateValidity"""

    from_: str
    until: str | None = None


@dataclass
class _DiscountBase:
    """Auto-generated from schema: Discount"""

    value: float | None = None
    type: str | None = None


@dataclass
class _DownloadBase:
    """Auto-generated from schema: Download"""

    location: str | None = None
    expires: str | None = None


@dataclass
class _DurationinminutesBase:
    """Auto-generated from schema: DurationInMinutes"""

    unit: str | None = None
    value: float | None = None


@dataclass
class _DurationinminutesfullBase:
    """Auto-generated from schema: DurationInMinutesFull"""

    unit: str | None = None
    value: float | None = None


@dataclass
class _EmailBase:
    """Auto-generated from schema: Email"""

    type: str | None = None
    email: str | None = None


@dataclass
class _ExpiryBase:
    """Auto-generated from schema: Expiry"""

    expires_after: str | None = None
    action_after_expiry: str | None = None


@dataclass
class _ForattentionofBase:
    """Auto-generated from schema: ForAttentionOf"""

    name: str | None = None
    contact: dict[str, Any] | None = None


@dataclass
class _IdandnameBase:
    """Auto-generated from schema: IdAndName"""

    id: str | None = None
    name: str | None = None


@dataclass
class _InvoicesgroupedlinesrequestBase:
    """Auto-generated from schema: InvoicesGroupedLinesRequest"""

    section: dict[str, Any] | None = None
    line_items: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class _InvoicesgroupedlinesresponseBase:
    """Auto-generated from schema: InvoicesGroupedLinesResponse"""

    section: dict[str, Any] | None = None
    line_items: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class _InvoiceslistinvoiceeBase:
    """Auto-generated from schema: InvoicesListInvoicee"""

    name: str | None = None
    vat_number: str | None = None
    customer: dict[str, Any] | None = None
    for_attention_of: dict[str, Any] | None = None


@dataclass
class _InvoicesrequestinvoiceeBase:
    """Auto-generated from schema: InvoicesRequestInvoicee"""

    customer: dict[str, Any]
    for_attention_of: dict[str, Any] | None = None


@dataclass
class _InvoicesresponseinvoiceeBase:
    """Auto-generated from schema: InvoicesResponseInvoicee"""

    name: str | None = None
    vat_number: str | None = None
    customer: dict[str, Any] | None = None
    for_attention_of: dict[str, Any] | None = None
    email: str | None = None
    national_identification_number: str | None = None


@dataclass
class _InvoicingpreferencesBase:
    """Auto-generated from schema: InvoicingPreferences"""

    electronic_invoicing_address: str | None = None


@dataclass
class _LeadrequestBase:
    """Auto-generated from schema: LeadRequest"""

    customer: dict[str, Any]
    contact_person_id: str | None = None


@dataclass
class _LeadresponseBase:
    """Auto-generated from schema: LeadResponse"""

    customer: dict[str, Any] | None = None
    contact_person: dict[str, Any] | None = None


@dataclass
class _LineitemrequestBase:
    """Auto-generated from schema: LineItemRequest"""

    quantity: float
    description: str
    tax_rate_id: str
    extended_description: str | None = None
    unit_of_measure_id: str | None = None
    unit_price: dict[str, Any] | None = None
    discount: dict[str, Any] | None = None
    product_id: str | None = None


@dataclass
class _LineitemresponseBase:
    """Auto-generated from schema: LineItemResponse"""

    product: dict[str, Any] | None = None
    quantity: float | None = None
    description: str | None = None
    extended_description: str | None = None
    unit: dict[str, Any] | None = None
    unit_price: dict[str, Any] | None = None
    tax: dict[str, Any] | None = None
    discount: dict[str, Any] | None = None
    total: dict[str, Any] | None = None


@dataclass
class _LostreasonBase:
    """Auto-generated from schema: lost_reason"""

    reason: dict[str, Any] | None = None
    remark: str | None = None


@dataclass
class _MetaBase:
    """Auto-generated from schema: Meta"""

    page: dict[str, Any] | None = None
    matches: float | None = None


@dataclass
class _MilestonesactualsBase:
    """Auto-generated from schema: MilestonesActuals"""

    billable_amount: dict[str, Any] | None = None
    costs: dict[str, Any] | None = None
    result: dict[str, Any] | None = None


@dataclass
class _MilestonesbudgetBase:
    """Auto-generated from schema: MilestonesBudget"""

    provided: dict[str, Any] | None = None
    spent: dict[str, Any] | None = None
    remaining: dict[str, Any] | None = None
    allocated: dict[str, Any] | None = None
    forecasted: dict[str, Any] | None = None


@dataclass
class _MoneyBase:
    """Auto-generated from schema: Money"""

    amount: float
    currency: str


@dataclass
class _OrdersgroupedlinesresponseBase:
    """Auto-generated from schema: OrdersGroupedLinesResponse"""

    section: dict[str, Any] | None = None
    line_items: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class _PageBase:
    """Auto-generated from schema: Page"""

    size: float | None = None
    number: float | None = None


@dataclass
class _PaginationBase:
    """Auto-generated from schema: Pagination"""

    size: float | None = None
    number: float | None = None


@dataclass
class _ParticipantBase:
    """Auto-generated from schema: Participant"""

    customer: dict[str, Any] | None = None
    contact: dict[str, Any] | None = None


@dataclass
class _ParticipantsBase:
    """Auto-generated from schema: Participants"""

    participant: dict[str, Any] | None = None
    role: str | None = None


@dataclass
class _PaymenttermBase:
    """Auto-generated from schema: PaymentTerm"""

    type: str | None = None
    days: float | None = None


@dataclass
class _PeriodBase:
    """Auto-generated from schema: Period"""

    start_date: str | None = None
    end_date: str | None = None


@dataclass
class _ProductconfigurationreadBase:
    """Auto-generated from schema: ProductConfigurationRead"""

    stock_threshold: dict[str, Any] | None = None


@dataclass
class _ProductconfigurationwriteBase:
    """Auto-generated from schema: ProductConfigurationWrite"""

    stock_threshold: dict[str, Any] | None = None


@dataclass
class _ProductpricewriteBase:
    """Auto-generated from schema: ProductPriceWrite"""

    amount: float
    currency: str


@dataclass
class _ProjectsactualsBase:
    """Auto-generated from schema: ProjectsActuals"""

    billable_amount: dict[str, Any] | None = None
    costs: dict[str, Any] | None = None
    result: dict[str, Any] | None = None
    profit_percentage: float | None = None


@dataclass
class _ProjectsbudgetBase:
    """Auto-generated from schema: ProjectsBudget"""

    provided: dict[str, Any] | None = None
    spent: dict[str, Any] | None = None
    remaining: dict[str, Any] | None = None
    allocated: dict[str, Any] | None = None
    forecasted: dict[str, Any] | None = None


@dataclass
class _QuotationsgroupedlinesrequestBase:
    """Auto-generated from schema: QuotationsGroupedLinesRequest"""

    section: dict[str, Any] | None = None
    line_items: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class _QuotationsgroupedlinesresponseBase:
    """Auto-generated from schema: QuotationsGroupedLinesResponse"""

    section: dict[str, Any] | None = None
    line_items: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class _RelatedcontactsBase:
    """Auto-generated from schema: RelatedContacts"""

    type: str | None = None
    id: str | None = None
    position: str | None = None
    secondary_position: str | None = None
    division: str | None = None
    is_decision_maker: bool | None = None


@dataclass
class _RequiresattentionafterBase:
    """Auto-generated from schema: RequiresAttentionAfter"""

    amount: float | None = None
    unit: str | None = None


@dataclass
class _SenderBase:
    """Auto-generated from schema: Sender"""

    type: str
    id: str


@dataclass
class _SentbyBase:
    """Auto-generated from schema: SentBy"""

    type: str | None = None
    id: str | None = None


@dataclass
class _SortBase:
    """Auto-generated from schema: Sort"""

    field: str
    order: str | None = None


@dataclass
class _StockBase:
    """Auto-generated from schema: Stock"""

    amount: float | None = None


@dataclass
class _StockthresholdBase:
    """Auto-generated from schema: StockThreshold"""

    minimum: float
    action: str


@dataclass
class _SubscriptionsgroupedlinesrequestBase:
    """Auto-generated from schema: SubscriptionsGroupedLinesRequest"""

    section: dict[str, Any] | None = None
    line_items: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class _SubscriptionsgroupedlinesresponseBase:
    """Auto-generated from schema: SubscriptionsGroupedLinesResponse"""

    section: dict[str, Any] | None = None
    line_items: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class _SubscriptionsresponseinvoiceeBase:
    """Auto-generated from schema: SubscriptionsResponseInvoicee"""

    customer: dict[str, Any] | None = None
    for_attention_of: dict[str, Any] | None = None


@dataclass
class _TaxesBase:
    """Auto-generated from schema: Taxes"""

    rate: float | None = None
    taxable: dict[str, Any] | None = None
    tax: dict[str, Any] | None = None


@dataclass
class _TelephoneBase:
    """Auto-generated from schema: Telephone"""

    type: str | None = None
    number: str | None = None


@dataclass
class _TimeBase:
    """Auto-generated from schema: Time"""

    value: float | None = None
    unit: str | None = None


@dataclass
class _TimetrackingmaterialsBase:
    """Auto-generated from schema: TimeTrackingMaterials"""

    product: dict[str, Any] | None = None
    description: str | None = None
    unit_price: dict[str, Any] | None = None
    quantity: float | None = None


@dataclass
class _ToemailBase:
    """Auto-generated from schema: ToEmail"""

    email: str
    customer: dict[str, Any] | None = None


@dataclass
class _ToemailaddressBase:
    """Auto-generated from schema: ToEmailAddress"""

    email_address: str
    customer: dict[str, Any] | None = None


@dataclass
class _TypeandidBase:
    """Auto-generated from schema: TypeAndId"""

    id: str | None = None
    type: str | None = None


@dataclass
class _UseravailabilityBase:
    """Auto-generated from schema: UserAvailability"""

    gross_time_available: dict[str, Any] | None = None
    net_time_available: dict[str, Any] | None = None
    planned_time: dict[str, Any] | None = None
    unplanned_time: dict[str, Any] | None = None


@dataclass
class _UserpreferencesBase:
    """Auto-generated from schema: UserPreferences"""

    invoiceable: bool | None = None
    historic_time_tracking_limit: dict[str, Any] | None = None
    whitelabeling: bool | None = None


@dataclass
class _WebhookBase:
    """Auto-generated from schema: WebHook"""

    url: str
    types: list[str] = field(default_factory=list)


@dataclass
class _AccountsProjectsV2StatusresponseBase:
    """Auto-generated from schema: accounts.projects-v2-statusresponse"""

    data: dict[str, Any] | None = None


@dataclass
class _ActivitytypesListrequestBase:
    """Auto-generated from schema: activityTypes.listrequest"""

    filter: dict[str, Any] | None = None
    page: dict[str, Any] | None = None


@dataclass
class _ActivitytypesListresponseBase:
    """Auto-generated from schema: activityTypes.listresponse"""

    data: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class _BusinesstypesListrequestBase:
    """Auto-generated from schema: businessTypes.listrequest"""

    country: str | None = None


@dataclass
class _BusinesstypesListresponseBase:
    """Auto-generated from schema: businessTypes.listresponse"""

    data: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class _CalloutcomesListrequestBase:
    """Auto-generated from schema: callOutcomes.listrequest"""

    page: dict[str, Any] | None = None


@dataclass
class _CalloutcomesListresponseBase:
    """Auto-generated from schema: callOutcomes.listresponse"""

    data: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class _CallsAddrequestBase:
    """Auto-generated from schema: calls.addrequest"""

    participant: dict[str, Any]
    due_at: str
    assignee: dict[str, Any]
    description: str | None = None
    deal_id: str | None = None
    custom_fields: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class _CallsAddresponseBase:
    """Auto-generated from schema: calls.addresponse"""

    data: dict[str, Any] | None = None


@dataclass
class _CallsCompleterequestBase:
    """Auto-generated from schema: calls.completerequest"""

    id: str
    call_outcome_id: str | None = None
    outcome_summary: str | None = None


@dataclass
class _CallsInforequestBase:
    """Auto-generated from schema: calls.inforequest"""

    id: str


@dataclass
class _CallsInforesponseBase:
    """Auto-generated from schema: calls.inforesponse"""

    data: dict[str, Any] | None = None


@dataclass
class _CallsListrequestBase:
    """Auto-generated from schema: calls.listrequest"""

    filter: dict[str, Any] | None = None
    page: dict[str, Any] | None = None


@dataclass
class _CallsListresponseBase:
    """Auto-generated from schema: calls.listresponse"""

    meta: dict[str, Any] | None = None
    data: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class _CallsUpdaterequestBase:
    """Auto-generated from schema: calls.updaterequest"""

    id: str
    description: str | None = None
    participant: dict[str, Any] | None = None
    due_at: str | None = None
    assignee: dict[str, Any] | None = None
    deal_id: str | None = None
    custom_fields: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class _ClosingdaysAddrequestBase:
    """Auto-generated from schema: closingDays.addrequest"""

    day: str


@dataclass
class _ClosingdaysAddresponseBase:
    """Auto-generated from schema: closingDays.addresponse"""

    data: dict[str, Any] | None = None


@dataclass
class _ClosingdaysDeleterequestBase:
    """Auto-generated from schema: closingDays.deleterequest"""

    id: str


@dataclass
class _ClosingdaysListrequestBase:
    """Auto-generated from schema: closingDays.listrequest"""

    filter: dict[str, Any] | None = None
    page: dict[str, Any] | None = None


@dataclass
class _ClosingdaysListresponseBase:
    """Auto-generated from schema: closingDays.listresponse"""

    meta: dict[str, Any] | None = None
    data: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class _CloudplatformsUrlrequestBase:
    """Auto-generated from schema: cloudPlatforms.urlrequest"""

    type: str
    id: str


@dataclass
class _CloudplatformsUrlresponseBase:
    """Auto-generated from schema: cloudPlatforms.urlresponse"""

    data: dict[str, Any] | None = None


@dataclass
class _CommercialdiscountsListrequestBase:
    """Auto-generated from schema: commercialDiscounts.listrequest"""

    filter: dict[str, Any] | None = None


@dataclass
class _CommercialdiscountsListresponseBase:
    """Auto-generated from schema: commercialDiscounts.listresponse"""

    data: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class _CompaniesAddrequestBase:
    """Auto-generated from schema: companies.addrequest"""

    name: str
    business_type_id: str | None = None
    vat_number: str | None = None
    national_identification_number: str | None = None
    website: str | None = None
    iban: str | None = None
    bic: str | None = None
    language: str | None = None
    responsible_user_id: str | None = None
    remarks: str | None = None
    marketing_mails_consent: bool | None = None
    preferred_currency: dict[str, Any] | None = None
    emails: list[dict[str, Any]] = field(default_factory=list)
    telephones: list[dict[str, Any]] = field(default_factory=list)
    addresses: list[dict[str, Any]] = field(default_factory=list)
    tags: list[str] = field(default_factory=list)
    custom_fields: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class _CompaniesAddresponseBase:
    """Auto-generated from schema: companies.addresponse"""

    data: dict[str, Any] | None = None


@dataclass
class _CompaniesDeleterequestBase:
    """Auto-generated from schema: companies.deleterequest"""

    id: str


@dataclass
class _CompaniesInforequestBase:
    """Auto-generated from schema: companies.inforequest"""

    id: str
    includes: str | None = None


@dataclass
class _CompaniesInforesponseBase:
    """Auto-generated from schema: companies.inforesponse"""

    data: dict[str, Any] | None = None


@dataclass
class _CompaniesListrequestBase:
    """Auto-generated from schema: companies.listrequest"""

    filter: dict[str, Any] | None = None
    page: dict[str, Any] | None = None
    includes: str | None = None
    sort: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class _CompaniesListresponseBase:
    """Auto-generated from schema: companies.listresponse"""

    data: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class _CompaniesTagrequestBase:
    """Auto-generated from schema: companies.tagrequest"""

    id: str
    tags: list[str] = field(default_factory=list)


@dataclass
class _CompaniesUntagrequestBase:
    """Auto-generated from schema: companies.untagrequest"""

    id: str
    tags: list[str] = field(default_factory=list)


@dataclass
class _CompaniesUpdaterequestBase:
    """Auto-generated from schema: companies.updaterequest"""

    id: str
    name: str | None = None
    business_type_id: str | None = None
    vat_number: str | None = None
    national_identification_number: str | None = None
    website: str | None = None
    iban: str | None = None
    bic: str | None = None
    language: str | None = None
    responsible_user_id: str | None = None
    remarks: str | None = None
    marketing_mails_consent: bool | None = None
    preferred_currency: dict[str, Any] | None = None
    emails: list[dict[str, Any]] = field(default_factory=list)
    telephones: list[dict[str, Any]] = field(default_factory=list)
    addresses: list[dict[str, Any]] = field(default_factory=list)
    tags: list[str] = field(default_factory=list)
    custom_fields: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class _CompaniesUploadlogorequestBase:
    """Auto-generated from schema: companies.uploadLogorequest"""

    id: str
    image: str | None


@dataclass
class _ContactsAddrequestBase:
    """Auto-generated from schema: contacts.addrequest"""

    last_name: str
    first_name: str | None = None
    salutation: str | None = None
    website: str | None = None
    language: str | None = None
    gender: dict[str, Any] | None = None
    birthdate: str | None = None
    iban: str | None = None
    bic: str | None = None
    national_identification_number: str | None = None
    remarks: str | None = None
    marketing_mails_consent: bool | None = None
    emails: list[dict[str, Any]] = field(default_factory=list)
    telephones: list[dict[str, Any]] = field(default_factory=list)
    addresses: list[dict[str, Any]] = field(default_factory=list)
    tags: list[str] = field(default_factory=list)
    custom_fields: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class _ContactsAddresponseBase:
    """Auto-generated from schema: contacts.addresponse"""

    data: dict[str, Any] | None = None


@dataclass
class _ContactsDeleterequestBase:
    """Auto-generated from schema: contacts.deleterequest"""

    id: str


@dataclass
class _ContactsInforequestBase:
    """Auto-generated from schema: contacts.inforequest"""

    id: str


@dataclass
class _ContactsInforesponseBase:
    """Auto-generated from schema: contacts.inforesponse"""

    data: dict[str, Any] | None = None


@dataclass
class _ContactsLinktocompanyrequestBase:
    """Auto-generated from schema: contacts.linkToCompanyrequest"""

    id: str
    company_id: str
    position: str | None = None
    decision_maker: bool | None = None


@dataclass
class _ContactsListrequestBase:
    """Auto-generated from schema: contacts.listrequest"""

    filter: dict[str, Any] | None = None
    page: dict[str, Any] | None = None
    includes: str | None = None
    sort: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class _ContactsListresponseBase:
    """Auto-generated from schema: contacts.listresponse"""

    data: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class _ContactsTagrequestBase:
    """Auto-generated from schema: contacts.tagrequest"""

    id: str
    tags: list[str] = field(default_factory=list)


@dataclass
class _ContactsUnlinkfromcompanyrequestBase:
    """Auto-generated from schema: contacts.unlinkFromCompanyrequest"""

    id: str
    company_id: str


@dataclass
class _ContactsUntagrequestBase:
    """Auto-generated from schema: contacts.untagrequest"""

    id: str
    tags: list[str] = field(default_factory=list)


@dataclass
class _ContactsUpdatecompanylinkrequestBase:
    """Auto-generated from schema: contacts.updateCompanyLinkrequest"""

    id: str
    company_id: str
    position: str | None = None
    decision_maker: bool | None = None


@dataclass
class _ContactsUpdaterequestBase:
    """Auto-generated from schema: contacts.updaterequest"""

    id: str
    first_name: str | None = None
    last_name: str | None = None
    salutation: str | None = None
    website: str | None = None
    language: str | None = None
    gender: dict[str, Any] | None = None
    birthdate: str | None = None
    iban: str | None = None
    bic: str | None = None
    national_identification_number: str | None = None
    remarks: str | None = None
    marketing_mails_consent: bool | None = None
    emails: list[dict[str, Any]] = field(default_factory=list)
    telephones: list[dict[str, Any]] = field(default_factory=list)
    addresses: list[dict[str, Any]] = field(default_factory=list)
    tags: list[str] = field(default_factory=list)
    custom_fields: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class _ContactsUploadavatarrequestBase:
    """Auto-generated from schema: contacts.uploadAvatarrequest"""

    id: str
    image: str | None


@dataclass
class _CreditnotesDownloadrequestBase:
    """Auto-generated from schema: creditNotes.downloadrequest"""

    id: str
    format: dict[str, Any]


@dataclass
class _CreditnotesDownloadresponseBase:
    """Auto-generated from schema: creditNotes.downloadresponse"""

    data: dict[str, Any] | None = None


@dataclass
class _CreditnotesInforequestBase:
    """Auto-generated from schema: creditNotes.inforequest"""

    id: str


@dataclass
class _CreditnotesInforesponseBase:
    """Auto-generated from schema: creditNotes.inforesponse"""

    data: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class _CreditnotesListrequestBase:
    """Auto-generated from schema: creditNotes.listrequest"""

    filter: dict[str, Any] | None = None
    page: dict[str, Any] | None = None


@dataclass
class _CreditnotesListresponseBase:
    """Auto-generated from schema: creditNotes.listresponse"""

    data: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class _CreditnotesSendviapeppolBase:
    """Auto-generated from schema: creditNotes.sendViaPeppol"""

    id: str


@dataclass
class _CurrenciesExchangeratesrequestBase:
    """Auto-generated from schema: currencies.exchangeRatesrequest"""

    base: str


@dataclass
class _CurrenciesExchangeratesresponseBase:
    """Auto-generated from schema: currencies.exchangeRatesresponse"""

    data: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class _CustomfielddefinitionsCreaterequestBase:
    """Auto-generated from schema: customFieldDefinitions.createrequest"""

    label: str
    type: dict[str, Any]
    context: dict[str, Any]
    configuration: dict[str, Any] | None = None


@dataclass
class _CustomfielddefinitionsCreateresponseBase:
    """Auto-generated from schema: customFieldDefinitions.createresponse"""

    data: dict[str, Any] | None = None


@dataclass
class _CustomfielddefinitionsInforequestBase:
    """Auto-generated from schema: customFieldDefinitions.inforequest"""

    id: str


@dataclass
class _CustomfielddefinitionsInforesponseBase:
    """Auto-generated from schema: customFieldDefinitions.inforesponse"""

    data: dict[str, Any] | None = None


@dataclass
class _CustomfielddefinitionsListrequestBase:
    """Auto-generated from schema: customFieldDefinitions.listrequest"""

    filter: dict[str, Any] | None = None
    page: dict[str, Any] | None = None
    sort: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class _CustomfielddefinitionsListresponseBase:
    """Auto-generated from schema: customFieldDefinitions.listresponse"""

    data: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class _DayofftypesCreaterequestBase:
    """Auto-generated from schema: dayOffTypes.createrequest"""

    name: str
    color: str | None = None
    date_validity: dict[str, Any] | None = None


@dataclass
class _DayofftypesCreateresponseBase:
    """Auto-generated from schema: dayOffTypes.createresponse"""

    data: dict[str, Any] | None = None


@dataclass
class _DayofftypesDeleterequestBase:
    """Auto-generated from schema: dayOffTypes.deleterequest"""

    id: str


@dataclass
class _DayofftypesListresponseBase:
    """Auto-generated from schema: dayOffTypes.listresponse"""

    data: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class _DayofftypesUpdaterequestBase:
    """Auto-generated from schema: dayOffTypes.updaterequest"""

    id: str
    name: str | None = None
    color: str | None = None
    date_validity: dict[str, Any] | None = None


@dataclass
class _DaysoffBulkdeleterequestBase:
    """Auto-generated from schema: daysOff.bulkDeleterequest"""

    user_id: str
    ids: list[str] = field(default_factory=list)


@dataclass
class _DaysoffImportrequestBase:
    """Auto-generated from schema: daysOff.importrequest"""

    user_id: str
    leave_type_id: str
    days: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class _DealphasesCreaterequestBase:
    """Auto-generated from schema: dealPhases.createrequest"""

    name: str
    deal_pipeline_id: str
    requires_attention_after: dict[str, Any]
    estimated_probability: float | None = None
    follow_up_actions: list[str] = field(default_factory=list)


@dataclass
class _DealphasesCreateresponseBase:
    """Auto-generated from schema: dealPhases.createresponse"""

    data: dict[str, Any] | None = None


@dataclass
class _DealphasesDeleterequestBase:
    """Auto-generated from schema: dealPhases.deleterequest"""

    id: str
    new_phase_id: str | None = None


@dataclass
class _DealphasesDuplicaterequestBase:
    """Auto-generated from schema: dealPhases.duplicaterequest"""

    id: str


@dataclass
class _DealphasesDuplicateresponseBase:
    """Auto-generated from schema: dealPhases.duplicateresponse"""

    data: dict[str, Any] | None = None


@dataclass
class _DealphasesListrequestBase:
    """Auto-generated from schema: dealPhases.listrequest"""

    filter: dict[str, Any] | None = None
    page: dict[str, Any] | None = None


@dataclass
class _DealphasesListresponseBase:
    """Auto-generated from schema: dealPhases.listresponse"""

    data: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class _DealphasesMoverequestBase:
    """Auto-generated from schema: dealPhases.moverequest"""

    id: str
    after_phase_id: str


@dataclass
class _DealphasesUpdaterequestBase:
    """Auto-generated from schema: dealPhases.updaterequest"""

    id: str
    requires_attention_after: dict[str, Any]
    name: str | None = None
    estimated_probability: float | None = None
    follow_up_actions: list[str] = field(default_factory=list)


@dataclass
class _DealpipelinesCreaterequestBase:
    """Auto-generated from schema: dealPipelines.createrequest"""

    name: str


@dataclass
class _DealpipelinesCreateresponseBase:
    """Auto-generated from schema: dealPipelines.createresponse"""

    data: dict[str, Any] | None = None


@dataclass
class _DealpipelinesDeleterequestBase:
    """Auto-generated from schema: dealPipelines.deleterequest"""

    id: str
    migrate_phases: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class _DealpipelinesDuplicaterequestBase:
    """Auto-generated from schema: dealPipelines.duplicaterequest"""

    id: str


@dataclass
class _DealpipelinesDuplicateresponseBase:
    """Auto-generated from schema: dealPipelines.duplicateresponse"""

    data: dict[str, Any] | None = None


@dataclass
class _DealpipelinesListrequestBase:
    """Auto-generated from schema: dealPipelines.listrequest"""

    filter: dict[str, Any] | None = None
    page: dict[str, Any] | None = None


@dataclass
class _DealpipelinesListresponseBase:
    """Auto-generated from schema: dealPipelines.listresponse"""

    meta: dict[str, Any] | None = None
    data: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class _DealpipelinesMarkasdefaultrequestBase:
    """Auto-generated from schema: dealPipelines.markAsDefaultrequest"""

    id: str


@dataclass
class _DealpipelinesUpdaterequestBase:
    """Auto-generated from schema: dealPipelines.updaterequest"""

    id: str
    name: str


@dataclass
class _DealsourcesListrequestBase:
    """Auto-generated from schema: dealSources.listrequest"""

    filter: dict[str, Any] | None = None
    page: dict[str, Any] | None = None
    sort: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class _DealsourcesListresponseBase:
    """Auto-generated from schema: dealSources.listresponse"""

    data: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class _DealsCreaterequestBase:
    """Auto-generated from schema: deals.createrequest"""

    lead: dict[str, Any]
    title: str
    summary: str | None = None
    source_id: str | None = None
    department_id: str | None = None
    responsible_user_id: str | None = None
    phase_id: str | None = None
    estimated_value: dict[str, Any] | None = None
    estimated_probability: float | None = None
    estimated_closing_date: str | None = None
    currency: dict[str, Any] | None = None
    custom_fields: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class _DealsCreateresponseBase:
    """Auto-generated from schema: deals.createresponse"""

    data: dict[str, Any] | None = None


@dataclass
class _DealsDeleterequestBase:
    """Auto-generated from schema: deals.deleterequest"""

    id: str


@dataclass
class _DealsInforequestBase:
    """Auto-generated from schema: deals.inforequest"""

    id: str


@dataclass
class _DealsInforesponseBase:
    """Auto-generated from schema: deals.inforesponse"""

    data: dict[str, Any] | None = None


@dataclass
class _DealsListrequestBase:
    """Auto-generated from schema: deals.listrequest"""

    filter: dict[str, Any] | None = None
    page: dict[str, Any] | None = None
    includes: str | None = None
    sort: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class _DealsListresponseBase:
    """Auto-generated from schema: deals.listresponse"""

    data: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class _DealsLoserequestBase:
    """Auto-generated from schema: deals.loserequest"""

    id: str
    reason_id: str | None = None
    extra_info: str | None = None


@dataclass
class _DealsMoverequestBase:
    """Auto-generated from schema: deals.moverequest"""

    id: str
    phase_id: str


@dataclass
class _DealsUpdaterequestBase:
    """Auto-generated from schema: deals.updaterequest"""

    id: str
    lead: dict[str, Any] | None = None
    title: str | None = None
    summary: str | None = None
    source_id: str | None = None
    department_id: str | None = None
    responsible_user_id: str | None = None
    estimated_value: dict[str, Any] | None = None
    estimated_probability: float | None = None
    estimated_closing_date: str | None = None
    currency: dict[str, Any] | None = None
    custom_fields: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class _DealsWinrequestBase:
    """Auto-generated from schema: deals.winrequest"""

    id: str


@dataclass
class _DepartmentsInforequestBase:
    """Auto-generated from schema: departments.inforequest"""

    id: str


@dataclass
class _DepartmentsInforesponseBase:
    """Auto-generated from schema: departments.inforesponse"""

    data: dict[str, Any] | None = None


@dataclass
class _DepartmentsListrequestBase:
    """Auto-generated from schema: departments.listrequest"""

    filter: dict[str, Any] | None = None
    sort: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class _DepartmentsListresponseBase:
    """Auto-generated from schema: departments.listresponse"""

    data: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class _DocumenttemplatesListrequestBase:
    """Auto-generated from schema: documentTemplates.listrequest"""

    filter: dict[str, Any]


@dataclass
class _DocumenttemplatesListresponseBase:
    """Auto-generated from schema: documentTemplates.listresponse"""

    data: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class _EmailtrackingCreaterequestBase:
    """Auto-generated from schema: emailTracking.createrequest"""

    subject: dict[str, Any]
    content: str
    title: str | None = None
    attachments: list[str] = field(default_factory=list)


@dataclass
class _EmailtrackingCreateresponseBase:
    """Auto-generated from schema: emailTracking.createresponse"""

    data: dict[str, Any] | None = None


@dataclass
class _EmailtrackingListrequestBase:
    """Auto-generated from schema: emailTracking.listrequest"""

    filter: dict[str, Any]
    page: dict[str, Any] | None = None


@dataclass
class _EmailtrackingListresponseBase:
    """Auto-generated from schema: emailTracking.listresponse"""

    data: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class _EventsCancelrequestBase:
    """Auto-generated from schema: events.cancelrequest"""

    id: str


@dataclass
class _EventsCreaterequestBase:
    """Auto-generated from schema: events.createrequest"""

    title: str
    activity_type_id: str
    starts_at: str
    ends_at: str
    description: str | None = None
    location: str | None = None
    work_type_id: str | None = None
    attendees: list[dict[str, Any]] = field(default_factory=list)
    links: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class _EventsCreateresponseBase:
    """Auto-generated from schema: events.createresponse"""

    data: dict[str, Any] | None = None


@dataclass
class _EventsInforequestBase:
    """Auto-generated from schema: events.inforequest"""

    id: str


@dataclass
class _EventsInforesponseBase:
    """Auto-generated from schema: events.inforesponse"""

    data: dict[str, Any] | None = None


@dataclass
class _EventsListrequestBase:
    """Auto-generated from schema: events.listrequest"""

    filter: dict[str, Any] | None = None
    page: dict[str, Any] | None = None
    sort: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class _EventsListresponseBase:
    """Auto-generated from schema: events.listresponse"""

    data: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class _EventsUpdaterequestBase:
    """Auto-generated from schema: events.updaterequest"""

    id: str
    title: str | None = None
    description: str | None = None
    starts_at: str | None = None
    ends_at: str | None = None
    location: str | None = None
    work_type_id: str | None = None
    attendees: list[dict[str, Any]] = field(default_factory=list)
    links: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class _ExpensesListrequestBase:
    """Auto-generated from schema: expenses.listrequest"""

    filter: dict[str, Any] | None = None
    page: dict[str, Any] | None = None
    sort: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class _ExpensesListresponseBase:
    """Auto-generated from schema: expenses.listresponse"""

    meta: dict[str, Any] | None = None
    data: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class _FilesDeleterequestBase:
    """Auto-generated from schema: files.deleterequest"""

    id: str


@dataclass
class _FilesDownloadrequestBase:
    """Auto-generated from schema: files.downloadrequest"""

    id: str


@dataclass
class _FilesDownloadresponseBase:
    """Auto-generated from schema: files.downloadresponse"""

    data: dict[str, Any] | None = None


@dataclass
class _FilesInforequestBase:
    """Auto-generated from schema: files.inforequest"""

    id: str


@dataclass
class _FilesInforesponseBase:
    """Auto-generated from schema: files.inforesponse"""

    data: dict[str, Any] | None = None


@dataclass
class _FilesListrequestBase:
    """Auto-generated from schema: files.listrequest"""

    filter: dict[str, Any]
    page: dict[str, Any] | None = None
    sort: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class _FilesListresponseBase:
    """Auto-generated from schema: files.listresponse"""

    data: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class _FilesUploadrequestBase:
    """Auto-generated from schema: files.uploadrequest"""

    name: str
    subject: dict[str, Any]
    folder: str | None = None


@dataclass
class _FilesUploadresponseBase:
    """Auto-generated from schema: files.uploadresponse"""

    data: dict[str, Any] | None = None


@dataclass
class _IncomingcreditnotesListpaymentsrequestBase:
    """Auto-generated from schema: incomingCreditNotes.listPaymentsrequest"""

    id: str


@dataclass
class _IncomingcreditnotesListpaymentsresponseBase:
    """Auto-generated from schema: receipts.listPaymentsresponse"""

    meta: dict[str, Any] | None = None
    data: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class _IncomingcreditnotesRegisterpaymentrequestBase:
    """Auto-generated from schema: receipts.incomingCreditNotes"""

    id: str
    payment: dict[str, Any]
    paid_at: str
    payment_method_id: str | None = None
    remark: str | None = None


@dataclass
class _IncomingcreditnotesRegisterpaymentresponseBase:
    """Auto-generated from schema: receipts.registerPaymentresponse"""

    data: dict[str, Any] | None = None


@dataclass
class _IncomingcreditnotesRemovepaymentrequestBase:
    """Auto-generated from schema: receipts.removePaymentrequest"""

    id: str
    payment_id: str


@dataclass
class _IncomingcreditnotesUpdatepaymentrequestBase:
    """Auto-generated from schema: incomingCreditNotes.updatePaymentrequest"""

    id: str
    payment_id: str
    payment: dict[str, Any] | None = None
    paid_at: str | None = None
    payment_method_id: str | None = None
    remark: str | None = None


@dataclass
class _IncominginvoicesListpaymentsrequestBase:
    """Auto-generated from schema: incomingInvoices.listPaymentsrequest"""

    id: str


@dataclass
class _IncominginvoicesListpaymentsresponseBase:
    """Auto-generated from schema: receipts.listPaymentsresponse"""

    meta: dict[str, Any] | None = None
    data: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class _IncominginvoicesRegisterpaymentrequestBase:
    """Auto-generated from schema: incomingInvoices.registerPaymentrequest"""

    id: str
    payment: dict[str, Any]
    paid_at: str
    payment_method_id: str | None = None
    remark: str | None = None


@dataclass
class _IncominginvoicesRegisterpaymentresponseBase:
    """Auto-generated from schema: receipts.registerPaymentresponse"""

    data: dict[str, Any] | None = None


@dataclass
class _IncominginvoicesRemovepaymentrequestBase:
    """Auto-generated from schema: incomingInvoices.removePaymentrequest"""

    id: str
    payment_id: str


@dataclass
class _IncominginvoicesUpdatepaymentrequestBase:
    """Auto-generated from schema: incomingInvoices.updatePaymentrequest"""

    id: str
    payment_id: str
    payment: dict[str, Any] | None = None
    paid_at: str | None = None
    payment_method_id: str | None = None
    remark: str | None = None


@dataclass
class _InvoicesBookrequestBase:
    """Auto-generated from schema: invoices.bookrequest"""

    id: str
    on: str


@dataclass
class _InvoicesCopyrequestBase:
    """Auto-generated from schema: invoices.copyrequest"""

    id: str


@dataclass
class _InvoicesCopyresponseBase:
    """Auto-generated from schema: invoices.copyresponse"""

    data: dict[str, Any] | None = None


@dataclass
class _InvoicesCreditpartiallyrequestBase:
    """Auto-generated from schema: invoices.creditPartiallyrequest"""

    id: str
    credit_note_date: str | None = None
    grouped_lines: list[dict[str, Any]] = field(default_factory=list)
    discounts: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class _InvoicesCreditpartiallyresponseBase:
    """Auto-generated from schema: invoices.creditPartiallyresponse"""

    data: dict[str, Any] | None = None


@dataclass
class _InvoicesCreditrequestBase:
    """Auto-generated from schema: invoices.creditrequest"""

    id: str
    credit_note_date: str | None = None


@dataclass
class _InvoicesCreditresponseBase:
    """Auto-generated from schema: invoices.creditresponse"""

    data: dict[str, Any] | None = None


@dataclass
class _InvoicesDeleterequestBase:
    """Auto-generated from schema: invoices.deleterequest"""

    id: str


@dataclass
class _InvoicesDownloadrequestBase:
    """Auto-generated from schema: invoices.downloadrequest"""

    id: str
    format: dict[str, Any]


@dataclass
class _InvoicesDownloadresponseBase:
    """Auto-generated from schema: invoices.downloadresponse"""

    data: dict[str, Any] | None = None


@dataclass
class _InvoicesDraftrequestBase:
    """Auto-generated from schema: invoices.draftrequest"""

    invoicee: dict[str, Any]
    department_id: str
    payment_term: dict[str, Any]
    currency: dict[str, Any] | None = None
    project_id: str | None = None
    purchase_order_number: str | None = None
    invoice_date: str | None = None
    note: str | None = None
    expected_payment_method: dict[str, Any] | None = None
    document_template_id: str | None = None
    delivery_date: str | None = None
    grouped_lines: list[dict[str, Any]] = field(default_factory=list)
    discounts: list[dict[str, Any]] = field(default_factory=list)
    custom_fields: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class _InvoicesDraftresponseBase:
    """Auto-generated from schema: invoices.draftresponse"""

    data: dict[str, Any] | None = None


@dataclass
class _InvoicesInforequestBase:
    """Auto-generated from schema: invoices.inforequest"""

    id: str | None = None
    includes: str | None = None


@dataclass
class _InvoicesInforesponseBase:
    """Auto-generated from schema: invoices.inforesponse"""

    data: dict[str, Any] | None = None


@dataclass
class _InvoicesListrequestBase:
    """Auto-generated from schema: invoices.listrequest"""

    filter: dict[str, Any] | None = None
    page: dict[str, Any] | None = None
    includes: str | None = None
    sort: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class _InvoicesListresponseBase:
    """Auto-generated from schema: invoices.listresponse"""

    data: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class _InvoicesRegisterpaymentrequestBase:
    """Auto-generated from schema: invoices.registerPaymentrequest"""

    id: str
    payment: dict[str, Any]
    paid_at: str
    payment_method_id: str | None = None


@dataclass
class _InvoicesRemovepaymentsrequestBase:
    """Auto-generated from schema: invoices.removePaymentsrequest"""

    id: str


@dataclass
class _InvoicesSendviapeppolBase:
    """Auto-generated from schema: invoices.sendViaPeppol"""

    id: str


@dataclass
class _InvoicesSendrequestBase:
    """Auto-generated from schema: invoices.sendrequest"""

    id: str
    content: dict[str, Any]
    recipients: dict[str, Any] | None = None
    attachments: list[str] = field(default_factory=list)


@dataclass
class _InvoicesUpdatebookedrequestBase:
    """Auto-generated from schema: invoices.updateBookedrequest"""

    id: str
    invoicee: dict[str, Any] | None = None
    payment_term: dict[str, Any] | None = None
    project_id: str | None = None
    invoice_date: str | None = None
    note: str | None = None
    grouped_lines: list[dict[str, Any]] = field(default_factory=list)
    custom_fields: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class _InvoicesUpdaterequestBase:
    """Auto-generated from schema: invoices.updaterequest"""

    id: str
    invoicee: dict[str, Any] | None = None
    payment_term: dict[str, Any] | None = None
    currency: dict[str, Any] | None = None
    project_id: str | None = None
    purchase_order_number: str | None = None
    invoice_date: str | None = None
    note: str | None = None
    expected_payment_method: dict[str, Any] | None = None
    document_template_id: str | None = None
    delivery_date: str | None = None
    grouped_lines: list[dict[str, Any]] = field(default_factory=list)
    discounts: list[dict[str, Any]] = field(default_factory=list)
    custom_fields: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class _LeveltwoareasListrequestBase:
    """Auto-generated from schema: levelTwoAreas.listrequest"""

    country: str
    language: str | None = None


@dataclass
class _LeveltwoareasListresponseBase:
    """Auto-generated from schema: levelTwoAreas.listresponse"""

    data: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class _LostreasonsListrequestBase:
    """Auto-generated from schema: lostReasons.listrequest"""

    filter: dict[str, Any] | None = None
    page: dict[str, Any] | None = None
    sort: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class _LostreasonsListresponseBase:
    """Auto-generated from schema: lostReasons.listresponse"""

    data: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class _MailtemplatesListrequestBase:
    """Auto-generated from schema: mailTemplates.listrequest"""

    filter: dict[str, Any]


@dataclass
class _MailtemplatesListresponseBase:
    """Auto-generated from schema: mailTemplates.listresponse"""

    data: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class _MeetingsCompleterequestBase:
    """Auto-generated from schema: meetings.completerequest"""

    id: str


@dataclass
class _MeetingsCreatereportrequestBase:
    """Auto-generated from schema: meetings.createReportrequest"""

    id: str
    attach_to: dict[str, Any]
    summary: str | None = None
    custom_fields: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class _MeetingsCreatereportresponseBase:
    """Auto-generated from schema: meetings.createReportresponse"""

    data: dict[str, Any] | None = None


@dataclass
class _MeetingsDeleterequestBase:
    """Auto-generated from schema: meetings.deleterequest"""

    id: str


@dataclass
class _MeetingsInforequestBase:
    """Auto-generated from schema: meetings.inforequest"""

    id: str
    includes: str | None = None


@dataclass
class _MeetingsInforesponseBase:
    """Auto-generated from schema: meetings.inforesponse"""

    data: dict[str, Any] | None = None


@dataclass
class _MeetingsListrequestBase:
    """Auto-generated from schema: meetings.listrequest"""

    filter: dict[str, Any] | None = None
    page: dict[str, Any] | None = None
    includes: str | None = None
    sort: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class _MeetingsListresponseBase:
    """Auto-generated from schema: meetings.listresponse"""

    data: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class _MeetingsSchedulerequestBase:
    """Auto-generated from schema: meetings.schedulerequest"""

    title: str
    starts_at: str
    ends_at: str
    description: str | None = None
    customer: dict[str, Any] | None = None
    location: dict[str, Any] | None = None
    milestone_id: str | None = None
    deal_id: str | None = None
    work_order_id: str | None = None
    attendees: list[dict[str, Any]] = field(default_factory=list)
    custom_fields: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class _MeetingsScheduleresponseBase:
    """Auto-generated from schema: meetings.scheduleresponse"""

    data: dict[str, Any] | None = None


@dataclass
class _MeetingsUpdaterequestBase:
    """Auto-generated from schema: meetings.updaterequest"""

    id: str
    title: str | None = None
    starts_at: str | None = None
    ends_at: str | None = None
    description: str | None = None
    customer: dict[str, Any] | None = None
    location: dict[str, Any] | None = None
    milestone_id: str | None = None
    deal_id: str | None = None
    attendees: list[dict[str, Any]] = field(default_factory=list)
    custom_fields: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class _MigrateActivitytyperequestBase:
    """Auto-generated from schema: migrate.activityTyperequest"""

    type: str | None = None


@dataclass
class _MigrateActivitytyperesponseBase:
    """Auto-generated from schema: migrate.activityTyperesponse"""

    data: dict[str, Any] | None = None


@dataclass
class _MigrateIdrequestBase:
    """Auto-generated from schema: migrate.idrequest"""

    type: str | None = None
    id: float | None = None


@dataclass
class _MigrateIdresponseBase:
    """Auto-generated from schema: migrate.idresponse"""

    data: dict[str, Any] | None = None


@dataclass
class _MigrateTaxraterequestBase:
    """Auto-generated from schema: migrate.taxRaterequest"""

    department_id: str | None = None
    tax_rate: str | None = None


@dataclass
class _MigrateTaxrateresponseBase:
    """Auto-generated from schema: migrate.taxRateresponse"""

    data: dict[str, Any] | None = None


@dataclass
class _MilestonesCloserequestBase:
    """Auto-generated from schema: milestones.closerequest"""

    id: str


@dataclass
class _MilestonesCreateresponseBase:
    """Auto-generated from schema: milestones.createresponse"""

    data: dict[str, Any] | None = None


@dataclass
class _MilestonesDeleterequestBase:
    """Auto-generated from schema: milestones.deleterequest"""

    id: str


@dataclass
class _MilestonesInforequestBase:
    """Auto-generated from schema: milestones.inforequest"""

    id: str


@dataclass
class _MilestonesInforesponseBase:
    """Auto-generated from schema: milestones.inforesponse"""

    data: dict[str, Any] | None = None


@dataclass
class _MilestonesListrequestBase:
    """Auto-generated from schema: milestones.listrequest"""

    filter: dict[str, Any] | None = None
    page: dict[str, Any] | None = None
    sort: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class _MilestonesListresponseBase:
    """Auto-generated from schema: milestones.listresponse"""

    data: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class _MilestonesOpenrequestBase:
    """Auto-generated from schema: milestones.openrequest"""

    id: str


@dataclass
class _MilestonesUpdaterequestBase:
    """Auto-generated from schema: milestones.updaterequest"""

    id: str
    starts_on: str | None = None
    due_on: str | None = None
    name: str | None = None
    description: str | None = None
    responsible_user_id: str | None = None
    depends_on: str | None = None
    propagate_date_changes: bool | None = None
    custom_fields: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class _NotesCreaterequestBase:
    """Auto-generated from schema: notes.createrequest"""

    subject: dict[str, Any]
    content: str
    notify: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class _NotesCreateresponseBase:
    """Auto-generated from schema: notes.createresponse"""

    data: dict[str, Any] | None = None


@dataclass
class _NotesListrequestBase:
    """Auto-generated from schema: notes.listrequest"""

    filter: dict[str, Any]
    page: dict[str, Any] | None = None


@dataclass
class _NotesListresponseBase:
    """Auto-generated from schema: notes.listresponse"""

    data: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class _NotesUpdaterequestBase:
    """Auto-generated from schema: notes.updaterequest"""

    id: str
    content: str | None = None


@dataclass
class _OrdersInforequestBase:
    """Auto-generated from schema: orders.inforequest"""

    id: str
    includes: str | None = None


@dataclass
class _OrdersInforesponseBase:
    """Auto-generated from schema: orders.inforesponse"""

    data: dict[str, Any] | None = None


@dataclass
class _OrdersListrequestBase:
    """Auto-generated from schema: orders.listrequest"""

    filter: dict[str, Any] | None = None
    includes: str | None = None


@dataclass
class _OrdersListresponseBase:
    """Auto-generated from schema: orders.listresponse"""

    data: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class _PaymentmethodsListrequestBase:
    """Auto-generated from schema: paymentMethods.listrequest"""

    filter: dict[str, Any] | None = None
    page: dict[str, Any] | None = None


@dataclass
class _PaymentmethodsListresponseBase:
    """Auto-generated from schema: paymentMethods.listresponse"""

    data: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class _PaymenttermsListresponseBase:
    """Auto-generated from schema: paymentTerms.listresponse"""

    meta: dict[str, Any] | None = None
    data: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class _PlannableitemsInforequestBase:
    """Auto-generated from schema: plannableItems.inforequest"""

    id: str | None = None
    source: dict[str, Any] | None = None


@dataclass
class _PlannableitemsInforesponseBase:
    """Auto-generated from schema: plannableItems.inforesponse"""

    data: dict[str, Any] | None = None


@dataclass
class _PlannableitemsListrequestBase:
    """Auto-generated from schema: plannableItems.listrequest"""

    filter: dict[str, Any] | None = None
    page: dict[str, Any] | None = None
    sort: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class _PlannableitemsListresponseBase:
    """Auto-generated from schema: plannableItems.listresponse"""

    data: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class _PricelistsListrequestBase:
    """Auto-generated from schema: priceLists.listrequest"""

    filter: dict[str, Any] | None = None


@dataclass
class _PricelistsListresponseBase:
    """Auto-generated from schema: priceLists.listresponse"""

    data: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class _ProductcategoriesListrequestBase:
    """Auto-generated from schema: productCategories.listrequest"""

    filter: dict[str, Any] | None = None


@dataclass
class _ProductcategoriesListresponseBase:
    """Auto-generated from schema: productCategories.listresponse"""

    data: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class _ProductsAddrequestBase:
    """Auto-generated from schema: products.addrequest"""

    name: str | None = None
    code: str | None = None
    description: str | None = None
    purchase_price: dict[str, Any] | None = None
    selling_price: dict[str, Any] | None = None
    unit_of_measure_id: str | None = None
    stock: dict[str, Any] | None = None
    configuration: dict[str, Any] | None = None
    department_id: str | None = None
    product_category_id: str | None = None
    tax_rate_id: str | None = None
    price_list_prices: list[dict[str, Any]] = field(default_factory=list)
    custom_fields: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class _ProductsAddresponseBase:
    """Auto-generated from schema: products.addresponse"""

    data: dict[str, Any] | None = None


@dataclass
class _ProductsDeleterequestBase:
    """Auto-generated from schema: products.deleterequest"""

    id: str


@dataclass
class _ProductsInforequestBase:
    """Auto-generated from schema: products.inforequest"""

    id: str
    includes: str | None = None


@dataclass
class _ProductsInforesponseBase:
    """Auto-generated from schema: products.inforesponse"""

    data: dict[str, Any] | None = None


@dataclass
class _ProductsListrequestBase:
    """Auto-generated from schema: products.listrequest"""

    filter: dict[str, Any] | None = None
    page: dict[str, Any] | None = None


@dataclass
class _ProductsListresponseBase:
    """Auto-generated from schema: products.listresponse"""

    data: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class _ProductsUpdaterequestBase:
    """Auto-generated from schema: products.updaterequest"""

    id: str
    name: str | None = None
    code: str | None = None
    purchase_price: dict[str, Any] | None = None
    description: str | None = None
    selling_price: dict[str, Any] | None = None
    unit_of_measure_id: str | None = None
    stock: dict[str, Any] | None = None
    configuration: dict[str, Any] | None = None
    department_id: str | None = None
    product_category_id: str | None = None
    tax_rate_id: str | None = None
    price_list_prices: list[list[Any]] = field(default_factory=list)
    custom_fields: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class _ProjectsV2AddcustomerrequestBase:
    """Auto-generated from schema: projects-v2.addCustomerrequest"""

    id: str
    customer: dict[str, Any]


@dataclass
class _ProjectsV2AdddealrequestBase:
    """Auto-generated from schema: projects-v2.addDealrequest"""

    id: str
    deal_id: str


@dataclass
class _ProjectsV2AddownerrequestBase:
    """Auto-generated from schema: projects-v2.addOwnerrequest"""

    id: str
    user_id: str


@dataclass
class _ProjectsV2AddquotationrequestBase:
    """Auto-generated from schema: projects-v2.addQuotationrequest"""

    id: str
    quotation_id: str


@dataclass
class _ProjectsV2AssignrequestBase:
    """Auto-generated from schema: projects-v2.assignrequest"""

    id: str
    assignee: dict[str, Any]


@dataclass
class _ProjectsV2CloserequestBase:
    """Auto-generated from schema: projects-v2.closerequest"""

    id: str
    closing_strategy: str


@dataclass
class _ProjectsV2CreaterequestBase:
    """Auto-generated from schema: projects-v2.createrequest"""

    title: str
    description: str | None = None
    time_budget: dict[str, Any] | None = None
    billing_method: str | None = None
    external_budget: dict[str, Any] | None = None
    internal_budget: dict[str, Any] | None = None
    fixed_price: dict[str, Any] | None = None
    start_date: str | None = None
    end_date: str | None = None
    purchase_order_number: str | None = None
    company_entity_id: str | None = None
    color: dict[str, Any] | None = None
    initial_time_tracked: dict[str, Any] | None = None
    initial_price: dict[str, Any] | None = None
    initial_cost: dict[str, Any] | None = None
    initial_amount_billed: dict[str, Any] | None = None
    initial_amount_paid: dict[str, Any] | None = None
    owner_ids: list[str] = field(default_factory=list)
    customers: list[dict[str, Any]] = field(default_factory=list)
    assignees: list[dict[str, Any]] = field(default_factory=list)
    deal_ids: list[str] = field(default_factory=list)
    quotation_ids: list[str] = field(default_factory=list)
    custom_fields: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class _ProjectsV2DeleterequestBase:
    """Auto-generated from schema: projects-v2.deleterequest"""

    id: str
    delete_strategy: str


@dataclass
class _ProjectsV2DuplicaterequestBase:
    """Auto-generated from schema: projects-v2.duplicaterequest"""

    id: str
    title: str


@dataclass
class _ProjectsV2DuplicateresponseBase:
    """Auto-generated from schema: projects-v2.duplicateresponse"""

    data: dict[str, Any] | None = None


@dataclass
class _ProjectsV2InforequestBase:
    """Auto-generated from schema: projects-v2.inforequest"""

    id: str
    includes: str | None = None


@dataclass
class _ProjectsV2InforesponseBase:
    """Auto-generated from schema: projects.inforesponse1"""

    data: dict[str, Any] | None = None


@dataclass
class _ProjectsV2ListrequestBase:
    """Auto-generated from schema: projects-v2.listrequest"""

    filter: dict[str, Any] | None = None
    page: dict[str, Any] | None = None
    includes: str | None = None
    sort: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class _ProjectsV2ListresponseBase:
    """Auto-generated from schema: projects-v2.listresponse"""

    meta: dict[str, Any] | None = None
    data: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class _ProjectsV2RemovecustomerrequestBase:
    """Auto-generated from schema: projects-v2.removeCustomerrequest"""

    id: str
    customer: dict[str, Any]


@dataclass
class _ProjectsV2RemovedealrequestBase:
    """Auto-generated from schema: projects-v2.removeDealrequest"""

    id: str
    deal_id: str


@dataclass
class _ProjectsV2RemoveownerrequestBase:
    """Auto-generated from schema: projects-v2.removeOwnerrequest"""

    id: str
    user_id: str


@dataclass
class _ProjectsV2RemovequotationrequestBase:
    """Auto-generated from schema: projects-v2.removeQuotationrequest"""

    id: str
    quotation_id: str


@dataclass
class _ProjectsV2UnassignrequestBase:
    """Auto-generated from schema: projects-v2.unassignrequest"""

    id: str
    assignee: dict[str, Any]


@dataclass
class _ProjectsV2UpdaterequestBase:
    """Auto-generated from schema: projects-v2.updaterequest"""

    id: str
    title: str | None = None
    description: str | None = None
    time_budget: dict[str, Any] | None = None
    billing_method: dict[str, Any] | None = None
    external_budget: dict[str, Any] | None = None
    internal_budget: dict[str, Any] | None = None
    fixed_price: dict[str, Any] | None = None
    start_date: str | None = None
    end_date: str | None = None
    purchase_order_number: str | None = None
    company_entity_id: str | None = None
    color: dict[str, Any] | None = None
    custom_fields: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class _ProjectsV2_externalpartiesAddtoprojectrequestBase:
    """Auto-generated from schema: projects-v2_externalParties.addToProjectrequest"""

    project_id: str
    customer: dict[str, Any]
    function: str | None = None
    sub_function: str | None = None


@dataclass
class _ProjectsV2_externalpartiesDeleterequestBase:
    """Auto-generated from schema: projects-v2_externalParties.deleterequest"""

    id: str


@dataclass
class _ProjectsV2_externalpartiesUpdaterequestBase:
    """Auto-generated from schema: projects-v2_externalParties.updaterequest"""

    id: str
    customer: dict[str, Any] | None = None
    function: str | None = None
    sub_function: str | None = None


@dataclass
class _ProjectsV2_materialsAssignrequestBase:
    """Auto-generated from schema: projects-v2_materials.assignrequest"""

    id: str
    assignee: dict[str, Any]


@dataclass
class _ProjectsV2_materialsCreaterequestBase:
    """Auto-generated from schema: projects-v2_materials.createrequest"""

    project_id: str
    title: str
    group_id: str | None = None
    after_id: str | None = None
    description: str | None = None
    billing_method: str | None = None
    quantity: float | None = None
    quantity_estimated: float | None = None
    unit_price: dict[str, Any] | None = None
    unit_cost: dict[str, Any] | None = None
    unit_id: str | None = None
    fixed_price: dict[str, Any] | None = None
    external_budget: dict[str, Any] | None = None
    internal_budget: dict[str, Any] | None = None
    start_date: str | None = None
    end_date: str | None = None
    product_id: str | None = None
    assignees: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class _ProjectsV2_materialsCreateresponseBase:
    """Auto-generated from schema: projects-v2_materials.createresponse"""

    data: dict[str, Any] | None = None


@dataclass
class _ProjectsV2_materialsDeleterequestBase:
    """Auto-generated from schema: projects-v2_materials.deleterequest"""

    id: str


@dataclass
class _ProjectsV2_materialsDuplicaterequestBase:
    """Auto-generated from schema: projects-v2_materials.duplicaterequest"""

    origin_id: str


@dataclass
class _ProjectsV2_materialsDuplicateresponseBase:
    """Auto-generated from schema: projects-v2_materials.duplicateresponse"""

    data: dict[str, Any] | None = None


@dataclass
class _ProjectsV2_materialsInforequestBase:
    """Auto-generated from schema: projects-v2_materials.inforequest"""

    id: str


@dataclass
class _ProjectsV2_materialsInforesponseBase:
    """Auto-generated from schema: projects-v2_materials.inforesponse"""

    data: dict[str, Any] | None = None


@dataclass
class _ProjectsV2_materialsListrequestBase:
    """Auto-generated from schema: projects-v2_materials.listrequest"""

    filter: dict[str, Any] | None = None


@dataclass
class _ProjectsV2_materialsListresponseBase:
    """Auto-generated from schema: projects-v2_materials.listresponse"""

    data: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class _ProjectsV2_materialsUnassignrequestBase:
    """Auto-generated from schema: projects-v2_materials.unassignrequest"""

    id: str
    assignee: dict[str, Any]


@dataclass
class _ProjectsV2_materialsUpdaterequestBase:
    """Auto-generated from schema: projects-v2_materials.updaterequest"""

    id: str
    title: str | None = None
    description: str | None = None
    status: str | None = None
    billing_method: str | None = None
    quantity: float | None = None
    quantity_estimated: float | None = None
    unit_price: dict[str, Any] | None = None
    unit_cost: dict[str, Any] | None = None
    unit_id: str | None = None
    fixed_price: dict[str, Any] | None = None
    external_budget: dict[str, Any] | None = None
    internal_budget: dict[str, Any] | None = None
    start_date: str | None = None
    end_date: str | None = None
    product_id: str | None = None


@dataclass
class _ProjectsV2_projectgroupsAssignrequestBase:
    """Auto-generated from schema: projects-v2_projectGroups.assignrequest"""

    id: str
    assignee: dict[str, Any]


@dataclass
class _ProjectsV2_projectgroupsCreaterequestBase:
    """Auto-generated from schema: projects-v2_projectGroups.createrequest"""

    project_id: str
    title: str
    description: str | None = None
    color: dict[str, Any] | None = None
    billing_method: str | None = None
    fixed_price: dict[str, Any] | None = None
    external_budget: dict[str, Any] | None = None
    internal_budget: dict[str, Any] | None = None
    start_date: str | None = None
    end_date: str | None = None
    assignees: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class _ProjectsV2_projectgroupsCreateresponseBase:
    """Auto-generated from schema: projects-v2_projectGroups.createresponse"""

    data: dict[str, Any] | None = None


@dataclass
class _ProjectsV2_projectgroupsDeleterequestBase:
    """Auto-generated from schema: projects-v2_projectGroups.deleterequest"""

    id: str
    delete_strategy: str


@dataclass
class _ProjectsV2_projectgroupsDuplicaterequestBase:
    """Auto-generated from schema: projects-v2_projectGroups.duplicaterequest"""

    origin_id: str


@dataclass
class _ProjectsV2_projectgroupsDuplicateresponseBase:
    """Auto-generated from schema: projects-v2_projectGroups.duplicateresponse"""

    data: dict[str, Any] | None = None


@dataclass
class _ProjectsV2_projectgroupsInforequestBase:
    """Auto-generated from schema: projects-v2_projectGroups.inforequest"""

    id: str


@dataclass
class _ProjectsV2_projectgroupsInforesponseBase:
    """Auto-generated from schema: projects-v2_projectGroups.inforesponse"""

    data: dict[str, Any] | None = None


@dataclass
class _ProjectsV2_projectgroupsListrequestBase:
    """Auto-generated from schema: projects-v2_projectGroups.listrequest"""

    filter: dict[str, Any] | None = None


@dataclass
class _ProjectsV2_projectgroupsListresponseBase:
    """Auto-generated from schema: projects-v2_projectGroups.listresponse"""

    data: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class _ProjectsV2_projectgroupsUnassignrequestBase:
    """Auto-generated from schema: projects-v2_projectGroups.unassignrequest"""

    id: str
    assignee: dict[str, Any]


@dataclass
class _ProjectsV2_projectgroupsUpdaterequestBase:
    """Auto-generated from schema: projects-v2_projectGroups.updaterequest"""

    id: str
    title: str | None = None
    description: str | None = None
    color: dict[str, Any] | None = None
    billing_method: dict[str, Any] | None = None
    fixed_price: dict[str, Any] | None = None
    external_budget: dict[str, Any] | None = None
    internal_budget: dict[str, Any] | None = None
    start_date: str | None = None
    end_date: str | None = None


@dataclass
class _ProjectsV2_projectlinesAddtogrouprequestBase:
    """Auto-generated from schema: projects-v2_projectLines.addToGrouprequest"""

    line_id: str
    group_id: str


@dataclass
class _ProjectsV2_projectlinesListrequestBase:
    """Auto-generated from schema: projects-v2_projectLines.listrequest"""

    project_id: str
    filter: dict[str, Any] | None = None


@dataclass
class _ProjectsV2_projectlinesListresponseBase:
    """Auto-generated from schema: projects-v2_projectLines.listresponse"""

    data: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class _ProjectsV2_projectlinesRemovefromgrouprequestBase:
    """Auto-generated from schema: projects-v2_projectLines.removeFromGrouprequest"""

    line_id: str


@dataclass
class _ProjectsV2_tasksAssignrequestBase:
    """Auto-generated from schema: projects-v2_tasks.assignrequest"""

    id: str
    assignee: dict[str, Any]


@dataclass
class _ProjectsV2_tasksCreaterequestBase:
    """Auto-generated from schema: projects-v2_tasks.createrequest"""

    project_id: str
    title: str
    group_id: str | None = None
    work_type_id: str | None = None
    task_type_id: str | None = None
    description: str | None = None
    billing_method: str | None = None
    fixed_price: dict[str, Any] | None = None
    external_budget: dict[str, Any] | None = None
    internal_budget: dict[str, Any] | None = None
    custom_rate: dict[str, Any] | None = None
    start_date: str | None = None
    end_date: str | None = None
    time_estimated: dict[str, Any] | None = None
    assignees: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class _ProjectsV2_tasksDeleterequestBase:
    """Auto-generated from schema: projects-v2_tasks.deleterequest"""

    id: str
    delete_strategy: str


@dataclass
class _ProjectsV2_tasksDuplicaterequestBase:
    """Auto-generated from schema: projects-v2_tasks.duplicaterequest"""

    origin_id: str


@dataclass
class _ProjectsV2_tasksDuplicateresponseBase:
    """Auto-generated from schema: projects-v2_tasks.duplicateresponse"""

    data: dict[str, Any] | None = None


@dataclass
class _ProjectsV2_tasksInforesponseBase:
    """Auto-generated from schema: projects-v2_tasks.inforesponse"""

    data: dict[str, Any] | None = None


@dataclass
class _ProjectsV2_tasksListrequestBase:
    """Auto-generated from schema: projects-v2_tasks.listrequest"""

    filter: dict[str, Any] | None = None
    page: dict[str, Any] | None = None


@dataclass
class _ProjectsV2_tasksListresponseBase:
    """Auto-generated from schema: projects-v2_tasks.listresponse"""

    data: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class _ProjectsV2_tasksUnassignrequestBase:
    """Auto-generated from schema: projects-v2_tasks.unassignrequest"""

    id: str
    assignee: dict[str, Any]


@dataclass
class _ProjectsV2_tasksUpdaterequestBase:
    """Auto-generated from schema: projects-v2_tasks.updaterequest"""

    id: str
    work_type_id: str | None = None
    task_type_id: str | None = None
    status: str | None = None
    title: str | None = None
    description: str | None = None
    billing_method: str | None = None
    fixed_price: dict[str, Any] | None = None
    external_budget: dict[str, Any] | None = None
    internal_budget: dict[str, Any] | None = None
    custom_rate: dict[str, Any] | None = None
    start_date: str | None = None
    end_date: str | None = None
    time_estimated: dict[str, Any] | None = None


@dataclass
class _ProjectsAddparticipantrequestBase:
    """Auto-generated from schema: projects.addParticipantrequest"""

    id: str
    participant: dict[str, Any]
    role: str | None = None


@dataclass
class _ProjectsCloserequestBase:
    """Auto-generated from schema: projects.closerequest"""

    id: str


@dataclass
class _ProjectsCreaterequestBase:
    """Auto-generated from schema: projects.createrequest"""

    title: str
    starts_on: str
    description: str | None = None
    purchase_order_number: str | None = None
    customer: dict[str, Any] | None = None
    milestones: list[dict[str, Any]] = field(default_factory=list)
    participants: list[dict[str, Any]] = field(default_factory=list)
    custom_fields: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class _ProjectsCreateresponseBase:
    """Auto-generated from schema: projects.createresponse"""

    data: dict[str, Any] | None = None


@dataclass
class _ProjectsDeleterequestBase:
    """Auto-generated from schema: projects.deleterequest"""

    id: str


@dataclass
class _ProjectsInforequestBase:
    """Auto-generated from schema: projects.inforequest"""

    id: str


@dataclass
class _ProjectsInforesponseBase:
    """Auto-generated from schema: projects.inforesponse"""

    data: dict[str, Any] | None = None


@dataclass
class _ProjectsListrequestBase:
    """Auto-generated from schema: projects.listrequest"""

    filter: dict[str, Any] | None = None
    page: dict[str, Any] | None = None
    sort: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class _ProjectsListresponseBase:
    """Auto-generated from schema: projects.listresponse"""

    data: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class _ProjectsReopenrequestBase:
    """Auto-generated from schema: projects.reopenrequest"""

    id: str


@dataclass
class _ProjectsUpdateparticipantrequestBase:
    """Auto-generated from schema: projects.updateParticipantrequest"""

    id: str
    role: str
    participant: dict[str, Any] | None = None


@dataclass
class _ProjectsUpdaterequestBase:
    """Auto-generated from schema: projects.updaterequest"""

    id: str
    title: str | None = None
    description: str | None = None
    status: str | None = None
    starts_on: str | None = None
    customer: dict[str, Any] | None = None
    budget: dict[str, Any] | None = None
    purchase_order_number: str | None = None
    custom_fields: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class _QuotationsAcceptrequestBase:
    """Auto-generated from schema: quotations.acceptrequest"""

    id: str


@dataclass
class _QuotationsCreaterequestBase:
    """Auto-generated from schema: quotations.createrequest"""

    deal_id: str
    currency: dict[str, Any] | None = None
    text: str | None = None
    document_template_id: str | None = None
    expiry: dict[str, Any] | None = None
    grouped_lines: list[dict[str, Any]] = field(default_factory=list)
    discounts: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class _QuotationsCreateresponseBase:
    """Auto-generated from schema: quotations.createresponse"""

    data: dict[str, Any] | None = None


@dataclass
class _QuotationsDeleterequestBase:
    """Auto-generated from schema: quotations.deleterequest"""

    id: str


@dataclass
class _QuotationsDownloadrequestBase:
    """Auto-generated from schema: quotations.downloadrequest"""

    id: str
    format: str


@dataclass
class _QuotationsDownloadresponseBase:
    """Auto-generated from schema: quotations.downloadresponse"""

    data: dict[str, Any] | None = None


@dataclass
class _QuotationsInforequestBase:
    """Auto-generated from schema: quotations.inforequest"""

    id: str


@dataclass
class _QuotationsInforesponseBase:
    """Auto-generated from schema: quotations.inforesponse"""

    data: dict[str, Any] | None = None


@dataclass
class _QuotationsListrequestBase:
    """Auto-generated from schema: quotations.listrequest"""

    filter: dict[str, Any] | None = None
    page: dict[str, Any] | None = None


@dataclass
class _QuotationsListresponseBase:
    """Auto-generated from schema: quotations.listresponse"""

    data: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class _QuotationsSendrequestBase:
    """Auto-generated from schema: quotations.sendrequest"""

    recipients: dict[str, Any]
    subject: str
    content: str
    language: str
    from_: dict[str, Any] | None = None
    quotations: list[str] = field(default_factory=list)
    attachments: list[str] = field(default_factory=list)


@dataclass
class _QuotationsUpdaterequestBase:
    """Auto-generated from schema: quotations.updaterequest"""

    id: str
    currency: dict[str, Any] | None = None
    text: str | None = None
    document_template_id: str | None = None
    expiry: dict[str, Any] | None = None
    grouped_lines: list[dict[str, Any]] = field(default_factory=list)
    discounts: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class _ReceiptsListpaymentsrequestBase:
    """Auto-generated from schema: receipts.listPaymentsrequest"""

    id: str


@dataclass
class _ReceiptsListpaymentsresponseBase:
    """Auto-generated from schema: receipts.listPaymentsresponse"""

    meta: dict[str, Any] | None = None
    data: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class _ReceiptsRegisterpaymentrequestBase:
    """Auto-generated from schema: receipts.registerPaymentrequest"""

    id: str
    payment: dict[str, Any]
    paid_at: str
    payment_method_id: str | None = None
    remark: str | None = None


@dataclass
class _ReceiptsRegisterpaymentresponseBase:
    """Auto-generated from schema: receipts.registerPaymentresponse"""

    data: dict[str, Any] | None = None


@dataclass
class _ReceiptsRemovepaymentrequestBase:
    """Auto-generated from schema: receipts.removePaymentrequest"""

    id: str
    payment_id: str


@dataclass
class _ReceiptsUpdatepaymentrequestBase:
    """Auto-generated from schema: receipts.updatePaymentrequest"""

    id: str
    payment_id: str
    payment: dict[str, Any] | None = None
    paid_at: str | None = None
    payment_method_id: str | None = None
    remark: str | None = None


@dataclass
class _ReservationsCreaterequestBase:
    """Auto-generated from schema: reservations.createrequest"""

    plannable_item_id: str
    date: str
    duration: dict[str, Any]
    assignee: dict[str, Any]


@dataclass
class _ReservationsCreateresponseBase:
    """Auto-generated from schema: reservations.createresponse"""

    data: dict[str, Any] | None = None


@dataclass
class _ReservationsDeleterequestBase:
    """Auto-generated from schema: reservations.deleterequest"""

    id: str


@dataclass
class _ReservationsListrequestBase:
    """Auto-generated from schema: reservations.listrequest"""

    filter: dict[str, Any] | None = None
    page: dict[str, Any] | None = None


@dataclass
class _ReservationsListresponseBase:
    """Auto-generated from schema: reservations.listresponse"""

    data: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class _ReservationsUpdaterequestBase:
    """Auto-generated from schema: reservations.updaterequest"""

    id: str
    date: str | None = None
    duration: dict[str, Any] | None = None
    assignee: dict[str, Any] | None = None


@dataclass
class _SubscriptionsCreaterequestBase:
    """Auto-generated from schema: subscriptions.createrequest"""

    invoicee: dict[str, Any]
    department_id: str
    starts_on: str
    billing_cycle: dict[str, Any]
    title: str
    payment_term: dict[str, Any]
    invoice_generation: dict[str, Any]
    ends_on: str | None = None
    deal_id: str | None = None
    project_id: str | None = None
    note: str | None = None
    document_template_id: str | None = None
    grouped_lines: list[dict[str, Any]] = field(default_factory=list)
    custom_fields: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class _SubscriptionsCreateresponseBase:
    """Auto-generated from schema: subscriptions.createresponse"""

    data: dict[str, Any] | None = None


@dataclass
class _SubscriptionsDeactivaterequestBase:
    """Auto-generated from schema: subscriptions.deactivaterequest"""

    id: str


@dataclass
class _SubscriptionsInforequestBase:
    """Auto-generated from schema: subscriptions.inforequest"""

    id: str


@dataclass
class _SubscriptionsInforesponseBase:
    """Auto-generated from schema: subscriptions.inforesponse"""

    data: dict[str, Any] | None = None


@dataclass
class _SubscriptionsListrequestBase:
    """Auto-generated from schema: subscriptions.listrequest"""

    filter: dict[str, Any] | None = None
    page: dict[str, Any] | None = None
    sort: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class _SubscriptionsListresponseBase:
    """Auto-generated from schema: subscriptions.listresponse"""

    data: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class _SubscriptionsUpdaterequestBase:
    """Auto-generated from schema: subscriptions.updaterequest"""

    id: str
    starts_on: str | None = None
    billing_cycle: dict[str, Any] | None = None
    ends_on: str | None = None
    title: str | None = None
    invoicee: dict[str, Any] | None = None
    department_id: str | None = None
    payment_term: dict[str, Any] | None = None
    project_id: str | None = None
    deal_id: str | None = None
    note: str | None = None
    invoice_generation: dict[str, Any] | None = None
    document_template_id: str | None = None
    grouped_lines: list[dict[str, Any]] = field(default_factory=list)
    custom_fields: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class _TagsListrequestBase:
    """Auto-generated from schema: tags.listrequest"""

    page: dict[str, Any] | None = None
    sort: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class _TagsListresponseBase:
    """Auto-generated from schema: tags.listresponse"""

    data: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class _TasksCompleterequestBase:
    """Auto-generated from schema: tasks.completerequest"""

    id: str


@dataclass
class _TasksCreaterequestBase:
    """Auto-generated from schema: tasks.createrequest1"""

    title: str
    due_on: str
    work_type_id: str
    description: str | None = None
    milestone_id: str | None = None
    project_id: str | None = None
    deal_id: str | None = None
    ticket_id: str | None = None
    estimated_duration: dict[str, Any] | None = None
    assignee: dict[str, Any] | None = None
    customer: dict[str, Any] | None = None
    custom_fields: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class _TasksCreateresponseBase:
    """Auto-generated from schema: tasks.createresponse"""

    data: dict[str, Any] | None = None


@dataclass
class _TasksDeleterequestBase:
    """Auto-generated from schema: tasks.deleterequest1"""

    id: str


@dataclass
class _TasksInforequestBase:
    """Auto-generated from schema: tasks.inforequest"""

    id: str


@dataclass
class _TasksInforesponseBase:
    """Auto-generated from schema: tasks.inforesponse1"""

    data: dict[str, Any] | None = None


@dataclass
class _TasksListrequestBase:
    """Auto-generated from schema: tasks.listrequest1"""

    filter: dict[str, Any] | None = None
    page: dict[str, Any] | None = None
    sort: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class _TasksListresponseBase:
    """Auto-generated from schema: tasks.listresponse1"""

    data: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class _TasksReopenrequestBase:
    """Auto-generated from schema: tasks.reopenrequest"""

    id: str


@dataclass
class _TasksSchedulerequestBase:
    """Auto-generated from schema: tasks.schedulerequest"""

    id: str
    starts_at: str
    ends_at: str


@dataclass
class _TasksScheduleresponseBase:
    """Auto-generated from schema: tasks.scheduleresponse"""

    data: dict[str, Any] | None = None


@dataclass
class _TasksUpdaterequestBase:
    """Auto-generated from schema: tasks.updaterequest1"""

    id: str
    title: str | None = None
    description: str | None = None
    due_on: str | None = None
    work_type_id: str | None = None
    milestone_id: str | None = None
    project_id: str | None = None
    deal_id: str | None = None
    ticket_id: str | None = None
    estimated_duration: dict[str, Any] | None = None
    assignee: dict[str, Any] | None = None
    customer: dict[str, Any] | None = None
    custom_fields: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class _TaxratesListrequestBase:
    """Auto-generated from schema: taxRates.listrequest"""

    filter: dict[str, Any] | None = None
    page: dict[str, Any] | None = None
    sort: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class _TaxratesListresponseBase:
    """Auto-generated from schema: taxRates.listresponse"""

    data: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class _TeamsListrequestBase:
    """Auto-generated from schema: teams.listrequest"""

    filter: dict[str, Any] | None = None
    sort: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class _TeamsListresponseBase:
    """Auto-generated from schema: teams.listresponse"""

    data: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class _TicketstatusListrequestBase:
    """Auto-generated from schema: ticketStatus.listrequest"""

    filter: dict[str, Any] | None = None


@dataclass
class _TicketstatusListresponseBase:
    """Auto-generated from schema: ticketStatus.listresponse"""

    data: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class _TicketsAddinternalmessagerequestBase:
    """Auto-generated from schema: tickets.addInternalMessagerequest"""

    id: str
    body: str
    ticket_status_id: str | None = None
    attachments: list[str] = field(default_factory=list)


@dataclass
class _TicketsAddinternalmessageresponseBase:
    """Auto-generated from schema: tickets.addInternalMessageresponse"""

    data: dict[str, Any] | None = None


@dataclass
class _TicketsAddreplyrequestBase:
    """Auto-generated from schema: tickets.addReplyrequest"""

    id: str
    body: str
    ticket_status_id: str | None = None
    attachments: list[str] = field(default_factory=list)


@dataclass
class _TicketsAddreplyresponseBase:
    """Auto-generated from schema: tickets.addReplyresponse"""

    data: dict[str, Any] | None = None


@dataclass
class _TicketsCreaterequestBase:
    """Auto-generated from schema: tickets.createrequest"""

    subject: str
    customer: dict[str, Any]
    ticket_status_id: str
    assignee: dict[str, Any] | None = None
    description: str | None = None
    participant: dict[str, Any] | None = None
    initial_reply: str | None = None
    milestone_id: str | None = None
    custom_fields: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class _TicketsCreateresponseBase:
    """Auto-generated from schema: tickets.createresponse"""

    data: dict[str, Any] | None = None


@dataclass
class _TicketsGetmessagerequestBase:
    """Auto-generated from schema: tickets.getMessagerequest"""

    message_id: str | None = None


@dataclass
class _TicketsGetmessageresponseBase:
    """Auto-generated from schema: tickets.getMessageresponse"""

    message_id: str | None = None
    body: str | None = None
    raw_body: str | None = None
    created_at: str | None = None
    sent_by: dict[str, Any] | None = None
    ticket: dict[str, Any] | None = None
    type: str | None = None
    attachments: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class _TicketsImportmessagerequestBase:
    """Auto-generated from schema: tickets.importMessagerequest"""

    id: str
    body: str
    sent_by: dict[str, Any]
    sent_at: str
    attachments: list[str] = field(default_factory=list)


@dataclass
class _TicketsImportmessageresponseBase:
    """Auto-generated from schema: tickets.importMessageresponse"""

    data: dict[str, Any] | None = None


@dataclass
class _TicketsInforequestBase:
    """Auto-generated from schema: tickets.inforequest"""

    id: str


@dataclass
class _TicketsInforesponseBase:
    """Auto-generated from schema: tickets.inforesponse"""

    id: str | None = None
    reference: float | None = None
    subject: str | None = None
    status: dict[str, Any] | None = None
    assignee: dict[str, Any] | None = None
    created_at: str | None = None
    closed_at: str | None = None
    customer: dict[str, Any] | None = None
    participant: dict[str, Any] | None = None
    last_message_at: str | None = None
    description: str | None = None
    project: dict[str, Any] | None = None
    milestone: dict[str, Any] | None = None
    custom_fields: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class _TicketsListmessagesrequestBase:
    """Auto-generated from schema: tickets.listMessagesrequest"""

    id: str | None = None
    filter: dict[str, Any] | None = None
    page: dict[str, Any] | None = None


@dataclass
class _TicketsListmessagesresponseBase:
    """Auto-generated from schema: tickets.listMessagesresponse"""

    meta: dict[str, Any] | None = None
    data: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class _TicketsListrequestBase:
    """Auto-generated from schema: tickets.listrequest"""

    filter: dict[str, Any] | None = None
    page: dict[str, Any] | None = None


@dataclass
class _TicketsListresponseBase:
    """Auto-generated from schema: tickets.listresponse"""

    data: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class _TicketsUpdaterequestBase:
    """Auto-generated from schema: tickets.updaterequest"""

    id: str
    subject: str | None = None
    description: str | None = None
    ticket_status_id: str | None = None
    customer: dict[str, Any] | None = None
    assignee: dict[str, Any] | None = None
    participant: dict[str, Any] | None = None
    milestone_id: str | None = None
    custom_fields: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class _TimetrackingAddresponseBase:
    """Auto-generated from schema: timeTracking.addresponse"""

    data: dict[str, Any] | None = None


@dataclass
class _TimetrackingDeleterequestBase:
    """Auto-generated from schema: timeTracking.deleterequest"""

    id: str


@dataclass
class _TimetrackingInforequestBase:
    """Auto-generated from schema: timeTracking.inforequest"""

    id: str
    includes: str | None = None


@dataclass
class _TimetrackingInforesponseBase:
    """Auto-generated from schema: timeTracking.inforesponse"""

    data: dict[str, Any] | None = None
    meta: dict[str, Any] | None = None


@dataclass
class _TimetrackingListrequestBase:
    """Auto-generated from schema: timeTracking.listrequest"""

    filter: dict[str, Any] | None = None
    page: dict[str, Any] | None = None
    includes: str | None = None
    sort: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class _TimetrackingListresponseBase:
    """Auto-generated from schema: timeTracking.listresponse"""

    data: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class _TimetrackingResumerequestBase:
    """Auto-generated from schema: timeTracking.resumerequest"""

    id: str
    started_at: str | None = None


@dataclass
class _TimetrackingResumeresponseBase:
    """Auto-generated from schema: timeTracking.resumeresponse"""

    data: dict[str, Any] | None = None


@dataclass
class _TimersCurrentresponseBase:
    """Auto-generated from schema: timers.currentresponse"""

    data: dict[str, Any] | None = None


@dataclass
class _TimersStartrequestBase:
    """Auto-generated from schema: timers.startrequest"""

    work_type_id: str | None = None
    started_at: str | None = None
    description: str | None = None
    subject: dict[str, Any] | None = None
    invoiceable: bool | None = None


@dataclass
class _TimersStartresponseBase:
    """Auto-generated from schema: timers.startresponse"""

    data: dict[str, Any] | None = None


@dataclass
class _TimersStopresponseBase:
    """Auto-generated from schema: timers.stopresponse"""

    data: dict[str, Any] | None = None


@dataclass
class _TimersUpdaterequestBase:
    """Auto-generated from schema: timers.updaterequest"""

    work_type_id: str | None = None
    started_at: str | None = None
    description: str | None = None
    subject: dict[str, Any] | None = None
    invoiceable: bool | None = None


@dataclass
class _UnitsofmeasureListresponseBase:
    """Auto-generated from schema: unitsOfMeasure.listresponse"""

    data: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class _UseravailabilityDailyrequestBase:
    """Auto-generated from schema: userAvailability.dailyrequest"""

    period: dict[str, Any]
    filter: dict[str, Any] | None = None
    page: dict[str, Any] | None = None


@dataclass
class _UseravailabilityDailyresponseBase:
    """Auto-generated from schema: userAvailability.dailyresponse"""

    data: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class _UseravailabilityTotalrequestBase:
    """Auto-generated from schema: userAvailability.totalrequest"""

    period: dict[str, Any]
    filter: dict[str, Any] | None = None
    page: dict[str, Any] | None = None


@dataclass
class _UseravailabilityTotalresponseBase:
    """Auto-generated from schema: userAvailability.totalresponse"""

    data: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class _UsersGetweekschedulerequestBase:
    """Auto-generated from schema: users.getWeekSchedulerequest"""

    id: str


@dataclass
class _UsersGetweekscheduleresponseBase:
    """Auto-generated from schema: users.getWeekScheduleresponse"""

    data: dict[str, Any] | None = None


@dataclass
class _UsersInforequestBase:
    """Auto-generated from schema: users.inforequest"""

    id: str
    includes: str | None = None


@dataclass
class _UsersInforesponseBase:
    """Auto-generated from schema: users.inforesponse"""

    data: dict[str, Any] | None = None


@dataclass
class _UsersListdaysoffrequestBase:
    """Auto-generated from schema: users.listDaysOffrequest"""

    id: str
    filter: dict[str, Any] | None = None
    page: dict[str, Any] | None = None


@dataclass
class _UsersListdaysoffresponseBase:
    """Auto-generated from schema: users.listDaysOffresponse"""

    meta: dict[str, Any] | None = None
    data: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class _UsersListrequestBase:
    """Auto-generated from schema: users.listrequest"""

    filter: dict[str, Any] | None = None
    page: dict[str, Any] | None = None
    sort: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class _UsersListresponseBase:
    """Auto-generated from schema: users.listresponse"""

    data: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class _UsersMeresponseBase:
    """Auto-generated from schema: users.meresponse"""

    data: dict[str, Any] | None = None


@dataclass
class _WebhooksListresponseBase:
    """Auto-generated from schema: webhooks.listresponse"""

    data: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class _WithholdingtaxratesListrequestBase:
    """Auto-generated from schema: withholdingTaxRates.listrequest"""

    filter: dict[str, Any] | None = None


@dataclass
class _WithholdingtaxratesListresponseBase:
    """Auto-generated from schema: withholdingTaxRates.listresponse"""

    data: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class _WorktypesListrequestBase:
    """Auto-generated from schema: workTypes.listrequest"""

    filter: dict[str, Any] | None = None
    page: dict[str, Any] | None = None
    sort: dict[str, Any] | None = None


@dataclass
class _WorktypesListresponseBase:
    """Auto-generated from schema: workTypes.listresponse"""

    data: list[dict[str, Any]] = field(default_factory=list)

