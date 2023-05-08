from unittest import mock

from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


class TestUserLogin:
    def test_post_request_without_body_returns_422(self):
        """body should have username and password"""
        response = client.post("/users")
        assert response.status_code == 422

    def test_post_request_with_improper_body_returns_422(self):
        """both username and password are required"""
        response = client.post("/users", json={"username": "test"})
        assert response.status_code == 422

    def test_authenticate_user(self):
        pass

