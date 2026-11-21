from splent_framework.repositories.BaseRepository import BaseRepository

from app.features.filmdataset.models import FilmDataset


class FilmdatasetRepository(BaseRepository):
    def __init__(self):
        super().__init__(FilmDataset)

