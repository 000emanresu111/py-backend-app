from fastapi.testclient import TestClient
from unittest.mock import MagicMock
from app.database import get_db
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.routers.login import authenticate_user
from app import crud, schema, auth
from unittest import mock

from main import app

client = TestClient(app)


class TestUserLogin:
    def test_post_request_without_body_returns_422(self):
        """body should have username and password"""
        response = client.post("/users/auth")
        assert response.status_code == 422

    def test_post_request_with_improper_body_returns_422(self):
        """both username and password are required"""
        response = client.post(
            "/users/auth",
            json={"username": "test"}
        )
        assert response.status_code == 422

    def test_authenticate_user(self):
        pass

    @mock.patch("app.auth.check_username_password")
    def test_successful_authentication(self, mock_check_username_password):
        mock_check_username_password.return_value = True
        response = client.post("/users/auth", json={"username": "test", "password": "test"})
        assert response.status_code == 200
        assert "access_token" in response.json()
        assert response.json()["token_type"] == "Bearer"
