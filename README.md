# bashair
Air Monitoring for Bashkiria


## Inspired

* https://github.com/stefanthoss/air-quality-influxdb-bridge
* https://github.com/leoncvlt/loconotion


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
