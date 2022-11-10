THIS_FILE := $(lastword $(MAKEFILE_LIST))
.PHONY: build start stop down restart

project_name = chemondis
compose_file = docker/docker-compose.yml

build:
	docker-compose -p $(project_name) -f $(compose_file) build

start:
	docker-compose -p $(project_name) -f $(compose_file) up -d

stop:
	docker-compose -p $(project_name) -f $(compose_file) stop

down:
	docker-compose -p $(project_name) -f $(compose_file) down

restart:
	docker-compose -p $(project_name) -f $(compose_file) build
	docker-compose -p $(project_name) -f $(compose_file) down
	docker-compose -p $(project_name) -f $(compose_file) up -d
