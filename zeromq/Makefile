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