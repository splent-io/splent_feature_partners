from locust import HttpUser, TaskSet, task
from splent_framework.environment.host import get_host_for_locust_testing


class SplentFeaturePartnersBehavior(TaskSet):
    def on_start(self):
        self.index()

    @task
    def index(self):
        response = self.client.get("/splent_feature_partners")

        if response.status_code != 200:
            print(f"SplentFeaturePartners index failed: {response.status_code}")


class SplentFeaturePartnersUser(HttpUser):
    tasks = [SplentFeaturePartnersBehavior]
    min_wait = 5000
    max_wait = 9000
    host = get_host_for_locust_testing()
