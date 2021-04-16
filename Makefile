.PHONY: help

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
.DEFAULT_GOAL := help

%:
	@:

prod = `arg="$(filter-out $@,$(MAKECMDGOALS))" && echo $${arg:-${1}}`


generate: ## Билдим статичный сайт из Notion
	@docker-compose up notion

reg: ## Отсылаем на сервер Reg.ru (bashair.ru)
# 	@scp -r dist/life2film/bashair/* reg:www/bashair.ru
	@rsync -a -e ssh --stats --progress dist/bashair/* reg:www/bashair.ru

gcloud: ## Отсылаем на сервер gcloud life
	@gsutil cp -r dist/* gs://bashair_ru

import: ## Импортим в базу данные из Madavi
	@docker-compose run --rm fastapi python backup/madavi/import_all.py
# MAIN

# Быстрая команда: сбилдить и залить на сервер
up: generate reg
d: up
