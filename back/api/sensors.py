import os
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
from http.client import HTTPException

from typing import Optional
import logging
from asgiref.sync import sync_to_async
from fastapi import APIRouter
from influxdb_client import Point
from influxdb_client.client.write_api import SYNCHRONOUS
from fastapi import Request
from fastapi.responses import JSONResponse
from back.time_series.air import get_air_values_mean

from back.schemas.sensors import SensorData, SensorMeasurement
from config.envs import envs
from config.influx import client
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY

router = APIRouter(tags=["sensors"], prefix="")

NAME_MAP = {
    "Max_cycle": "max_micro",
    "Samples": "samples",
    "Min_cycle": "min_micro",
    "Signal": "signal",
    "SDS_P1": "pm10",
    "SDS_P2": "pm25",
    "BME280_temperature": "temperature",
    "BME280_humidity": "humidity",
    "BME280_pressure": "pressure",
}


# @router.get('/data/mean')
# async def get_sensor_data(city: Optional[str] = '', field: Optional[str] = 'pm25', period: Optional[str] = '-1h'):
#
#     result = get_air_values_mean(field=field, start=period, city=city)
#     print(f'get mean city: {city} = {result}')
#
#     return JSONResponse(content={
#         'result': result,
#         'field': field,
#         'period': period,
#         'city': city,
#     })


@router.post('/upload_measurement')
def upload_measurement(data: SensorData, request: Request):
    """
    Принимаем данные от датчиков
    """
    # print('upload_measurement', data)
    from back.models.node import Node, SensorLocation
    node = None
    try:
        node: Node = Node.objects.select_related('location').get(uid=data.node_tag)
    except Exception as e:
        print(e, data.node_tag)

    if not node:
        return JSONResponse(content={'result': False})

    print(request.client.host, node)

    data_points = {}
    for dp in data.sensordatavalues:
        data_points[dp.value_type] = dp.value
        data_points[NAME_MAP.get(dp.value_type, dp.value_type)] = dp.value

    try:
        sensor_measurement = SensorMeasurement(**data_points)
    except Exception as e:
        print(data.node_tag, e)
        return JSONResponse(content={'result': False})

    sensor_measurement.aqi = sensor_measurement.get_aqi_value
    sensor_measurement.aqi_category = sensor_measurement.get_aqi_category

    # print(sensor_measurement.dict())

    write_api = client.write_api(write_options=SYNCHRONOUS)

    _dict = {
        "measurement": envs.MEASUREMENT_NAME,
        "fields": sensor_measurement.dict(),
        "tags": {
            "node": data.node_tag,
            "location": node.location.location,
            "lat": node.location.latitude,
            "lon": node.location.longitude,
            "city": node.location.city.name,
            "city_id": node.location.city.id,
            "street": node.location.street_name,
        },
    }

    p = Point.from_dict(_dict)

    write_api.write(bucket=envs.MEASUREMENT_NAME, record=p)

    return JSONResponse(content={'result': True})
