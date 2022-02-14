from pprint import pprint
import sys
sys.path.append('.')

from back.schemas.node import NodePointGet
from fastapi.testclient import TestClient
from config.asgi import fastapp
client = TestClient(fastapp)


def test_node():
    response = client.get("/node/1/")
    assert response.status_code == 200
    schema = NodePointGet(**response.json())
    pprint(schema)
    assert schema

    response = client.get("/node/1/history/")
    assert response.status_code == 200
