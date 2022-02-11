from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel


class SignalPropertiesBase(BaseModel):
    name: str
    group: str


class SignalProperties(SignalPropertiesBase):
    id: int

    class Config:
        orm_mode = True


class SignalBase(BaseModel):
    text: str
    location: str
    latitude: float
    longitude: float
    time_of_incident: datetime
    status: str


class SignalCreate(SignalBase):
    properties: Optional[List[int]]


class Signal(SignalBase):
    id: int
    owner_id: int
    properties: Optional[List[SignalProperties]]

    created: datetime
    modified: datetime

    class Config:
        orm_mode = True


class SignalToInstanceBase(BaseModel):
    text: str
    time_of_report: datetime
    response: str
    time_of_response: datetime
    status: str
    other_comment: str


class SignalToInstanceCreate(SignalToInstanceBase):
    signal_id: int
    instance_id: int


class SignalToInstance(SignalToInstanceBase):
    id: int
    signal_id: int
    instance_id: int

    class Config:
        orm_mode = True
