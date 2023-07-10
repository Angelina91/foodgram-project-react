cd foodgram_progect || exit
python3 manage.py migrate;
python3 manage.py collectstatic --noinput;
gunicorn -b 0:8000 foodgram_progect.wsgi.py;