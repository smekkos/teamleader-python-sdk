"""Unit tests for FilesResource and the File model.

Tests are purely in-process: ``client._post`` is replaced with a
``MagicMock`` so no real HTTP calls are made.

Coverage
--------
File.from_api
  - deserialises a bare data dict
  - unwraps a ``{"data": {...}}`` wrapper
  - handles all nullable fields absent → defaults to None / empty strings / 0

FilesResource.upload
  - POSTs to ``files.upload`` with name + subject in body
  - passes optional folder when provided
  - omits folder key when not provided
  - returns the data dict from the response

FilesResource.upload_content
  - calls upload() to obtain location + id
  - PUTs raw bytes to the signed URL with correct Content-Type header
  - returns the file id from the upload response (NOT from PUT response body)
  - raises HTTPError when the PUT returns a non-2xx status

FilesResource.download
  - POSTs to ``files.download`` with {"id": id}
  - returns the data dict (location + expires_at)

FilesResource.list
  - POSTs to ``files.list`` with correct filter + page body
  - returns a Page[File]
  - passes optional sort into the body
  - Page.data contains properly deserialised File instances

FilesResource.get  (inherited CrudResource.get)
  - POSTs to ``files.info`` with {"id": id}
  - returns a deserialised File

FilesResource.delete  (inherited CrudResource.delete)
  - POSTs to ``files.delete`` with {"id": id}
  - returns None

FilesResource.create / update / iterate
  - raise NotImplementedError
"""

from __future__ import annotations

from typing import Any
from unittest.mock import MagicMock, patch, call

import pytest
import responses as responses_lib

from teamleader.models.file import File
from teamleader.resources.base import Page
from teamleader.resources.files import FilesResource


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

_FILE_UUID = "aabbccdd-0000-1111-2222-333344445555"
_SIGNED_URL = "https://storage.example.com/upload?token=abc123"
_CDN_URL = "https://cdn.example.com/files/aabbccdd"

_FILE_DATA: dict[str, Any] = {
    "id": _FILE_UUID,
    "name": "report.pdf",
    "mime_type": "application/pdf",
    "size": 12345,
    "updated_at": "2024-06-01T12:00:00+00:00",
    "subject": {"type": "deal", "id": "deal-uuid-0001"},
    "uploaded_by": {"type": "user", "id": "user-uuid-0001"},
    "folder": "Documents",
}

_UPLOAD_RESPONSE: dict[str, Any] = {
    "data": {
        "id": _FILE_UUID,
        "location": _SIGNED_URL,
        "expires_at": "2024-06-01T12:02:00+00:00",
    }
}

_DOWNLOAD_RESPONSE: dict[str, Any] = {
    "data": {
        "location": _CDN_URL,
        "expires_at": "2024-06-01T12:05:00+00:00",
    }
}

_INFO_RESPONSE: dict[str, Any] = {"data": _FILE_DATA}

_LIST_RESPONSE: dict[str, Any] = {
    "data": [_FILE_DATA],
    "meta": {"matches": 1},
}


def _make_resource() -> tuple[FilesResource, MagicMock]:
    """Return a FilesResource wired to a MagicMock client."""
    mock_client = MagicMock()
    resource = FilesResource(mock_client)
    return resource, mock_client


# ---------------------------------------------------------------------------
# File.from_api
# ---------------------------------------------------------------------------


class TestFileFromApi:
    def test_deserialises_bare_dict(self) -> None:
        f = File.from_api(_FILE_DATA)
        assert f.id == _FILE_UUID
        assert f.name == "report.pdf"
        assert f.mime_type == "application/pdf"
        assert f.size == 12345
        assert f.updated_at == "2024-06-01T12:00:00+00:00"
        assert f.subject == {"type": "deal", "id": "deal-uuid-0001"}
        assert f.uploaded_by == {"type": "user", "id": "user-uuid-0001"}
        assert f.folder == "Documents"

    def test_unwraps_data_wrapper(self) -> None:
        f = File.from_api({"data": _FILE_DATA})
        assert f.id == _FILE_UUID

    def test_nullable_fields_default_to_none(self) -> None:
        f = File.from_api({"id": "x", "name": "x.txt"})
        assert f.subject is None
        assert f.uploaded_by is None
        assert f.folder is None

    def test_numeric_defaults(self) -> None:
        f = File.from_api({})
        assert f.id == ""
        assert f.name == ""
        assert f.mime_type == ""
        assert f.size == 0
        assert f.updated_at == ""


# ---------------------------------------------------------------------------
# FilesResource.upload
# ---------------------------------------------------------------------------


class TestFilesUpload:
    def test_posts_to_files_upload(self) -> None:
        resource, mock_client = _make_resource()
        mock_client._post.return_value = _UPLOAD_RESPONSE

        resource.upload("report.pdf", {"type": "deal", "id": "deal-uuid-0001"})

        mock_client._post.assert_called_once_with(
            "files.upload",
            {"name": "report.pdf", "subject": {"type": "deal", "id": "deal-uuid-0001"}},
        )

    def test_includes_folder_when_provided(self) -> None:
        resource, mock_client = _make_resource()
        mock_client._post.return_value = _UPLOAD_RESPONSE

        resource.upload("report.pdf", {"type": "deal", "id": "x"}, folder="Documents")

        _, body = mock_client._post.call_args.args
        assert body["folder"] == "Documents"

    def test_omits_folder_key_when_not_provided(self) -> None:
        resource, mock_client = _make_resource()
        mock_client._post.return_value = _UPLOAD_RESPONSE

        resource.upload("report.pdf", {"type": "deal", "id": "x"})

        _, body = mock_client._post.call_args.args
        assert "folder" not in body

    def test_returns_data_dict(self) -> None:
        resource, mock_client = _make_resource()
        mock_client._post.return_value = _UPLOAD_RESPONSE

        result = resource.upload("report.pdf", {"type": "deal", "id": "x"})

        assert result["id"] == _FILE_UUID
        assert result["location"] == _SIGNED_URL


# ---------------------------------------------------------------------------
# FilesResource.upload_content
# ---------------------------------------------------------------------------


class TestFilesUploadContent:
    def test_returns_file_id_from_step2_post_response(self) -> None:
        """The file UUID is returned by the Teamleader step-2 upload endpoint, not step-1."""
        resource, mock_client = _make_resource()
        mock_client._post.return_value = _UPLOAD_RESPONSE

        with patch("teamleader.resources.files._requests.post") as mock_post:
            mock_post.return_value.raise_for_status = MagicMock()
            mock_post.return_value.json.return_value = {"data": {"id": _FILE_UUID}}
            file_id = resource.upload_content(
                "report.pdf",
                b"PDF content",
                {"type": "deal", "id": "deal-uuid-0001"},
            )

        assert file_id == _FILE_UUID

    def test_posts_bytes_to_upload_url(self) -> None:
        resource, mock_client = _make_resource()
        mock_client._post.return_value = _UPLOAD_RESPONSE

        with patch("teamleader.resources.files._requests.post") as mock_post:
            mock_post.return_value.raise_for_status = MagicMock()
            mock_post.return_value.json.return_value = {"data": {"id": _FILE_UUID}}
            resource.upload_content("report.pdf", b"PDF content", {"type": "deal", "id": "x"})

        mock_post.assert_called_once()
        post_args, post_kwargs = mock_post.call_args
        assert post_args[0] == _SIGNED_URL
        assert post_kwargs["data"] == b"PDF content"

    def test_sends_default_content_type_header(self) -> None:
        resource, mock_client = _make_resource()
        mock_client._post.return_value = _UPLOAD_RESPONSE

        with patch("teamleader.resources.files._requests.post") as mock_post:
            mock_post.return_value.raise_for_status = MagicMock()
            mock_post.return_value.json.return_value = {"data": {"id": _FILE_UUID}}
            resource.upload_content("f.bin", b"bytes", {"type": "deal", "id": "x"})

        _, post_kwargs = mock_post.call_args
        assert post_kwargs["headers"]["Content-Type"] == "application/octet-stream"

    def test_sends_custom_content_type_header(self) -> None:
        resource, mock_client = _make_resource()
        mock_client._post.return_value = _UPLOAD_RESPONSE

        with patch("teamleader.resources.files._requests.post") as mock_post:
            mock_post.return_value.raise_for_status = MagicMock()
            mock_post.return_value.json.return_value = {"data": {"id": _FILE_UUID}}
            resource.upload_content(
                "doc.pdf", b"bytes", {"type": "deal", "id": "x"},
                content_type="application/pdf",
            )

        _, post_kwargs = mock_post.call_args
        assert post_kwargs["headers"]["Content-Type"] == "application/pdf"

    def test_raises_http_error_on_post_failure(self) -> None:
        resource, mock_client = _make_resource()
        mock_client._post.return_value = _UPLOAD_RESPONSE

        import requests as _req
        with patch("teamleader.resources.files._requests.post") as mock_post:
            mock_post.return_value.raise_for_status.side_effect = _req.HTTPError("403 Forbidden")
            with pytest.raises(_req.HTTPError):
                resource.upload_content("f.bin", b"x", {"type": "deal", "id": "x"})

    def test_file_id_comes_from_step2_post_response_not_step1(self) -> None:
        """The step-1 files.upload response has no id — the UUID comes from the step-2 POST."""
        resource, mock_client = _make_resource()
        # Upload response has no id field (confirmed by the API spec)
        upload_resp_without_id = {"data": {"location": _SIGNED_URL, "expires_at": "2024-06-01T12:02:00+00:00"}}
        mock_client._post.return_value = upload_resp_without_id

        with patch("teamleader.resources.files._requests.post") as mock_post:
            mock_post.return_value.raise_for_status = MagicMock()
            mock_post.return_value.json.return_value = {"data": {"id": _FILE_UUID}}

            file_id = resource.upload_content("f.pdf", b"x", {"type": "deal", "id": "x"})

        assert file_id == _FILE_UUID


# ---------------------------------------------------------------------------
# FilesResource.download
# ---------------------------------------------------------------------------


class TestFilesDownload:
    def test_posts_to_files_download(self) -> None:
        resource, mock_client = _make_resource()
        mock_client._post.return_value = _DOWNLOAD_RESPONSE

        resource.download(_FILE_UUID)

        mock_client._post.assert_called_once_with("files.download", {"id": _FILE_UUID})

    def test_returns_data_dict(self) -> None:
        resource, mock_client = _make_resource()
        mock_client._post.return_value = _DOWNLOAD_RESPONSE

        result = resource.download(_FILE_UUID)

        assert result["location"] == _CDN_URL
        assert "expires_at" in result


# ---------------------------------------------------------------------------
# FilesResource.list
# ---------------------------------------------------------------------------


class TestFilesList:
    def _list_response(self, items: list[dict[str, Any]], matches: int | None = None) -> dict[str, Any]:
        return {
            "data": items,
            "meta": {"matches": matches if matches is not None else len(items)},
        }

    def test_posts_to_files_list_with_filter_and_page(self) -> None:
        resource, mock_client = _make_resource()
        mock_client._post.return_value = self._list_response([_FILE_DATA], matches=1)

        subject_filter = {"subject": {"type": "deal", "id": "deal-uuid-0001"}}
        resource.list(subject_filter, page=1, page_size=5)

        path, body = mock_client._post.call_args.args
        assert path == "files.list"
        assert body["filter"] == subject_filter
        assert body["page"] == {"size": 5, "number": 1}

    def test_returns_page_of_file_instances(self) -> None:
        resource, mock_client = _make_resource()
        mock_client._post.return_value = self._list_response([_FILE_DATA], matches=1)

        page = resource.list({"subject": {"type": "deal", "id": "x"}})

        assert isinstance(page, Page)
        assert len(page.data) == 1
        assert isinstance(page.data[0], File)
        assert page.data[0].id == _FILE_UUID

    def test_page_total_count_from_meta_matches(self) -> None:
        resource, mock_client = _make_resource()
        mock_client._post.return_value = self._list_response([_FILE_DATA], matches=42)

        page = resource.list({"subject": {"type": "deal", "id": "x"}})

        assert page.total_count == 42

    def test_passes_sort_into_body(self) -> None:
        resource, mock_client = _make_resource()
        mock_client._post.return_value = self._list_response([], matches=0)

        sort = [{"field": "updated_at", "order": "desc"}]
        resource.list({"subject": {"type": "deal", "id": "x"}}, sort=sort)

        _, body = mock_client._post.call_args.args
        assert body["sort"] == sort

    def test_omits_sort_when_not_provided(self) -> None:
        resource, mock_client = _make_resource()
        mock_client._post.return_value = self._list_response([], matches=0)

        resource.list({"subject": {"type": "deal", "id": "x"}})

        _, body = mock_client._post.call_args.args
        assert "sort" not in body

    def test_empty_result_returns_empty_page(self) -> None:
        resource, mock_client = _make_resource()
        mock_client._post.return_value = self._list_response([], matches=0)

        page = resource.list({"subject": {"type": "deal", "id": "x"}})

        assert page.data == []
        assert page.total_count == 0
        assert page.has_next is False


# ---------------------------------------------------------------------------
# FilesResource.get  (inherited CrudResource.get → files.info)
# ---------------------------------------------------------------------------


class TestFilesGet:
    def test_posts_to_files_info(self) -> None:
        resource, mock_client = _make_resource()
        mock_client._post.return_value = _INFO_RESPONSE

        resource.get(_FILE_UUID)

        mock_client._post.assert_called_once_with("files.info", {"id": _FILE_UUID})

    def test_returns_file_instance(self) -> None:
        resource, mock_client = _make_resource()
        mock_client._post.return_value = _INFO_RESPONSE

        f = resource.get(_FILE_UUID)

        assert isinstance(f, File)
        assert f.id == _FILE_UUID
        assert f.name == "report.pdf"


# ---------------------------------------------------------------------------
# FilesResource.delete  (inherited CrudResource.delete → files.delete)
# ---------------------------------------------------------------------------


class TestFilesDelete:
    def test_posts_to_files_delete(self) -> None:
        resource, mock_client = _make_resource()
        mock_client._post.return_value = {}

        resource.delete(_FILE_UUID)

        mock_client._post.assert_called_once_with("files.delete", {"id": _FILE_UUID})

    def test_returns_none(self) -> None:
        resource, mock_client = _make_resource()
        mock_client._post.return_value = {}

        result = resource.delete(_FILE_UUID)

        assert result is None


# ---------------------------------------------------------------------------
# Unsupported operations
# ---------------------------------------------------------------------------


class TestFilesUnsupportedOperations:
    def test_create_raises_not_implemented(self) -> None:
        resource, _ = _make_resource()
        with pytest.raises(NotImplementedError, match="upload_content"):
            resource.create(name="x.pdf")

    def test_update_raises_not_implemented(self) -> None:
        resource, _ = _make_resource()
        with pytest.raises(NotImplementedError):
            resource.update(_FILE_UUID, name="new.pdf")

    def test_iterate_raises_not_implemented(self) -> None:
        resource, _ = _make_resource()
        with pytest.raises(NotImplementedError, match="list\\(\\)"):
            # iterate() is a generator — must consume it to trigger the error
            list(resource.iterate())
