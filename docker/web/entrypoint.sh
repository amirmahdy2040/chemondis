#!/usr/bin/env bash

while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
    sleep 1
done

python manage.py collectstatic --noinput
python manage.py migrate
python manage.py loaddata app/fixture/*.json

exec "$@"
