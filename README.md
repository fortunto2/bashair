# bashair
Air Monitoring for Bashkiria


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


design:

* https://airly.org/map/en/

used:

* https://github.com/leoncvlt/loconotion - Landing from Notion.so



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
