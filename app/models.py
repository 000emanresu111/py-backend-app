from sqlalchemy import Column, Integer, String, Boolean

from app.database import Base


class UserInfo(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    email = Column(String)
    password = Column(String)
    is_2fa_enabled = Column(Boolean, default=False)


class UsersOTP(Base):
    __tablename__ = "users_otp"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    otp = Column(String)