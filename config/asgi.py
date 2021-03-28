"""
ASGI config for mysite project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/asgi/
"""
import os

from django.core.asgi import get_asgi_application

from back.api import sensors, ping, notify

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

application = get_asgi_application()

from fastapi import FastAPI

fastapp = FastAPI()
# fastapp = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)

fastapp.include_router(sensors.router, tags=["sensors"], prefix="/v1")
fastapp.include_router(notify.router, tags=["notify"], prefix="/v1")
fastapp.include_router(ping.router, tags=["ping"], prefix="")
