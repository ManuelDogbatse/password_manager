@echo off
call python3 ./keygen.py
docker compose up --build --no-recreate --no-start
::docker compose up --build --force-recreate --no-start
docker compose rm app -f
docker compose run --rm app
docker compose stop db