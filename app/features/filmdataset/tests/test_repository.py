"""Repository-level tests for the filmdataset feature against a real database."""

from datetime import datetime, timedelta, timezone

import pytest

from app.features.auth.repositories import UserRepository
from app.features.dataset.models import PublicationType
from app.features.dataset.repositories import DataSetRepository, DSMetaDataRepository
from app.features.filmdataset.models import FilmDataset
from app.features.filmdataset.repositories import FilmdatasetRepository

pytestmark = pytest.mark.repository


def _make_user(email):
    return UserRepository().create(email=email, password="secret")


def _make_film_dataset(
    user,
    title="Sample Film Dataset",
    doi=None,
    csv_filename="movies.csv",
    total_movies=5,
    file_size=512,
    created_at=None,
):
    meta = DSMetaDataRepository().create(
        title=title,
        description=f"Description for {title}",
        publication_type=PublicationType.DATA_MANAGEMENT_PLAN,
        dataset_doi=doi,
        tags="cinema,tmdb",
    )
    return FilmdatasetRepository().create(
        user_id=user.id,
        ds_meta_data_id=meta.id,
        csv_filename=csv_filename,
        total_movies=total_movies,
        min_year=1972,
        max_year=2010,
        primary_genre="Crime",
        avg_rating=8.8,
        file_size=file_size,
        checksum="abc123",
        created_at=created_at or datetime.now(timezone.utc),
    )


def test_polymorphic_identity_distinguishes_film_and_uvl_datasets(test_app, clean_database):
    with test_app.app_context():
        owner = _make_user("poly@example.com")
        film = _make_film_dataset(owner, title="Film DS", doi="10.1234/film")

        uvl_meta = DSMetaDataRepository().create(
            title="UVL DS",
            description="UVL description",
            publication_type=PublicationType.DATA_MANAGEMENT_PLAN,
            dataset_doi="10.1234/uvl",
        )
        uvl = DataSetRepository().create(user_id=owner.id, ds_meta_data_id=uvl_meta.id)

        loaded_film = DataSetRepository().get_by_id(film.id)
        assert isinstance(loaded_film, FilmDataset)
        assert loaded_film.dataset_type == "film"
        assert uvl.dataset_type == "uvl"

        film_only = FilmdatasetRepository().get_synchronized(owner.id)
        assert [d.id for d in film_only] == [film.id]


def test_synchronized_and_unsynchronized_queries_respect_owner_and_doi(test_app, clean_database):
    with test_app.app_context():
        owner = _make_user("owner@example.com")
        other = _make_user("other@example.com")
        synced = _make_film_dataset(owner, title="Synced", doi="10.1234/synced")
        local = _make_film_dataset(owner, title="Local")
        _make_film_dataset(other, title="Other", doi="10.1234/other")

        repo = FilmdatasetRepository()
        assert [d.id for d in repo.get_synchronized(owner.id)] == [synced.id]
        assert [d.id for d in repo.get_unsynchronized(owner.id)] == [local.id]
        assert repo.get_unsynchronized_dataset(owner.id, local.id).id == local.id
        assert repo.get_unsynchronized_dataset(owner.id, synced.id) is None
        assert repo.get_unsynchronized_dataset(other.id, local.id) is None


def test_count_and_latest_synchronized_order_newest_first(test_app, clean_database):
    with test_app.app_context():
        owner = _make_user("latest@example.com")
        base = datetime(2025, 1, 1, tzinfo=timezone.utc)
        ds1 = _make_film_dataset(owner, title="DS1", doi="10.1234/1", created_at=base)
        ds2 = _make_film_dataset(owner, title="DS2", doi="10.1234/2", created_at=base + timedelta(days=1))
        ds3 = _make_film_dataset(owner, title="DS3", doi="10.1234/3", created_at=base + timedelta(days=2))
        _make_film_dataset(owner, title="Unsynced")

        repo = FilmdatasetRepository()
        assert repo.count_synchronized_datasets() == 3
        assert [d.id for d in repo.latest_synchronized(limit=2)] == [ds3.id, ds2.id]
        assert ds1.id not in [d.id for d in repo.latest_synchronized(limit=2)]


def test_film_dataset_model_methods_and_to_dict(test_app, clean_database):
    with test_app.app_context():
        owner = _make_user("model@example.com")
        film = _make_film_dataset(owner, title="Model Film", doi="10.1234/model", file_size=2048)

        assert film.files() == []
        assert film.get_files_count() == 1
        assert film.get_file_total_size() == 2048
        assert repr(film) == f"FilmDataset<{film.id}>"

        with test_app.test_request_context("/"):
            data = film.to_dict()
        assert data["dataset_type"] == "film"
        assert data["csv_filename"] == "movies.csv"
        assert data["total_movies"] == 5
        assert data["min_year"] == 1972
        assert data["max_year"] == 2010
        assert data["primary_genre"] == "Crime"
        assert data["avg_rating"] == 8.8
        assert data["checksum"] == "abc123"
        assert data["preview_url"] == f"/filmdataset/{film.id}/preview"
