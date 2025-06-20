"""
WSGI config for ticketbooking project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

# Usa settings_production se siamo su Railway
if os.environ.get('RAILWAY_ENVIRONMENT'):
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ticketbooking.settings_production')
else:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ticketbooking.settings')

application = get_wsgi_application()