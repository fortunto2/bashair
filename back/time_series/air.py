from statistics import mean
import sys

from influxdb_client.client.flux_table import FluxTable, FluxRecord

sys.path.append('.')
from config.influx import query_api


def get_air_values_mean(bucket='air', field='pm25', start='-1h', measurement="air", city=None):

    city_q = ''
    if city:
        city_q = f'|> filter(fn: (r) => r["city"] == "{city}")'

    tables = query_api.query(
        f"""
        from(bucket: "{bucket}")
          |> range(start: {start})
          |> filter(fn: (r) => r["_measurement"] == "{measurement}")
          |> filter(fn: (r) => r["_field"] == "{field}")
          {city_q}
          |> aggregateWindow(every: 1m, fn: mean, createEmpty: false)
          |> group(columns: ["_field"])
          |> mean(column: "_value")
        """
    )

    if tables:
        field_mean = next(x.get_value() for x in tables[0].records)
        return round(field_mean, 2)


if __name__ == "__main__":

    get_air_values_mean(field='pm25')
    get_air_values_mean(field='pm10')
    get_air_values_mean(field='aqi')
    get_air_values_mean(field='temperature')
