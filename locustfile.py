from locust import HttpUser, task, between
import random
import uuid
from datetime import datetime


class FraudUser(HttpUser):
    host = "http://web:8000"
    wait_time = between(1, 3)  # simulate real user delay

    def generate_payload(self):
        locations = ["mumbai", "delhi", "chennai", "bangalore"]
        devices = ["android", "iphone", "web"]

        return {
            "user": 1,
            "amount": random.randint(100, 100000),
            "location": random.choice(locations),
            "device": random.choice(devices),
            "timestamp": datetime.utcnow().isoformat(),
            "external_id": str(uuid.uuid4())  # unique every time
        }

    @task
    def create_transaction(self):
        payload = self.generate_payload()

        self.client.post(
            "/api/v1/transactions/",
            json=payload,
            headers={"Content-Type": "application/json"},
        )