from influxdb_client import InfluxDBClient, BucketRetentionRules

from config.base import settings

client = InfluxDBClient(
    url=settings.INFLUXDB_V2_URL,
    org=settings.INFLUXDB_V2_ORG,
    token=settings.INFLUXDB_V2_TOKEN
)

buckets_api = client.buckets_api()
query_api = client.query_api()
