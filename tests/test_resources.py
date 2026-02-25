"""Unit tests for CrudResource and Page — Phase 7.

Tests are purely in-process: ``client._post`` is patched with
``unittest.mock.patch.object`` so no real HTTP calls are made and no
``@responses.activate`` decorator is needed.

Coverage
--------
Page
  - has_next is True when more pages exist
  - has_next is False on the last page
  - has_next is False when there are fewer items than page_size
  - has_next is False when total_count is zero
  - next() forwards page+1 and page_size to _resource.list()
  - next() forwards all stored _filters
  - next() raises ValueError when has_next is False

CrudResource._path
  - builds "prefix.operation" strings

CrudResource.list
  - POSTs to {prefix}.list with page / page_size body keys
  - merges **filters into the POST body
  - returns a Page with correct data, total_count, current_page, page_size
  - sets _resource and _filters on the returned Page
  - handles an empty result set (data=[])

CrudResource.get
  - POSTs to {prefix}.info with {"id": id}
  - returns the deserialised model

CrudResource.create
  - POSTs to {prefix}.add with the kwargs payload
  - re-fetches the full object via get() using the returned id
  - returns the fetched model

CrudResource.update
  - POSTs to {prefix}.update with {"id": id, **kwargs}
  - re-fetches via get() and returns the updated model

CrudResource.delete
  - POSTs to {prefix}.delete with {"id": id}
  - returns None

CrudResource.iterate
  - yields all items from a single page
  - fetches subsequent pages transparently for multi-page sets
  - stops after the last page (does not over-fetch)
  - custom page_size is forwarded to list()
  - **filters are forwarded to every list() call
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any
from unittest.mock import MagicMock, call, patch

import pytest

from teamleader.resources.base import CrudResource, Page


# ---------------------------------------------------------------------------
# Minimal fake model + resource used across all tests
# ---------------------------------------------------------------------------


@dataclass
class _FakeModel:
    id: str
    name: str = ""

    @classmethod
    def from_api(cls, data: dict[str, Any]) -> _FakeModel:
        return cls(id=data["id"], name=data.get("name", ""))


class _FakeResource(CrudResource[_FakeModel]):
    prefix = "fakes"
    model = _FakeModel


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_list_resp(
    items: list[dict[str, Any]],
    *,
    matches: int | None = None,
) -> dict[str, Any]:
    """Build a synthetic contacts.list-style response body."""
    return {
        "data": items,
        "meta": {"matches": matches if matches is not None else len(items)},
    }


def _make_info_resp(id: str, name: str = "Alice") -> dict[str, Any]:
    """Build a synthetic contacts.info-style response body."""
    return {"data": {"id": id, "name": name}}


def _make_add_resp(id: str) -> dict[str, Any]:
    """Build a synthetic contacts.add-style response body."""
    return {"data": {"type": "fake", "id": id}}


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture()
def mock_client() -> MagicMock:
    """A MagicMock that stands in for TeamleaderClient."""
    return MagicMock()


@pytest.fixture()
def resource(mock_client: MagicMock) -> _FakeResource:
    """A _FakeResource wired to the mock client."""
    return _FakeResource(mock_client)


# ===========================================================================
# Page tests
# ===========================================================================


class TestPageHasNext:
    def test_has_next_true_when_more_items_remain(self) -> None:
        page = Page(data=[], total_count=50, current_page=1, page_size=20)
        assert page.has_next is True

    def test_has_next_false_on_last_full_page(self) -> None:
        # 2 pages of 20 = 40 items; on page 2, 2*20 == 40 → no next
        page = Page(data=[], total_count=40, current_page=2, page_size=20)
        assert page.has_next is False

    def test_has_next_false_when_result_fits_in_one_page(self) -> None:
        # 5 items requested with page_size=20 → 1*20 >= 5 → no next
        page = Page(data=[], total_count=5, current_page=1, page_size=20)
        assert page.has_next is False

    def test_has_next_false_when_total_count_is_zero(self) -> None:
        page = Page(data=[], total_count=0, current_page=1, page_size=20)
        assert page.has_next is False

    def test_has_next_true_on_first_of_three_pages(self) -> None:
        # 55 items, page_size=20 → 3 pages; page 1: 1*20 < 55 → True
        page = Page(data=[], total_count=55, current_page=1, page_size=20)
        assert page.has_next is True

    def test_has_next_false_on_last_partial_page(self) -> None:
        # 55 items, page_size=20 → page 3: 3*20=60 >= 55 → False
        page = Page(data=[], total_count=55, current_page=3, page_size=20)
        assert page.has_next is False


class TestPageNext:
    def test_next_calls_resource_list_with_incremented_page(self) -> None:
        mock_resource = MagicMock()
        page = Page(data=[], total_count=50, current_page=1, page_size=20)
        page._resource = mock_resource
        page._filters = {}

        page.next()

        mock_resource.list.assert_called_once_with(page=2, page_size=20)

    def test_next_forwards_stored_filters(self) -> None:
        mock_resource = MagicMock()
        page = Page(data=[], total_count=50, current_page=1, page_size=20)
        page._resource = mock_resource
        page._filters = {"filter": {"email": "x@y.com"}, "sort": [{"field": "name"}]}

        page.next()

        mock_resource.list.assert_called_once_with(
            page=2,
            page_size=20,
            filter={"email": "x@y.com"},
            sort=[{"field": "name"}],
        )

    def test_next_returns_whatever_resource_list_returns(self) -> None:
        next_page = Page(data=[], total_count=50, current_page=2, page_size=20)
        mock_resource = MagicMock()
        mock_resource.list.return_value = next_page

        page = Page(data=[], total_count=50, current_page=1, page_size=20)
        page._resource = mock_resource
        page._filters = {}

        result = page.next()

        assert result is next_page

    def test_next_raises_value_error_when_no_more_pages(self) -> None:
        page = Page(data=[], total_count=5, current_page=1, page_size=20)
        page._resource = MagicMock()

        with pytest.raises(ValueError, match="No more pages"):
            page.next()


# ===========================================================================
# CrudResource._path
# ===========================================================================


class TestCrudResourcePath:
    def test_path_list(self, resource: _FakeResource) -> None:
        assert resource._path("list") == "fakes.list"

    def test_path_info(self, resource: _FakeResource) -> None:
        assert resource._path("info") == "fakes.info"

    def test_path_add(self, resource: _FakeResource) -> None:
        assert resource._path("add") == "fakes.add"

    def test_path_custom_operation(self, resource: _FakeResource) -> None:
        assert resource._path("tag") == "fakes.tag"


# ===========================================================================
# CrudResource.list
# ===========================================================================


class TestCrudResourceList:
    def test_list_posts_to_correct_endpoint(
        self, resource: _FakeResource, mock_client: MagicMock
    ) -> None:
        mock_client._post.return_value = _make_list_resp([])

        resource.list()

        path = mock_client._post.call_args[0][0]
        assert path == "fakes.list"

    def test_list_posts_page_params_in_body(
        self, resource: _FakeResource, mock_client: MagicMock
    ) -> None:
        mock_client._post.return_value = _make_list_resp([])

        resource.list(page=3, page_size=10)

        body = mock_client._post.call_args[0][1]
        assert body["page"] == {"size": 10, "number": 3}

    def test_list_default_page_params(
        self, resource: _FakeResource, mock_client: MagicMock
    ) -> None:
        mock_client._post.return_value = _make_list_resp([])

        resource.list()

        body = mock_client._post.call_args[0][1]
        assert body["page"] == {"size": 20, "number": 1}

    def test_list_merges_filters_into_body(
        self, resource: _FakeResource, mock_client: MagicMock
    ) -> None:
        mock_client._post.return_value = _make_list_resp([])

        resource.list(filter={"name": "Bob"}, sort=[{"field": "name"}])

        body = mock_client._post.call_args[0][1]
        assert body["filter"] == {"name": "Bob"}
        assert body["sort"] == [{"field": "name"}]

    def test_list_returns_page_with_correct_data(
        self, resource: _FakeResource, mock_client: MagicMock
    ) -> None:
        mock_client._post.return_value = _make_list_resp(
            [{"id": "id-1", "name": "Alice"}, {"id": "id-2", "name": "Bob"}],
            matches=42,
        )

        result = resource.list()

        assert len(result.data) == 2
        assert result.data[0] == _FakeModel(id="id-1", name="Alice")
        assert result.data[1] == _FakeModel(id="id-2", name="Bob")

    def test_list_returns_page_with_correct_metadata(
        self, resource: _FakeResource, mock_client: MagicMock
    ) -> None:
        mock_client._post.return_value = _make_list_resp([], matches=99)

        result = resource.list(page=2, page_size=10)

        assert result.total_count == 99
        assert result.current_page == 2
        assert result.page_size == 10

    def test_list_sets_resource_on_page(
        self, resource: _FakeResource, mock_client: MagicMock
    ) -> None:
        mock_client._post.return_value = _make_list_resp([])

        result = resource.list()

        assert result._resource is resource

    def test_list_sets_filters_on_page(
        self, resource: _FakeResource, mock_client: MagicMock
    ) -> None:
        mock_client._post.return_value = _make_list_resp([])

        result = resource.list(filter={"name": "Bob"})

        assert result._filters == {"filter": {"name": "Bob"}}

    def test_list_empty_result(
        self, resource: _FakeResource, mock_client: MagicMock
    ) -> None:
        mock_client._post.return_value = _make_list_resp([], matches=0)

        result = resource.list()

        assert result.data == []
        assert result.total_count == 0
        assert result.has_next is False


# ===========================================================================
# CrudResource.get
# ===========================================================================


class TestCrudResourceGet:
    def test_get_posts_to_info_endpoint(
        self, resource: _FakeResource, mock_client: MagicMock
    ) -> None:
        mock_client._post.return_value = _make_info_resp("id-1")

        resource.get("id-1")

        mock_client._post.assert_called_once_with("fakes.info", {"id": "id-1"})

    def test_get_returns_deserialised_model(
        self, resource: _FakeResource, mock_client: MagicMock
    ) -> None:
        mock_client._post.return_value = _make_info_resp("id-1", "Alice")

        result = resource.get("id-1")

        assert result == _FakeModel(id="id-1", name="Alice")

    def test_get_passes_id_in_body(
        self, resource: _FakeResource, mock_client: MagicMock
    ) -> None:
        mock_client._post.return_value = _make_info_resp("uuid-xyz")

        resource.get("uuid-xyz")

        body = mock_client._post.call_args[0][1]
        assert body == {"id": "uuid-xyz"}


# ===========================================================================
# CrudResource.create
# ===========================================================================


class TestCrudResourceCreate:
    def test_create_posts_to_add_endpoint(
        self, resource: _FakeResource, mock_client: MagicMock
    ) -> None:
        mock_client._post.side_effect = [
            _make_add_resp("new-id"),           # .add call
            _make_info_resp("new-id", "Carol"),  # .info re-fetch
        ]

        resource.create(name="Carol")

        first_call_path = mock_client._post.call_args_list[0][0][0]
        assert first_call_path == "fakes.add"

    def test_create_sends_kwargs_as_body(
        self, resource: _FakeResource, mock_client: MagicMock
    ) -> None:
        mock_client._post.side_effect = [
            _make_add_resp("new-id"),
            _make_info_resp("new-id", "Carol"),
        ]

        resource.create(name="Carol", extra="value")

        add_body = mock_client._post.call_args_list[0][0][1]
        assert add_body == {"name": "Carol", "extra": "value"}

    def test_create_refetches_by_returned_id(
        self, resource: _FakeResource, mock_client: MagicMock
    ) -> None:
        mock_client._post.side_effect = [
            _make_add_resp("new-id"),
            _make_info_resp("new-id", "Carol"),
        ]

        resource.create(name="Carol")

        info_call = mock_client._post.call_args_list[1]
        assert info_call == call("fakes.info", {"id": "new-id"})

    def test_create_returns_full_model(
        self, resource: _FakeResource, mock_client: MagicMock
    ) -> None:
        mock_client._post.side_effect = [
            _make_add_resp("new-id"),
            _make_info_resp("new-id", "Carol"),
        ]

        result = resource.create(name="Carol")

        assert result == _FakeModel(id="new-id", name="Carol")


# ===========================================================================
# CrudResource.update
# ===========================================================================


class TestCrudResourceUpdate:
    def test_update_posts_to_update_endpoint(
        self, resource: _FakeResource, mock_client: MagicMock
    ) -> None:
        mock_client._post.side_effect = [
            {},                                 # .update call (empty body)
            _make_info_resp("id-1", "Dave"),    # .info re-fetch
        ]

        resource.update("id-1", name="Dave")

        first_call_path = mock_client._post.call_args_list[0][0][0]
        assert first_call_path == "fakes.update"

    def test_update_sends_id_and_kwargs_in_body(
        self, resource: _FakeResource, mock_client: MagicMock
    ) -> None:
        mock_client._post.side_effect = [
            {},
            _make_info_resp("id-1", "Dave"),
        ]

        resource.update("id-1", name="Dave", extra="data")

        update_body = mock_client._post.call_args_list[0][0][1]
        assert update_body == {"id": "id-1", "name": "Dave", "extra": "data"}

    def test_update_refetches_after_update(
        self, resource: _FakeResource, mock_client: MagicMock
    ) -> None:
        mock_client._post.side_effect = [
            {},
            _make_info_resp("id-1", "Dave"),
        ]

        resource.update("id-1", name="Dave")

        info_call = mock_client._post.call_args_list[1]
        assert info_call == call("fakes.info", {"id": "id-1"})

    def test_update_returns_refreshed_model(
        self, resource: _FakeResource, mock_client: MagicMock
    ) -> None:
        mock_client._post.side_effect = [
            {},
            _make_info_resp("id-1", "Dave"),
        ]

        result = resource.update("id-1", name="Dave")

        assert result == _FakeModel(id="id-1", name="Dave")


# ===========================================================================
# CrudResource.delete
# ===========================================================================


class TestCrudResourceDelete:
    def test_delete_posts_to_delete_endpoint(
        self, resource: _FakeResource, mock_client: MagicMock
    ) -> None:
        mock_client._post.return_value = {}

        resource.delete("id-1")

        mock_client._post.assert_called_once_with("fakes.delete", {"id": "id-1"})

    def test_delete_returns_none(
        self, resource: _FakeResource, mock_client: MagicMock
    ) -> None:
        mock_client._post.return_value = {}

        result = resource.delete("id-1")

        assert result is None


# ===========================================================================
# CrudResource.iterate
# ===========================================================================


class TestCrudResourceIterate:
    def test_iterate_yields_all_items_single_page(
        self, resource: _FakeResource, mock_client: MagicMock
    ) -> None:
        mock_client._post.return_value = _make_list_resp(
            [{"id": "a", "name": "A"}, {"id": "b", "name": "B"}],
            matches=2,
        )

        result = list(resource.iterate())

        assert result == [_FakeModel("a", "A"), _FakeModel("b", "B")]

    def test_iterate_fetches_multiple_pages(
        self, resource: _FakeResource, mock_client: MagicMock
    ) -> None:
        mock_client._post.side_effect = [
            _make_list_resp(
                [{"id": "a", "name": "A"}, {"id": "b", "name": "B"}],
                matches=4,
            ),
            _make_list_resp(
                [{"id": "c", "name": "C"}, {"id": "d", "name": "D"}],
                matches=4,
            ),
        ]

        result = list(resource.iterate(page_size=2))

        assert result == [
            _FakeModel("a", "A"),
            _FakeModel("b", "B"),
            _FakeModel("c", "C"),
            _FakeModel("d", "D"),
        ]

    def test_iterate_makes_exactly_two_api_calls_for_two_pages(
        self, resource: _FakeResource, mock_client: MagicMock
    ) -> None:
        mock_client._post.side_effect = [
            _make_list_resp([{"id": "a"}], matches=2),
            _make_list_resp([{"id": "b"}], matches=2),
        ]

        list(resource.iterate(page_size=1))

        assert mock_client._post.call_count == 2

    def test_iterate_stops_after_last_page_no_extra_fetch(
        self, resource: _FakeResource, mock_client: MagicMock
    ) -> None:
        # 3 items, page_size=20 → only one API call, no second page
        mock_client._post.return_value = _make_list_resp(
            [{"id": "a"}, {"id": "b"}, {"id": "c"}],
            matches=3,
        )

        list(resource.iterate(page_size=20))

        assert mock_client._post.call_count == 1

    def test_iterate_forwards_custom_page_size(
        self, resource: _FakeResource, mock_client: MagicMock
    ) -> None:
        mock_client._post.return_value = _make_list_resp([], matches=0)

        list(resource.iterate(page_size=50))

        body = mock_client._post.call_args[0][1]
        assert body["page"]["size"] == 50

    def test_iterate_forwards_filters_to_every_page(
        self, resource: _FakeResource, mock_client: MagicMock
    ) -> None:
        mock_client._post.side_effect = [
            _make_list_resp([{"id": "a"}], matches=2),
            _make_list_resp([{"id": "b"}], matches=2),
        ]

        list(resource.iterate(page_size=1, filter={"name": "X"}))

        for c in mock_client._post.call_args_list:
            body = c[0][1]
            assert body.get("filter") == {"name": "X"}

    def test_iterate_empty_result_yields_nothing(
        self, resource: _FakeResource, mock_client: MagicMock
    ) -> None:
        mock_client._post.return_value = _make_list_resp([], matches=0)

        result = list(resource.iterate())

        assert result == []
