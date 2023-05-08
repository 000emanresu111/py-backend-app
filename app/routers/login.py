from typing import List, Optional

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
from fastapi.responses import JSONResponse

router = APIRouter()

ACCESS_TOKEN_EXPIRE_MINUTES = 15


def send_2fa_code(username: str) -> JSONResponse:
    otp = str(random.randint(000000, 999999))
    print(f"OTP for user {username}: {otp}")
    return JSONResponse(content={"message": f"OTP sent to {username}.", "otp": otp})


@router.post("/login")
async def login(
    db: AsyncSession = Depends(get_db),
    username: str = Form(...),
    password: str = Form(...),
    send_otp: Optional[bool] = Form(False),
):
    user = await auth.authenticate_user(db, username, password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if user.is_2fa_enabled and send_otp:
        otp = str(random.randint(100000, 999999))
        return {"detail": f"Please provide the following OTP: {otp}"}

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token_data = {"sub": user.username}
    access_token = create_access_token(access_token_data, access_token_expires)

    return {"access_token": access_token, "token_type": "bearer"}
