import json
from pprint import pprint
import sys
sys.path.append('.')

from back.schemas.node import NodePointGet, ListNodes
from fastapi.testclient import TestClient
from config.asgi import fastapp
client = TestClient(fastapp)


def test_node():
    response = client.get("/node/1")
    assert response.status_code == 200
    schema = NodePointGet(**response.json())
    pprint(schema)
    assert schema


def test_node_history():
    response = client.get("/node/1/history")
    assert response.status_code == 200


def test_node_all():
    response = client.get("/node/all")
    assert response.status_code == 200

    for node in response.json():
        schema = NodePointGet(**node)
        assert schema
