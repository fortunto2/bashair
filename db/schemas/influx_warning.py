from datetime import datetime
from typing import Optional, Union

from pydantic import BaseModel


class InfluxWarning(BaseModel):
    node: str
    pm25: Optional[float]
    pm10: Optional[float]
    temperature: Optional[float]
    pressure: Optional[float]
    humidity: Optional[float]
    aqi: Optional[float]
    aqi_category: Optional[str]

    _check_id: str
    _check_name: str
    _level: str
    _start: datetime
    _stop: datetime
    _time: datetime


