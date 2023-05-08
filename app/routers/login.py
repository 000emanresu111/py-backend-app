from typing import List

from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
import datetime
from app import crud
from app import schema
from app.database import get_db
from app import auth

router = APIRouter()

ACCESS_TOKEN_EXPIRE_MINUTES = 15


@router.post("/users/auth", response_model=schema.TokenData, tags=["users"])
async def authenticate_user(user: schema.UserAuthenticate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user is None or not auth.check_username_password(db, user):
        raise HTTPException(status_code=403, detail="Username or password is incorrect")

    # access_token_expires = datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    # access_token = auth.encode_jwt_token(data={"sub": user.username}, expires_delta=access_token_expires)
    # return {"access_token": access_token, "token_type": "Bearer"}
