# Codegen — Updating the Generated Layer

The SDK is partially generated from the Teamleader Focus OpenAPI spec published on npm
as `@teamleader/focus-api-specification`.  The committed snapshot at
`codegen/spec/api.yaml` (currently **v1.112.0**) serves as the canonical baseline for
diffing against future spec versions.

---

## What is generated

| File | Contents | Safe to overwrite? |
|---|---|---|
| `teamleader/_generated/enums.py` | 23 `str, Enum` subclasses | ✅ Yes |
| `teamleader/_generated/models.py` | 483 `@dataclass` base classes | ✅ Yes |
| `teamleader/_generated/endpoints.py` | 290 `Endpoint` dataclasses + `ENDPOINTS` dict | ✅ Yes |

Everything in `teamleader/models/`, `teamleader/resources/`, and the rest of the
`teamleader/` package is **curated code** — never touched by the generator.

---

## Update workflow

```bash
# 1. Fetch the latest spec from npm and regenerate all three files
python codegen/generate.py

# 2. Review what changed in the generated layer
git diff teamleader/_generated/

# 3. Run the full test suite — curated code may need updating
pytest

# 4. Fix any curated code broken by schema changes
#    (new fields, renamed enums, etc.)

# 5. Regenerate the documentation endpoint index
python codegen/generate_docs_endpoints.py

# 6. Commit both generated files and curated fixes together
git add teamleader/_generated/ teamleader/models/ teamleader/resources/ \
        codegen/spec/api.yaml docs/api-reference/generated-endpoints.md
git commit -m "chore: update generated layer to spec vX.Y.Z"
```

---

## Generator scripts

| Script | Purpose |
|---|---|
| `codegen/generate.py` | Master entry point — runs all three generators below |
| `codegen/fetch_spec.py` | Downloads the npm tarball, extracts the dereferenced YAML |
| `codegen/generate_enums.py` | Emits `teamleader/_generated/enums.py` |
| `codegen/generate_models.py` | Emits `teamleader/_generated/models.py` |
| `codegen/generate_endpoints.py` | Emits `teamleader/_generated/endpoints.py` |
| `codegen/generate_docs_endpoints.py` | Emits `docs/api-reference/generated-endpoints.md` |

---

## Key implementation details

| Detail | Notes |
|---|---|
| Spec tarball path | `package/dist/api.focus.teamleader.eu.dereferenced.yaml` (nested under `dist/`) |
| All paths are POST | Body params live in `requestBody.content.application/json.schema.allOf[0]` |
| Properties are snake_case | No renaming needed — already conform to Python conventions |
| Hex enum values | `#00B2B2` → strip underscores before digit-guard → `VALUE_00B2B2` |
| `oneOf` schemas | **Skipped** — discriminated unions can't be represented as plain dataclasses |
| `allOf`/`oneOf` in properties | Collapsed to `dict[str, Any]` — curated `from_api()` handles proper deserialisation |

---

## Generated vs. curated models

The generated `teamleader/_generated/models.py` contains **base classes** with all
fields as `Any`.  The curated models in `teamleader/models/` subclass those bases,
adding:

- Strict type hints
- `from_api(dict) -> Self` deserialisation
- Computed `@property` accessors

When the spec gains new fields on a curated model, add them to the curated class and
update `from_api()` — do **not** edit the generated base.

---

## Re-generating documentation

The `docs/api-reference/generated-endpoints.md` page is generated from `codegen/spec/api.yaml`
by `codegen/generate_docs_endpoints.py`.  It runs automatically as an `mkdocs` pre-build
hook (configured in `mkdocs.yml`), so a plain `mkdocs build` or `mkdocs serve` always
reflects the current spec snapshot.

Run it manually after a spec update with:

```bash
python codegen/generate_docs_endpoints.py
```
