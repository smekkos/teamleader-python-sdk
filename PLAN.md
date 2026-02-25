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
| Time-freezing in tests | `@freeze_time` decorator (freezegun) instead of `pytest-freezegun` | Avoids extra dependency; `freezer` fixture not needed when all boundary times are constant (`FROZEN_NOW`) |
| OAuth scopes in auth URL | **Omit by default** — Teamleader grants app-configured permissions automatically | Passing free-form scope strings returns `invalid_scope 400`; scopes are set at the Marketplace app level, not per-request |
| Refresh token `.env` auto-persist | `test_refresh_token_rotation` calls `_persist_tokens_to_env()` — writes both `os.environ` **and** `.env` file | Writing only `.env` leaves `os.environ` stale; subsequent fixtures in the same pytest session must see the new token pair immediately |
| pytest-django settings | `tests/settings_test.py` — SQLite in-memory, `MIGRATION_MODULES={"teamleader_django": None}`, minimal `TEAMLEADER` dict | Creates the `TeamleaderToken` table directly from the model; `TEAMLEADER` dict makes `TeamleaderConfig.ready()` pass at startup |
| Pagination include | `CrudResource.list()` auto-injects `pagination` into `includes` before every POST | `meta.matches` is **opt-in** — only returned when `includes=pagination` is sent; absent for `contacts.list` (unsupported) so a length-heuristic fallback is also implemented |
| Deal status enum | `Deal.status` is `str` (not a closed enum); computed properties guard known values only | Live API returns undocumented values (e.g. `"new"`) not in spec v1.112.0; a closed enum would crash on forward-compatible reads |
| List vs info response shapes | `contacts.list` returns `primary_address` (flat object); `contacts.info` returns `addresses` (typed list) | Spec intentionally uses different shapes for list vs detail; `Contact.from_api()` handles both via `.get()` defaults |

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
│   ├── client.py               ✅ TeamleaderClient — Phase 6
│   ├── auth.py                 ✅ Token, TokenBackend, MemoryTokenBackend, OAuth2Handler
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
│   │   ├── __init__.py         ✅ Phase 8
│   │   ├── common.py           ✅ TypeAndId, Address, AddressEntry, Email, Telephone, Money, CustomField, PaymentTerm, WebLink
│   │   ├── contact.py          ✅ Contact — 24 fields, 4 computed properties
│   │   ├── company.py          ✅ Company — 22 fields, 3 computed properties
│   │   ├── deal.py             ✅ Deal — 19 fields, 5 computed properties
│   │   ├── invoice.py          ✅ Invoice — 19 fields, 5 computed properties incl. is_overdue
│   │   └── quotation.py        ✅ Quotation — 13 fields, 5 computed properties
│   │
│   ├── resources/
│   │   ├── __init__.py         ✅ Phase 7/9
│   │   ├── base.py             ✅ Page[M], CrudResource[M] — Phase 7
│   │   ├── contacts.py         ✅ Phase 9 — tag, untag, link_to_company, unlink_from_company
│   │   ├── companies.py        ✅ Phase 9 — tag, untag
│   │   ├── deals.py            ✅ Phase 9 — move_to_phase, win, lose, list_phases, list_sources
│   │   ├── invoices.py         ✅ Phase 9 — book, credit, register_payment, send, download
│   │   └── quotations.py       ✅ Phase 9 — send, accept
│   │
│   └── django/
│       ├── __init__.py         ✅ import guard + get_client() — wired to DatabaseTokenBackend (Phase 5)
│       ├── apps.py             ✅ TeamleaderConfig.ready() with REQUIRED_SETTINGS_KEYS validation — Phase 10
│       ├── models.py           ✅ TeamleaderToken singleton (pk=1 enforcement) — Phase 5
│       ├── token_store.py      ✅ DatabaseTokenBackend (get/save/clear with select_for_update) — Phase 5
│       ├── middleware.py       ✅ pass-through placeholder
│       └── management/
│           └── commands/
│               └── teamleader_setup.py  ✅ OAuth setup wizard (HTTP server on port 9999) — Phase 5
│
├── get_tokens.py               ✅ standalone token-fetching helper (dev tool — not part of the package)
│
├── tests/
│   ├── conftest.py             ✅ fixtures: backend, valid_token, expired_token, handler, token_response_body()
│   ├── settings_test.py        ✅ minimal Django/SQLite settings; TEAMLEADER dict added (Phase 5/10)
│   ├── test_auth.py            ✅ 32 unit tests — Token, MemoryTokenBackend, OAuth2Handler (Phase 4)
│   ├── test_django_apps.py     ✅ 16 unit tests — TeamleaderConfig.ready() validation (Phase 10)
│   ├── test_django_token_store.py  ✅ 12 unit tests — DatabaseTokenBackend ORM (Phase 5)
│   ├── test_teamleader_setup.py    ✅ 9 unit tests — _CallbackHandler HTTP (Phase 5)
│   ├── test_resources.py       ✅ 93 unit tests — Page, CrudResource, all extra resource methods (Phase 7/9)
│   ├── test_models.py          ✅ 111 unit tests — all curated models (Phase 8)
│   └── integration/
│       ├── conftest.py         ✅ auto-skip without credentials; load_dotenv(); shared integration_backend/handler/client fixtures (Phase 5/6)
│       ├── test_auth.py        ✅ 3 integration tests — get_valid_token, refresh rotation + .env auto-persist, /users.me API check (Phase 4/5)
│       ├── test_client.py      ✅ 4 integration tests — _post list, 404, 422, transparent refresh (Phase 6)
│       ├── test_contacts.py    ✅ 13 integration tests — list, get, model props, tag/untag, link/unlink (Phase 11)
│       ├── test_companies.py   ✅ 10 integration tests — list, get, model props, tag/untag (Phase 11)
│       ├── test_deals.py       ✅ 11 integration tests — list, get, status props, list_phases, list_sources (Phase 11)
│       ├── test_invoices.py    ✅ 10 integration tests — list, get, is_paid/is_overdue/total_due, download (Phase 11)
│       └── test_quotations.py  ✅ 7 integration tests — list, get, status props, total_* (Phase 11)
│
├── pyproject.toml              ✅ teamleader-sdk 0.1.0 — dev extras include freezegun, pytest-django
├── .gitignore                  ✅ Python/Django patterns
├── .env.example                ✅
└── README.md                   ✅ Phase 12
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

### ✅ Phase 4 — Auth Layer (`teamleader/auth.py`)

**`Token` dataclass**
- Fields: `access_token: str`, `refresh_token: str`, `expires_at: datetime`
- Property `is_expired`: `True` if `expires_at - now < TOKEN_EXPIRY_MARGIN_SECONDS` (60s)
- Naive `expires_at` normalised to UTC before comparison

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
- `_request_token(payload) -> Token` — shared POST helper; raises `TeamleaderAuthError` on non-2xx or malformed JSON

**Tests added (ahead of Phase 11):**
- `tests/conftest.py` — shared fixtures (`backend`, `valid_token`, `expired_token`, `handler`, `token_response_body()`) and `FROZEN_NOW` constant
- `tests/test_auth.py` — 32 unit tests across all classes; time-sensitive tests use `@freeze_time(FROZEN_NOW)` from `freezegun`; HTTP tests use `@responses.activate`
- `tests/integration/test_auth.py` — 2 integration tests (auto-skipped without env vars)

---

### ✅ Phase 5 — Django Integration

**`teamleader/django/models.py`** — `TeamleaderToken` singleton model
- Fields: `access_token`, `refresh_token`, `expires_at`, `updated_at`
- `save()` enforces singleton by pinning `self.pk = 1` before calling `super().save()`
- `Meta.app_label = "teamleader_django"` — no migrations shipped; users run `makemigrations`

**`teamleader/django/token_store.py`** — `DatabaseTokenBackend(TokenBackend)`
- `get()`: reads singleton row (pk=1), returns `Token` or `None`
- `save()`: upserts singleton row inside `transaction.atomic()` with `select_for_update()` to prevent multi-worker race conditions
- `clear()`: deletes the singleton row (no-op if absent)

**`teamleader/django/management/commands/teamleader_setup.py`**
1. Validates required settings keys, raises `CommandError` if absent
2. Builds authorization URL via `OAuth2Handler.get_authorization_url()`
3. Prints URL and instructs user to open in browser
4. Starts temporary `http.server` (background thread) on `OAUTH_CALLBACK_PORT` (default 9999)
5. Waits for redirect with `?code=...` via `_CallbackHandler`
6. Exchanges code → saves tokens via `DatabaseTokenBackend`
7. Prints confirmation with access-token expiry time
8. Shuts down temp server via `server.shutdown()`

**`teamleader/django/apps.py`** — `TeamleaderConfig.ready()` — stub, full implementation Phase 10

**`teamleader/django/__init__.py`** — `get_client() -> TeamleaderClient`
- Reads `settings.TEAMLEADER`, constructs `DatabaseTokenBackend` + `OAuth2Handler`
- Returns configured `TeamleaderClient`

**`get_tokens.py`** — standalone dev helper (not part of the package)
- Interactive script to obtain an initial access/refresh token pair on a dev machine
- Starts port-9999 local server, captures OAuth callback, exchanges code, prints `.env` block
- Fixed: omit `scope` parameter from auth URL (Teamleader grants app-configured permissions automatically; passing free-form scope strings returns `invalid_scope 400`)

**`tests/integration/conftest.py`** — added `load_dotenv()` at module level
- Enables `.env`-based credentials for integration tests without shell exports

**`tests/settings_test.py`** — minimal Django settings for pytest-django
- SQLite in-memory database; `MIGRATION_MODULES = {"teamleader_django": None}` to bypass missing migrations; `USE_TZ = True`

**`tests/test_django_token_store.py`** — 12 unit tests for `DatabaseTokenBackend`
- Covers: `get()` returns `None` on empty table; `save()` creates pk=1 singleton; second `save()` upserts (no duplicate rows); `get()` round-trips timezone-aware `expires_at`; `clear()` deletes row; `clear()` is idempotent; full lifecycle cycle
- Uses `@pytest.mark.django_db` against real in-memory SQLite; no migrations needed

**`tests/test_teamleader_setup.py`** — 9 unit tests for `_CallbackHandler`
- Covers: code capture from query string; `None` when code absent; multiple params; URL-decoded values; 200/400 status codes; HTML content-type; success message in body
- Uses real `HTTPServer` on an ephemeral OS-assigned port — no mocking

**`tests/integration/test_auth.py`** — extended to 3 tests
- `_persist_tokens_to_env()` helper rewrites `.env` via `dotenv.set_key()` after each successful rotation — **no manual `get_tokens.py` re-run needed between test sessions**
- New: `test_stored_access_token_is_accepted_by_api` — calls `GET /users.me` with the access token obtained from `get_valid_token()`; asserts HTTP 200 and `"data"` key in response

**Live test results (2026-02-24, spec v1.112.0) — 56/56 passing**

| Suite | Count | Notes |
|---|---|---|
| `tests/test_django_token_store.py` | 12 ✅ | DatabaseTokenBackend ORM — real SQLite |
| `tests/test_teamleader_setup.py` | 9 ✅ | _CallbackHandler — real HTTP server |
| `tests/test_auth.py` | 32 ✅ | Unit — Token, MemoryBackend, OAuth2Handler |
| `tests/integration/test_auth.py` | 3 ✅ | Live Teamleader API — token valid, rotation, /users.me 200 |

---

### ✅ Phase 6 — HTTP Client (`teamleader/client.py`)

**`TeamleaderClient`**
- Constructor: `auth_handler: OAuth2Handler`, optional `timeout: int` (default `DEFAULT_TIMEOUT`)
- Uses `requests.Session` for connection pooling
- `_auth_headers() -> dict` — calls `get_valid_token()` to inject fresh Bearer per request
- `_get(path, params) -> dict` — injects Bearer token, calls `_handle_response`
- `_post(path, json) -> dict` — same
- `_handle_response(response) -> dict`:
  - 2xx with empty body → `{}`
  - 401 → `TeamleaderAuthError`
  - 403 → `TeamleaderPermissionError`
  - 404 → `TeamleaderNotFoundError`
  - 422 → `TeamleaderValidationError`
  - 429 → `TeamleaderRateLimitError` (`retry_after` from `Retry-After` header; `None` if absent)
  - 5xx → `TeamleaderServerError`
  - other 4xx → `TeamleaderAPIError`
- `_extract_message(response)` — understands JSON:API `{"errors":[{"title":"..."}]}`, OAuth `{"error_description":"..."}`, and falls back to `response.text` / `"HTTP <status>"`
- Public resource attributes: `self.contacts`, `.companies`, `.deals`, `.invoices`, `.quotations`

**Tests added:**
- `tests/conftest.py` — `client` fixture: `TeamleaderClient` with real-clock-valid token (24 h expiry) so no `@freeze_time` needed per test
- `tests/test_client.py` — 31 unit tests covering: Bearer header injection, JSON body round-trip, 204 → `{}`, every error status code → correct exception, `retry_after` presence/absence, all `_extract_message` branches, resource attribute types, custom timeout
- `tests/integration/conftest.py` — extended with shared `integration_backend`, `integration_handler`, `integration_client` fixtures; `_persist_tokens_to_env` helper; `_env` helper (previously duplicated across test modules)
- `tests/integration/test_client.py` — 4 integration tests (auto-skip without credentials):
  - `test_post_contacts_list_returns_data_dict` — proves full POST path against real API
  - `test_nonexistent_id_raises_not_found_with_message` — validates real 404 body shape
  - `test_invalid_body_raises_validation_error_with_message` — validates real 422 body shape
  - `test_expired_token_is_transparently_refreshed` — exercises `_auth_headers()` → refresh seam live

**Live test results (2026-02-24): 63/63 passing (unit); 67/67 passing with credentials**

| Suite | Count | Notes |
|---|---|---|
| `tests/test_auth.py` | 32 ✅ | unchanged |
| `tests/test_client.py` | 31 ✅ | Phase 6 — new |
| `tests/integration/test_client.py` | 4 ⏭ | auto-skip without env vars; 4 ✅ with credentials |

---

### ✅ Phase 7 — Resource Base (`teamleader/resources/base.py`)

**`Page[M]`** dataclass
- Fields: `data: list[M]`, `total_count: int`, `current_page: int`, `page_size: int`
- Private (`init=False`): `_resource`, `_filters` — set by `CrudResource` after construction
- `has_next` property: `current_page * page_size < total_count`
- `next() -> Page[M]` — increments page, forwards `_filters`; raises `ValueError` if already on last page

**`CrudResource[M]`**
- Class attrs: `prefix: str`, `model: type[M]`
- `_path(operation) -> str` — builds `"prefix.operation"`
- `_deserialise(data) -> M` — delegates to `model.from_api(data)`
- `list(*, page, page_size, **filters) -> Page[M]` — POSTs `{"page": {"size": N, "number": N}, **filters, "includes": "...,pagination"}` to `.list`; auto-injects `pagination` into `includes` so `meta.matches` is returned where supported; falls back to page-fill heuristic when absent
- `get(id) -> M` — POSTs to `.info` (Teamleader convention)
- `create(**kwargs) -> M` — POSTs to `.add`, re-fetches full object via `get(returned_id)`
- `update(id, **kwargs) -> M` — POSTs to `.update`, re-fetches via `get(id)`
- `delete(id) -> None` — POSTs to `.delete`
- `iterate(page_size, **filters) -> Iterator[M]` — generator; transparently fetches all pages

**Tests added:**
- `tests/test_resources.py` — 43 unit tests across 10 classes; `client._post` mocked with `unittest.mock.MagicMock` (no HTTP I/O)
  - `TestPageHasNext` (6): boundary conditions for `has_next`
  - `TestPageNext` (4): page forwarding, filter passthrough, `ValueError` guard
  - `TestCrudResourcePath` (4): `_path()` string construction
  - `TestCrudResourceList` (9): POST body shape, page metadata, filter merging, `_resource`/`_filters` wiring
  - `TestCrudResourceGet` (3): `.info` endpoint, body, deserialization
  - `TestCrudResourceCreate` (4): `.add` → re-fetch by ID sequence
  - `TestCrudResourceUpdate` (4): `.update` → re-fetch sequence
  - `TestCrudResourceDelete` (2): `.delete` call, `None` return
  - `TestCrudResourceIterate` (7): single/multi-page, exact call count, filter/page_size forwarding, empty set

**Live test results (2026-02-25): 127/127 passing**

| Suite | Count | Notes |
|---|---|---|
| `tests/test_auth.py` | 32 ✅ | unchanged |
| `tests/test_client.py` | 31 ✅ | unchanged |
| `tests/test_django_token_store.py` | 12 ✅ | unchanged |
| `tests/test_teamleader_setup.py` | 9 ✅ | unchanged |
| `tests/test_resources.py` | 43 ✅ | Phase 7 — new |

---

### ✅ Phase 8 — Curated Models

**`teamleader/models/common.py`** — new sub-models: `TypeAndId`, `Address`, `AddressEntry`, `Email`, `Telephone`, `Money`, `CustomField`, `PaymentTerm`, `WebLink`.
All have `from_api(dict) -> Self` and `to_dict() -> dict`.

Key design decisions:
- `website: str | None` (single URL) — _not_ `websites: list[WebLink]` (spec uses a flat string)
- `addresses: list[AddressEntry]` — typed wrapper (role + `Address` + `addressee`)
- `CustomField.id` flattened from `definition.id` for convenience
- `AddressEntry` extracts `addressee` from inside the nested `address` dict

**Per-resource model files:**

| File | Fields | Computed properties |
|---|---|---|
| `contact.py` | 24 | `full_name`, `primary_email`, `primary_phone`, `is_active` |
| `company.py` | 22 + `related_*` optionals | `is_active`, `primary_email`, `primary_phone` |
| `deal.py` | 19 | `is_open`, `is_won`, `is_lost`, `customer_id`, `customer_type` |
| `invoice.py` | 19 | `is_paid`, `is_draft`, `is_overdue` (date-safe), `total_due`, `customer_name` |
| `quotation.py` | 13 | `is_open`, `is_accepted`, `is_expired`, `total_tax_exclusive`, `total_tax_inclusive` |

**Tests added:**
- `tests/test_models.py` — 111 unit tests across all common sub-models and per-resource models; `is_overdue` edge cases use `@freeze_time`

**Live test results (2026-02-25): 288/288 passing**

| Suite | Count | Notes |
|---|---|---|
| `tests/test_auth.py` | 32 ✅ | unchanged |
| `tests/test_client.py` | 31 ✅ | unchanged |
| `tests/test_django_token_store.py` | 12 ✅ | unchanged |
| `tests/test_teamleader_setup.py` | 9 ✅ | unchanged |
| `tests/test_resources.py` | 93 ✅ | Phase 7 base (43) + Phase 9 extra methods (50) |
| `tests/test_models.py` | 111 ✅ | Phase 8 — new |

---

### ✅ Phase 9 — Resource Implementations

| Resource | Extra methods |
|---|---|
| `ContactsResource` | `tag`, `untag`, `link_to_company`, `unlink_from_company` |
| `CompaniesResource` | `tag`, `untag` |
| `DealsResource` | `move_to_phase`, `win`, `lose`, `list_phases` (`dealPhases.list`), `list_sources` (`dealSources.list`) |
| `InvoicesResource` | `book`, `credit` → `TypeAndId`, `register_payment`, `send`, `download` → URL dict |
| `QuotationsResource` | `send` (list of IDs + recipients), `accept` |

Notes:
- `list_phases` / `list_sources` call `dealPhases.list` / `dealSources.list` directly — separate API resource families
- `invoices.download` returns `{"location": ..., "expires": ...}` (pre-signed URL), not raw bytes
- `quotations.decline` does **not exist** in spec v1.112.0 — omitted
- 50 unit tests added to `tests/test_resources.py` covering every extra method

---

### ✅ Phase 10 — Settings Validation

**`teamleader/django/apps.py`** — `TeamleaderConfig.ready()`:
- Constant `REQUIRED_SETTINGS_KEYS = frozenset({"CLIENT_ID", "CLIENT_SECRET", "REDIRECT_URI", "SCOPES"})`
- `getattr(settings, "TEAMLEADER", None)` → raises `ImproperlyConfigured` if not a `dict`
- `REQUIRED_SETTINGS_KEYS - cfg.keys()` → raises `ImproperlyConfigured` naming the missing keys
- Error messages include an actionable settings snippet

**`tests/settings_test.py`** — added minimal valid `TEAMLEADER` dict so `ready()` passes at startup.

**`tests/test_django_apps.py`** — 16 unit tests using `@override_settings`:
- 5 tests: absent/non-dict values (`None`, `str`, `int`, `list`, missing entirely)
- 6 tests: one missing required key per key + all missing + error message lists them
- 3 tests: happy path — all keys present, extra keys accepted, optional `TOKEN_BACKEND` accepted
- 2 tests: `REQUIRED_SETTINGS_KEYS` constant is correct and is a `frozenset`

**Live test results (2026-02-25): 304/304 passing**

| Suite | Count | Notes |
|---|---|---|
| All previous suites | 288 ✅ | unchanged |
| `tests/test_django_apps.py` | 16 ✅ | Phase 10 — new |

---

### ✅ Phase 11 — Integration Tests

58 integration tests across 7 files — all auto-skip when `TEAMLEADER_INTEGRATION_CLIENT_ID` is absent.

| File | Tests | Live result (sandbox) |
|---|---|---|
| `test_auth.py` | 3 | 3 ✅ |
| `test_client.py` | 4 | 4 ✅ |
| `test_contacts.py` | 13 | 9 ✅ 2 ⏭ (no addresses/custom fields in sandbox) |
| `test_companies.py` | 10 | 9 ✅ 1 ⏭ (no custom fields in sandbox) |
| `test_deals.py` | 11 | 11 ✅ |
| `test_invoices.py` | 10 | 0 ✅ 10 ⏭ (no invoices in sandbox) |
| `test_quotations.py` | 7 | 1 ✅ 6 ⏭ (no quotations in sandbox) |
| **Total** | **58** | **39 ✅ 19 ⏭ 0 ❌** |

**Design principles:**
- Read-only by default; mutations use `try/finally` for guaranteed cleanup
- `_first_or_skip()` helper skips gracefully when sandbox has no data
- Write operations (book, credit, win/lose) excluded — too high-impact to automate
- Iterate tests use `islice(n=20)` to cap at one page — prevents rate-limit exhaustion on large accounts
- `_persist_tokens_to_env()` updates both `os.environ` and `.env` so token rotation within a session propagates to subsequent tests

**API spec-vs-reality discoveries (fixed during live testing):**

| # | Issue | Root cause | Fix |
|---|---|---|---|
| 1 | `KeyError: 'meta'` on every `list()` call | `meta.matches` is opt-in via `includes=pagination`; not returned by default | `base.py` now auto-injects `pagination` into `includes`; falls back to length heuristic when still absent (contacts.list doesn't support this include) |
| 2 | `test_post_contacts_list_returns_data_dict` failing | Previous assertion `"meta" in result` was wrong without `includes=pagination` | Updated to assert `isinstance(result["data"], list)` |
| 3 | `contacts.add {}` returns 400 not 422 | API changed validation error status code | Test updated to accept `status_code in (400, 422)` via `TeamleaderAPIError` parent |
| 4 | `test_expired_token` failed with `TeamleaderAuthExpiredError` | `test_refresh_token_rotation` rotated the refresh token and wrote new tokens to `.env` but not `os.environ`; next test loaded stale token from env | `_persist_tokens_to_env()` now also writes to `os.environ` immediately |
| 5 | Rate limit errors during integration run | `iterate(page_size=5)` on 493 companies = 99 API calls per test | Iterate tests now use `islice(iterate(page_size=20), 20)` to stay within one page |
| 6 | `deal.status` in `{'open','won','lost'}` assertion fails | API also returns `"new"` (undocumented pipeline-stage status) | Test updated to accept any non-empty string; status-boolean test asserts `sum(flags) <= 1` |

---

### ✅ Phase 12 — README

[`README.md`](README.md) covers:
1. Requirements and installation (`pip install teamleader-sdk[django]`)
2. Django setup — `INSTALLED_APPS`, settings dict, migrations, `teamleader_setup`
3. Non-Django quick-start — `MemoryTokenBackend` + `OAuth2Handler` + `TeamleaderClient`
4. CRUD methods — `list`, `get`, `create`, `update`, `delete`
5. Pagination — `Page`, `has_next`, `next()`, `iterate()`
6. Per-resource extra methods — contacts/companies/deals/invoices/quotations
7. Models and computed properties cheat-sheet
8. Error handling — exception hierarchy + usage pattern
9. Codegen update workflow — `python codegen/generate.py`

---

## Implementation Order

| Phase | Status | Deliverable | Depends On |
|---|---|---|---|
| 1 | ✅ | Project scaffold, `pyproject.toml` | — |
| 2 | ✅ | Codegen — fetch + 3 generators | 1 |
| 3 | ✅ | Exception hierarchy | 1 |
| 4 | ✅ | Auth layer — `Token`, `OAuth2Handler`, `MemoryTokenBackend` | 3 |
| 4b | ✅ | Auth tests — 32 unit + 2 integration; conftest fixtures | 4 |
| 5 | ✅ | Django integration — `TeamleaderToken`, `DatabaseTokenBackend`, `teamleader_setup`, `get_client()` | 4 |
| 6 | ✅ | HTTP client — `TeamleaderClient` | 3, 4 |
| 7 | ✅ | `CrudResource` base class, `Page` | 6 |
| 8 | ✅ | Curated models — `common.py` + per-resource; 111 unit tests | 2 |
| 9 | ✅ | Resource implementations + 50 unit tests | 7, 8 |
| 10 | ✅ | Settings validation in `apps.py`; 16 unit tests | 5, 6 |
| 11 | ✅ | 58 integration tests across 5 resources; all auto-skip without credentials | all |
| 12 | ✅ | README | all |
