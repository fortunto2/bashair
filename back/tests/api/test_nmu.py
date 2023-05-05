from pprint import pprint
import sys
sys.path.append('')

from back.schemas.nmu import NmuBase
from fastapi.testclient import TestClient
from config.asgi import fastapp
client = TestClient(fastapp)


def test_nmu():
    response = client.get("/nmu")
    assert response.status_code == 200
    schema = NmuBase(**response.json())
    pprint(schema)
    assert schema

