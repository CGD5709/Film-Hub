"""Service-level tests for the filmdataset feature and Zenodo CSV upload."""

import os
from io import BytesIO
from unittest.mock import MagicMock, patch

import pytest
from werkzeug.datastructures import FileStorage

from app.features.auth.repositories import UserRepository
from app.features.dataset.models import PublicationType
from app.features.filmdataset.forms import FilmdatasetForm
from app.features.filmdataset.models import FilmDataset
from app.features.filmdataset.services import FilmdatasetService
from app.features.profile.repositories import UserProfileRepository
from app.features.zenodo.services import ZenodoService

pytestmark = pytest.mark.service

VALID_CSV_BYTES = (
    b"title,year,genre,rating\n"
    b"The Godfather,1972,Crime,9.2\n"
    b"Pulp Fiction,1994,Crime,8.9\n"
    b"Inception,2010,Sci-Fi,8.8\n"
)


def _make_user_with_profile(email="owner@example.com"):
    user = UserRepository().create(email=email, password="secret")
    UserProfileRepository().create(
        user_id=user.id,
        name="Jane",
        surname="Doe",
        affiliation="ETSII US",
        orcid="0000-0000-0000-0001",
    )
    return user


def _csv_upload(filename, content=VALID_CSV_BYTES):
    return FileStorage(stream=BytesIO(content), filename=filename, content_type="text/csv")


def test_save_temp_csv_validates_rejects_bad_files_and_disambiguates(test_app, clean_database, monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("WORKING_DIR", str(tmp_path))

    with test_app.app_context():
        user = _make_user_with_profile()
        service = FilmdatasetService()

        bad_ext = service.save_temp_csv(_csv_upload("notes.txt"), user)
        assert bad_ext["code"] == 400

        bad_csv = service.save_temp_csv(_csv_upload("bad.csv", b"title,year\nOnly Two,2020\n"), user)
        assert bad_csv["code"] == 400
        assert "errors" in bad_csv
        assert not os.path.exists(os.path.join(user.temp_folder(), "bad.csv"))

        first = service.save_temp_csv(_csv_upload("movies.csv"), user)
        second = service.save_temp_csv(_csv_upload("movies.csv"), user)
        assert first["code"] == 200
        assert first["filename"] == "movies.csv"
        assert first["metrics"]["total_movies"] == 3
        assert second["code"] == 200
        assert second["filename"] == "movies (1).csv"


def test_delete_temp_csv_handles_missing_and_existing_files(test_app, clean_database, monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("WORKING_DIR", str(tmp_path))

    with test_app.app_context():
        user = _make_user_with_profile()
        service = FilmdatasetService()

        assert service.delete_temp_csv("", user)["code"] == 400
        assert service.delete_temp_csv("ghost.csv", user)["code"] == 404

        service.save_temp_csv(_csv_upload("movies.csv"), user)
        deleted = service.delete_temp_csv("movies.csv", user)
        assert deleted["code"] == 200
        assert not os.path.exists(os.path.join(user.temp_folder(), "movies.csv"))


def test_create_from_form_persists_film_dataset_and_moves_csv(test_app, clean_database, monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("WORKING_DIR", str(tmp_path))

    with test_app.app_context():
        user = _make_user_with_profile()
        service = FilmdatasetService()
        service.save_temp_csv(_csv_upload("movies.csv"), user)

        with test_app.test_request_context():
            form = FilmdatasetForm(
                data={
                    "title": "Top Movies",
                    "desc": "Curated film dataset",
                    "publication_type": PublicationType.DATA_MANAGEMENT_PLAN.value,
                    "tags": "movies,csv",
                    "csv_filename": "movies.csv",
                }
            )
            dataset = service.create_from_form(form, user)
            dest_path = service.move_csv_file(dataset, user)

        assert isinstance(dataset, FilmDataset)
        assert dataset.total_movies == 3
        assert dataset.min_year == 1972
        assert dataset.max_year == 2010
        assert dataset.primary_genre == "Crime"
        assert dataset.file_size > 0
        assert dataset.checksum is not None
        assert os.path.exists(dest_path)


def test_upload_dataset_syncs_with_zenodo_and_handles_partial_failure(test_app, clean_database, monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("WORKING_DIR", str(tmp_path))

    with test_app.app_context():
        user = _make_user_with_profile()
        service = FilmdatasetService()
        service.save_temp_csv(_csv_upload("movies.csv"), user)

        with patch("app.features.zenodo.services.ZenodoService") as zenodo_cls:
            zenodo_inst = zenodo_cls.return_value
            zenodo_inst.create_new_deposition.return_value = {"id": 99, "conceptrecid": "100"}
            zenodo_inst.get_doi.return_value = "10.5281/zenodo.filmhub.99"

            with test_app.test_request_context():
                form = FilmdatasetForm(
                    data={
                        "title": "Synced Movies",
                        "desc": "Desc",
                        "publication_type": PublicationType.NONE.value,
                        "csv_filename": "movies.csv",
                    }
                )
                result = service.upload_dataset(form, user)

        assert result["status"] == "ok"
        assert result["code"] == 200
        saved = service.get_or_404(result["dataset_id"])
        assert saved.ds_meta_data.dataset_doi == "10.5281/zenodo.filmhub.99"
        assert not os.path.exists(user.temp_folder())

        # Partial failure when Zenodo upload raises
        service.save_temp_csv(_csv_upload("movies2.csv"), user)
        with patch("app.features.zenodo.services.ZenodoService") as zenodo_cls:
            zenodo_inst = zenodo_cls.return_value
            zenodo_inst.create_new_deposition.return_value = {"id": 101, "conceptrecid": "102"}
            zenodo_inst.upload_dataset_file.side_effect = RuntimeError("zenodo unavailable")

            with test_app.test_request_context():
                form2 = FilmdatasetForm(
                    data={
                        "title": "Partial Movies",
                        "desc": "Desc",
                        "publication_type": PublicationType.NONE.value,
                        "csv_filename": "movies2.csv",
                    }
                )
                partial = service.upload_dataset(form2, user)

        assert partial["status"] == "partial"
        assert partial["code"] == 200
        assert "dataset_id" in partial


def test_get_preview_rows_paginates_and_handles_missing_file(test_app, clean_database, monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("WORKING_DIR", str(tmp_path))

    with test_app.app_context():
        user = _make_user_with_profile()
        service = FilmdatasetService()
        service.save_temp_csv(_csv_upload("movies.csv"), user)

        with test_app.test_request_context():
            form = FilmdatasetForm(
                data={
                    "title": "Preview Movies",
                    "desc": "Desc",
                    "publication_type": PublicationType.NONE.value,
                    "csv_filename": "movies.csv",
                }
            )
            dataset = service.create_from_form(form, user)
            dest_path = service.move_csv_file(dataset, user)

        page1 = service.get_preview_rows(dataset, page=1, per_page=2)
        page2 = service.get_preview_rows(dataset, page=2, per_page=2)

        assert page1["headers"] == ["title", "year", "genre", "rating"]
        assert page1["total"] == 3
        assert len(page1["rows"]) == 2
        assert page1["rows"][0]["title"] == "The Godfather"
        assert len(page2["rows"]) == 1
        assert page2["rows"][0]["title"] == "Inception"

        os.remove(dest_path)
        missing = service.get_preview_rows(dataset)
        assert missing["rows"] == []
        assert missing["total"] == 0


def test_zenodo_upload_dataset_file_posts_and_raises_on_error(test_app, clean_database, monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("WORKING_DIR", str(tmp_path))

    with test_app.app_context():
        user = _make_user_with_profile()
        service = FilmdatasetService()
        service.save_temp_csv(_csv_upload("movies.csv"), user)

        with test_app.test_request_context():
            form = FilmdatasetForm(
                data={
                    "title": "Zenodo File",
                    "desc": "Desc",
                    "publication_type": PublicationType.NONE.value,
                    "csv_filename": "movies.csv",
                }
            )
            dataset = service.create_from_form(form, user)
            service.move_csv_file(dataset, user)

        zenodo = ZenodoService()
        ok_resp = MagicMock(status_code=201)
        ok_resp.json.return_value = {"id": "file-1"}

        with patch("app.features.zenodo.services.requests.post", return_value=ok_resp) as post_mock:
            res = zenodo.upload_dataset_file(dataset, 55, "movies.csv", user=user)
            assert res == {"id": "file-1"}
            assert post_mock.call_args[0][0].endswith("/55/files")

        err_resp = MagicMock(status_code=400)
        err_resp.json.return_value = {"message": "bad file"}
        with patch("app.features.zenodo.services.requests.post", return_value=err_resp):
            with pytest.raises(Exception, match="Failed to upload files"):
                zenodo.upload_dataset_file(dataset, 55, "movies.csv", user=user)
