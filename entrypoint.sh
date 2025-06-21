#!/bin/bash
python manage.py collectstatic --noinput
python manage.py migrate
exec gunicorn ticketbooking.wsgi:application
