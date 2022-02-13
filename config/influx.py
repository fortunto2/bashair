from influxdb_client import InfluxDBClient, BucketRetentionRules

from config.envs import envs

client = InfluxDBClient(
    url=envs.INFLUXDB_V2_URL,
    org=envs.INFLUXDB_V2_ORG,
    token=envs.INFLUXDB_V2_TOKEN
)

buckets_api = client.buckets_api()
query_api = client.query_api()
