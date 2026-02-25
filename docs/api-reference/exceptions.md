# Exceptions — API Reference

All SDK exceptions inherit from `TeamleaderError`.
See the [Error Handling guide](../guides/error-handling.md) for usage patterns and a
visual hierarchy diagram.

---

## Base

::: teamleader.exceptions.TeamleaderError

---

## API / HTTP errors

::: teamleader.exceptions.TeamleaderAPIError

::: teamleader.exceptions.TeamleaderNotFoundError

::: teamleader.exceptions.TeamleaderRateLimitError

::: teamleader.exceptions.TeamleaderServerError

---

## Auth errors

::: teamleader.exceptions.TeamleaderAuthError

::: teamleader.exceptions.TeamleaderAuthExpiredError

---

## Request errors

::: teamleader.exceptions.TeamleaderValidationError

::: teamleader.exceptions.TeamleaderPermissionError
