from typing import Optional

from pydantic import BaseModel, validator

from back.schemas.sensors import get_aqi_category


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


class NodeMetrics(BaseModel):
    pm25: Optional[int]
    pm10: Optional[int]
    temperature: Optional[int]
    pressure: Optional[int]
    humidity: Optional[int]
    aqi: Optional[int]
    aqi_category: Optional[str]

    def get_aqi_category(self):
        return get_aqi_category(self.aqi)


class NodePointGet(NodeMetrics):
    id: int
    uid: str
    name: str
    description: Optional[str]
    description: Optional[str]
    location_id: int
    city: Optional[str]

    wind: Optional[NodePointWindGet]
    location: Optional[SensorLocationPointGet]

    # @validator(pre=True)
    # def get_city(cls, values):
    #     if cls.fi
    #     return values

    class Config:
        orm_mode = True
