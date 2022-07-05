#! /usr/bin/env sh

set -e

./manage.py makemigrations
./manage.py migrate
./manage.py collectstatic --noinput
gunicorn -b unix:/home/tigerfunk/tigerfunk.tk/tigerfunk/gunicorn.sock tigerfunk.wsgi:application
