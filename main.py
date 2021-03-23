import secrets
from datetime import datetime, time
from typing import Dict, Optional, List, Union

from fastapi import FastAPI, Request, Form, Depends, HTTPException, Body
from fastapi.responses import HTMLResponse, RedirectResponse, Response
from fastapi import status
import aqi
from influxdb_client import Point
from influxdb_client.client.write_api import ASYNCHRONOUS, SYNCHRONOUS
from pydantic import BaseModel

from config import settings
from db.influx import client
from db.mongo_async import engine

app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)

AQI_CATEGORIES = {
    (-1, 50): "Good",
    (50, 100): "Moderate",
    (100, 150): "Unhealthy for Sensitive Groups",
    (150, 200): "Unhealthy",
    (200, 300): "Very Unhealthy",
    (300, 500): "Hazardous",
}


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


@app.post('/upload_measurement')
async def upload_measurement(data: SensorData):
    print(data)

    data_points = {}
    for dp in data.sensordatavalues:
        data_points[dp.value_type] = dp.value

    sensor_measurement = SensorMeasurement(
        pm10=data_points['SDS_P1'],
        pm25=data_points['SDS_P2'],
        temperature=data_points['BME280_temperature'],
        pressure=data_points['BME280_pressure'],
        humidity=data_points['BME280_humidity'],
        samples=data_points['samples'],
        min_micro=data_points['min_micro'],
        max_micro=data_points['max_micro'],
        signal=data_points['signal'],
    )

    sensor_measurement.aqi = sensor_measurement.get_aqi_value
    sensor_measurement.aqi_category = sensor_measurement.get_aqi_category

    print(sensor_measurement.dict())

    write_api = client.write_api(write_options=SYNCHRONOUS)

    p = Point.from_dict({
        "measurement": settings.MEASUREMENT_NAME,
        "fields": sensor_measurement.dict(),
        "tags": {
            "node": data.node_tag
        },
    }
    )

    write_api.write(bucket=settings.MEASUREMENT_NAME, record=p)

    return data


if __name__ == "__main__":
    import asyncio
    import uvicorn

    # loop = asyncio.get_event_loop()
    # config = uvicorn.Config("main:app", host='0.0.0.0', port=8000, loop=loop, reload=True)
    # server = uvicorn.Server(config)
    # loop.run_until_complete(server.serve())
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
