from typing import List

from fastapi import APIRouter
from influxdb_client.client.flux_table import FluxTable, FluxRecord
from pydantic import ValidationError

from back.api.weather import get_weather
from back.models.city import City
from back.schemas.city import CityGet, CityTotalGet, ListCities
from back.schemas.node import NodePointGet
from back.time_series.air import InfluxAir
from back.utils.exceptions import NotFound, NoData
from config.influx import query_api
from config.owm import weather_manager

router = APIRouter(tags=["city"], prefix="/city")


@router.get('/all', response_model=ListCities)
def get_all_cities():
    city_query = City.objects.all()
    result = []

    for row in city_query:
        city = CityGet.from_orm(row)
        result.append(city)

    return result


@router.get('/{city_id}/total/')
def get_total(city_id: int):
    try:
        city = City.objects.get(id=city_id)
    except City.DoesNotExist:
        raise NotFound

    influx = InfluxAir(filters={'city_id': city_id}, last=True, mean=True, group=True)
    metrics = influx.get_metrics()

    # query = f"""
    # from(bucket: "air")
    #   |> range(start: -15m)
    #   |> filter(fn: (r) => r["city_id"] == "{city_id}")
    #   |> filter(fn: (r) =>
    #       r["_field"] == "aqi"
    #       or r["_field"] == "humidity"
    #       or r["_field"] == "pm10"
    #       or r["_field"] == "pm25"
    #       or r["_field"] == "pressure"
    #       or r["_field"] == "temperature")
    #   |> aggregateWindow(every: 15m, fn: mean, createEmpty: false)
    #   |> group(columns: ["_field"])
    #   |> last()
    # """

    try:
        city_total = CityTotalGet(**metrics.dict(), **city.__dict__)
    except ValidationError as e:
        raise NoData

    city_total.aqi_category = city_total.get_aqi_category()

    city_total.wind = get_weather(city.latitude, city.longitude)

    return city_total
