from typing import Optional

from pydantic import BaseModel


class TokenBase(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
    ttl: int


class TokenGet(TokenBase):

    class Config:
        orm_mode = True
