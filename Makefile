#!/usr/bin/make -f

SHELL = /bin/bash
.SHELLFLAGS = -o pipefail -e -c
.ONESHELL:

build:
	sudo DISPLAY=${DISPLAY} UID="$(shell id -u)" GID="$(shell id -g)" docker-compose build

run:
	xhost local:root
	sudo DISPLAY=${DISPLAY} UID="$(shell id -u)" GID="$(shell id -g)" \
        docker-compose up \
			--force-recreate \
			--remove-orphans 
			--no-start
	sudo docker-compose start "player" "broker"
	sudo docker-compose logs -f

image-shell:
	sudo docker run --rm -it "python:3.8-alpine3.11" sh

.PHONY: clean
clean:
	sudo docker-compose down