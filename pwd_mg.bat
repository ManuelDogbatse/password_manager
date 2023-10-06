@echo off
docker compose build
docker compose run --rm app
docker compose stop