from typing import Optional, List

from fastapi import APIRouter
from influxdb_client.client.flux_table import FluxTable, FluxRecord
from starlette.responses import JSONResponse

from back.schemas.nmu import NmuBase
from config.influx import query_api

router = APIRouter(tags=["nmu"], prefix="/nmu")


def get_nmu_influx(measurment='predictions', start='-24h', city_id=None, region_id=None):

    city_q = ''
    region_q = ''

    if region_id:
        region_q = f'|> filter(fn: (r) => r["region_id"] == "{region_id}")'
    if city_id:
        city_q = f'|> filter(fn: (r) => r["city_id"] == "{city_id}")'

    result: List[FluxTable] = query_api.query(
        f"""
        from(bucket: "air")
          |> range(start: {start})
          |> filter(fn: (r) => r["_measurement"] == "{measurment}")
          |> filter(fn: (r) => r["_field"] == "nmu")
          {region_q}
          {city_q}
          |> group(columns: ["_field"])
          |> last()
        """
    )

    results = []
    table: FluxTable
    for table in result:
        record: FluxRecord
        for record in table.records:
            results.append((record.get_value(), record.get_time()))

    if results:
        return results[-1]


@router.get('', response_model=NmuBase)
def get_nmu(region_id: Optional[str] = '', city_id: Optional[str] = ''):

    result = get_nmu_influx(city_id=city_id, region_id=region_id)
    mode = result[0]
    time = result[1]
    if result:

        print(f'get NMU for {region_id}, {city_id} = {result}')

        return {
            'mode': mode,
            'datetime': time,
            'time': time.strftime("%H:%M"),
            'date': time.strftime("%Y-%m-%d"),
        }



