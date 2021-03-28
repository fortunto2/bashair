import json
from pprint import pprint

from fastapi.testclient import TestClient

from config.asgi import fastapp

client = TestClient(fastapp)

with open('tests/data/warning.json') as json_file:
    data = json.load(json_file)

r_data = {'check_id': '074564c2b875a000',
          'check_name': 'PM2.5 warning',
          'level': 'crit',
          'node': 'esp8266-6504878',
          'pm25': 10.2,
          'start': '2021-03-24T19:13:55+00:00',
          'stop': '2021-03-24T19:14:05+00:00',
          'time': '2021-03-24T19:14:05+00:00'}


def test_api_warning():
    response = client.post("/influx/notify", json=data)
    pprint(response.json())
    assert response.status_code == 200
    assert response.json() == r_data
