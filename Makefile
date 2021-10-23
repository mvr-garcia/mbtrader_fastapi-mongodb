ENVIRONMENT_VARIABLES=$(shell grep -v '^\#' .env | xargs)

envvars:
	@echo "export ${ENVIRONMENT_VARIABLES}"

start-local:
	python main.py

build:
	docker-compose up -d --build

start:
	docker-compose up -d

logs:
	docker logs trader-mv