#!/bin/bash
cd foodgram_progect || exit
python manage.py migrate
python manage.py collectstatic --noinput
gunicorn -b 0:8000 foodgram_progect.wsgi