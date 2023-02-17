#!/bin/sh

set -e
poetry run python3 manage.py migrate
poetry run python3 manage.py collectstatic --noinput

export DJANGO_SETTINGS_MODULE=esufrn.settings

poetry run gunicorn -b 0.0.0.0 -p 8000 --worker-class=gevent --worker-connections=32 --workers=4 esufrn.wsgi:application
