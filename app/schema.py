from typing import Optional

from pydantic import BaseModel, EmailStr


class User(BaseModel):
    email: Optional[EmailStr]
    password: str
    username: str
    is_2fa_enabled: Optional[bool]

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class User2FA(BaseModel):
    username: str
    otp: str

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class UserAuthenticate(BaseModel):
    username: str
    password: str


class TokenData(BaseModel):
    username: str
    access_token: str
    token_type: str
