import pandas as pd
from influxdb_client.client.write_api import SYNCHRONOUS

from config import settings
from db.influx import client
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

start_date = dt.datetime(2021, 3, 20)
end_date = dt.datetime.now()

tags = ['location', 'lat', 'lon', 'sensor_type', 'sensor_id']

write_api = client.write_api(write_options=SYNCHRONOUS)

for node_id, sds_id, bme_id in sensors:
    print('-' * 20)
    print(node_id, sds_id, bme_id)

    for single_date in pd.date_range(start_date, end_date):
        xdate = single_date.strftime("%Y-%m-%d")
        print('-->', xdate)

        bme_url = f"https://archive.sensor.community/{xdate}/{xdate}_bme280_sensor_{bme_id}.csv"
        sds_url = f"https://archive.sensor.community/{xdate}/{xdate}_sds011_sensor_{sds_id}.csv"

        try:
            bme_df = pd.read_csv(bme_url, delimiter=';')
            bme_df.index = bme_df.timestamp

            print('bme:', bme_df.shape)

            write_api.write(bucket=settings.MEASUREMENT_NAME,
                            record=bme_df[['temperature', 'humidity', 'pressure'] + tags],
                            data_frame_measurement_name='air',
                            data_frame_tag_columns=tags
                            )

        except Exception as e:
            print(e)

        try:
            sds_df = pd.read_csv(sds_url, delimiter=';')
            sds_df.index = sds_df.timestamp

            sds_df = sds_df.rename(columns={'P1': 'pm10', 'P2': 'pm25'})

            print('sds:', sds_df.shape)
            # print(sds_df[['pm25']].mean())
            # print(sds_df[['pm10']].mean())

            write_api.write(bucket=settings.MEASUREMENT_NAME,
                            record=sds_df[['pm10', 'pm25'] + tags],
                            data_frame_measurement_name='air',
                            data_frame_tag_columns=tags
                            )

        except Exception as e:
            print(e)
