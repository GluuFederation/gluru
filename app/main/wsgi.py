"""
WSGI config for gluu project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/
"""

import os, sys

from dotenv import load_dotenv

sys.path.append('app')
load_dotenv(os.path.join(os.path.dirname(__file__), '../../.env'))

os.environ['REDISCLOUD_CACHE'] = 'redis://localhost:6379'
os.environ['REDISCLOUD_URL'] = 'redis://localhost:6379/0'

sys.path.append('Your system path will go here')


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "main.settings")

from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()
