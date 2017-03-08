#!/usr/bin/env bash
# rebuild_db.sh

python manage.py rebuild_db

rm -fr migrations

python manage.py db init

python manage.py db migrate

python manage.py db upgrade