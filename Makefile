.PHONY: help

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
.DEFAULT_GOAL := help

%:
	@:

prod = `arg="$(filter-out $@,$(MAKECMDGOALS))" && echo $${arg:-${1}}`


import: ## Импортим в базу данные из Madavi
	@docker-compose run --rm fastapi python backup/madavi/import_all.py
# MAIN

