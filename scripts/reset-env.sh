#!/bin/sh
rm -fr media
rm db.sqlite3
python manage.py migrate
