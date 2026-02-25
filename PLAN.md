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
| Refresh token `.env` auto-persist | `test_refresh_token_rotation` calls `_persist_tokens_to_env()` after rotation | After each rotation, `.env` is rewritten with the new token pair via `dotenv.set_key()`; no manual `get_tokens.py` re-run needed between test sessions |
| pytest-django settings | `tests/settings_test.py` — SQLite in-memory, `MIGRATION_MODULES={"teamleader_django": None}` | Creates the `TeamleaderToken` table directly from the model; no migration files shipped |

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
│   │   ├── __init__.py         🔲 Phase 8
│   │   ├── common.py           🔲 Address, Email, Telephone, Money, CustomField, WebLink
│   │   ├── contact.py          🔲 Contact (inherits _ContactBase)
│   │   ├── company.py          🔲 Company
│   │   ├── deal.py             🔲 Deal
│   │   ├── invoice.py          🔲 Invoice
│   │   └── quotation.py        🔲 Quotation
│   │
│   ├── resources/
│   │   ├── __init__.py         ✅ Phase 7/9
│   │   ├── base.py             ✅ Page[M], CrudResource[M] — Phase 7
│   │   ├── contacts.py         🔲 Phase 9
│   │   ├── companies.py        🔲 Phase 9
│   │   ├── deals.py            🔲 Phase 9
│   │   ├── invoices.py         🔲 Phase 9
│   │   └── quotations.py       🔲 Phase 9
│   │
│   └── django/
│       ├── __init__.py         ✅ import guard + get_client() — wired to DatabaseTokenBackend (Phase 5)
│       ├── apps.py             🔲 TeamleaderConfig.ready() validation — Phase 10
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
│   ├── settings_test.py        ✅ minimal Django/SQLite settings for pytest-django (Phase 5)
│   ├── test_auth.py            ✅ 32 unit tests — Token, MemoryTokenBackend, OAuth2Handler (Phase 4)
│   ├── test_django_token_store.py  ✅ 12 unit tests — DatabaseTokenBackend ORM (Phase 5)
│   ├── test_teamleader_setup.py    ✅ 9 unit tests — _CallbackHandler HTTP (Phase 5)
│   ├── test_resources.py       ✅ 43 unit tests — Page, CrudResource (Phase 7)
│   ├── test_models.py          🔲 Phase 11
│   └── integration/
│       ├── conftest.py         ✅ auto-skip without credentials; load_dotenv(); shared integration_backend/handler/client fixtures (Phase 5/6)
│       ├── test_auth.py        ✅ 3 integration tests — get_valid_token, refresh rotation + .env auto-persist, /users.me API check (Phase 4/5)
│       ├── test_client.py      ✅ 4 integration tests — _post list, 404, 422, transparent refresh (Phase 6)
│       └── test_deals.py       🔲 Phase 11
│
├── pyproject.toml              ✅ teamleader-sdk 0.1.0 — dev extras include freezegun, pytest-django
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
- `list(*, page, page_size, **filters) -> Page[M]` — POSTs `{"page": {"size": N, "number": N}, **filters}` to `.list`
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

### 🔲 Phase 8 — Curated Models

**`teamleader/models/common.py`** — `Users`, `Custom Fields`, `Contacts`, `Companies`, `Business Types`, `Tags`, `Addresses`,`Quotations`, `Orders`
Each has `from_api(dict) -> Self` and `to_dict() -> dict`.

**Per-resource model files** — inherit from generated base, add:
- `from_api(dict) -> Self` handling nested objects and enums
- `to_dict() -> dict` for sending back to the API
- Computed properties:
  - `Contact.full_name` → `"First Last"`
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
| 4 | ✅ | Auth layer — `Token`, `OAuth2Handler`, `MemoryTokenBackend` | 3 |
| 4b | ✅ | Auth tests — 32 unit + 2 integration; conftest fixtures | 4 |
| 5 | ✅ | Django integration — `TeamleaderToken`, `DatabaseTokenBackend`, `teamleader_setup`, `get_client()` | 4 |
| 6 | ✅ | HTTP client — `TeamleaderClient` | 3, 4 |
| 7 | ✅ | `CrudResource` base class, `Page` | 6 |
| 8 | 🔲 | Curated models — `common.py` + per-resource | 2 |
| 9 | 🔲 | Resource implementations | 7, 8 |
| 10 | 🔲 | Settings validation in `apps.py` | 5, 6 |
| 11 | 🔲 | Tests (resources, models, remaining integration) | all |
| 12 | 🔲 | README | all |
