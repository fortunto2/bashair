from pprint import pprint
from statistics import mean

from influxdb_client import InfluxDBClient, BucketRetentionRules

from config import settings

client = InfluxDBClient(
    url=settings.INFLUXDB_V2_URL,
    org=settings.INFLUXDB_V2_ORG,
    token=settings.INFLUXDB_V2_TOKEN
)

buckets_api = client.buckets_api()
query_api = client.query_api()


def create_bucket(bucket):

    org = list(filter(lambda it: it.name == settings.INFLUXDB_V2_ORG, client.organizations_api().find_organizations()))[
        0]

    retention_rules = BucketRetentionRules(type="expire", every_seconds=3600)
    created_bucket = buckets_api.create_bucket(bucket_name=bucket,
                                               retention_rules=retention_rules,
                                               org_id=org.id)

    return created_bucket


def get_air_values_mean(bucket='air', field='pm25', start='-1h', measurement="air"):
    print(bucket, field, start)
    field_mean = None

    tables = query_api.query(
        f"""
        from(bucket: "{bucket}")
          |> range(start: {start})
          |> filter(fn: (r) => r["_measurement"] == "{measurement}")
          |> filter(fn: (r) => r["_field"] == "{field}")
          |> aggregateWindow(every: 1h, fn: mean, createEmpty: false)
          |> yield(name: "mean")
        """
    )

    if tables:
        field_mean = round(mean([table.records[0]['_value'] for table in tables]), 1)
        print(field_mean)

    # for table in tables:
    #     print('-----------')
    #     for row in table.records:
    #         pprint(row.values)

    return field_mean


if __name__ == "__main__":

    get_air_values_mean(field='pm25')
    get_air_values_mean(field='pm10')
    get_air_values_mean(field='aqi')
    get_air_values_mean(field='temperature')
