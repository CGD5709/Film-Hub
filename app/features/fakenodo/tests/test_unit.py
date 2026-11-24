"""Unit tests for fakenodo — pure logic, no Flask app, no database.

Covers the in-memory ``FakenodoService`` directly: creation, publishing,
metadata-only vs file-change versioning, and the ``newversion`` action.
"""

import pytest

from app.features.fakenodo.services import FakenodoService

pytestmark = pytest.mark.unit


@pytest.fixture(autouse=True)
def _clean_store():
    """Reset the in-memory store before every test."""
    FakenodoService.clear_all()
    yield
    FakenodoService.clear_all()


# ------------------------------------------------------------------
# Basic CRUD
# ------------------------------------------------------------------


def test_create_deposition_returns_an_id_and_unsubmitted_state():
    dep = FakenodoService.create_deposition(metadata={"title": "My DS"})
    assert dep["id"] >= 1
    assert dep["state"] == "unsubmitted"
    assert dep["doi"] is None
    assert dep["metadata"]["title"] == "My DS"


def test_get_deposition_returns_none_for_unknown_id():
    assert FakenodoService.get_deposition(999) is None


def test_list_depositions_returns_all_created():
    FakenodoService.create_deposition()
    FakenodoService.create_deposition()
    assert len(FakenodoService.list_depositions()) == 2


def test_delete_deposition_removes_it():
    dep = FakenodoService.create_deposition()
    assert FakenodoService.delete_deposition(dep["id"]) is True
    assert FakenodoService.get_deposition(dep["id"]) is None


def test_delete_returns_false_for_unknown_id():
    assert FakenodoService.delete_deposition(999) is False


# ------------------------------------------------------------------
# File upload
# ------------------------------------------------------------------


def test_upload_file_stores_file_metadata():
    dep = FakenodoService.create_deposition()
    result = FakenodoService.upload_file(dep["id"], "model.uvl", b"features\n")
    assert result is not None
    assert result["filename"] == "model.uvl"
    assert result["filesize"] == len(b"features\n")


def test_upload_file_to_unknown_deposition_returns_none():
    assert FakenodoService.upload_file(999, "x.uvl", b"") is None


# ------------------------------------------------------------------
# Publish
# ------------------------------------------------------------------


def test_publish_assigns_a_doi():
    dep = FakenodoService.create_deposition(metadata={"title": "DS"})
    published = FakenodoService.publish_deposition(dep["id"])
    assert published["doi"] is not None
    assert published["doi"].startswith("10.5072/fakenodo.")
    assert published["state"] == "done"


def test_publish_unknown_deposition_returns_none():
    assert FakenodoService.publish_deposition(999) is None


# ------------------------------------------------------------------
# Versioning rule: metadata-only vs file-change
# ------------------------------------------------------------------


def test_metadata_only_edit_keeps_the_same_doi():
    dep = FakenodoService.create_deposition(metadata={"title": "v1"})
    published = FakenodoService.publish_deposition(dep["id"])
    original_doi = published["doi"]

    # Edit metadata only — no file upload.
    FakenodoService.update_metadata(dep["id"], {"title": "v1-edited"})
    re_published = FakenodoService.publish_deposition(dep["id"])

    assert re_published["doi"] == original_doi, "Metadata-only edit must keep the same DOI"


def test_file_change_then_publish_generates_new_doi():
    dep = FakenodoService.create_deposition(metadata={"title": "v1"})
    published = FakenodoService.publish_deposition(dep["id"])
    original_doi = published["doi"]

    # Upload a new file → marks files as changed.
    FakenodoService.upload_file(dep["id"], "extra.uvl", b"features\n")
    re_published = FakenodoService.publish_deposition(dep["id"])

    assert re_published["doi"] != original_doi, "File change must generate a new DOI"
    assert re_published["conceptdoi"] == published["conceptdoi"], "Concept DOI must stay the same"


# ------------------------------------------------------------------
# New version action
# ------------------------------------------------------------------


def test_new_version_creates_a_draft_with_same_concept_doi():
    dep = FakenodoService.create_deposition(metadata={"title": "original"})
    FakenodoService.publish_deposition(dep["id"])

    new_dep = FakenodoService.new_version(dep["id"])
    assert new_dep["id"] != dep["id"]
    assert new_dep["state"] == "unsubmitted"
    assert new_dep["doi"] is None
    assert new_dep["conceptdoi"] == dep["conceptdoi"]


def test_new_version_of_unknown_deposition_returns_none():
    assert FakenodoService.new_version(999) is None


def test_new_version_publish_assigns_new_doi():
    dep = FakenodoService.create_deposition(metadata={"title": "original"})
    published = FakenodoService.publish_deposition(dep["id"])

    new_dep = FakenodoService.new_version(dep["id"])
    FakenodoService.upload_file(new_dep["id"], "v2.uvl", b"content")
    new_published = FakenodoService.publish_deposition(new_dep["id"])

    assert new_published["doi"] is not None
    assert new_published["doi"] != published["doi"]
    assert new_published["conceptdoi"] == published["conceptdoi"]


# ------------------------------------------------------------------
# Update metadata
# ------------------------------------------------------------------


def test_update_metadata_replaces_the_metadata_dict():
    dep = FakenodoService.create_deposition(metadata={"title": "old"})
    updated = FakenodoService.update_metadata(dep["id"], {"title": "new"})
    assert updated["metadata"]["title"] == "new"


def test_update_metadata_on_unknown_deposition_returns_none():
    assert FakenodoService.update_metadata(999, {}) is None


# ------------------------------------------------------------------
# clear_all
# ------------------------------------------------------------------


def test_clear_all_empties_the_store():
    FakenodoService.create_deposition()
    FakenodoService.clear_all()
    assert FakenodoService.list_depositions() == []
