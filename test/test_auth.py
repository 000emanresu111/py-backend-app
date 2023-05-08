import unittest
from datetime import timedelta
from unittest.mock import MagicMock, AsyncMock
from unittest.mock import patch

import bcrypt
import jwt
from sqlalchemy.orm import Session

from app import auth
from app import crud, models, schema
from app.auth import authenticate_user
from app.auth import check_username_password, encode_jwt_token
from app.auth import pwd_context
from app.auth import verify_password
from app.schema import User


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

    def test_create_access_token(self):
        data = {"sub": "test@test.com"}
        expires_delta = 30

        token = auth.create_access_token(data, timedelta(expires_delta))
        print(token)

        decoded = jwt.decode(token, auth.SECRET_KEY, algorithms=[auth.JWT_ALGORITHM])
        assert decoded["sub"] == "test@test.com"

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

    async def test_get_current_user(self):
        db = AsyncMock()
        user = schema.User(id=1, username="test-user", email="test@test.com")
        crud.get_user_by_username = AsyncMock(return_value=user)
        token_data = schema.TokenData(username="test-user")
        token = "valid-token"
        payload = {"sub": "test-user"}

        with patch("jwt.decode", return_value=payload) as mock_jwt_decode:
            result = await auth.get_current_user(db=db, token=token)

            assert result != user

            mock_jwt_decode.assert_called_once_with(
                token, auth.SECRET_KEY, algorithms=[auth.JWT_ALGORITHM]
            )
            crud.get_user_by_username.assert_called_once_with(
                db, username=token_data.username
            )
