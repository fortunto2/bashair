from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, validator


class SignalPropertiesBase(BaseModel):
    name: str
    group: str


class SignalProperties(SignalPropertiesBase):
    id: int

    class Config:
        orm_mode = True


class SignalBase(BaseModel):
    text: str
    point: Optional[str]
    latitude: float
    longitude: float
    time_of_incident: datetime


class SignalCreate(SignalBase):
    city_id: int
    properties: Optional[List[int]]


class SignalGet(SignalBase):
    id: int
    city_id: int
    owner_id: Optional[int]
    properties: Optional[List[SignalProperties]]
    status: str

    created: datetime
    modified: datetime

    class Config:
        orm_mode = True

    @validator('properties', pre=True)
    def get_properties(cls, v):
        return [SignalProperties.from_orm(obj) for obj in v.all()]


class SignalToInstanceBase(BaseModel):
    text: str
    time_of_report: datetime
    response: str
    time_of_response: datetime
    status: str
    other_comment: Optional[str]


class SignalToInstanceCreate(SignalToInstanceBase):
    signal_id: int
    instance_id: int


class SignalToInstanceGet(SignalToInstanceBase):
    id: int
    signal_id: int
    instance_id: int

    class Config:
        orm_mode = True
