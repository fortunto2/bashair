import json
from pprint import pprint

from fastapi.testclient import TestClient

from main import app

client = TestClient(app)

with open('tests/data/warning.json') as json_file:
    data = json.load(json_file)

r_data = {'aqi': None,
          'aqi_category': None,
          'humidity': None,
          'node': 'esp8266-6504878',
          'pm10': None,
          'pm25': 10.2,
          'pressure': None,
          'temperature': None}


def test_api_warning():
    response = client.post("/notify", json=data)
    pprint(response.json())
    assert response.status_code == 200
    assert response.json() == r_data
