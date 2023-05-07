from typing import Optional

from pydantic import BaseModel, EmailStr


class User(BaseModel):
    email: EmailStr
    password: str
    username: str
    is_2fa_enabled: Optional[bool]

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
