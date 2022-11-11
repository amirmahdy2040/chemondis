#!/usr/bin/env bash

while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
    sleep 1
done

./manage.py collectstatic --noinput
./manage.py migrate
./manage.py loaddata app/fixture/*.json

exec "$@"
