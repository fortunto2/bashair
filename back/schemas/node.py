from datetime import datetime
from typing import Optional, List, Dict

from django.contrib.gis.geos import Point
from pydantic import BaseModel, validator

from back.schemas.sensors import get_aqi_category
from geojson_pydantic import Point as PointJson


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


class NodeMetricsBase(BaseModel):
    pm25: int
    pm10: int
    temperature: int
    pressure: int
    humidity: int
    aqi: int
    aqi_category: Optional[str]

    def get_aqi_category(self):
        return get_aqi_category(self.aqi)


class NodeMetrics(BaseModel):
    pm25: int
    pm10: int
    temperature: Optional[int]
    pressure: Optional[int]
    humidity: Optional[int]
    aqi: Optional[int]
    aqi_category: Optional[str]
    wind: Optional[NodePointWindGet]
    time: Optional[datetime]

    def get_aqi_category(self):
        return get_aqi_category(self.aqi)


class NodePointGet(NodeMetrics):
    id: int
    uid: str
    name: str
    description: Optional[str]
    point: Optional[str]

    latitude: Optional[float]
    longitude: Optional[float]

    city: Optional[str]
    street_name: Optional[str]
    street_number: Optional[str]

    created: Optional[datetime]
    modified: Optional[datetime]

    # @validator(pre=True)
    # def get_city(cls, values):
    #     if cls.fi
    #     return values

    @validator("point", pre=True)
    def point_validation(cls, v: Point):
        try:
            return v.json
        except Exception as e:
            print(e)
        return v

    class Config:
        orm_mode = True


class ListNodes(BaseModel):
    __root__: List[NodePointGet]


class ListNodeMetrics(BaseModel):
    __root__: List[NodeMetrics]

