"""
ASGI config for mysite project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/asgi/
"""
import os

from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

application = get_asgi_application()

from back.router import app_router

from fastapi import FastAPI

fastapp = FastAPI()

fastapp.include_router(app_router)

# fastapp = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)

# import sentry_sdk
# from sentry_sdk.integrations.asgi import SentryAsgiMiddleware
#
# sentry_sdk.init(dsn=envs.SENTRY)
#
# fastapp = SentryAsgiMiddleware(fastapp)
