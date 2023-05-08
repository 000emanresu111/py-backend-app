from typing import List

from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
import datetime
from app import crud
from app import schema
from app.database import get_db
from app import auth
from fastapi import APIRouter, Depends, HTTPException, status, Form
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from sqlalchemy.ext.asyncio import AsyncSession
import random
from app import crud, models, schema
from app.database import get_db
from app.auth import create_access_token, verify_password

router = APIRouter()

ACCESS_TOKEN_EXPIRE_MINUTES = 15


@router.post("/users/auth", response_model=schema.TokenData, tags=["users"])
async def authenticate_user(
    user: schema.UserAuthenticate, db: Session = Depends(get_db)
):
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user is None or not auth.check_username_password(db, user):
        raise HTTPException(status_code=403, detail="Username or password is incorrect")

    # access_token_expires = datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    # access_token = auth.encode_jwt_token(data={"sub": user.username}, expires_delta=access_token_expires)
    # return {"access_token": access_token, "token_type": "Bearer"}


@router.post("/login")
async def login(
    db: AsyncSession = Depends(get_db),
    username: str = Form(...),
    password: str = Form(...),
    otp_code: str = Form(None),
):
    user = await crud.get_user_by_username(db, username)
    if user is None or not verify_password(password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if user.is_2fa_enabled and otp_code is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="2FA required",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if user.is_2fa_enabled and otp_code is not None:
        otp = str(random.randint(000000, 999999))
        print(f"OTP for user {user.username}: {otp}")
        if otp_code != otp:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid OTP code",
                headers={"WWW-Authenticate": "Bearer"},
            )

    access_token_expires = timedelta(minutes=auth.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}
