from typing import Optional

from pydantic import BaseModel, AnyUrl, EmailStr

from back.schemas.node import NodeMetrics
from back.schemas.sensors import get_aqi_category


class CityBase(BaseModel):
    display_name: str
    latitude: Optional[float]
    longitude: Optional[float]
    country: Optional[str]
    region: Optional[str]
    subregion: Optional[str]
    population: Optional[str]
    feature_code: Optional[str]
    timezone: Optional[str]


class CityGet(CityBase):
    id: int

    class Config:
        orm_mode = True


class CityTotalGet(CityGet, NodeMetrics):
    pass

    def get_aqi_category(self):
        return get_aqi_category(self.aqi)
