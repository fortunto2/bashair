import json
from pprint import pprint

from fastapi.testclient import TestClient

from main import app

client = TestClient(app)

with open('tests/data/measurement.json') as json_file:
    data = json.load(json_file)

r_data = {'aqi': 16.0,
          'aqi_category': 'Good',
          'humidity': 23.77,
          'max_micro': 20370,
          'min_micro': 27,
          'pm10': 6.35,
          'pm25': 3.83,
          'pressure': 99505.19,
          'samples': 1039137,
          'signal': -50.0,
          'temperature': 26.43}


def test_api_warning():
    response = client.post("/upload_measurement", json=data)
    pprint(response.json())
    assert response.status_code == 200
    assert response.json() == r_data
