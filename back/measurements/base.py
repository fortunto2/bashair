from influxdb_client import BucketRetentionRules

from config.base import settings
from config.influx import client, buckets_api


def create_bucket(bucket):

    org = list(filter(lambda it: it.name == settings.INFLUXDB_V2_ORG, client.organizations_api().find_organizations()))[
        0]

    retention_rules = BucketRetentionRules(type="expire", every_seconds=3600)
    created_bucket = buckets_api.create_bucket(bucket_name=bucket,
                                               retention_rules=retention_rules,
                                               org_id=org.id)

    return created_bucket
