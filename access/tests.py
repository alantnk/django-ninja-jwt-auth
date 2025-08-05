from django.test import TestCase
from ninja.testing import TestClient
from .api import router
from django.contrib.auth import get_user_model

User = get_user_model()


class TokenTest(TestCase):
    def setUp(self):
        self.client = TestClient(router)
        self.user = {
            "username": "test_ok",
            "email": "test_ok@mail.com",
            "password": "testpass",
        }
        User.objects.create_user(**self.user)
        return super().setUp()

    def test_retrieve_token_ok(self):
        response = self.client.post(
            "/token",
            json=self.user,
        )

        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone("access_token", response.json())
        self.assertIsNotNone("refresh_token", response.json())

    def test_retrieve_token_invalid_credentials(self):
        response = self.client.post(
            "/token",
            json={"email": "fake@mail.com", "password": "fakepass"},
        )

        self.assertEqual(response.status_code, 401)
        self.assertIn("Invalid credentials", response.json()["detail"])

    def test_retrieve_token_invalid_data(self):
        response = self.client.post(
            "/token",
            json={"email": "fake2@mail.com"},
        )
        self.assertEqual(response.status_code, 422)
        self.assertIn("detail", response.json())


class RefreshTokenTest(TestCase):
    def setUp(self):
        self.client = TestClient(router)
        self.user = {
            "username": "test_ok",
            "email": "test_ok@mail.com",
            "password": "testpass",
        }
        User.objects.create_user(**self.user)
        return super().setUp()

    def test_refresh_token_ok(self):
        access_resp = self.client.post("/token", json=self.user)
        token = access_resp.json().get("refresh_token")
        response = self.client.post(
            "/refresh-token",
            json={"token": token},
        )
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone("refresh_token", response.json())

    def test_refresh_token_invalid(self):
        response = self.client.post(
            "/refresh-token",
            json={"token": "xxxxx"},
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("message", response.json())
