from typing import Optional, Dict, Union

from django.contrib.gis.geos import Point
from geojson import Point as PointJson
from pydantic import BaseModel, validator
import json


class LocationBase(BaseModel):
    city_id: int
    point: PointJson

    latitude: Optional[float]
    longitude: Optional[float]

    street_name: Optional[str]
    street_number: Optional[str]
    postalcode: Optional[int]

    @validator("point", pre=True)
    def point_validation(cls, v: Point):
        try:
            return json.loads(v.json)
        except Exception as e:
            print(e)
        return v
