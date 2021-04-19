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

    check_id: str
    check_name: str
    level: str
    start: datetime
    stop: datetime
    time: datetime


