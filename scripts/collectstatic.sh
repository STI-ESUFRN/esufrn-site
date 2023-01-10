#!/bin/sh

docker compose exec web ./manage.py collectstatic --noinput