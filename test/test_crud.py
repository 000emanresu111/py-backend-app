from unittest.mock import MagicMock, patch
import unittest
from fastapi.testclient import TestClient
from app import schema

from main import app

client = TestClient(app)


class TestCrud(unittest.TestCase):
    def test_get_all_users(self):
        expected_output = [
            {
                "username": "user1",
                "email": "user1@example.com",
                "password": "password1",
                "is_2fa_enabled": True,
            },
            {
                "username": "user2",
                "email": "user2@example.com",
                "password": "password2",
                "is_2fa_enabled": False,
            },
            {
                "username": "user3",
                "email": "user3@example.com",
                "password": "password3",
                "is_2fa_enabled": True,
            },
        ]

        db = MagicMock()
        db.query().all.return_value = expected_output

        with patch("app.crud.get_all_users", return_value=db.query().all()):
            response = client.get("/users")

            assert response.status_code == 200
            assert response.json() == expected_output

    def test_get_user_by_username(self):
        pass

    def get_user_by_email(self):
        pass

    def get_user_by_id(self):
        pass

    def test_create_user(self):
        email = "test@example2.com"
        password = "password1"
        username = "Test User"
        is_2fa_enabled = True

        user = schema.User(
            email=email,
            password=password,
            username=username,
            is_2fa_enabled=is_2fa_enabled,
        )

        db = MagicMock()
        db.query.return_value.filter.return_value.first.return_value = None
        db.add.return_value = None
        db.commit.return_value = None
        db.refresh.return_value = None

        with patch("app.crud.create_user", return_value=user):
            response = client.post(
                "/users",
                json={
                    "username": username,
                    "email": email,
                    "password": password,
                    "is_2fa_enabled": is_2fa_enabled,
                },
            )

            assert response.status_code == 201
            assert response.json() == user.dict()

    def delete_all_users(self):
        pass
