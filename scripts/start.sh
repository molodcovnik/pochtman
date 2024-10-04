#!/bin/sh

cd Mail_Service/

python manage.py migrate

# collects all static files in our app and puts it in the STATIC_ROOT
python manage.py collectstatic --noinput


gunicorn --workers=1 --bind 0.0.0.0:8000 core.wsgi