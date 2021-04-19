# BashAir

Civil Air Monitoring for Honest People from TERRA BASHKIRIA


## Backend dirs Structure

* adapters: The adapters to retrieve Django ORMs
* api: FastAPI routers
* models: Django ORM
* schemas: FastAPI Pydantic models
* timeseries: InfluxDB retrieve


## Inspired

Mother project:

* https://github.com/opendata-stuttgart/feinstaub-map-v2
* https://github.com/opendata-stuttgart/feinstaub-api

Code:

* https://github.com/stefanthoss/air-quality-influxdb-bridge
* https://github.com/MarcFinns/AtmoScan
  
data:

* https://github.com/ReagentX/purple_air_api
* https://www.kaggle.com/c/dsg-hackathon/data
* https://www.kaggle.com/epa/epa-historical-air-quality
* https://www.kaggle.com/shrutibhargava94/india-air-quality-data

* https://openaq.org
* https://openaq.medium.com/how-can-a-government-source-add-data-to-openaq-50b5d83ef13f
* https://docs.openaq.org/ - api
* https://github.com/openaq/openaq-fetch/issues?q=is%3Aissue+is%3Aopen+label%3A%22new+data%22

* https://nebo.live/docs/v2/index.html

design:

* https://airly.org/map/en/

used:

* https://github.com/leoncvlt/loconotion - Landing from Notion.so


Django+Fastapi:

* https://www.stavros.io/posts/fastapi-with-django/
* https://github.com/kigawas/fastapi-django

* Timeseries:
* https://github.com/schlunsen/django-timescaledb

GEO:
* https://docs.djangoproject.com/en/3.1/ref/contrib/gis/
* https://raphael-leger.medium.com/django-handle-latitude-and-longitude-54a4bb2f6e3b
* https://github.com/developmentseed/geojson-pydantic

ActivityPub - create AIR federatioin servers:
* https://en.wikipedia.org/wiki/ActivityPub
* https://github.com/rowanlupton/pylodon

Hardware:
* https://github.com/letscontrolit/ESPEasy


### install 

Ubuntu server

```shell
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker ${USER}
newgrp docker

sudo curl -L "https://github.com/docker/compose/releases/download/1.28.5/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

sudo apt-get install rsync

sudo chown 472:472 .docker/grafana
```

add crontab -e
```shell
* * * * * /usr/bin/rsync -a -e ssh /home/rustam/bashair/dist/bashair/* reg:www/bashair.ru
```

## Pydantic models

* Telegram https://github.com/devtud/pygramtic/blob/master/pygramtic/models.py


### TODO

```shell
Adsbexchange.com
GeoNames.org
Google.com
Mylnikov.org
Timezonedb.com
Wunderground.com
```

## Preasure

From BME280

Prel = Pabs + h/8.3

Prel is relative pressure (recalculating to the sea level) [hPa]
Pabs is absolute pressure at the messurement place/site [hPa]
h is altitude (height above sea level) [m]
