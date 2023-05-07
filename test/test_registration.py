from unittest.mock import MagicMock, patch

from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


class TestUserRegistration:
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
