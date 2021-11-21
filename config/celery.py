# https://devcenter.heroku.com/articles/celery-heroku
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# DJANGO_SETTINGS_MODULE is defined in 
# - docker-compose.yml for dev
# - start.sh for prod
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.dev')

app = Celery('config')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()