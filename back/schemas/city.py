from typing import Optional

from pydantic import BaseModel, AnyUrl, EmailStr


class CityBase(BaseModel):
    display_name: str
    latitude: Optional[float]
    longitude: Optional[float]
    # region: Optional[str]
    # country: Optional[str]


class CityGet(CityBase):
    id: int

    class Config:
        orm_mode = True
