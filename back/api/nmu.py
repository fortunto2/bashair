from typing import Optional

from fastapi import APIRouter
from starlette.responses import JSONResponse

from config.influx import query_api

router = APIRouter(tags=["nmu"], prefix="/nmu")


def get_nmu_influx(measurment='predictions', start='-24h', measurement="air", city=None, region=None):

    city_q = ''
    region_q = ''
    result = ''
    time = ''

    if region:
        region_q = f'|> filter(fn: (r) => r["region"] == "{region}")'
    if city:
        city_q = f'|> filter(fn: (r) => r["city"] == "{city}")'

    tables = query_api.query(
        f"""
        from(bucket: "air")
          |> range(start: {start})
          |> filter(fn: (r) => r["_measurement"] == "{measurment}")
          |> filter(fn: (r) => r["_field"] == "nmu")
          {region_q}
          {city_q}
          |> last()
        """
    )

    if tables:
        result = next(table.records[0]['_value'] for table in tables)
        time = next(table.records[0]['_time'] for table in tables)
        print(result, time)

    return result, time


@router.get('')
def get_nmu(region: Optional[str] = '', city: Optional[str] = ''):

    result, time = get_nmu_influx(city=city, region=region)
    if result:

        print(f'get NMU for {region}, {city}')

        return JSONResponse(content={
            'result': result,
            'last_date': str(time.date()),
            'last_time': str(time.time()).split('.')[0],
        })



