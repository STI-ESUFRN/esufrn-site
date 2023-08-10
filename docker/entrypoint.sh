#!/bin/bash

echo "Starting the application..."
until poetry run python3 manage.py check; do
    sleep 1
done

poetry run python3 manage.py compilemessages

exec "$@"
