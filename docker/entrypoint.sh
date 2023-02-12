#!/bin/bash

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $DATABASE_HOST $DATABASE_PORT; do
      sleep 0.1
    done
fi

poetry run python3 manage.py check
poetry run python3 manage.py compilemessages

exec "$@"
