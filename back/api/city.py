from fastapi import APIRouter

from config.influx import query_api

router = APIRouter(tags=["city"], prefix="/city")


@router.get('/{city_id}/total/')
def get_total(city_id: int):
    query = f"""
    from(bucket: "air")
      |> range(start: -15m)
      |> filter(fn: (r) => r["city_id"] == "{city_id}")
      |> filter(fn: (r) => r["_field"] == "aqi" or r["_field"] == "humidity" or r["_field"] == "pm10" or r["_field"] == "pm25" or r["_field"] == "pressure" or r["_field"] == "temperature")
      |> aggregateWindow(every: 15m, fn: sum, createEmpty: false)
      |> last()
    """
    total = {}
    fields = {}
    result = query_api.query_csv(query)
    for row in result:
        if len(row) > 1:
            if row[1] == 'result':
                for index, col in enumerate(row):
                    if col in ['_value', '_field']:
                        fields[col] = index
            if row[0] == '' and row[1] == '':
                field = row[fields['_field']]
                value = row[fields['_value']]
                if field in total:
                    total[field] += float(value)
                else:
                    total[field] = float(value)
    return total
