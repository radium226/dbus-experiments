#!/usr/bin/make -f

SHELL = /bin/bash
.SHELLFLAGS = -o pipefail -e -c
.ONESHELL:

.PHONY: stream
stream:
	poetry run streaming stream "./ocean.mp4" "1920x1012"

.PHONY: play
play:
	poetry run streaming play "1920x1012"

run:
	xhost local:root
	sudo DISPLAY=${DISPLAY} UID="$(shell id -u)" GID="$(shell id -g)" \
        docker-compose up \
			--build \
			--force-recreate \
			--remove-orphans

.PHONY: start-redis
start-redis:
	sudo DISPLAY=${DISPLAY} UID="$(shell id -u)" GID="$(shell id -g)" \
		docker-compose down && \
	sudo DISPLAY=${DISPLAY} UID="$(shell id -u)" GID="$(shell id -g)" \
        docker-compose up \
			--build \
			--force-recreate \
			--remove-orphans  \
			--no-start
	sudo docker-compose start "redis"
	sudo docker-compose logs -f "redis"

.PHONY: redis-cli
redis-cli:
	sudo docker-compose exec "redis" redis-cli