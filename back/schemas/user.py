from typing import Optional

from pydantic import BaseModel


class UserBase(BaseModel):
    username: str
    email: Optional[str]


class UserCreate(UserBase):
    password: str


class UserGet(UserBase):
    is_staff: bool
    is_active: bool
    is_superuser: bool

    class Config:
        orm_mode = True
