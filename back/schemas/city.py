from typing import Optional

from pydantic import BaseModel, AnyUrl, EmailStr


class City(BaseModel):

    id: int
    display_name: str
    latitude: Optional[float]
    longitude: Optional[float]
    # region: Optional[str]
    # country: Optional[str]

    class Config:
        orm_mode = True

