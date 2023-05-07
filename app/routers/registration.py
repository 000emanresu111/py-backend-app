from typing import List

from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session

from app import crud
from app import schema
from app.database import get_db

router = APIRouter()


@router.get("/users", response_model=List[schema.User])
async def get_all_users(db: Session = Depends(get_db)):
    return crud.get_all_users(db)


@router.post("/users", status_code=201, response_model=schema.User)
async def register_user(user: schema.User, db: Session = Depends(get_db)):
    if crud.get_user_by_email(db, email=user.email):
        raise HTTPException(status_code=400, detail="Email already registered")

    if crud.get_user_by_username(db, username=user.username):
        raise HTTPException(status_code=400, detail="Username already exists")

    try:
        db_user = crud.create_user(db=db, user=user)
    except Exception as e:
        print(f"Failed to create user: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
    return db_user


@router.delete("/users")
async def delete_all_users(db: Session = Depends(get_db)):
    try:
        crud.delete_all_users(db)
    except Exception as e:
        print(f"Failed to read users: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

    return {"message": "All users deleted"}