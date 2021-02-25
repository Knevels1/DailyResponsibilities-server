#!/bin/bash
rm -rf DailyTaskapi/migrations
rm db.sqlite3
python manage.py migrate
python manage.py makemigrations DailyTaskapi
python manage.py migrate DailyTaskapi
python manage.py loaddata users
python manage.py loaddata tokens
python manage.py loaddata my_user
python manage.py loaddata task