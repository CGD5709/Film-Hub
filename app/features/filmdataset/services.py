import csv
import logging
import os
import shutil
from collections import Counter

from splent_framework.services.BaseService import BaseService

from app.features.dataset.repositories import (
    AuthorRepository,
    DSDownloadRecordRepository,
    DSMetaDataRepository,
)
from app.features.dataset.services import calculate_checksum_and_size
from app.features.filmdataset.models import FilmDataset
from app.features.filmdataset.repositories import FilmdatasetRepository
from app.features.filmdataset.validator import RATING_COLUMNS, FilmCSVValidator

logger = logging.getLogger(__name__)


class FilmMetricsService:
    """Computes domain-specific movie metrics from validated CSV rows."""

    @staticmethod
    def compute(rows: list[dict[str, str]]) -> dict:
        if not rows:
            return {
                "total_movies": 0,
                "min_year": None,
                "max_year": None,
                "primary_genre": None,
                "avg_rating": None,
            }

        years = [int(row["year"]) for row in rows]
        genre_counts: Counter[str] = Counter()
        ratings: list[float] = []

        for row in rows:
            raw_genres = row.get("genre", "")
            for part in raw_genres.replace("|", ",").split(","):
                cleaned = part.strip()
                if cleaned:
                    genre_counts[cleaned] += 1

            for col in RATING_COLUMNS:
                raw_rating = row.get(col, "")
                if raw_rating:
                    ratings.append(float(raw_rating))
                    break

        primary_genre = genre_counts.most_common(1)[0][0] if genre_counts else None
        avg_rating = round(sum(ratings) / len(ratings), 2) if ratings else None

        return {
            "total_movies": len(rows),
            "min_year": min(years),
            "max_year": max(years),
            "primary_genre": primary_genre,
            "avg_rating": avg_rating,
        }


class FilmdatasetService(BaseService):
    def __init__(self):
        super().__init__(FilmdatasetRepository())
        self.author_repository = AuthorRepository()
        self.dsmetadata_repository = DSMetaDataRepository()
        self.dsdownloadrecord_repository = DSDownloadRecordRepository()
        self.validator = FilmCSVValidator()

    def get_synchronized(self, current_user_id: int):
        return self.repository.get_synchronized(current_user_id)

    def get_unsynchronized(self, current_user_id: int):
        return self.repository.get_unsynchronized(current_user_id)

    def get_unsynchronized_dataset(self, current_user_id: int, dataset_id: int):
        return self.repository.get_unsynchronized_dataset(current_user_id, dataset_id)

    def update_dsmetadata(self, id, **kwargs):
        return self.dsmetadata_repository.update(id, **kwargs)

    def save_temp_csv(self, file, current_user) -> dict:
        if not file or not file.filename or not file.filename.lower().endswith(".csv"):
            return {"status": "error", "code": 400, "message": "No valid CSV file"}

        temp_folder = current_user.temp_folder()
        os.makedirs(temp_folder, exist_ok=True)

        filename = os.path.basename(file.filename)
        target = os.path.join(temp_folder, filename)
        if os.path.exists(target):
            base, ext = os.path.splitext(filename)
            i = 1
            while os.path.exists(os.path.join(temp_folder, f"{base} ({i}){ext}")):
                i += 1
            filename = f"{base} ({i}){ext}"
            target = os.path.join(temp_folder, filename)

        try:
            file.save(target)
        except Exception as exc:
            return {"status": "error", "code": 500, "message": str(exc)}

        validation = self.validator.validate_file(target)
        if not validation.is_valid:
            if os.path.exists(target):
                os.remove(target)
            return {
                "status": "error",
                "code": 400,
                "message": validation.errors[0],
                "errors": validation.errors,
            }

        metrics = FilmMetricsService.compute(validation.rows)
        return {
            "status": "ok",
            "code": 200,
            "message": "CSV uploaded and validated successfully",
            "filename": filename,
            "metrics": metrics,
        }

    def delete_temp_csv(self, filename: str, current_user) -> dict:
        if not filename:
            return {"status": "error", "code": 400, "error": "Error: filename missing"}
        safe_name = os.path.basename(filename)
        target = os.path.join(current_user.temp_folder(), safe_name)
        if not os.path.exists(target):
            return {"status": "error", "code": 404, "error": "Error: File not found"}
        os.remove(target)
        return {"status": "ok", "code": 200, "message": "File deleted successfully"}

    def get_csv_path(self, dataset: FilmDataset) -> str:
        working_dir = os.getenv("WORKING_DIR", "")
        return os.path.join(
            working_dir,
            "uploads",
            f"user_{dataset.user_id}",
            f"dataset_{dataset.id}",
            dataset.csv_filename,
        )

    def move_csv_file(self, dataset: FilmDataset, current_user) -> str:
        source_path = os.path.join(current_user.temp_folder(), os.path.basename(dataset.csv_filename))
        dest_dir = os.path.dirname(self.get_csv_path(dataset))
        os.makedirs(dest_dir, exist_ok=True)
        dest_path = os.path.join(dest_dir, os.path.basename(dataset.csv_filename))
        shutil.move(source_path, dest_path)
        return dest_path

    def create_from_form(self, form, current_user) -> FilmDataset:
        csv_filename = os.path.basename(form.csv_filename.data)
        file_path = os.path.join(current_user.temp_folder(), csv_filename)
        validation = self.validator.validate_file(file_path)
        if not validation.is_valid:
            raise ValueError("; ".join(validation.errors))

        checksum, file_size = calculate_checksum_and_size(file_path)
        metrics = FilmMetricsService.compute(validation.rows)

        main_author = {
            "name": f"{current_user.profile.surname}, {current_user.profile.name}",
            "affiliation": current_user.profile.affiliation,
            "orcid": current_user.profile.orcid,
        }

        try:
            dsmetadata = self.dsmetadata_repository.create(commit=False, **form.get_dsmetadata())
            for author_data in [main_author] + form.get_authors():
                author = self.author_repository.create(commit=False, ds_meta_data_id=dsmetadata.id, **author_data)
                dsmetadata.authors.append(author)

            dataset = self.create(
                commit=False,
                user_id=current_user.id,
                ds_meta_data_id=dsmetadata.id,
                csv_filename=csv_filename,
                total_movies=metrics["total_movies"],
                min_year=metrics["min_year"],
                max_year=metrics["max_year"],
                primary_genre=metrics["primary_genre"],
                avg_rating=metrics["avg_rating"],
                file_size=file_size,
                checksum=checksum,
            )
            self.repository.session.commit()
        except Exception as exc:
            logger.exception("Exception creating film dataset from form: %s", exc)
            self.repository.session.rollback()
            raise exc

        return dataset

    def upload_dataset(self, form, current_user) -> dict:
        try:
            dataset = self.create_from_form(form=form, current_user=current_user)
            self.move_csv_file(dataset, current_user)
        except Exception as exc:
            logger.exception("Exception while creating film dataset locally: %s", exc)
            return {"status": "error", "code": 400, "message": str(exc)}

        from app.features.zenodo.services import ZenodoService

        zenodo = ZenodoService()
        zenodo_data = {}
        try:
            zenodo_data = zenodo.create_new_deposition(dataset) or {}
        except Exception as exc:
            logger.exception("Exception while creating deposition in Zenodo: %s", exc)

        if zenodo_data.get("conceptrecid"):
            deposition_id = zenodo_data.get("id")
            self.update_dsmetadata(dataset.ds_meta_data_id, deposition_id=deposition_id)
            try:
                zenodo.upload_dataset_file(dataset, deposition_id, dataset.csv_filename, user=current_user)
                zenodo.publish_deposition(deposition_id)
                deposition_doi = zenodo.get_doi(deposition_id)
                self.update_dsmetadata(dataset.ds_meta_data_id, dataset_doi=deposition_doi)
            except Exception as exc:
                msg = f"could not upload film dataset to Zenodo and update DOI: {exc}"
                return {"status": "partial", "code": 200, "message": msg, "dataset_id": dataset.id}

        temp_path = current_user.temp_folder()
        if os.path.isdir(temp_path):
            shutil.rmtree(temp_path)

        return {"status": "ok", "code": 200, "message": "Everything works!", "dataset_id": dataset.id}

    def get_preview_rows(self, dataset: FilmDataset, page: int = 1, per_page: int = 50) -> dict:
        page = max(1, page)
        per_page = max(1, min(per_page, 100))
        csv_path = self.get_csv_path(dataset)

        if not os.path.exists(csv_path):
            return {"headers": [], "rows": [], "page": page, "per_page": per_page, "total": 0}

        with open(csv_path, mode="r", encoding="utf-8-sig", newline="") as stream:
            reader = csv.DictReader(stream)
            headers = [h.strip().lower() for h in (reader.fieldnames or [])]
            all_rows = [
                {k.strip().lower(): (v.strip() if v is not None else "") for k, v in row.items()}
                for row in reader
            ]

        total = len(all_rows)
        start = (page - 1) * per_page
        end = start + per_page
        return {
            "headers": headers,
            "rows": all_rows[start:end],
            "page": page,
            "per_page": per_page,
            "total": total,
        }


FilmDataSetService = FilmdatasetService
