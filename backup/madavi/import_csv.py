#!/usr/bin/env python3


import os
import sys
import csv
from datetime import datetime, timedelta
from pprint import pprint

from influxdb_client import Point
from influxdb_client.client.write_api import SYNCHRONOUS, ASYNCHRONOUS

from config import settings
from config.influx import client
from back.schemas.sensors import SensorMeasurement


def get_timestamp(timestr):
    """Converts CSV time value to a UTC timestamp in seconds"""
    naive_dt = datetime.strptime(timestr, "%Y/%m/%d %H:%M:%S")
    utc = (naive_dt - datetime(1970, 1, 1)) / timedelta(seconds=1)
    return int(utc)


SENSOR_ID = 11545355
DATABASE = os.environ.get("INFLUXDB_DATABASE", "sensors")

# NODE = f"esp8266-{SENSOR_ID}"

NAME_MAP = {
    "Max_cycle": "max_micro",
    "Samples": "samples",
    "Min_cycle": "min_micro",
    "Signal": "signal",
    "SDS_P1": "pm10",
    "SDS_P2": "pm25",
    "BME280_temperature": "temperature",
    "BME280_humidity": "humidity",
    "BME280_pressure": "pressure",
}

with open('backup/madavi/test.csv') as csvfile:
    READER = csv.DictReader(csvfile, delimiter=";")

    for row in READER:
        # error out on legacy format until it's clear what that format is
        if row["Time"] == "time":
            raise Exception(
                "Looks like a legacy format not supported yet. Send the file to the author please."
            )

        # catch multiple column headers
        if row["Time"] == "Time":
            continue

        measurements = {}
        for header, value in row.items():
            if header == "Time" or not value:
                continue
            # measurements.append("{0}={1}".format(NAME_MAP.get(header, header), value))
            measurements[NAME_MAP.get(header, header)]= value

        # pprint(measurements)

        try:
            sensor_measurement = SensorMeasurement(**measurements)
        except Exception as e:
            print(row["Time"], measurements)
            print(e)
            continue

        sensor_measurement.aqi = sensor_measurement.get_aqi_value
        sensor_measurement.aqi_category = sensor_measurement.get_aqi_category

        # pprint(sensor_measurement.dict())

        write_api = client.write_api(write_options=SYNCHRONOUS)

        p = Point.from_dict({
            "measurement": settings.MEASUREMENT_NAME,
            "fields": sensor_measurement.dict(),
            "time": get_timestamp(row["Time"]),
            "tags": {
                "node": SENSOR_ID
            },
        })

        write_api.write(bucket=settings.MEASUREMENT_NAME, record=p)
