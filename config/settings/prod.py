from .base import *
import django_heroku

DEBUG = True
ALLOWED_HOSTS = ['localhost','127.0.0.1','.herokuapp.com']

CELERY_BROKER_URL = os.environ.get('REDIS_URL')
CELERY_RESULT_BACKEND = os.environ.get('REDIS_URL')

# For test suites (ENV variables imported from travis-ci)
ZAIM_USER = os.environ.get('ZAIM_USER')
ZAIM_PASSWORD = os.environ.get('ZAIM_PASSWORD')

django_heroku.settings(locals())