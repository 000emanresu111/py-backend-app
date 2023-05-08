import logging as logger
from datetime import datetime, timedelta
from typing import Annotated
from typing import Dict
from typing import Optional

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose.jwt import decode, encode
from jwt import decode, InvalidTokenError
from jose import JWTError
from passlib.context import CryptContext
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from app import schema, crud

SECRET_KEY = "5b6e92308fa8806e55d8848cd88882a31e44cd5c65fa7fc9f8a8550616898b04"
JWT_ALGORITHM = "HS256"
JWT_ACCESS_TOKEN_EXPIRE_MINUTES = 15

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def encode_jwt_token(data: Dict, expires_delta: Optional[timedelta] = None) -> str:
    payload = data.copy()

    if expires_delta is None:
        expires_delta = JWT_ACCESS_TOKEN_EXPIRE_MINUTES
    expires_at = datetime.utcnow() + expires_delta
    payload["exp"] = expires_at

    encoded_jwt = encode(payload, SECRET_KEY, algorithm=JWT_ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str) -> dict:
    try:
        decoded_token = decode(token, SECRET_KEY, JWT_ALGORITHM)
        exp_timestamp = decoded_token["exp"]
        if datetime.utcnow() > datetime.fromtimestamp(exp_timestamp):
            raise InvalidTokenError("Token has expired")
        return decoded_token
    except InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")


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
    encoded_jwt = encode(to_encode, SECRET_KEY, algorithm=JWT_ALGORITHM)
    return encoded_jwt


def verify_otp_code(db: Session, username: str, otp_code: str):
    stored_otp = crud.get_otp_by_username(db, username)
    return otp_code == stored_otp


async def get_current_user(db: Session, token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode(token, SECRET_KEY, algorithms=[JWT_ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = schema.TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = crud.get_user_by_username(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user