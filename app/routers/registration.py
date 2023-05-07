from typing import List

from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from app import crud
from app import schema
from app.database import get_db

router = APIRouter()


@router.get("/users", response_model=List[schema.User])
async def get_all_users(db: Session = Depends(get_db)):
    return crud.get_all_users(db)
