import json
from pprint import pprint
import sys


sys.path.append('..')
sys.path.append('.')

from back.schemas.nmu import NmuBase
from back.schemas.instance import InstanceGet
from back.schemas.signal import SignalGet
from back.schemas.community import CommunityGet
from back.schemas.node import NodePointGet
from back.schemas.city import CityGet

from fastapi.testclient import TestClient
from config.asgi import fastapp
client = TestClient(fastapp)


def test_nmu():
    response = client.get("/nmu")
    assert response.status_code == 200
    schema = NmuBase(**response.json())
    pprint(schema)
    assert schema


def test_instance():
    response = client.get("/instance/1")
    assert response.status_code == 200
    schema = InstanceGet(**response.json())
    pprint(schema)
    assert schema


def test_signal():
    response = client.get("/signal/count/")
    assert response.status_code == 200

    response = client.get("/signal/10/")
    assert response.status_code == 200
    pprint(response.json())
    try:
        schema = SignalGet(**response.json())
        pprint(schema)
        assert schema
    except Exception as e:
        print(e)
        assert response.json()['text']


def test_community():
    response = client.get("/community/1")
    assert response.status_code == 200
    schema = CommunityGet(**response.json())
    pprint(schema)
    assert schema


def test_node():
    response = client.get("/node/1/")
    assert response.status_code == 200
    schema = NodePointGet(**response.json())
    pprint(schema)
    assert schema

    response = client.get("/node/1/history/")
    assert response.status_code == 200


def test_city():
    response = client.get("/city/all")
    assert response.status_code == 200

    city_id = response.json()[0]['id']
    assert city_id

    response = client.get(f"/city/{city_id}/total/")
    assert response.status_code == 200

    schema = CityGet(**response.json())
    pprint(schema)
    assert schema



