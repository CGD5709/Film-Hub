from splent_framework.seeders.BaseSeeder import BaseSeeder


class FakenodoSeeder(BaseSeeder):
    priority = 99

    def run(self):
        # Nothing to seed — fakenodo uses in-memory storage.
        pass
