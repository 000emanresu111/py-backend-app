
import bcrypt

import jwt
from sqlalchemy.orm import Session
import datetime


from typing import Dict, Optional

from app import models, schema, crud


SECRET_KEY = "5b6e92308fa8806e55d8848cd88882a31e44cd5c65fa7fc9f8a8550616898b04"
JWT_ALGORITHM = "HS256"
JWT_DEFAULT_EXPIRATION = 15


def check_username_password(db: Session, user: schema.UserAuthenticate) -> bool:
    db_user_info: models.UserInfo = crud.get_user_by_username(db, username=user.username)

    if not db_user_info:
        return False

    db_password: bytes = db_user_info.password
    request_password: bytes = user.password.encode('utf-8')

    return bcrypt.checkpw(request_password, db_password)


def encode_jwt_token(data: Dict, expires_delta: Optional[datetime.timedelta] = None) -> str:
    payload = data.copy()

    if expires_delta is None:
        expires_delta = JWT_DEFAULT_EXPIRATION
    expires_at = datetime.datetime.utcnow() + expires_delta
    payload["exp"] = expires_at

    encoded_jwt = jwt.encode(payload, SECRET_KEY, algorithm=JWT_ALGORITHM)
    return encoded_jwt
