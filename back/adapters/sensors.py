import os
from http.client import HTTPException
from typing import TypeVar, Type

from back import models
from back.models.sensors import Sensor


ModelT = TypeVar("ModelT", bound=models.Model)


# def retrieve_node(model_class: Type[ModelT], uid: str) -> ModelT:
#     instance = model_class.objects.filter(uid=uid).first()
#     if not instance:
#         raise HTTPException(status_code=404, detail="Node not found.")
#     return instance


# def retrieve_node(c_id: int = Path(..., description="get sensor from db")):
#     return retrieve_object(Sensor, c_id)


def retrieve_sensors():
    return Sensor.objects.all()
