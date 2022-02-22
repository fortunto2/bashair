import sys
from datetime import datetime
from pprint import pprint
from typing import Optional, List, Dict, Union

sys.path.append('.')

from influxdb_client.client.flux_table import FluxTable, FluxRecord
from pydantic import ValidationError, BaseModel

from back.schemas.node import NodeMetrics, ListNodes
from config.influx import query_api


class InfluxAirFilter(BaseModel):
    city: Optional[str]
    city_id: Optional[int]
    node: Optional[str]


class InfluxAir(BaseModel):

    bucket: str = 'air'
    measurement: str = 'air'

    fields: List = ['aqi', 'humidity', 'pm10', 'pm25', 'pressure', 'temperature']

    start: str = '-15m'
    filters: Optional[Union[InfluxAirFilter, Dict]]
    aggregate: str = '15m'
    function: str = 'mean'

    result: Optional[NodeMetrics]

    # def __post_init__(self):
    #     print('post_init')
    #     self.result = self.get_metrics()

    def __transform_answer(self, tables):
        results = {}
        field_table: FluxTable
        for field_table in tables:
            record: FluxRecord

            for record in field_table.records:
                results[record.get_field()] = round(record.get_value(), 2)

        if results:
            try:
                metrics = NodeMetrics(**results)
            except ValidationError as e:
                print(e)
                return None

            return metrics

    def __create_filter(self, filters: InfluxAirFilter):

        query = ''

        if self.filters:
            for attr, value in self.filters.dict().items():
                if not value: continue
                query += f'|> filter(fn: (r) => r["{attr}"] == "{value}") '

        return query

    def __create_fields(self, fields):
        from copy import deepcopy

        query = ''
        fields_copy = deepcopy(fields)

        if fields_copy:
            field = fields_copy.pop()
            query = f'|> filter(fn: (r) => r["_field"] == "{field}" '

            while fields_copy:
                field = fields_copy.pop()
                if field:
                    query += f' or r["_field"] == "{field}"'
            query += ')'
        return query

    def __create_query(self, group=False, mean=False, last=False):
        query_str = f"""
                    from(bucket: "{self.bucket}")
                      |> range(start: {self.start})
                      |> filter(fn: (r) => r["_measurement"] == "{self.measurement}")
                      {self.__create_filter(self.filters)}
                      {self.__create_fields(self.fields)}
                      |> aggregateWindow(every: {self.aggregate}, fn: {self.function}, createEmpty: false)
                    """

        if group:
            query_str += '|> group(columns: ["_field"]) '

        if mean:
            query_str += '|> mean(column: "_value") '

        if last:
            query_str += '|> last() '

        # print(query_str)
        return query_str

    def get_metrics(self) -> NodeMetrics:

        tables = query_api.query(self.__create_query(group=True, mean=True, last=True))
        # print('tables len:', len(tables))

        return self.__transform_answer(tables)

    def get_history(self, start='-24h', aggregate='1h') -> List[NodeMetrics]:

        self.start = start
        self.aggregate = aggregate

        query_str = self.__create_query()
        query_str += f'|> truncateTimeColumn(unit: {aggregate})'

        # print(query_str)

        tables = query_api.query(query_str)
        # print('tables len:', len(tables))

        results = {}
        history = []

        field_table: FluxTable
        for field_table in tables:
            record: FluxRecord

            for record in field_table.records:
                time: datetime = record.get_time()
                results.setdefault(time, {})

            for record in field_table.records:
                time: datetime = record.get_time()
                results[time].update({record.get_field(): round(record.get_value(), 2)})

        for key, value in results.items():

            metrics = NodeMetrics(**value)
            metrics.time = key
            metrics.aqi_category = metrics.get_aqi_category()

            history.append(metrics)

        return history


if __name__ == "__main__":

    # x = InfluxAir(filters={'city_id': 1})
    x = InfluxAir(filters={'node': 'esp8266-11645760'})
    pprint(x)
    pprint(x.get_metrics())
    pprint(x.get_history())

#     txt = \
# """
# Средние данные за час воздуха в Стерлитамаке:
# PM2.5: {pm25}
# PM10: {pm10}
# AQI: {aqi}
# TEMP: {temperature}
# Подробнее на карте https://aircms.online/#/d/11545355
# """.format(**x.get_metrics().dict())
#
#     print(txt)
