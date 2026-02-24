# ============================================================
# AUTO-GENERATED — DO NOT EDIT BY HAND
# Run `python codegen/generate.py` to regenerate.
# Spec version: 1.112.0
# Generated at: 2026-02-24T13:41:23Z
# ============================================================

from __future__ import annotations

from enum import Enum


class Billingstatus(str, Enum):
    """Auto-generated from schema: BillingStatus"""

    NOT_BILLABLE = 'not_billable'
    NOT_BILLED = 'not_billed'
    PARTIALLY_BILLED = 'partially_billed'
    FULLY_BILLED = 'fully_billed'


class Color(str, Enum):
    """Auto-generated from schema: Color"""

    VALUE_00B2B2 = '#00B2B2'
    VALUE_008A8C = '#008A8C'
    VALUE_992600 = '#992600'
    ED9E00 = '#ED9E00'
    D157D3 = '#D157D3'
    A400B2 = '#A400B2'
    VALUE_0071F2 = '#0071F2'
    VALUE_004DA6 = '#004DA6'
    VALUE_64788F = '#64788F'
    C0C0C4 = '#C0C0C4'
    VALUE_82828C = '#82828C'
    VALUE_1A1C20 = '#1A1C20'


class Context(str, Enum):
    """Auto-generated from schema: Context"""

    CONTACT = 'contact'
    COMPANY = 'company'
    DEAL = 'deal'
    PROJECT = 'project'
    MILESTONE = 'milestone'
    PRODUCT = 'product'
    INVOICE = 'invoice'
    SUBSCRIPTION = 'subscription'
    TICKET = 'ticket'


class Creditnotedownloadformat(str, Enum):
    """Auto-generated from schema: Format"""

    PDF = 'pdf'
    UBL_E_FFF = 'ubl/e-fff'


class Currencycode(str, Enum):
    """Auto-generated from schema: CurrencyCode"""

    BAM = 'BAM'
    CAD = 'CAD'
    CHF = 'CHF'
    CLP = 'CLP'
    CNY = 'CNY'
    COP = 'COP'
    CZK = 'CZK'
    DKK = 'DKK'
    EUR = 'EUR'
    GBP = 'GBP'
    INR = 'INR'
    ISK = 'ISK'
    JPY = 'JPY'
    MAD = 'MAD'
    MXN = 'MXN'
    NOK = 'NOK'
    PEN = 'PEN'
    PLN = 'PLN'
    RON = 'RON'
    SEK = 'SEK'
    TRY_ = 'TRY'
    USD = 'USD'
    ZAR = 'ZAR'


class Customfielddefinitiontype(str, Enum):
    """Auto-generated from schema: CustomFieldDefinitionType"""

    SINGLE_LINE = 'single_line'
    MULTI_LINE = 'multi_line'
    SINGLE_SELECT = 'single_select'
    MULTI_SELECT = 'multi_select'
    DATE = 'date'
    MONEY = 'money'
    AUTO_INCREMENT = 'auto_increment'
    INTEGER = 'integer'
    NUMBER = 'number'
    BOOLEAN = 'boolean'
    EMAIL = 'email'
    TELEPHONE = 'telephone'
    URL = 'url'
    COMPANY = 'company'
    CONTACT = 'contact'
    PRODUCT = 'product'
    USER = 'user'


class Documenttype(str, Enum):
    """Auto-generated from schema: DocumentType"""

    DELIVERY_NOTE = 'delivery_note'
    INVOICE = 'invoice'
    ORDER = 'order'
    ORDER_CONFIRMATION = 'order_confirmation'
    QUOTATION = 'quotation'
    TIMETRACKING_REPORT = 'timetracking_report'
    WORKORDER = 'workorder'


class Emailtrackingsubjecttypes(str, Enum):
    """Auto-generated from schema: EmailTrackingSubjectTypes"""

    CONTACT = 'contact'
    COMPANY = 'company'
    DEAL = 'deal'
    INVOICE = 'invoice'
    CREDITNOTE = 'creditNote'
    SUBSCRIPTION = 'subscription'
    PRODUCT = 'product'
    QUOTATION = 'quotation'
    NEXTGENPROJECT = 'nextgenProject'


class Followupactions(str, Enum):
    """Auto-generated from schema: FollowUpActions"""

    CREATE_EVENT = 'create_event'
    CREATE_CALL = 'create_call'
    CREATE_TASK = 'create_task'


class Gender(str, Enum):
    """Auto-generated from schema: Gender"""

    FEMALE = 'female'
    MALE = 'male'
    NON_BINARY = 'non_binary'
    PREFERS_NOT_TO_SAY = 'prefers_not_to_say'
    UNKNOWN = 'unknown'


class Invoicedownloadformat(str, Enum):
    """Auto-generated from schema: Format"""

    PDF = 'pdf'
    UBL_E_FFF = 'ubl/e-fff'
    UBL_PEPPOL_BIS_3 = 'ubl/peppol_bis_3'


class Mimetype(str, Enum):
    """Auto-generated from schema: MimeType"""

    APPLICATION_MSWORD = 'application/msword'
    APPLICATION_OCTET_STREAM = 'application/octet-stream'
    APPLICATION_PDF = 'application/pdf'
    APPLICATION_VND_MS_EXCEL = 'application/vnd.ms-excel'
    APPLICATION_VND_MS_POWERPOINT = 'application/vnd.ms-powerpoint'
    APPLICATION_VND_OPENXMLFORMATS_OFFICEDOCUMENT_PRESENTATIONML_PRESENTATION = 'application/vnd.openxmlformats-officedocument.presentationml.presentation'
    APPLICATION_VND_OPENXMLFORMATS_OFFICEDOCUMENT_SPREADSHEETML_SHEET = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    APPLICATION_VND_OPENXMLFORMATS_OFFICEDOCUMENT_WORDPROCESSINGML_DOCUMENT = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    APPLICATION_XML = 'application/xml'
    APPLICATION_ZIP = 'application/zip'
    AUDIO_MPEG = 'audio/mpeg'
    AUDIO_WAV = 'audio/wav'
    IMAGE_GIF = 'image/gif'
    IMAGE_JPEG = 'image/jpeg'
    IMAGE_PNG = 'image/png'
    TEXT_CSS = 'text/css'
    TEXT_CSV = 'text/csv'
    TEXT_HTML = 'text/html'
    TEXT_JAVASCRIPT = 'text/javascript'
    TEXT_PLAIN = 'text/plain'
    VIDEO_3GPP = 'video/3gpp'
    VIDEO_MPEG = 'video/mpeg'
    VIDEO_QUICKTIME = 'video/quicktime'
    VIDEO_X_MSVIDEO = 'video/x-msvideo'


class Notesubjecttypes(str, Enum):
    """Auto-generated from schema: NoteSubjectTypes"""

    COMPANY = 'company'
    CONTACT = 'contact'
    CREDITNOTE = 'creditNote'
    DEAL = 'deal'
    INVOICE = 'invoice'
    NEXTGENPROJECT = 'nextgenProject'
    PRODUCT = 'product'
    PROJECT = 'project'
    QUOTATION = 'quotation'
    SUBSCRIPTION = 'subscription'


class Notesubjecttypescreate(str, Enum):
    """Auto-generated from schema: NoteSubjectTypes"""

    COMPANY = 'company'
    CONTACT = 'contact'
    CREDITNOTE = 'creditNote'
    DEAL = 'deal'
    INVOICE = 'invoice'
    NEXTGENPROJECT = 'nextgenProject'
    PRODUCT = 'product'
    QUOTATION = 'quotation'
    SUBSCRIPTION = 'subscription'


class Order(str, Enum):
    """Auto-generated from schema: Order"""

    ASC = 'asc'
    DESC = 'desc'


class Peppolstatus(str, Enum):
    """Auto-generated from schema: PeppolStatus"""

    SENDING = 'sending'
    SENDING_FAILED = 'sending_failed'
    SENT = 'sent'
    APPLICATION_ACKNOWLEDGED = 'application_acknowledged'
    APPLICATION_ACCEPTED = 'application_accepted'
    APPLICATION_REJECTED = 'application_rejected'
    RECEIVER_ACKNOWLEDGED = 'receiver_acknowledged'
    RECEIVER_ACCEPTED = 'receiver_accepted'
    RECEIVER_REJECTED = 'receiver_rejected'
    RECEIVER_IS_PROCESSING = 'receiver_is_processing'
    RECEIVER_AWAITS_FEEDBACK = 'receiver_awaits_feedback'
    RECEIVER_CONDITIONALLY_ACCEPTED = 'receiver_conditionally_accepted'
    RECEIVER_PAID = 'receiver_paid'


class Priority(str, Enum):
    """Auto-generated from schema: Priority"""

    A = 'A'
    B = 'B'
    C = 'C'
    D = 'D'


class Quotationlanguage(str, Enum):
    """Auto-generated from schema: QuotationLanguage"""

    EN = 'en'
    NL = 'nl'
    FR = 'fr'
    CH = 'ch'
    JP = 'jp'
    DE = 'de'
    ES = 'es'
    PT = 'pt'
    IT = 'it'
    GR = 'gr'
    TR = 'tr'
    CS = 'cs'
    SO = 'so'
    SK = 'sk'
    RU = 'ru'
    KO = 'ko'
    IR = 'ir'
    IQ = 'iq'
    HU = 'hu'
    GH = 'gh'
    BG = 'bg'
    BS = 'bs'
    BR = 'br'
    AR = 'ar'
    AG = 'ag'
    AL = 'al'
    AF = 'af'
    RO = 'ro'
    PL = 'pl'
    CA = 'ca'
    DA = 'da'
    UK = 'uk'
    NO = 'no'
    FI = 'fi'
    SV = 'sv'


class Role(str, Enum):
    """Auto-generated from schema: Role"""

    DECISION_MAKER = 'decision_maker'
    MEMBER = 'member'


class Sourcetype(str, Enum):
    """Auto-generated from schema: SourceType"""

    CALL = 'call'
    CLOSINGDAY = 'closingDay'
    DAYOFFTYPE = 'dayOffType'
    EXTERNALEVENT = 'externalEvent'
    MEETING = 'meeting'
    TASK = 'task'


class Timetrackingrelatestotypes(str, Enum):
    """Auto-generated from schema: TimeTrackingRelatesToTypes"""

    CONTACT = 'contact'
    COMPANY = 'company'
    PROJECT = 'project'
    MILESTONE = 'milestone'
    TICKET = 'ticket'
    NEXTGENPROJECT = 'nextgenProject'
    NEXTGENPROJECTGROUP = 'nextgenProjectGroup'


class Userlanguage(str, Enum):
    """Auto-generated from schema: UserLanguage"""

    NL_BE = 'nl-BE'
    DA = 'da'
    DE = 'de'
    EN = 'en'
    ES = 'es'
    FI = 'fi'
    FR = 'fr'
    IT = 'it'
    NB = 'nb'
    NL = 'nl'
    PL = 'pl'
    PT = 'pt'
    SV = 'sv'
    TR = 'tr'


class Weekday(str, Enum):
    """Auto-generated from schema: Weekday"""

    MONDAY = 'monday'
    TUESDAY = 'tuesday'
    WEDNESDAY = 'wednesday'
    THURSDAY = 'thursday'
    FRIDAY = 'friday'
    SATURDAY = 'saturday'
    SUNDAY = 'sunday'

