from typing import Optional

from pydantic import BaseModel, validator, AnyUrl


class InstanceBase(BaseModel):
    name: str
    description: str
    phone: str
    email: Optional[str]
    address: Optional[str]
    website: Optional[AnyUrl]
    report_url: Optional[AnyUrl]


class InstanceGet(InstanceBase):
    id: int
    city_id: int

    @validator("phone", pre=True)
    def phone_validation(cls, v):
        return str(v)

    @validator("email", pre=True)
    def email_validation(cls, v):
        return str(v)

    class Config:
        orm_mode = True
