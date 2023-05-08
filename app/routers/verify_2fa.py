from fastapi import APIRouter, Depends, HTTPException, status, Form
from app.auth import create_access_token
from datetime import timedelta
from app import auth
from app import crud
from fastapi import APIRouter, Depends, HTTPException, status, Form
from datetime import timedelta
from sqlalchemy.ext.asyncio import AsyncSession
import random
from app import crud, models, schema
from app.database import get_db
from sqlalchemy.orm import Session
from fastapi import Header

router = APIRouter()


@router.post("/verify-2fa")
async def verify_2fa(
    db: Session = Depends(get_db),
    username: str = Form(...),
    otp_code: str = Form(...),
):
    user = crud.get_user_by_username(db, username)

    otp = crud.get_otp_by_username(db, username).__dict__.get("otp")

    if otp_code != otp:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or OTP",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=auth.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token_data = {"sub": user.username}
    access_token = create_access_token(access_token_data, access_token_expires)

    return {"access_token": access_token, "token_type": "bearer"}
