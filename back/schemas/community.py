from typing import Optional

from pydantic import BaseModel, AnyUrl, EmailStr, validator


class Community(BaseModel):
    """
    Модель сообщества городского, которое модерирует данные по городу
    И Новости на фронт берем
    """
    name: str
    description: Optional[str]
    phone: Optional[str]
    email: Optional[str]
    address: Optional[str]
    website: Optional[AnyUrl]
    social: Optional[AnyUrl]
    social2: Optional[AnyUrl]
    social3: Optional[AnyUrl]
    news_feed: Optional[AnyUrl]

    city_id: Optional[int]
    owner_id: Optional[int]
    logo: Optional[str]

    @validator("phone", pre=True)
    def phone_validation(cls, v):
        return str(v)

    @validator("logo", pre=True)
    def logo_validation(cls, v):
        return str(v)

    class Config:
        orm_mode = True
        # use_enum_values = True
