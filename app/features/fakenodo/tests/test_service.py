"""Service-level tests for fakenodo — exercises the versioning rules through
the service layer with a Flask app context (but no real HTTP calls).

These tests verify the core business rule:
  • Metadata-only edits → same DOI.
  • File changes + publish → new DOI, same concept DOI.
"""

import pytest

from app.features.fakenodo.services import FakenodoService

pytestmark = pytest.mark.service


@pytest.fixture(autouse=True)
def _clean_store():
    FakenodoService.clear_all()
    yield
    FakenodoService.clear_all()


def test_full_lifecycle_create_upload_publish_delete(test_app):
    """Walk through the entire lifecycle a ZenodoService consumer performs."""
    with test_app.app_context():
        # 1. Create
        dep = FakenodoService.create_deposition(metadata={"title": "Test DS", "upload_type": "dataset"})
        assert dep["state"] == "unsubmitted"

        # 2. Upload a file
        file_entry = FakenodoService.upload_file(dep["id"], "test.uvl", b"features\n    Root\n")
        assert file_entry["filename"] == "test.uvl"

        # 3. Publish
        published = FakenodoService.publish_deposition(dep["id"])
        assert published["doi"] is not None
        assert published["state"] == "done"

        # 4. Delete
        assert FakenodoService.delete_deposition(dep["id"]) is True
        assert FakenodoService.get_deposition(dep["id"]) is None


def test_metadata_edit_then_republish_keeps_doi(test_app):
    with test_app.app_context():
        dep = FakenodoService.create_deposition(metadata={"title": "v1"})
        published = FakenodoService.publish_deposition(dep["id"])
        original_doi = published["doi"]

        FakenodoService.update_metadata(dep["id"], {"title": "v1 edited"})
        re_published = FakenodoService.publish_deposition(dep["id"])

        assert re_published["doi"] == original_doi


def test_file_upload_after_publish_then_republish_changes_doi(test_app):
    with test_app.app_context():
        dep = FakenodoService.create_deposition(metadata={"title": "v1"})
        published = FakenodoService.publish_deposition(dep["id"])
        original_doi = published["doi"]

        FakenodoService.upload_file(dep["id"], "new.uvl", b"new content")
        re_published = FakenodoService.publish_deposition(dep["id"])

        assert re_published["doi"] != original_doi
        assert re_published["conceptdoi"] == published["conceptdoi"]


def test_newversion_workflow_produces_independent_draft(test_app):
    with test_app.app_context():
        dep = FakenodoService.create_deposition(metadata={"title": "original"})
        FakenodoService.publish_deposition(dep["id"])

        new = FakenodoService.new_version(dep["id"])
        assert new["id"] != dep["id"]
        assert new["conceptdoi"] == dep["conceptdoi"]

        FakenodoService.upload_file(new["id"], "v2.uvl", b"content v2")
        new_pub = FakenodoService.publish_deposition(new["id"])

        assert new_pub["doi"] is not None
        # Original deposition is untouched.
        original = FakenodoService.get_deposition(dep["id"])
        assert original is not None
