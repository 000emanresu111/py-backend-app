from typing import List, Type, Optional
import bcrypt
from sqlalchemy.orm import Session
from fastapi import HTTPException

from app import models, schema
from app.models import UserInfo


def get_all_users(db: Session) -> List[Type[UserInfo]]:
    return db.query(models.UserInfo).all()


def get_user_by_username(db: Session, username: str):
    return db.query(models.UserInfo).filter(models.UserInfo.username == username).first()


def get_user_by_email(db: Session, email: str) -> Optional[schema.User]:
    return db.query(models.UserInfo).filter(models.UserInfo.email == email).first()


def get_user_by_id(db: Session, user_id: int) -> Optional[schema.User]:
    return db.query(models.UserInfo).filter(models.UserInfo.id == user_id).first()


def create_user(db: Session, user: schema.User) -> schema.User:
    if get_user_by_email(db, user.email):
        raise HTTPException(status_code=400, detail="Email already registered")

    if get_user_by_username(db, user.username):
        raise HTTPException(status_code=400, detail="Username already registered")

    hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())

    db_user = models.UserInfo(username=user.username, password=hashed_password, email=user.email, is_2fa_enabled=user.is_2fa_enabled)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


def delete_all_users(db: Session):
    db.query(models.UserInfo).delete()
    db.commit()
