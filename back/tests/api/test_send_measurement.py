import json
from pprint import pprint
import sys

from back.schemas.sensors import SensorMeasurement

sys.path.append('../../..')
sys.path.append('')


from fastapi.testclient import TestClient

from config.asgi import fastapp

client = TestClient(fastapp)

with open('back/tests/api/data/measurement.json') as json_file:
    data = json.load(json_file)
    print(data)

with open('back/tests/api/data/measurement_bad.json') as json_file:
    data_bad = json.load(json_file)
    print(data_bad)

r_data = {'aqi': 16.0,
          # 'aqi_category': 'Good',
          'humidity': 23.77,
          'max_micro': 20370,
          'min_micro': 27,
          'pm10': 6.35,
          'pm25': 3.83,
          'pressure': 99505.19,
          'samples': 1039137,
          'signal': -50.0,
          'temperature': 26.43,
          }


def test_api_measurement():
    response = client.post("/upload_measurement", json=data)
    pprint(response.json())
    assert response.status_code == 200
    # assert response.json() == r_data
    assert response.json()['result'] == True
    fields = SensorMeasurement(**response.json()['fields'])
    pprint(fields)


def test_bad_2sensor():
    response = client.post("/upload_measurement", json=data_bad)
    pprint(response.status_code)
    assert response.json()['result'] == True


def test_bad_temperature():
    data['sensordatavalues'][2]['value'] = '-100'
    pprint(data)
    response = client.post("/upload_measurement", json=data)
    pprint(response.status_code)
    assert response.json()['result'] == True


def test_bad_sensor_api_measurement():
    "этот тест запускать последним, затирает глобальный data"
    data['esp8266id'] = 'xxxx'
    response = client.post("/upload_measurement", json=data)
    pprint(response.status_code)
    assert response.json()['result'] == False

