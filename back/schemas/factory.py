import json
from typing import Optional, List, Dict

# from django.contrib.gis.geos import Point
from django.contrib.gis.geos import Point
from pydantic import BaseModel, AnyUrl, validator
from geojson_pydantic import Feature, FeatureCollection, MultiPolygon

from back.schemas.location import LocationBase


class FactoryBase(LocationBase):
    name: str
    description: Optional[str]
    phone: Optional[str]
    email: Optional[str]
    website: Optional[AnyUrl]

    factory_type: Optional[str]
    danger_score: Optional[float]

    photo: Optional[str]
    icon: Optional[str]

    polygon: MultiPolygon

    @validator("phone", pre=True)
    def phone_validation(cls, v):
        return str(v)

    @validator("photo", pre=True)
    def photo_validation(cls, v):
        return str(v)

    @validator("icon", pre=True)
    def icon_validation(cls, v):
        return str(v)

    @validator("polygon", pre=True)
    def point_validation(cls, v: Point):
        try:
            return json.loads(v.json)
        except Exception as e:
            print(e)
        return v


class FactoryGet(FactoryBase):
    id: int

    class Config:
        orm_mode = True


class ListFactories(BaseModel):
    __root__: List[FactoryGet]


