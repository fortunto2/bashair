from pprint import pprint
import sys

sys.path.append('')

from back.schemas.city import CityGet, CityTotalGet

from fastapi.testclient import TestClient
from config.asgi import fastapp
client = TestClient(fastapp)


def test_city_all():
    response = client.get("/city/all")
    assert response.status_code == 200

    city_id = response.json()[0]['id']
    assert city_id


def test_city_total():

    response = client.get(f"/city/1/total")
    assert response.status_code == 200

    schema = CityTotalGet(**response.json())
    pprint(schema)
    assert schema

