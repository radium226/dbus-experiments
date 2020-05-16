#!/usr/bin/make -f

SHELL = /bin/bash
.SHELLFLAGS = -o pipefail -e -c
.ONESHELL:

build:
	sudo UID="$(shell id -u)" GID="$(shell id -g)" docker-compose build

run:
	sudo DISPLAY="${DISPLAY}" UID="$(shell id -u)" GID="$(shell id -g)" docker-compose up --force-recreate --remove-orphans

image-shell:
	sudo docker run --rm -it "python:3.8-alpine3.11" sh

.PHONY: clean
clean:
	true