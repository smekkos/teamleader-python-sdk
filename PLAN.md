# Teamleader Python SDK — Implementation Plan

## Overview

Python SDK for the Teamleader Focus API, installable via pip, designed to integrate into multiple Django projects. The SDK is partially generated from the OpenAPI spec published on npm as `@teamleader/focus-api-specification`, and partially hand-written.

- **Generated code** lives in `teamleader/_generated/` — always safe to overwrite by the generator.
- **Curated code** lives everywhere else — never touched by the generator.

### Key style conventions (from `easytrans-sdk` reference)
- Pure dataclasses with type hints — no attrs/pydantic
- Semantic exception hierarchy
- Django settings integration via `TEAMLEADER = {}` dict in `settings.py`
- Framework-agnostic core; Django-specific code isolated in `teamleader/django/`
- `from_api(dict)` classmethods for deserialisation

---

## Design Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Django dependency | **Optional extra** — `pip install teamleader-sdk[django]`; guard once in `teamleader/django/__init__.py` | Keeps the core importable in non-Django contexts (FastAPI, scripts, Celery) |
| OAuth callback port | `settings.TEAMLEADER['OAUTH_CALLBACK_PORT']`, **default `9999`** | Different environments may need different ports |
| Django migrations | **Not shipped** — users run `makemigrations teamleader_django` then `migrate` | Avoids migration conflicts in downstream projects |
| Spec cache | `codegen/spec/api.yaml` **committed** | Serves as canonical snapshot for diffing against future spec versions |
| Spec tarball path | `package/dist/api.focus.teamleader.eu.dereferenced.yaml` | Discovered empirically — the npm package nests files under `dist/` |
| Enum member naming | Strip underscores before digit-prefix guard | Fixes `#00B2B2` → `VALUE_00B2B2` (hex colour edge case) |
| `oneOf` schemas | **Skipped** in model generation | Discriminated unions cannot be represented as simple dataclasses |
| `allOf`/`oneOf` in properties | Collapsed to `dict[str, Any]` | Too complex to inline; curated `from_api()` handles proper deserialization |

---

## Settings Contract

| Key | Required | Default | Description |
|---|---|---|---|
| `CLIENT_ID` | ✅ | — | OAuth2 client ID |
| `CLIENT_SECRET` | ✅ | — | OAuth2 client secret |
| `REDIRECT_URI` | ✅ | — | Must match Teamleader app config |
| `SCOPES` | ✅ | — | List of OAuth scopes |
| `OAUTH_CALLBACK_PORT` | ❌ | `9999` | Port for the setup command's local HTTP server |
| `TOKEN_BACKEND` | ❌ | `DatabaseTokenBackend` | Token storage backend class path |
| `TIMEOUT` | ❌ | `30` | HTTP request timeout in seconds |

---

## Project Structure

```
teamleader-sdk/
├── codegen/
│   ├── fetch_spec.py           ✅ fetches npm tarball, extracts dereferenced YAML
│   ├── generate_enums.py       ✅ str,Enum subclasses from schemas
│   ├── generate_models.py      ✅ @dataclass base classes from schemas
│   ├── generate_endpoints.py   ✅ Endpoint dataclass + ENDPOINTS dict from paths
│   ├── generate.py             ✅ master entry point
│   └── spec/
│       └── api.yaml            ✅ committed spec snapshot (v1.112.0)
│
├── teamleader/
│   ├── __init__.py             ✅ exports 19 public symbols
│   ├── client.py               🔲 TeamleaderClient — Phase 6
│   ├── auth.py                 🔲 Token, OAuth2Handler — Phase 4
│   ├── exceptions.py           ✅ full hierarchy — 9 exception classes
│   ├── constants.py            ✅ API URLs and defaults
│   ├── py.typed                ✅ PEP 561 marker
│   │
│   ├── _generated/             ✅ safe to overwrite
│   │   ├── __init__.py
│   │   ├── enums.py            ✅ 23 enum classes (v1.112.0)
│   │   ├── models.py           ✅ 483 base classes (v1.112.0)
│   │   └── endpoints.py        ✅ 290 endpoints (v1.112.0)
│   │
│   ├── models/
│   │   ├── __init__.py         🔲 Phase 8
│   │   ├── common.py           🔲 Address, Email, Telephone, Money, CustomField, WebLink
│   │   ├── contact.py          🔲 Contact (inherits _ContactBase)
│   │   ├── company.py          🔲 Company
│   │   ├── deal.py             🔲 Deal
│   │   ├── invoice.py          🔲 Invoice
│   │   └── quotation.py        🔲 Quotation
│   │
│   ├── resources/
│   │   ├── __init__.py         🔲 Phase 7/9
│   │   ├── base.py             🔲 Page[M], CrudResource[M] — Phase 7
│   │   ├── contacts.py         🔲 Phase 9
│   │   ├── companies.py        🔲 Phase 9
│   │   ├── deals.py            🔲 Phase 9
│   │   ├── invoices.py         🔲 Phase 9
│   │   └── quotations.py       🔲 Phase 9
│   │
│   └── django/
│       ├── __init__.py         ✅ import guard + get_client() stub
│       ├── apps.py             🔲 TeamleaderConfig.ready() validation — Phase 10
│       ├── models.py           🔲 TeamleaderToken singleton — Phase 5
│       ├── token_store.py      🔲 DatabaseTokenBackend — Phase 5
│       ├── middleware.py       ✅ pass-through placeholder
│       └── management/
│           └── commands/
│               └── teamleader_setup.py  🔲 OAuth setup wizard — Phase 5
│
├── tests/
│   ├── conftest.py             🔲 Phase 11
│   ├── test_auth.py            🔲 Phase 11
│   ├── test_resources.py       🔲 Phase 11
│   ├── test_models.py          🔲 Phase 11
│   └── integration/
│       ├── conftest.py         🔲 Phase 11 (auto-skip without credentials)
│       └── test_deals.py       🔲 Phase 11
│
├── pyproject.toml              ✅ teamleader-sdk 0.1.0
├── .gitignore                  ✅ Python/Django patterns
├── .env.example                ✅
└── README.md                   🔲 Phase 13
```

---

## Phases

### ✅ Phase 1 — Project Scaffold
- `pyproject.toml`: `teamleader-sdk`, Python ≥3.10, `requests`, `[django]` + `[dev]` extras
- Full directory structure with importable stubs for all future phases
- `teamleader/__init__.py` exports 19 public symbols; `__version__ = "0.1.0"`
- `py.typed` marker, `constants.py`, `.gitignore`, `.env.example`

### ✅ Phase 2 — Codegen
Generates three files under `teamleader/_generated/` from the live npm spec.

Key implementation notes:
- Spec tarball path is `package/dist/` not `package/` (discovered empirically)
- All Teamleader paths are POST; params live in `requestBody.content.application/json.schema.allOf[0]`
- Properties are already snake_case in the spec
- Hex enum values like `#00B2B2` handled by stripping underscores before digit-prefix guard → `VALUE_00B2B2`
- 9 `oneOf` schemas skipped (discriminated unions)
- `allOf`/`oneOf` in properties → `dict[str, Any]`

**Results from spec v1.112.0:** 23 enums, 483 model base classes, 290 endpoints.

**Update workflow:**
```bash
python codegen/generate.py
git diff teamleader/_generated/
pytest
# fix any curated code broken by schema changes
# commit both _generated/ and fixes with version in message
```

### ✅ Phase 3 — Exception Hierarchy
Implemented in Phase 1 (no dependencies, simple).

```
TeamleaderError
├── TeamleaderAPIError
│   ├── TeamleaderNotFoundError      (404)
│   ├── TeamleaderRateLimitError     (429) — adds retry_after field
│   └── TeamleaderServerError        (5xx)
├── TeamleaderAuthError              (401)
│   └── TeamleaderAuthExpiredError   (refresh token revoked)
├── TeamleaderValidationError        (422)
└── TeamleaderPermissionError        (403)
```

Each exception carries: `message`, `status_code`, `raw_response`.

---

### 🔲 Phase 4 — Auth Layer (`teamleader/auth.py`)

**`Token` dataclass**
- Fields: `access_token: str`, `refresh_token: str`, `expires_at: datetime`
- Property `is_expired`: `True` if `expires_at - now < TOKEN_EXPIRY_MARGIN_SECONDS` (60s)

**`TokenBackend` (ABC)**
- `get() -> Token | None`
- `save(token: Token) -> None`
- `clear() -> None`

**`MemoryTokenBackend`** — stores token in instance variable; for tests and non-Django use.

**`OAuth2Handler`**
- Constructor: `client_id`, `client_secret`, `redirect_uri`, `token_backend`, `scopes`
- `get_authorization_url() -> str` — builds Teamleader OAuth URL with scopes
- `exchange_code(code: str) -> Token` — POSTs to TOKEN_URL, saves via backend
- `get_valid_token() -> str` — load → check missing (raise `TeamleaderAuthError`) → check expired (refresh) → return `access_token`
- `_refresh(token: Token) -> Token` — POSTs with `grant_type=refresh_token`; raises `TeamleaderAuthExpiredError` if rejected

---

### 🔲 Phase 5 — Django Integration

**`teamleader/django/models.py`** — `TeamleaderToken` singleton model
- Fields: `access_token`, `refresh_token`, `expires_at`, `updated_at`
- `save()` enforces singleton (only one row allowed)
- `Meta.app_label = "teamleader_django"` — no migrations shipped; users run `makemigrations`

**`teamleader/django/token_store.py`** — `DatabaseTokenBackend(TokenBackend)`
- `get()`: reads singleton row, returns `Token` or `None`
- `save()`: upserts singleton row inside `transaction.atomic()` with `select_for_update()`

**`teamleader/django/management/commands/teamleader_setup.py`**
1. Build authorization URL from settings
2. Print URL and instruct user to open in browser
3. Start temporary `http.server` on `settings.TEAMLEADER['OAUTH_CALLBACK_PORT']` (default 9999)
4. Wait for redirect with `?code=...`
5. Exchange code → save tokens via `DatabaseTokenBackend`
6. Print confirmation with expiry time
7. Shut down temp server

**`teamleader/django/apps.py`** — `TeamleaderConfig.ready()`
- Validates required settings keys → `ImproperlyConfigured` with helpful message (Phase 10)

**`teamleader/django/__init__.py`** — `get_client() -> TeamleaderClient`
- Reads `settings.TEAMLEADER`, constructs `DatabaseTokenBackend`
- Returns configured `TeamleaderClient`

---

### 🔲 Phase 6 — HTTP Client (`teamleader/client.py`)

**`TeamleaderClient`**
- Constructor: `auth_handler: OAuth2Handler`
- `_get(path, params) -> dict` — injects Bearer token, calls `_handle_response`
- `_post(path, json) -> dict` — same
- `_handle_response(response) -> dict`:
  - 401 → `TeamleaderAuthError`
  - 403 → `TeamleaderPermissionError`
  - 404 → `TeamleaderNotFoundError`
  - 422 → `TeamleaderValidationError` (include body)
  - 429 → `TeamleaderRateLimitError` (include `Retry-After` header)
  - 5xx → `TeamleaderServerError`
- Public resource attributes: `self.contacts`, `.companies`, `.deals`, `.invoices`, `.quotations`

---

### 🔲 Phase 7 — Resource Base (`teamleader/resources/base.py`)

**`Page[M]`** dataclass
- Fields: `data: list[M]`, `total_count: int`, `current_page: int`, `page_size: int`
- Private: `_resource`, `_filters`
- `has_next` property
- `next() -> Page[M]`

**`CrudResource[M]`**
- Class attrs: `prefix: str`, `model: type[M]`
- `_path(operation) -> str`
- `_deserialise(data) -> M` — calls `model.from_api(data)`
- `list(*, page, page_size, **filters) -> Page[M]`
- `get(id) -> M`
- `create(**kwargs) -> M` — POSTs to `.add`, fetches by returned ID
- `update(id, **kwargs) -> M` — POSTs to `.update`, re-fetches
- `delete(id) -> None`
- `iterate(page_size, **filters) -> Iterator[M]`

---

### 🔲 Phase 8 — Curated Models

**`teamleader/models/common.py`** — `Address`, `Email`, `Telephone`, `Money`, `CustomField`, `WebLink`
Each has `from_api(dict) -> Self` and `to_dict() -> dict`.

**Per-resource model files** — inherit from generated base, add:
- `from_api(dict) -> Self` handling nested objects and enums
- `to_dict() -> dict` for sending back to the API
- Computed properties:
  - `Contact.full_name` → `"First Last"`
  - `Invoice.is_overdue` → due date past + status not paid

---

### 🔲 Phase 9 — Resource Implementations

| Resource | Extra methods |
|---|---|
| `ContactsResource` | `link_to_company`, `unlink_from_company`, `tag`, `untag` |
| `CompaniesResource` | `tag`, `untag` |
| `DealsResource` | `move_to_phase`, `win`, `lose`, `list_phases`, `list_sources` |
| `InvoicesResource` | `book`, `credit`, `send`, `register_payment`, `download` |
| `QuotationsResource` | `send`, `accept`, `decline` |

---

### 🔲 Phase 10 — Settings Validation

`TeamleaderConfig.ready()` in `teamleader/django/apps.py`:
- Check `settings.TEAMLEADER` exists
- Check required keys: `CLIENT_ID`, `CLIENT_SECRET`, `REDIRECT_URI`, `SCOPES`
- Raise `django.core.exceptions.ImproperlyConfigured` with an actionable message listing missing keys

---

### 🔲 Phase 11 — Tests

**Unit tests** (`tests/`, uses `responses` library to mock HTTP)
- `conftest.py`: `TeamleaderClient` with `MemoryTokenBackend` pre-loaded with valid + expired tokens
- `test_auth.py`: `is_expired`, refresh flow, `TeamleaderAuthExpiredError` on 401
- `test_resources.py`: list/get/create/update/delete per resource; pagination; `iterate()` across pages
- `test_models.py`: `from_api` round-trips; `full_name`; `is_overdue`

**Integration tests** (`tests/integration/`, skipped without env vars)
- `conftest.py`: auto-skip if `TEAMLEADER_INTEGRATION_CLIENT_ID` absent
- Read-only where possible; create+delete cycles for mutation coverage

---

### 🔲 Phase 12 — README

Installation, Django configuration, non-Django usage, OAuth setup, codegen update workflow.

---

## Implementation Order

| Phase | Status | Deliverable | Depends On |
|---|---|---|---|
| 1 | ✅ | Project scaffold, `pyproject.toml` | — |
| 2 | ✅ | Codegen — fetch + 3 generators | 1 |
| 3 | ✅ | Exception hierarchy | 1 |
| 4 | 🔲 | Auth layer — `Token`, `OAuth2Handler`, `MemoryTokenBackend` | 3 |
| 5 | 🔲 | Django integration | 4 |
| 6 | 🔲 | HTTP client — `TeamleaderClient` | 3, 4 |
| 7 | 🔲 | `CrudResource` base class, `Page` | 6 |
| 8 | 🔲 | Curated models — `common.py` + per-resource | 2 |
| 9 | 🔲 | Resource implementations | 7, 8 |
| 10 | 🔲 | Settings validation in `apps.py` | 5, 6 |
| 11 | 🔲 | Tests | all |
| 12 | 🔲 | README | all |
