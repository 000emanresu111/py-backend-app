from unittest.mock import MagicMock, patch
from sqlalchemy.orm import Session
from app import crud, models, schema
from app.auth import check_username_password, encode_jwt_token
import bcrypt
import unittest
import jwt
from datetime import timedelta
from app import auth


class TestUserAuth(unittest.TestCase):
    def test_check_username_password(self):
        username = "testuser"
        password = "testpassword"

        user = models.UserInfo(
            username=username,
            password=bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
        )

        db = MagicMock(spec=Session)

        crud.get_user_by_username = MagicMock(return_value=user)

        with patch("app.crud.get_user_by_username", return_value=user):
            assert check_username_password(db, schema.UserAuthenticate(username=username, password=password))
            assert not check_username_password(db, schema.UserAuthenticate(username=username, password="wrong_password"))

    def test_encode_jwt_token(self):
        data = {'user_id': 1234, 'email': 'example@example.com'}
        expires_delta = timedelta(minutes=30)

        token = encode_jwt_token(data, expires_delta)

        self.assertNotEqual(token, '')
        self.assertIsInstance(token, str)

        decoded_token = jwt.decode(token, auth.SECRET_KEY, algorithms=[auth.JWT_ALGORITHM])

        self.assertEqual(decoded_token['user_id'], data['user_id'])
        self.assertEqual(decoded_token['email'], data['email'])

        self.assertIn('exp', decoded_token)

