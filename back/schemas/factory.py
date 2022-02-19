from typing import Optional, List

from pydantic import BaseModel, AnyUrl, EmailStr, validator


class FactoryBase(BaseModel):
    name: str
    description: Optional[str]
    phone: Optional[str]
    email: Optional[str]
    address: Optional[str]
    website: Optional[AnyUrl]

    city_id: int
    point: Optional[str]
    latitude: Optional[float]
    longitude: Optional[float]

    factory_type: Optional[str]
    danger_score: Optional[float]

    photo: Optional[str]
    icon: Optional[str]

    @validator("phone", pre=True)
    def phone_validation(cls, v):
        return str(v)

    @validator("photo", pre=True)
    def photo_validation(cls, v):
        return str(v)

    @validator("icon", pre=True)
    def icon_validation(cls, v):
        return str(v)


class FactoryGet(FactoryBase):
    id: int

    class Config:
        orm_mode = True


class ListFactories(BaseModel):
    __root__: List[FactoryGet]


