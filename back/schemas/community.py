from typing import Optional

from pydantic import BaseModel, AnyUrl, EmailStr


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
    city: Optional[str]
    owner: Optional[str]
    logo: Optional[str]
