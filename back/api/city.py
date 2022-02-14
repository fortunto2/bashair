from typing import List

from fastapi import APIRouter
from influxdb_client.client.flux_table import FluxTable, FluxRecord
from pydantic import ValidationError

from back.models.city import City
from back.schemas.city import CityGet, CityTotalGet
from back.schemas.node import NodePointGet
from back.utils.exceptions import NotFound, NoData
from config.influx import query_api
from config.owm import weather_manager

router = APIRouter(tags=["city"], prefix="/city")


@router.get('/all')
def get_all_cities():
    city_query = City.objects.all()
    cities = [CityGet.from_orm(obj).dict() for obj in city_query]
    return cities


@router.get('/{city_id}/total/')
def get_total(city_id: int):
    try:
        city = City.objects.get(id=city_id)
    except City.DoesNotExist:
        raise NotFound

    query = f"""
    from(bucket: "air")
      |> range(start: -15m)
      |> filter(fn: (r) => r["city_id"] == "{city_id}")
      |> filter(fn: (r) => 
          r["_field"] == "aqi" 
          or r["_field"] == "humidity" 
          or r["_field"] == "pm10" 
          or r["_field"] == "pm25" 
          or r["_field"] == "pressure" 
          or r["_field"] == "temperature")
      |> aggregateWindow(every: 15m, fn: mean, createEmpty: false)
      |> group(columns: ["_field"])
      |> last()
    """

    result_query = query_api.query(query)

    results = {}
    table: FluxTable
    for table in result_query:
        record: FluxRecord

        for record in table.records:
            results[record.get_field()] = round(record.get_value(), 2)

    try:
        city_total = CityTotalGet(**results, **city.__dict__)
    except ValidationError as e:
        raise NoData

    city_total.aqi_category = city_total.get_aqi_category()

    if city.latitude is not None and city.longitude is not None:
        try:
            response = weather_manager.weather_at_coords(
                lat=float(city.latitude),
                lon=float(city.longitude)
            )
            city_total.wind = response.weather.wnd
        except Exception as e:
            print(f'WARNING! Error weather API: {e}')

    return city_total
