@echo off
call python3 ./keygen.py
::docker compose down
docker compose up --build --no-start
docker compose rm app -f
docker compose run --rm app
docker compose stop db
pause