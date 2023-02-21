"""
ASGI config for mysite project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/asgi/
"""
import os
from django.core.asgi import get_asgi_application
from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from config import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
application = get_asgi_application()

from config.auth import auth_handler
from back.router import app_router
from fastapi import FastAPI

fastapp = FastAPI()
fastapp.include_router(app_router)
fastapp.mount("", auth_handler)

fastapp.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

fastapp.add_middleware(SessionMiddleware, secret_key=settings.SECRET_KEY)

@fastapp.middleware("http")
async def add_process_time_header(request, call_next):
    response = await call_next(request)
    response.headers["X-Token"] = str(request.session.get("token"))
    return response


@fastapp.on_event("startup")
async def on_startup() -> None:
    FastAPICache.init(InMemoryBackend(), prefix="fastapi-cache")


# fastapp = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)

# import sentry_sdk
# from sentry_sdk.integrations.asgi import SentryAsgiMiddleware
#
# sentry_sdk.init(dsn=envs.SENTRY)
#
# fastapp = SentryAsgiMiddleware(fastapp)
