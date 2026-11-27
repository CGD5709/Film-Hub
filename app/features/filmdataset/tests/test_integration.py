"""HTTP integration tests for the filmdataset feature via the Flask test client."""

from io import BytesIO
from unittest.mock import patch

import pytest

from app.features.auth.repositories import UserRepository
from app.features.dataset.models import PublicationType
from app.features.dataset.repositories import DataSetRepository, DSDownloadRecordRepository, DSMetaDataRepository
from app.features.filmdataset.models import FilmDataset
from app.features.filmdataset.repositories import FilmdatasetRepository

pytestmark = pytest.mark.integration

VALID_CSV_BYTES = (
    b"title,year,genre,rating\n"
    b"The Godfather,1972,Crime,9.2\n"
    b"Pulp Fiction,1994,Crime,8.9\n"
    b"Inception,2010,Sci-Fi,8.8\n"
)


def _signup(test_client, email="owner@example.com", password="ownerpass"):
    response = test_client.post(
        "/signup/",
        data={"email": email, "password": password, "name": "Olivia", "surname": "Owner"},
        follow_redirects=False,
    )
    assert response.status_code in (302, 303)
    with test_client.application.app_context():
        return UserRepository().get_by_email(email).id


def test_filmdataset_index_and_upload_page_auth(test_client):
    assert test_client.get("/filmdataset").status_code == 200

    anon = test_client.get("/filmdataset/upload", follow_redirects=False)
    assert anon.status_code == 302
    assert "/login" in anon.headers["Location"]

    _signup(test_client)
    upload_page = test_client.get("/filmdataset/upload")
    assert upload_page.status_code == 200
    upload_html = upload_page.get_data(as_text=True)
    assert "filmDropzone" in upload_html
    assert "csv_filename" in upload_html
    assert "film_csv_errors" in upload_html
    assert "film_upload_button" in upload_html


def test_temp_csv_upload_and_delete_endpoints(test_client, monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("WORKING_DIR", str(tmp_path))
    _signup(test_client)

    bad_ext = test_client.post(
        "/filmdataset/file/upload",
        data={"file": (BytesIO(b"hello"), "notes.txt")},
        content_type="multipart/form-data",
    )
    assert bad_ext.status_code == 400

    bad_csv = test_client.post(
        "/filmdataset/file/upload",
        data={"file": (BytesIO(b"title,year\nMatrix,1999\n"), "bad.csv")},
        content_type="multipart/form-data",
    )
    assert bad_csv.status_code == 400
    assert "errors" in bad_csv.get_json()

    ok = test_client.post(
        "/filmdataset/file/upload",
        data={"file": (BytesIO(VALID_CSV_BYTES), "movies.csv")},
        content_type="multipart/form-data",
    )
    assert ok.status_code == 200
    payload = ok.get_json()
    assert payload["filename"] == "movies.csv"
    assert payload["metrics"]["total_movies"] == 3

    deleted = test_client.post("/filmdataset/file/delete", json={"file": "movies.csv"})
    assert deleted.status_code == 200
    assert test_client.post("/filmdataset/file/delete", json={"file": "movies.csv"}).status_code == 404


def test_end_to_end_upload_preview_and_download_flow(test_client, monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("WORKING_DIR", str(tmp_path))
    user_id = _signup(test_client, email="creator@example.com")

    bad_form = test_client.post("/filmdataset/upload", data={"title": "", "desc": ""})
    assert bad_form.status_code == 400

    upload_resp = test_client.post(
        "/filmdataset/file/upload",
        data={"file": (BytesIO(VALID_CSV_BYTES), "movies.csv")},
        content_type="multipart/form-data",
    )
    assert upload_resp.status_code == 200

    with patch("app.features.zenodo.services.ZenodoService") as zenodo_cls:
        zenodo_inst = zenodo_cls.return_value
        zenodo_inst.create_new_deposition.return_value = {"id": 77, "conceptrecid": "78"}
        zenodo_inst.get_doi.return_value = "10.5281/zenodo.filmhub.77"

        create_resp = test_client.post(
            "/filmdataset/upload",
            data={
                "title": "Integration Film Dataset",
                "desc": "Uploaded through integration test",
                "publication_type": PublicationType.DATA_MANAGEMENT_PLAN.value,
                "tags": "movies,integration",
                "csv_filename": "movies.csv",
            },
        )
    assert create_resp.status_code == 200
    create_payload = create_resp.get_json()
    dataset_id = create_payload["dataset_id"]
    assert create_payload["dataset_url"].endswith("/doi/10.5281/zenodo.filmhub.77/")

    with test_client.application.app_context():
        persisted = FilmdatasetRepository().get_by_id(dataset_id)
        assert isinstance(persisted, FilmDataset)
        assert persisted.user_id == user_id
        assert persisted.total_movies == 3

    # Detail page uses Film-Hub template with metrics and preview container, keeping common blocks
    detail_resp = test_client.get("/doi/10.5281/zenodo.filmhub.77/")
    assert detail_resp.status_code == 200
    detail_html = detail_resp.get_data(as_text=True)
    assert "film-metrics-cards" in detail_html
    assert "film-preview-section" in detail_html
    assert f"/filmdataset/{dataset_id}/preview" in detail_html
    assert "1972 - 2010" in detail_html
    assert "Crime" in detail_html
    assert "movies.csv" in detail_html
    assert "Embed badge" in detail_html
    assert "UVL models" not in detail_html

    # Film catalog index lists the published film dataset
    catalog_resp = test_client.get("/filmdataset")
    assert catalog_resp.status_code == 200
    assert "Integration Film Dataset" in catalog_resp.get_data(as_text=True)

    # Preview works with pagination for synchronized dataset
    preview = test_client.get(f"/filmdataset/{dataset_id}/preview?page=1&per_page=2")
    assert preview.status_code == 200
    preview_data = preview.get_json()
    assert preview_data["total"] == 3
    assert len(preview_data["rows"]) == 2
    assert preview_data["rows"][0]["title"] == "The Godfather"

    # Unknown dataset returns 404
    assert test_client.get("/filmdataset/99999/preview").status_code == 404

    # Download returns zip archive and records download
    dl = test_client.get(f"/filmdataset/download/{dataset_id}")
    assert dl.status_code == 200
    assert dl.mimetype == "application/zip"
    assert "download_cookie" in dl.headers.get("Set-Cookie", "")

    with test_client.application.app_context():
        assert DSDownloadRecordRepository().total_dataset_downloads() == 1


def test_unsynchronized_preview_is_private_to_owner(test_client, monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("WORKING_DIR", str(tmp_path))
    owner_id = _signup(test_client, email="private_owner@example.com")

    test_client.post(
        "/filmdataset/file/upload",
        data={"file": (BytesIO(VALID_CSV_BYTES), "private.csv")},
        content_type="multipart/form-data",
    )
    with patch("app.features.zenodo.services.ZenodoService") as zenodo_cls:
        zenodo_cls.return_value.create_new_deposition.return_value = {}
        resp = test_client.post(
            "/filmdataset/upload",
            data={
                "title": "Private Draft",
                "desc": "No DOI yet",
                "publication_type": PublicationType.NONE.value,
                "csv_filename": "private.csv",
            },
        )
    dataset_id = resp.get_json()["dataset_id"]

    # Owner can preview unsynchronized dataset and view its film detail page
    assert test_client.get(f"/filmdataset/{dataset_id}/preview").status_code == 200
    unsync_view = test_client.get(f"/dataset/unsynchronized/{dataset_id}/")
    assert unsync_view.status_code == 200
    unsync_html = unsync_view.get_data(as_text=True)
    assert "Private Draft" in unsync_html
    assert "film-preview-section" in unsync_html

    # Logout & login as another user -> 404
    test_client.get("/logout", follow_redirects=False)
    assert test_client.get(f"/filmdataset/{dataset_id}/preview").status_code == 404

    other_id = _signup(test_client, email="stranger@example.com")
    assert other_id != owner_id
    assert test_client.get(f"/filmdataset/{dataset_id}/preview").status_code == 404

    # Once DOI is set, everyone can preview
    with test_client.application.app_context():
        ds = FilmdatasetRepository().get_by_id(dataset_id)
        DSMetaDataRepository().update(ds.ds_meta_data_id, dataset_doi="10.1234/public-now")
    assert test_client.get(f"/filmdataset/{dataset_id}/preview").status_code == 200


def test_uvl_detail_view_keeps_original_layout_without_film_blocks(test_client):
    user_id = _signup(test_client, email="uvl_owner@example.com")
    with test_client.application.app_context():
        meta = DSMetaDataRepository().create(
            title="UVL Regression Dataset",
            description="Classic UVL dataset",
            publication_type=PublicationType.SOFTWARE_DOCUMENTATION,
            dataset_doi="10.1234/uvl-regression",
            tags="uvl",
        )
        DataSetRepository().create(user_id=user_id, ds_meta_data_id=meta.id)

    resp = test_client.get("/doi/10.1234/uvl-regression/")
    assert resp.status_code == 200
    body = resp.get_data(as_text=True)
    assert "UVL models" in body
    assert "film-preview-section" not in body
    assert "film-metrics-cards" not in body
