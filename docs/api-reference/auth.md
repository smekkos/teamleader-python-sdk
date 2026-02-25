# Auth — API Reference

OAuth2 Authorization Code flow with automatic refresh-token rotation.

See the [Django Integration](../guides/django.md) and
[Non-Django Usage](../guides/non-django.md) guides for setup examples.

---

## Token

::: teamleader.auth.Token

---

## TokenBackend

Abstract base class for token storage backends.  Implement this to add custom storage
(Redis, file, etc.).

::: teamleader.auth.TokenBackend

---

## MemoryTokenBackend

In-process backend for tests, scripts, and non-Django environments.

::: teamleader.auth.MemoryTokenBackend

---

## OAuth2Handler

Full OAuth2 lifecycle: authorization URL → code exchange → transparent refresh.

::: teamleader.auth.OAuth2Handler

---

## DatabaseTokenBackend *(Django only)*

Stores the token pair in a Django database table (`TeamleaderToken` singleton).
Requires `pip install teamleader-sdk[django]`.

::: teamleader.django.token_store.DatabaseTokenBackend
