import os
from typing import Dict
import sys

import requests
from bs4 import BeautifulSoup
from influxdb_client import Point
from influxdb_client.client.write_api import SYNCHRONOUS

sys.path.append('.')
# from back.models.city import City, Region
from config.envs import envs
from config.influx import client

"""
Неблагоприятные метереологические условия НМУ. МОгут быть 1, 2, 3. Чем выше тем хуже.
http://www.meteorb.ru/monitoring/prognoz-zagryazneniya-atmosfery

Если способствует рассеиванию это отсутствие нму.
Если способствует  накоплению это  режимы НМУ - незначительное  загрязнение атмосферы  это 1 режим НМУ.
Повышенное загрязнение атмосферы это 2 режим НМУ. Чрезвычайное 3. На моей памяти 3 не было.

"""


def insert_to_influx(fields: Dict, tags: Dict, measurement='predictions'):

    write_api = client.write_api(write_options=SYNCHRONOUS)

    _dict = {
        "measurement": measurement,
        "fields": fields,
        "tags": {
            **tags
        },
    }

    print(_dict)

    p = Point.from_dict(_dict)
    print(p)

    x = write_api.write(bucket=envs.MEASUREMENT_NAME, record=p)
    # x = write_api.write(bucket='test', record=p)
    return x


url = 'http://www.meteorb.ru/monitoring/prognoz-zagryazneniya-atmosfery'
page = requests.get(url)
# print(page.status_code)

soup = BeautifulSoup(page.text, "html.parser")
rows = soup.findAll('td')

nmu = 0

for row in rows:
    text = row.get_text()
    if 'сутки' in text:
        print(text)
        if 'накоплен' in text and 'незначительн' in text:
            nmu = 1
        elif 'резвычайн' in text:
            nmu = 3
        elif 'повышенн' in text:
            nmu = 2

print(nmu)

# city = City.objects.get(name='Стерлитамак')
# region = Region.objects.get(name='Башкортостан')

fields = {
    'nmu': nmu
}

tags = {
    'city': "Стерлитамак",
    'city_id': 1,
    'region': "Башкортостан",
    'region_id': 1,
}

print(tags)

insert_to_influx(fields, tags)

