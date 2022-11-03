#!/bin/sh

if [ "$DATABASE" = "mysql" ]
then
    echo "Waiting for MySQL..."

    while ! nc -z mysql 3306; do
      sleep 0.1
    done

    echo "MySQL started"
fi

python manage.py migrate --noinput &&
python manage.py collectstatic --noinput &&
python manage.py clearsessions

echo "$@"
exec "$@"
