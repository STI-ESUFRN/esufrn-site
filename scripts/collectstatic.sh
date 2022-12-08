#!/bin/sh

docker compose -f docker-compose.yml -f dev.docker-compose.yml exec web ./manage.py collectstatic --noinput