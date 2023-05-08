import random
from datetime import timedelta
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status, Form
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from app import auth, crud
from app.auth import create_access_token
from app.database import get_db

router = APIRouter()


def send_2fa_code(username: str) -> JSONResponse:
    otp = str(random.randint(000000, 999999))
    print(f"OTP for user {username}: {otp}")
    return JSONResponse(content={"message": f"OTP sent to {username}.", "otp": otp})


@router.post("/login")
async def login(
    db: Session = Depends(get_db),
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
        crud.create_otp_info(secret=otp, db=db, user=user)
        return {"detail": f"Please provide the following OTP: {otp}"}

    access_token_expires = timedelta(minutes=auth.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token_data = {"sub": user.username}
    access_token = create_access_token(access_token_data, access_token_expires)

    return {"access_token": access_token, "token_type": "bearer"}
