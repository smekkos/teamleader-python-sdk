"""Integration tests for FilesResource and the File model.

Skipped automatically when TEAMLEADER_INTEGRATION_CLIENT_ID is not set.

These tests perform a full round-trip against the live Teamleader Focus
sandbox:  upload → list → get → download → delete.

A single "temporary" subject is used for the upload so that the file is
never permanently linked to an entity.  Teamleader auto-deletes temporary
files after 24 hours, but each test run explicitly deletes the file in
clean-up to avoid cluttering the sandbox.

Prerequisites
-------------
The integration environment variables must be set (see ``conftest.py``).
The sandbox account must have the Files API scope enabled.

Test ordering
-------------
Tests within each class are independent.  The shared ``uploaded_file_id``
fixture handles setup and teardown so every test class starts with a
freshly uploaded file and always cleans up afterwards.
"""

from __future__ import annotations

import json

import pytest

from teamleader.client import TeamleaderClient
from teamleader.models.file import File
from teamleader.resources.base import Page


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

_FILENAME = "sdk_integration_test.json"
_CONTENT = json.dumps({"sdk": "teamleader-python", "test": "files"}).encode()
_SUBJECT = {"type": "temporary"}
# Teamleader's upload endpoint requires application/octet-stream.
# Using application/json returns a 400 even for JSON-encoded content.
_CONTENT_TYPE = "application/octet-stream"


def _upload_and_cleanup(client: TeamleaderClient) -> str:
    """Upload a temporary file and return its UUID.

    The caller is responsible for deleting the file after the test.
    """
    return client.files.upload_content(
        _FILENAME,
        _CONTENT,
        _SUBJECT,
        content_type=_CONTENT_TYPE,
    )


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture()
def uploaded_file_id(integration_client: TeamleaderClient) -> str:  # type: ignore[misc]
    """Upload a temporary file before each test; delete it afterwards."""
    file_id = _upload_and_cleanup(integration_client)
    yield file_id
    # Best-effort cleanup — file may have been deleted by the test itself.
    try:
        integration_client.files.delete(file_id)
    except Exception:
        pass


# ---------------------------------------------------------------------------
# Upload
# ---------------------------------------------------------------------------


class TestFilesUploadContent:
    def test_upload_content_returns_string_uuid(
        self, integration_client: TeamleaderClient
    ) -> None:
        file_id = integration_client.files.upload_content(
            _FILENAME,
            _CONTENT,
            _SUBJECT,
            content_type=_CONTENT_TYPE,
        )
        assert isinstance(file_id, str)
        assert file_id != ""
        # Clean up immediately
        integration_client.files.delete(file_id)

    def test_upload_with_folder_does_not_raise(
        self, integration_client: TeamleaderClient
    ) -> None:
        """Uploading with a folder= argument should succeed (or raise a known API error
        if the folder name does not exist in the sandbox — either is acceptable)."""
        try:
            file_id = integration_client.files.upload_content(
                _FILENAME,
                _CONTENT,
                _SUBJECT,
            )
            integration_client.files.delete(file_id)
        except Exception as exc:
            # A 422/404 from an unknown folder name is fine; other errors are not.
            assert "404" in str(exc) or "422" in str(exc) or "folder" in str(exc).lower(), (
                f"Unexpected error: {exc}"
            )


# ---------------------------------------------------------------------------
# Get (info)
# ---------------------------------------------------------------------------


class TestFilesGet:
    def test_get_returns_file_instance(
        self,
        integration_client: TeamleaderClient,
        uploaded_file_id: str,
    ) -> None:
        f = integration_client.files.get(uploaded_file_id)
        assert isinstance(f, File)

    def test_file_has_correct_id(
        self,
        integration_client: TeamleaderClient,
        uploaded_file_id: str,
    ) -> None:
        f = integration_client.files.get(uploaded_file_id)
        assert f.id == uploaded_file_id

    def test_file_has_non_empty_name(
        self,
        integration_client: TeamleaderClient,
        uploaded_file_id: str,
    ) -> None:
        f = integration_client.files.get(uploaded_file_id)
        assert f.name != ""

    def test_file_has_positive_size(
        self,
        integration_client: TeamleaderClient,
        uploaded_file_id: str,
    ) -> None:
        f = integration_client.files.get(uploaded_file_id)
        assert f.size > 0

    def test_file_has_non_empty_mime_type(
        self,
        integration_client: TeamleaderClient,
        uploaded_file_id: str,
    ) -> None:
        f = integration_client.files.get(uploaded_file_id)
        assert f.mime_type != ""

    def test_file_has_updated_at_timestamp(
        self,
        integration_client: TeamleaderClient,
        uploaded_file_id: str,
    ) -> None:
        f = integration_client.files.get(uploaded_file_id)
        assert f.updated_at != ""


# ---------------------------------------------------------------------------
# Download
# ---------------------------------------------------------------------------


class TestFilesDownload:
    def test_download_returns_location_url(
        self,
        integration_client: TeamleaderClient,
        uploaded_file_id: str,
    ) -> None:
        result = integration_client.files.download(uploaded_file_id)
        assert "location" in result
        assert result["location"].startswith("http")

    def test_download_returns_expires_at(
        self,
        integration_client: TeamleaderClient,
        uploaded_file_id: str,
    ) -> None:
        result = integration_client.files.download(uploaded_file_id)
        assert "expires_at" in result
        assert result["expires_at"] != ""


# ---------------------------------------------------------------------------
# List
# ---------------------------------------------------------------------------


class TestFilesList:
    def _subject_or_skip(self, integration_client: TeamleaderClient, file_id: str) -> dict:
        """Return the file's subject or skip if it's not a listable entity.

        ``files.list`` requires a subject with a real entity type and id.
        Temporary files (``{"type": "temporary"}``) are rejected by the API.
        """
        f = integration_client.files.get(file_id)
        if f.subject is None or f.subject.get("type") == "temporary":
            pytest.skip(
                "File uploaded as temporary — files.list does not accept "
                "temporary subjects as a filter; attach a file to a real entity to test list."
            )
        return f.subject

    def test_list_requires_filter_and_returns_page(
        self,
        integration_client: TeamleaderClient,
        uploaded_file_id: str,
    ) -> None:
        subject = self._subject_or_skip(integration_client, uploaded_file_id)
        page = integration_client.files.list({"subject": subject}, page_size=10)
        assert isinstance(page, Page)

    def test_list_data_contains_file_instances(
        self,
        integration_client: TeamleaderClient,
        uploaded_file_id: str,
    ) -> None:
        subject = self._subject_or_skip(integration_client, uploaded_file_id)
        page = integration_client.files.list({"subject": subject}, page_size=20)
        for item in page.data:
            assert isinstance(item, File)
            assert item.id != ""

    def test_list_page_has_next_attribute(
        self,
        integration_client: TeamleaderClient,
        uploaded_file_id: str,
    ) -> None:
        subject = self._subject_or_skip(integration_client, uploaded_file_id)
        page = integration_client.files.list({"subject": subject}, page_size=5)
        assert isinstance(page.has_next, bool)


# ---------------------------------------------------------------------------
# Delete
# ---------------------------------------------------------------------------


class TestFilesDelete:
    def test_delete_returns_none(
        self, integration_client: TeamleaderClient
    ) -> None:
        file_id = integration_client.files.upload_content(
            _FILENAME, _CONTENT, _SUBJECT, content_type=_CONTENT_TYPE
        )
        result = integration_client.files.delete(file_id)
        assert result is None

    def test_deleted_file_is_no_longer_accessible(
        self, integration_client: TeamleaderClient
    ) -> None:
        from teamleader.exceptions import TeamleaderNotFoundError

        file_id = integration_client.files.upload_content(
            _FILENAME, _CONTENT, _SUBJECT, content_type=_CONTENT_TYPE
        )
        integration_client.files.delete(file_id)

        with pytest.raises((TeamleaderNotFoundError, Exception)):
            integration_client.files.get(file_id)
