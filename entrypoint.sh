#!/bin/sh

if [ "$DATABASE" = "mysql" ]
then
    echo "Waiting for MySQL..."

    while ! nc -z mysql 3306; do
      sleep 0.1
    done

    echo "MySQL started"
fi

cd src &&
python manage.py clearsessions &&
python manage.py collectstatic --noinput &&
python manage.py migrate --noinput

echo "$@"
exec "$@"
