from unittest.mock import MagicMock, patch
from sqlalchemy.orm import Session
from app import crud, models, schema
from app.auth import check_username_password, encode_jwt_token
import bcrypt
import unittest
import jwt
from datetime import timedelta
from app import auth
from unittest.mock import MagicMock
from sqlalchemy.orm import Session
from app.schema import User
from app.crud import get_user_by_username
from app.auth import verify_password
from app.auth import authenticate_user
from app.auth import pwd_context


class TestUserAuth(unittest.TestCase):
    def test_verify_password(self):
        hashed_password = pwd_context.hash("password")
        assert verify_password("password", hashed_password) is True

        hashed_password = pwd_context.hash("password")
        assert verify_password("wrong-password", hashed_password) is False

    def test_get_password_hash(self):
        password_hash = auth.get_password_hash("password")
        assert pwd_context.verify("password", password_hash) is True
        assert pwd_context.verify("wrong-password", password_hash) is False

    async def test_mock_check_username_password(self):
        username = "test-user"
        password = "test-password"

        user = models.UserInfo(
            username=username,
            password=bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()),
        )

        db = MagicMock(spec=Session)

        crud.get_user_by_username = MagicMock(return_value=user)

        with patch("app.crud.get_user_by_username", return_value=user):
            assert await check_username_password(
                db, schema.UserAuthenticate(username=username, password=password)
            )
            assert not await check_username_password(
                db,
                schema.UserAuthenticate(username=username, password="wrong-password"),
            )

    def test_encode_jwt_token(self):
        data = {"user_id": 1234, "email": "test@test.com"}
        expires_delta = timedelta(minutes=30)

        token = encode_jwt_token(data, expires_delta)

        self.assertNotEqual(token, "")
        self.assertIsInstance(token, str)

        decoded_token = jwt.decode(
            token, auth.SECRET_KEY, algorithms=[auth.JWT_ALGORITHM]
        )

        self.assertEqual(decoded_token["user_id"], data["user_id"])
        self.assertEqual(decoded_token["email"], data["email"])

        self.assertIn("exp", decoded_token)

    async def test_authenticate_user(self):
        db = MagicMock(spec=Session)
        test_user = User(id=1, username="test-user", password="test-password")
        auth.get_user_by_username = MagicMock(return_value=test_user)
        auth.verify_password = MagicMock(return_value=True)

        authenticated_user = await authenticate_user(db, "test-user", "test-password")
        assert authenticated_user == test_user

        authenticated_user = await authenticate_user(
            db, "test-user", "invalid-password"
        )
        assert authenticated_user is None

        auth.verify_password.assert_called_once_with("test-password", "test-password")
