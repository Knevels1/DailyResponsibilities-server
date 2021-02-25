#!/bin/bash
rm -rf DailyTaskapi/migrations
rm db.sqlite3
python manage.py migrate
python manage.py makemigrations DailyTaskApi
python manage.py migrate DailyTaskApi
python manage.py loaddata users
python manage.py loaddata tokens
python manage.py loaddata task_users
python manage.py loaddata task