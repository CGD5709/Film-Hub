from app.features.filmdataset.repositories import FilmdatasetRepository
from splent_framework.services.BaseService import BaseService


class FilmdatasetService(BaseService):
    def __init__(self):
        super().__init__(FilmdatasetRepository())
