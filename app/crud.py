from sqlalchemy.orm import Session
from app import models, schema

from typing import List, Type

from app.models import UserInfo


def get_all_users(db: Session) -> List[Type[UserInfo]]:
    return db.query(models.UserInfo).all()
