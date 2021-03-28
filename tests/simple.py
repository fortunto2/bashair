import json
from pprint import pprint

import requests

with open('tests/data/warning.json') as json_file:
    data = json.load(json_file)

r = requests.post("http://localhost:8000/sensor/push", json=data)
pprint(r.json())
