import json
from pprint import pprint

import requests

with open('tests/data/measurement.json') as json_file:
    data = json.load(json_file)

    # print(data)

r = requests.post("http://localhost:8000/upload_measurement", json=data)
pprint(r.json())
