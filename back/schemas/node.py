from typing import Optional

from pydantic import BaseModel, validator


class SensorTypeBase(BaseModel):
    pass


class SensorTypeGet(SensorTypeBase):
    pass


class NodeBase(BaseModel):
    pass


class NodeCreate(NodeBase):
    pass


class NodeGet(NodeBase):
    pass


class SensorBase(BaseModel):
    pass


class SensorGet(SensorBase):
    pass


class SensorLocationBase(BaseModel):
    pass


class SensorLocationGet(SensorLocationBase):
    pass


class SensorLocationPointGet(BaseModel):
    longitude: Optional[float]
    latitude: Optional[float]

    class Config:
        orm_mode = True


class NodePointWindGet(BaseModel):
    speed: Optional[float]
    deg: Optional[int]

    class Config:
        orm_mode = True


class NodePointGet(BaseModel):
    id: int
    uid: str
    name: str
    description: Optional[str]
    description: Optional[str]
    location_id: int
    city: Optional[str]

    pm25: Optional[float]
    wind: Optional[NodePointWindGet]
    location: SensorLocationPointGet

    # @validator(pre=True)
    # def get_city(cls, values):
    #     if cls.fi
    #     return values

    class Config:
        orm_mode = True
