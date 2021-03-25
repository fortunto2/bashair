import json
from pprint import pprint

import requests

with open('tests/data/warning.json') as json_file:
    data = json.load(json_file)

r = requests.post("http://api.localhost/notify", json=data)
pprint(r.json())
