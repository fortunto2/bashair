from fastapi import APIRouter

from back.api import sensors, ping, instance, signal, node, city, community, auth, nmu, factory,notify, geo

app_router = APIRouter()

app_router.include_router(sensors.router)
app_router.include_router(instance.router)
app_router.include_router(signal.router)
app_router.include_router(community.router)
app_router.include_router(nmu.router)
app_router.include_router(node.router)
app_router.include_router(city.router)
app_router.include_router(auth.router)
app_router.include_router(ping.router)
app_router.include_router(factory.router)
app_router.include_router(notify.router)
app_router.include_router(geo.router)
