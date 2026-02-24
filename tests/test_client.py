"""Unit tests for TeamleaderClient — Phase 6.

Covers:
- _post / _get inject the correct Authorization: Bearer header
- _post / _get return the parsed JSON body on success
- 204 No Content → empty dict
- Each error status code → the correct SDK exception subclass
- TeamleaderRateLimitError.retry_after from Retry-After header
- TeamleaderRateLimitError.retry_after is None when header is absent
- _extract_message understands JSON:API errors array
- _extract_message understands OAuth error_description / message / error keys
- _extract_message falls back to response.text for non-JSON and unknown bodies
- Resource attributes are the correct types
- Custom timeout is stored and passed through
"""

from __future__ import annotations

import json

import pytest
import responses

from teamleader.client import TeamleaderClient
from teamleader.constants import BASE_URL
from teamleader.exceptions import (
    TeamleaderAPIError,
    TeamleaderAuthError,
    TeamleaderNotFoundError,
    TeamleaderPermissionError,
    TeamleaderRateLimitError,
    TeamleaderServerError,
    TeamleaderValidationError,
)
from teamleader.resources.companies import CompaniesResource
from teamleader.resources.contacts import ContactsResource
from teamleader.resources.deals import DealsResource
from teamleader.resources.invoices import InvoicesResource
from teamleader.resources.quotations import QuotationsResource


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

_LIST_URL = f"{BASE_URL}/contacts.list"
_ME_URL = f"{BASE_URL}/users.me"
_JSON_HEADERS = {"Content-Type": "application/json"}


def _json_body(payload: dict) -> str:
    return json.dumps(payload)


# ---------------------------------------------------------------------------
# Resource attribute types
# ---------------------------------------------------------------------------


class TestResourceAttributes:
    def test_contacts_is_contacts_resource(self, client: TeamleaderClient) -> None:
        assert isinstance(client.contacts, ContactsResource)

    def test_companies_is_companies_resource(self, client: TeamleaderClient) -> None:
        assert isinstance(client.companies, CompaniesResource)

    def test_deals_is_deals_resource(self, client: TeamleaderClient) -> None:
        assert isinstance(client.deals, DealsResource)

    def test_invoices_is_invoices_resource(self, client: TeamleaderClient) -> None:
        assert isinstance(client.invoices, InvoicesResource)

    def test_quotations_is_quotations_resource(self, client: TeamleaderClient) -> None:
        assert isinstance(client.quotations, QuotationsResource)


# ---------------------------------------------------------------------------
# Timeout
# ---------------------------------------------------------------------------


class TestTimeout:
    def test_default_timeout_is_stored(self, handler) -> None:
        from teamleader.constants import DEFAULT_TIMEOUT

        c = TeamleaderClient(handler)
        assert c._timeout == DEFAULT_TIMEOUT

    def test_custom_timeout_is_stored(self, handler) -> None:
        c = TeamleaderClient(handler, timeout=5)
        assert c._timeout == 5


# ---------------------------------------------------------------------------
# _post — happy path
# ---------------------------------------------------------------------------


class TestPost:
    @responses.activate
    def test_post_sends_bearer_token(self, client: TeamleaderClient) -> None:
        responses.add(
            responses.POST,
            _LIST_URL,
            json={"data": []},
            status=200,
        )

        client._post("contacts.list")

        assert len(responses.calls) == 1
        auth = responses.calls[0].request.headers.get("Authorization")
        assert auth == "Bearer acc_valid"

    @responses.activate
    def test_post_returns_parsed_json(self, client: TeamleaderClient) -> None:
        payload = {"data": [{"id": "abc", "type": "contact"}], "meta": {"count": 1}}
        responses.add(responses.POST, _LIST_URL, json=payload, status=200)

        result = client._post("contacts.list", json={"page": {"size": 20, "number": 1}})

        assert result == payload

    @responses.activate
    def test_post_forwards_json_body(self, client: TeamleaderClient) -> None:
        responses.add(responses.POST, _LIST_URL, json={}, status=200)

        client._post("contacts.list", json={"filter": {"name": "Alice"}})

        sent_body = json.loads(responses.calls[0].request.body)
        assert sent_body == {"filter": {"name": "Alice"}}

    @responses.activate
    def test_post_none_body_sends_no_json(self, client: TeamleaderClient) -> None:
        responses.add(responses.POST, _LIST_URL, json={}, status=200)

        client._post("contacts.list")  # json=None by default

        # requests sends no body / Content-Type when json=None
        assert responses.calls[0].request.body is None


# ---------------------------------------------------------------------------
# _get — happy path
# ---------------------------------------------------------------------------


class TestGet:
    @responses.activate
    def test_get_sends_bearer_token(self, client: TeamleaderClient) -> None:
        responses.add(responses.GET, _ME_URL, json={"data": {}}, status=200)

        client._get("users.me")

        auth = responses.calls[0].request.headers.get("Authorization")
        assert auth == "Bearer acc_valid"

    @responses.activate
    def test_get_returns_parsed_json(self, client: TeamleaderClient) -> None:
        payload = {"data": {"id": "u1", "type": "user"}}
        responses.add(responses.GET, _ME_URL, json=payload, status=200)

        result = client._get("users.me")

        assert result == payload

    @responses.activate
    def test_get_passes_query_params(self, client: TeamleaderClient) -> None:
        responses.add(responses.GET, _ME_URL, json={}, status=200)

        client._get("users.me", params={"foo": "bar"})

        assert "foo=bar" in responses.calls[0].request.url

    @responses.activate
    def test_get_204_returns_empty_dict(self, client: TeamleaderClient) -> None:
        responses.add(responses.GET, _ME_URL, body=b"", status=204)

        result = client._get("users.me")

        assert result == {}


# ---------------------------------------------------------------------------
# _handle_response — error mapping
# ---------------------------------------------------------------------------


class TestHandleResponse:
    @responses.activate
    def test_401_raises_auth_error(self, client: TeamleaderClient) -> None:
        responses.add(
            responses.POST,
            _LIST_URL,
            json={"error": "unauthorized", "error_description": "Bad token."},
            status=401,
        )

        with pytest.raises(TeamleaderAuthError) as exc_info:
            client._post("contacts.list")

        assert exc_info.value.status_code == 401
        assert exc_info.value.message == "Bad token."

    @responses.activate
    def test_403_raises_permission_error(self, client: TeamleaderClient) -> None:
        responses.add(
            responses.POST,
            _LIST_URL,
            json={"errors": [{"title": "Forbidden."}]},
            status=403,
        )

        with pytest.raises(TeamleaderPermissionError) as exc_info:
            client._post("contacts.list")

        assert exc_info.value.status_code == 403

    @responses.activate
    def test_404_raises_not_found(self, client: TeamleaderClient) -> None:
        responses.add(
            responses.POST,
            _LIST_URL,
            json={"errors": [{"title": "Not found."}]},
            status=404,
        )

        with pytest.raises(TeamleaderNotFoundError) as exc_info:
            client._post("contacts.list")

        assert exc_info.value.status_code == 404
        assert exc_info.value.message == "Not found."

    @responses.activate
    def test_422_raises_validation_error(self, client: TeamleaderClient) -> None:
        responses.add(
            responses.POST,
            _LIST_URL,
            json={"errors": [{"title": "field is required."}]},
            status=422,
        )

        with pytest.raises(TeamleaderValidationError) as exc_info:
            client._post("contacts.list")

        assert exc_info.value.status_code == 422

    @responses.activate
    def test_429_raises_rate_limit_error_with_retry_after(
        self, client: TeamleaderClient
    ) -> None:
        responses.add(
            responses.POST,
            _LIST_URL,
            json={"errors": [{"title": "Too many requests."}]},
            status=429,
            headers={"Retry-After": "42"},
        )

        with pytest.raises(TeamleaderRateLimitError) as exc_info:
            client._post("contacts.list")

        err = exc_info.value
        assert err.status_code == 429
        assert err.retry_after == 42

    @responses.activate
    def test_429_retry_after_none_when_header_absent(
        self, client: TeamleaderClient
    ) -> None:
        responses.add(
            responses.POST,
            _LIST_URL,
            json={"errors": [{"title": "Too many requests."}]},
            status=429,
        )

        with pytest.raises(TeamleaderRateLimitError) as exc_info:
            client._post("contacts.list")

        assert exc_info.value.retry_after is None

    @responses.activate
    def test_500_raises_server_error(self, client: TeamleaderClient) -> None:
        responses.add(
            responses.POST,
            _LIST_URL,
            json={"errors": [{"title": "Internal Server Error."}]},
            status=500,
        )

        with pytest.raises(TeamleaderServerError) as exc_info:
            client._post("contacts.list")

        assert exc_info.value.status_code == 500

    @responses.activate
    def test_503_raises_server_error(self, client: TeamleaderClient) -> None:
        responses.add(
            responses.POST,
            _LIST_URL,
            body=b"Service Unavailable",
            status=503,
        )

        with pytest.raises(TeamleaderServerError) as exc_info:
            client._post("contacts.list")

        assert exc_info.value.status_code == 503

    @responses.activate
    def test_unexpected_4xx_raises_api_error(self, client: TeamleaderClient) -> None:
        responses.add(
            responses.POST,
            _LIST_URL,
            json={"errors": [{"title": "Conflict."}]},
            status=409,
        )

        with pytest.raises(TeamleaderAPIError) as exc_info:
            client._post("contacts.list")

        assert exc_info.value.status_code == 409

    @responses.activate
    def test_raw_response_attached_to_exception(
        self, client: TeamleaderClient
    ) -> None:
        responses.add(responses.POST, _LIST_URL, json={}, status=404)

        with pytest.raises(TeamleaderNotFoundError) as exc_info:
            client._post("contacts.list")

        assert exc_info.value.raw_response is not None


# ---------------------------------------------------------------------------
# _extract_message
# ---------------------------------------------------------------------------


class TestExtractMessage:
    """Tests for _extract_message via _post so we get a real Response object."""

    @responses.activate
    def test_json_api_errors_array(self, client: TeamleaderClient) -> None:
        responses.add(
            responses.POST,
            _LIST_URL,
            json={"errors": [{"title": "First error."}, {"title": "Second error."}]},
            status=422,
        )

        with pytest.raises(TeamleaderValidationError) as exc_info:
            client._post("contacts.list")

        assert exc_info.value.message == "First error.; Second error."

    @responses.activate
    def test_oauth_error_description_key(self, client: TeamleaderClient) -> None:
        responses.add(
            responses.POST,
            _LIST_URL,
            json={"error": "invalid_token", "error_description": "Token has expired."},
            status=401,
        )

        with pytest.raises(TeamleaderAuthError) as exc_info:
            client._post("contacts.list")

        assert exc_info.value.message == "Token has expired."

    @responses.activate
    def test_message_key(self, client: TeamleaderClient) -> None:
        responses.add(
            responses.POST,
            _LIST_URL,
            json={"message": "Something went wrong."},
            status=500,
        )

        with pytest.raises(TeamleaderServerError) as exc_info:
            client._post("contacts.list")

        assert exc_info.value.message == "Something went wrong."

    @responses.activate
    def test_error_key_fallback(self, client: TeamleaderClient) -> None:
        responses.add(
            responses.POST,
            _LIST_URL,
            json={"error": "bad_request"},
            status=400,
        )

        with pytest.raises(TeamleaderAPIError) as exc_info:
            client._post("contacts.list")

        assert exc_info.value.message == "bad_request"

    @responses.activate
    def test_non_json_body_falls_back_to_text(
        self, client: TeamleaderClient
    ) -> None:
        responses.add(
            responses.POST,
            _LIST_URL,
            body=b"Gateway Timeout",
            status=504,
        )

        with pytest.raises(TeamleaderServerError) as exc_info:
            client._post("contacts.list")

        assert exc_info.value.message == "Gateway Timeout"

    @responses.activate
    def test_empty_error_body_uses_http_status_fallback(
        self, client: TeamleaderClient
    ) -> None:
        responses.add(
            responses.POST,
            _LIST_URL,
            body=b"",
            status=500,
        )

        with pytest.raises(TeamleaderServerError) as exc_info:
            client._post("contacts.list")

        assert exc_info.value.message == "HTTP 500"
