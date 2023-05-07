from typing import List
from pydantic import BaseModel, Field, EmailStr, validator
from typing import Optional


class User(BaseModel):
    email: EmailStr
    password: str
    username: str
    is_2fa_enabled: Optional[bool]

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
