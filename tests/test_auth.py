"""Unit tests for the auth layer.

Full implementation in Phase 11.

Covers:
- Token.is_expired: True when expires_at - now < TOKEN_EXPIRY_MARGIN_SECONDS
- OAuth2Handler.get_valid_token: raises TeamleaderAuthError when no token stored
- OAuth2Handler._refresh: happy path returns new Token
- OAuth2Handler._refresh: raises TeamleaderAuthExpiredError on 401 from token endpoint
"""

from __future__ import annotations
