#!/bin/sh

if [ "$DATABASE" = "mysql" ]
then
    echo "Waiting for MySQL..."

    while ! nc -z mysql 3306; do
      sleep 0.1
    done

    echo "MySQL started"
fi

# python manage.py flush --no-input
python manage.py migrate

exec "$@"