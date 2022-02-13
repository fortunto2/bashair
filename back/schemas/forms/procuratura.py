from datetime import datetime
from typing import Optional

from pydantic import BaseModel, AnyUrl, EmailStr, validator, Field


class ProcuraturaData(BaseModel):
    """
    Поля нужные для создания формы в природоохранную прокуратуру.
    """
    last_name: str
    first_name: str
    patronymic: str
    email: str
    phone: str
    text: Optional[str]
    timezone: int = 5

    date: datetime = Field(default_factory=datetime.utcnow)
    city: str
    address: str
    edds: Optional[int]

    @property
    def get_date(self):
         self.date = self.date.strftime("%Y-%m-%d %H:%M")



