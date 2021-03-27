from typing import Type
from typing import TypeVar

from django.db import models
from fastapi import HTTPException
from fastapi import Path

from back.models.sensors import Sensor

ModelT = TypeVar("ModelT", bound=models.Model)


def retrieve_object(model_class: Type[ModelT], id: int) -> ModelT:
    instance = model_class.objects.filter(pk=id).first()
    if not instance:
        raise HTTPException(status_code=404, detail="Object not found.")
    return instance


def retrieve_sensor(c_id: int = Path(..., description="get sensor from db")):
    return retrieve_object(Sensor, c_id)


def retrieve_sensors():
    return Sensor.objects.all()
