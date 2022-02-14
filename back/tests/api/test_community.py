from pprint import pprint
import sys

sys.path.append('')

from back.schemas.community import CommunityGet

from fastapi.testclient import TestClient
from config.asgi import fastapp
client = TestClient(fastapp)


def test_community():
    response = client.get("/community/1")
    assert response.status_code == 200
    schema = CommunityGet(**response.json())
    pprint(schema)
    assert schema
