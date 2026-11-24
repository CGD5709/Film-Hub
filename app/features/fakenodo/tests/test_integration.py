"""HTTP integration tests for fakenodo via the Flask test client.

These tests hit the actual Flask routes that emulate the Zenodo API and
verify the HTTP contract that ``ZenodoService`` expects:

  POST   /fakenodo/api/deposit/depositions            → 201
  GET    /fakenodo/api/deposit/depositions            → 200
  GET    /fakenodo/api/deposit/depositions/<id>        → 200 | 404
  DELETE /fakenodo/api/deposit/depositions/<id>        → 204 | 404
  POST   /fakenodo/api/deposit/depositions/<id>/files  → 201 | 404
  POST   .../actions/publish                           → 202 | 404
  POST   .../actions/newversion                        → 201 | 404

It also verifies the versioning rule at the HTTP level:
  • metadata-only → same DOI  •  file change → new DOI
"""

import io

import pytest

from app.features.fakenodo.services import FakenodoService

pytestmark = pytest.mark.integration

API = "/fakenodo/api/deposit/depositions"


@pytest.fixture(autouse=True)
def _clean_store():
    FakenodoService.clear_all()
    yield
    FakenodoService.clear_all()


# ------------------------------------------------------------------
# Create / List
# ------------------------------------------------------------------


def test_create_deposition_returns_201(test_client):
    resp = test_client.post(API, json={"metadata": {"title": "DS"}})
    assert resp.status_code == 201
    body = resp.get_json()
    assert "id" in body
    assert body["state"] == "unsubmitted"


def test_list_depositions_returns_200(test_client):
    test_client.post(API, json={})
    test_client.post(API, json={})
    resp = test_client.get(API)
    assert resp.status_code == 200
    assert len(resp.get_json()) == 2


# ------------------------------------------------------------------
# Get / Delete
# ------------------------------------------------------------------


def test_get_deposition_returns_200(test_client):
    create = test_client.post(API, json={"metadata": {"title": "DS"}})
    dep_id = create.get_json()["id"]
    resp = test_client.get(f"{API}/{dep_id}")
    assert resp.status_code == 200
    assert resp.get_json()["id"] == dep_id


def test_get_unknown_deposition_returns_404(test_client):
    resp = test_client.get(f"{API}/9999")
    assert resp.status_code == 404


def test_delete_deposition_returns_204(test_client):
    create = test_client.post(API, json={})
    dep_id = create.get_json()["id"]
    resp = test_client.delete(f"{API}/{dep_id}")
    assert resp.status_code == 204


def test_delete_unknown_deposition_returns_404(test_client):
    resp = test_client.delete(f"{API}/9999")
    assert resp.status_code == 404


# ------------------------------------------------------------------
# File upload
# ------------------------------------------------------------------


def test_upload_file_returns_201(test_client):
    create = test_client.post(API, json={})
    dep_id = create.get_json()["id"]
    resp = test_client.post(
        f"{API}/{dep_id}/files",
        data={"name": "model.uvl", "file": (io.BytesIO(b"features\n"), "model.uvl")},
        content_type="multipart/form-data",
    )
    assert resp.status_code == 201
    assert resp.get_json()["filename"] == "model.uvl"


def test_upload_to_unknown_deposition_returns_404(test_client):
    resp = test_client.post(
        f"{API}/9999/files",
        data={"name": "x.uvl", "file": (io.BytesIO(b""), "x.uvl")},
        content_type="multipart/form-data",
    )
    assert resp.status_code == 404


# ------------------------------------------------------------------
# Publish
# ------------------------------------------------------------------


def test_publish_returns_202_with_doi(test_client):
    create = test_client.post(API, json={"metadata": {"title": "DS"}})
    dep_id = create.get_json()["id"]
    resp = test_client.post(f"{API}/{dep_id}/actions/publish")
    assert resp.status_code == 202
    body = resp.get_json()
    assert body["doi"] is not None
    assert body["state"] == "done"


def test_publish_unknown_deposition_returns_404(test_client):
    resp = test_client.post(f"{API}/9999/actions/publish")
    assert resp.status_code == 404


# ------------------------------------------------------------------
# New version
# ------------------------------------------------------------------


def test_newversion_returns_201(test_client):
    create = test_client.post(API, json={"metadata": {"title": "DS"}})
    dep_id = create.get_json()["id"]
    test_client.post(f"{API}/{dep_id}/actions/publish")

    resp = test_client.post(f"{API}/{dep_id}/actions/newversion")
    assert resp.status_code == 201
    body = resp.get_json()
    assert body["id"] != dep_id
    assert body["conceptdoi"] == create.get_json()["conceptdoi"]


def test_newversion_unknown_returns_404(test_client):
    resp = test_client.post(f"{API}/9999/actions/newversion")
    assert resp.status_code == 404


# ------------------------------------------------------------------
# Versioning rule at the HTTP level
# ------------------------------------------------------------------


def test_metadata_only_edit_preserves_doi_through_http(test_client):
    # Create + publish
    create = test_client.post(API, json={"metadata": {"title": "v1"}})
    dep_id = create.get_json()["id"]
    pub = test_client.post(f"{API}/{dep_id}/actions/publish")
    original_doi = pub.get_json()["doi"]

    # Metadata-only edit
    test_client.put(f"{API}/{dep_id}", json={"metadata": {"title": "v1 edited"}})
    re_pub = test_client.post(f"{API}/{dep_id}/actions/publish")

    assert re_pub.get_json()["doi"] == original_doi


def test_file_change_then_publish_changes_doi_through_http(test_client):
    # Create + publish
    create = test_client.post(API, json={"metadata": {"title": "v1"}})
    dep_id = create.get_json()["id"]
    pub = test_client.post(f"{API}/{dep_id}/actions/publish")
    original_doi = pub.get_json()["doi"]

    # Upload a file (changes files)
    test_client.post(
        f"{API}/{dep_id}/files",
        data={"name": "extra.uvl", "file": (io.BytesIO(b"features\n"), "extra.uvl")},
        content_type="multipart/form-data",
    )
    re_pub = test_client.post(f"{API}/{dep_id}/actions/publish")

    assert re_pub.get_json()["doi"] != original_doi
    assert re_pub.get_json()["conceptdoi"] == create.get_json()["conceptdoi"]


# ------------------------------------------------------------------
# Web view / Record preview
# ------------------------------------------------------------------


def test_view_record_returns_200_for_existing_deposition(test_client):
    create = test_client.post(API, json={"metadata": {"title": "DS"}})
    dep_id = create.get_json()["id"]
    resp = test_client.get(f"/fakenodo/records/{dep_id}")
    assert resp.status_code == 200
    assert resp.get_json()["id"] == dep_id


def test_view_record_returns_404_for_unknown_deposition(test_client):
    resp = test_client.get("/fakenodo/records/9999")
    assert resp.status_code == 404
