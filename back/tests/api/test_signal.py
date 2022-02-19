from pprint import pprint
import sys
sys.path.append('')
from back.schemas.signal import SignalGet

from fastapi.testclient import TestClient
from config.asgi import fastapp
client = TestClient(fastapp)


def test_signal():
    response = client.get("/signal/count")
    assert response.status_code == 200

    response = client.get("/signal/10")
    assert response.status_code == 200
    pprint(response.json())
    try:
        schema = SignalGet(**response.json())
        pprint(schema)
        assert schema
    except Exception as e:
        print(e)
        assert response.json()['text']
