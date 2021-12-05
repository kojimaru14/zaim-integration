from .base import *
import django_heroku

DEBUG = True
ALLOWED_HOSTS = ['localhost','127.0.0.1','.herokuapp.com']

CELERY_BROKER_URL = os.environ.get('REDIS_URL')
CELERY_RESULT_BACKEND = os.environ.get('REDIS_URL')

if( os.getenv('DATABASE_URL') ): # If DATABASE_URL is defined, use it. If not, the default sqlite is used (which is the case when test is run via TravisCI)
  import dj_database_url
  DATABASES['default'] = dj_database_url.config(conn_max_age=600)

# For test suites (ENV variables imported from travis-ci)
ZAIM_USER = os.environ.get('ZAIM_USER')
ZAIM_PASSWORD = os.environ.get('ZAIM_PASSWORD')

django_heroku.settings(locals())