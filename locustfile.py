from locust import HttpUser, task, constant
import random
import string

class UserBehavior(HttpUser):
    # Simulate realistic user think time: 100–300ms
    wait_time = constant(6)

    def random_string(self, length=6):
        return "".join(random.choices(string.ascii_lowercase, k=length))

    @task(4)
    def get_root(self):
        self.client.get("/")

    @task(2)
    def get_health(self):
        self.client.get("/health")

    @task(3)
    def get_users(self):
        self.client.get("/users")

    @task(1)
    def post_user(self):
        payload = {
            "name": f"user_{self.random_string()}",
            "email": f"{self.random_string()}@example.com"
        }
        self.client.post("/users", json=payload)