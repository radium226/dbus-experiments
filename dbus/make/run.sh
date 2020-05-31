#!/bin/bash

main()
{
    sudo DISPLAY="${DISPLAY}" UID="$( id -u )" GID="$( id -g )" docker-compose up --force-recreate --remove-orphans
}

main "${@}"