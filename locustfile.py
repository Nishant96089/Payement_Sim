from locust import HttpUser, task, between
import uuid


SECRET_KEY = "sk_696c369d5b3b1cb04c3f18398b672fe5946495907d98991dbc77285f993afee8"


class PaymentUser(HttpUser):

    wait_time = between(0.1, 0.5)

    @task
    def create_payment(self):

        idempotency_key = str(uuid.uuid4())

        self.client.post(
            "/api/payments/",
            headers={
                "Authorization": f"Bearer {SECRET_KEY}",
                "Idempotency-Key": idempotency_key,
                "Content-Type": "application/json"
            },
            json={
                "amount": 100,
                "currency": "INR"
            }
        )