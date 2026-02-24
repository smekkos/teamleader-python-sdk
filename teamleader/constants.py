"""Teamleader Focus API — fixed constants.

All values are taken from the official Teamleader documentation.
Do not modify; use settings.TEAMLEADER for runtime overrides.
"""

# Base URL for all API calls
BASE_URL: str = "https://api.focus.teamleader.eu"

# OAuth2 endpoints
AUTHORIZATION_URL: str = "https://focus.teamleader.eu/oauth2/authorize"
TOKEN_URL: str = "https://focus.teamleader.eu/oauth2/access_token"

# Seconds before expiry to consider a token "expired" and trigger a refresh
TOKEN_EXPIRY_MARGIN_SECONDS: int = 60

# Default HTTP timeout in seconds (overridable via settings.TEAMLEADER["TIMEOUT"])
DEFAULT_TIMEOUT: int = 30

# Default OAuth callback port (overridable via settings.TEAMLEADER["OAUTH_CALLBACK_PORT"])
DEFAULT_OAUTH_CALLBACK_PORT: int = 9999

# Pagination defaults
DEFAULT_PAGE_SIZE: int = 20
MAX_PAGE_SIZE: int = 100
