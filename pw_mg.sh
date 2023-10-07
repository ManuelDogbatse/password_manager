#! /bin/bash
docker compose up --build --no-recreate --no-start
docker compose run --rm app
docker compose stop