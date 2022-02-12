import sys

sys.path.append('.')
from back.schemas.sensors import get_aqi_category, get_aqi

import pandas as pd
from influxdb_client.client.write_api import SYNCHRONOUS

from config.influx import client
import datetime as dt


sensors = [
    ['11545355', '56333', '56334'],
    ['6520336', '60050', '60051'],
    ['6504878', '60054', '60055'],
    ['15568680', '60068', '60069'],
    ['6506785', '60086', '60087'],
    ['11645760', '60088', '60089'],
    ['11590088', '60090', '60091'],
    ['6515405', '60092', '60093'],
    ['15567731', '60100', '60101'],
]

start_date = dt.datetime(2022, 2, 1)
end_date = dt.datetime.now()

tags = ['location', 'lat', 'lon', 'node']

write_api = client.write_api(write_options=SYNCHRONOUS)

for node_id, sds_id, bme_id in sensors:
    print('-' * 20)
    print(node_id, sds_id, bme_id)

    for single_date in pd.date_range(start_date, end_date):
        xdate = single_date.strftime("%Y-%m-%d")
        print('-->', xdate)

        bme_url = f"https://archive.sensor.community/{xdate}/{xdate}_bme280_sensor_{bme_id}.csv"
        sds_url = f"https://archive.sensor.community/{xdate}/{xdate}_sds011_sensor_{sds_id}.csv"
        print(sds_url)
        try:
            sds_df = pd.read_csv(sds_url, delimiter=';')
            sds_df.index = sds_df.timestamp
            sds_df['node'] = f"esp8266-{node_id}"

            sds_df = sds_df.rename(columns={'P1': 'pm10', 'P2': 'pm25'})

            print('sds:', sds_df.shape)
            # print(sds_df[['pm25']].mean())
            # print(sds_df[['pm10']].mean())

            sds_df['aqi'] = sds_df.apply(lambda x: get_aqi(x.pm10, x.pm25), axis=1)
            sds_df['aqi_category'] = sds_df.apply(lambda x: get_aqi_category(x.aqi), axis=1)
            print(sds_df)

            write_api.write(bucket='air',
                            record=sds_df[['pm10', 'pm25', 'aqi', 'aqi_category'] + tags],
                            data_frame_measurement_name='air',
                            data_frame_tag_columns=tags
                            )

        except Exception as e:
            print(e)
