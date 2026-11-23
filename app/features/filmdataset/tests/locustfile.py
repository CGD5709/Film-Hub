from locust import HttpUser, TaskSet, between, task
from splent_framework.environment.host import get_host_for_locust_testing


class FilmdatasetBehavior(TaskSet):
    @task
    def index(self):
        response = self.client.get("/filmdataset")
        if response.status_code != 200:
            print(f"Filmdataset index failed: {response.status_code}")


class FilmdatasetUser(HttpUser):
    tasks = [FilmdatasetBehavior]
    wait_time = between(5, 9)
    host = get_host_for_locust_testing()
