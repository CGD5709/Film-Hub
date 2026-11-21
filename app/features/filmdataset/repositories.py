from splent_framework.repositories.BaseRepository import BaseRepository
from sqlalchemy import desc

from app.features.dataset.models import DSMetaData
from app.features.filmdataset.models import FilmDataset


class FilmdatasetRepository(BaseRepository):
    def __init__(self):
        super().__init__(FilmDataset)

    def get_synchronized(self, current_user_id: int):
        return (
            self.model.query.join(DSMetaData)
            .filter(FilmDataset.user_id == current_user_id, DSMetaData.dataset_doi.isnot(None))
            .order_by(self.model.created_at.desc())
            .all()
        )

    def get_unsynchronized(self, current_user_id: int):
        return (
            self.model.query.join(DSMetaData)
            .filter(FilmDataset.user_id == current_user_id, DSMetaData.dataset_doi.is_(None))
            .order_by(self.model.created_at.desc())
            .all()
        )

    def get_unsynchronized_dataset(self, current_user_id: int, dataset_id: int):
        return (
            self.model.query.join(DSMetaData)
            .filter(
                FilmDataset.user_id == current_user_id,
                FilmDataset.id == dataset_id,
                DSMetaData.dataset_doi.is_(None),
            )
            .first()
        )

    def count_synchronized_datasets(self) -> int:
        return self.model.query.join(DSMetaData).filter(DSMetaData.dataset_doi.isnot(None)).count()

    def latest_synchronized(self, limit: int = 5):
        return (
            self.model.query.join(DSMetaData)
            .filter(DSMetaData.dataset_doi.isnot(None))
            .order_by(desc(self.model.id))
            .limit(limit)
            .all()
        )


FilmDataSetRepository = FilmdatasetRepository
