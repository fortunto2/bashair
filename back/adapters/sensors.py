from fastapi import Path

from back.adapters.base import retrieve_object
from back.models.sensors import Sensor


def retrieve_sensor(c_id: int = Path(..., description="get sensor from db")):
    return retrieve_object(Sensor, c_id)


def retrieve_sensors():
    return Sensor.objects.all()
