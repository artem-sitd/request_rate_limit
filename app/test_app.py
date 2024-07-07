import os
from unittest import TestCase
from dotenv import load_dotenv
from . import app
from .router import all_routes

app.register_blueprint(all_routes)


class RateLimitTestCase(TestCase):
    def setUp(self) -> None:
        load_dotenv()
        self.TEST_IP1 = os.getenv("TEST_IP1")
        self.TEST_IP2 = os.getenv("TEST_IP2")
        app.testing = True
        self.client = app.test_client()

    def test_rate_limit(self):
        for i in range(100):
            response = self.client.get("/", headers={"X-Forwarded-For": self.TEST_IP1})
            self.assertEqual(response.status_code, 200)

        for i in range(5):
            response = self.client.get('/', headers={"X-Forwarded-For": self.TEST_IP1})
            self.assertEqual(response.status_code, 429)

        for i in range(100):
            response = self.client.get("/", headers={"X-Forwarded-For": self.TEST_IP2})
            self.assertEqual(response.status_code, 200)

        for i in range(5):
            response = self.client.get('/', headers={"X-Forwarded-For": self.TEST_IP2})
            self.assertEqual(response.status_code, 429)

    def test_reset(self):
        response = self.client.post("/reset", headers={"X-Forwarded-For": self.TEST_IP2})
        self.assertEqual(response.status_code, 200)

        response = self.client.post("/reset", headers={"X-Forwarded-For": self.TEST_IP1})
        self.assertEqual(response.status_code, 200)
