from .base import *
import django_heroku

DEBUG = False
ALLOWED_HOSTS = ['localhost','127.0.0.1','.herokuapp.com']

CELERY_BROKER_URL = os.environ.get('REDIS_URL')
CELERY_RESULT_BACKEND = os.environ.get('REDIS_URL')

django_heroku.settings(locals())