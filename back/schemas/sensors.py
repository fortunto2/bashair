from typing import Optional, Union, List

import aqi
from pydantic import BaseModel

AQI_CATEGORIES = {
    (-1, 50): "Good",
    (50, 100): "Moderate",
    (100, 150): "Unhealthy for Sensitive Groups",
    (150, 200): "Unhealthy",
    (200, 300): "Very Unhealthy",
    (300, 500): "Hazardous",
}


def get_aqi(pm10, pm25):
    aqi_value = float(
        aqi.to_aqi([(aqi.POLLUTANT_PM10, pm10), (aqi.POLLUTANT_PM25, pm25)])
    )
    return aqi_value


def get_aqi_category(aqi_value):
    for limits, category in AQI_CATEGORIES.items():
        if aqi_value > limits[0] and aqi_value <= limits[1]:
            return category


class SensorMeasurement(BaseModel):
    """
    Final data to save
    """
    pm25: float
    pm10: float
    temperature: float
    pressure: float
    humidity: float
    aqi: Optional[float]
    aqi_category: Optional[str]

    samples: int
    min_micro: int
    max_micro: int
    signal: float

    @property
    def get_aqi_value(self):
        if self.pm25 and self.pm10:
            self.aqi = float(
                aqi.to_aqi([(aqi.POLLUTANT_PM10, self.pm10), (aqi.POLLUTANT_PM25, self.pm25)])
            )
            return self.aqi

    @property
    def get_aqi_category(self):
        self.aqi_category = get_aqi_category(self.get_aqi_value)
        return self.aqi_category


class SensorDataValues(BaseModel):
    value_type: str
    value: Union[float, int]


class SensorData(BaseModel):
    """
    Measurement from air sensor to store in DB
    """
    sensordatavalues: List[SensorDataValues]
    software_version: str
    esp8266id: Optional[str]
    rpiid: Optional[str]

    @property
    def node_tag(self):
        node_tag = "unknown"

        if self.esp8266id:
            node_tag = f"esp8266-{self.esp8266id}"
        elif self.rpiid:
            node_tag = f"rpi-{self.rpiid}"

        return node_tag
