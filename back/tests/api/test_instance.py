from pprint import pprint
import sys
sys.path.append('')

from back.schemas.instance import InstanceGet

from fastapi.testclient import TestClient
from config.asgi import fastapp
client = TestClient(fastapp)


def test_instance():
    response = client.get("/instance/1")
    assert response.status_code == 200
    schema = InstanceGet(**response.json())
    pprint(schema)
    assert schema

