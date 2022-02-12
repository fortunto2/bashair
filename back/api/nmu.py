from typing import Optional

from fastapi import APIRouter
from starlette.responses import JSONResponse

from back.schemas.nmu import NmuBase
from config.influx import query_api

router = APIRouter(tags=["nmu"], prefix="/nmu")


def get_nmu_influx(measurment='predictions', start='-24h', city_id=None, region_id=None):

    city_q = ''
    region_q = ''
    result = ''
    time = ''

    if region_id:
        region_q = f'|> filter(fn: (r) => r["region_id"] == "{region_id}")'
    if city_id:
        city_q = f'|> filter(fn: (r) => r["city_id"] == "{city_id}")'

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


@router.get('', response_model=NmuBase)
def get_nmu(region_id: Optional[str] = '', city_id: Optional[str] = ''):

    result, time = get_nmu_influx(city_id=city_id, region_id=region_id)
    if result:

        print(f'get NMU for {region_id}, {city_id} = {result}')

        return {
            'mode': result,
            'datetime': time,
        }



