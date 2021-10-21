ENVIRONMENT_VARIABLES=$(shell grep -v '^\#' .env | xargs)

envvars:
	@echo "export ${ENVIRONMENT_VARIABLES}"

start:
	python main.py