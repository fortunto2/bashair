import os
from typing import Optional

from fastapi import APIRouter
from influxdb_client import Point
from influxdb_client.client.write_api import SYNCHRONOUS
from fastapi import Request
from fastapi.responses import JSONResponse

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


@router.post('/upload_measurement')
def upload_measurement(data: SensorData, request: Request):
    """
    Принимаем данные от датчиков
    """

    # print('upload_measurement', data)
    from back.models.node import Node
    node = None

    test_mode = data.test

    try:
        node: Node = Node.objects.get(uid=data.node_tag)
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

    write_api = client.write_api(write_options=SYNCHRONOUS)

    _dict = {
        "measurement": envs.MEASUREMENT_NAME,
        "fields": sensor_measurement.dict(),
        "tags": {
            "node": data.node_tag,
            "name": node.name,
            "lat": float(node.latitude),
            "lon": float(node.longitude),
            "city": node.city.name,
            "city_id": node.city.id,
            "street": node.street_name,
        },
    }

    p = Point.from_dict(_dict)

    if test_mode:
        x = write_api.write(bucket='test', record=p)
        print(_dict)
        print(x)
        return JSONResponse(content={'result': True, **_dict})
    else:
        write_api.write(bucket=envs.MEASUREMENT_NAME, record=p)

    return JSONResponse(content={'result': True})
