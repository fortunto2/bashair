from fastapi import APIRouter

from back.api import sensors, ping, instance, signal

app_router = APIRouter()

app_router.include_router(sensors.router)
app_router.include_router(instance.router)
app_router.include_router(signal.router)
app_router.include_router(ping.router)
