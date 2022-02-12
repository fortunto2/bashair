from pydantic import BaseModel


class InstanceBase(BaseModel):
    name: str
    description: str
    phone: str
    email: str
    address: str
    website: str
    report_url: str


class Instance(InstanceBase):
    id: int
    city_id: int

    class Config:
        orm_mode = True
