from splent_framework.repositories.BaseRepository import BaseRepository

from app.features.fakenodo.models import Fakenodo


class FakenodoRepository(BaseRepository):
    def __init__(self):
        super().__init__(Fakenodo)
