from typing import Optional, List, Union

from pydantic import BaseModel, AnyUrl, EmailStr

from back.schemas.node import NodeMetrics
from back.schemas.sensors import get_aqi_category


class CountryBase(BaseModel):
    id: int
    name: str
    slug: Optional[str]
    tld: Optional[str]


class RegionBase(BaseModel):
    id: int
    name: str
    slug: Optional[str]
    tld: Optional[str]


class CityBase(BaseModel):
    display_name: str
    latitude: Optional[float]
    longitude: Optional[float]
    # country: Optional[Union[str, CountryBase]]
    country_id: Optional[int]
    # region: Optional[Union[str, RegionBase]]
    region_id: Optional[int]
    subregion_id: Optional[int]
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


class ListCities(BaseModel):
    __root__: List[CityGet]

