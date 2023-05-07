from typing import List, Type

from sqlalchemy.orm import Session

from app import models
from app.models import UserInfo


def get_all_users(db: Session) -> List[Type[UserInfo]]:
    return db.query(models.UserInfo).all()
