"""DatabaseTokenBackend — Django ORM implementation of TokenBackend.

Full implementation in Phase 5.
"""

from __future__ import annotations

from teamleader.auth import Token, TokenBackend


class DatabaseTokenBackend(TokenBackend):
    """Stores the OAuth2 token in the ``TeamleaderToken`` Django model.

    Uses ``select_for_update()`` inside ``transaction.atomic()`` to
    prevent race conditions in multi-worker deployments.

    Full implementation in Phase 5.
    """

    def get(self) -> Token | None:
        raise NotImplementedError  # Phase 5

    def save(self, token: Token) -> None:
        raise NotImplementedError  # Phase 5

    def clear(self) -> None:
        raise NotImplementedError  # Phase 5
