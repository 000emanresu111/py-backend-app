import logging as logger
from datetime import datetime, timedelta
from typing import Dict, Optional, Union
from sqlalchemy.orm import Session

import bcrypt
import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.context import CryptContext
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession

from app import database
from app import models, schema, crud

SECRET_KEY = "5b6e92308fa8806e55d8848cd88882a31e44cd5c65fa7fc9f8a8550616898b04"
JWT_ALGORITHM = "HS256"
JWT_ACCESS_TOKEN_EXPIRE_MINUTES = 15

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


async def check_username_password(
    db: AsyncSession, user: schema.UserAuthenticate
) -> bool:
    db_user_info: Optional[models.UserInfo] = await crud.get_user_by_username(
        db, username=user.username
    )

    db_password: bytes = db_user_info.password.encode("utf-8")
    request_password: bytes = user.password.encode("utf-8")

    if not db_user_info or not bcrypt.checkpw(request_password, db_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )

    return True


def encode_jwt_token(data: Dict, expires_delta: Optional[timedelta] = None) -> str:
    payload = data.copy()

    if expires_delta is None:
        expires_delta = JWT_ACCESS_TOKEN_EXPIRE_MINUTES
    expires_at = datetime.utcnow() + expires_delta
    payload["exp"] = expires_at

    encoded_jwt = jwt.encode(payload, SECRET_KEY, algorithm=JWT_ALGORITHM)
    return encoded_jwt


async def authenticate_user(
    db: AsyncSession, username: str, password: str
) -> Optional[schema.User]:
    try:
        user = crud.get_user_by_username(db, username)
        if not user or not verify_password(password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return schema.User(
            username=user.username,
            password=user.password,
            email=user.email,
            is_2fa_enabled=user.is_2fa_enabled,
        )
    except ValidationError as e:
        logger.error(f"Validation error in authenticate_user: {e}")
        return None
    except Exception as e:
        logger.exception(f"Exception error in authenticate_user: {e}")
        raise e


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=JWT_ALGORITHM)
    return encoded_jwt


async def get_current_user(
    db: AsyncSession = Depends(database.get_db), token: str = Depends(oauth2_scheme)
) -> schema.User:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[JWT_ALGORITHM])
        username: str = payload.get("sub")

        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        token_data = schema.TokenData(username=username)
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = await crud.get_user_by_username(db, username=token_data.username)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return user
