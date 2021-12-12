from .base import *
import django_heroku

DEBUG = False
ALLOWED_HOSTS = ['localhost','127.0.0.1','.herokuapp.com']

CELERY_BROKER_URL = os.environ.get('REDIS_URL')
CELERY_RESULT_BACKEND = os.environ.get('REDIS_URL')

if( os.environ.get('DATABASE_URL') ): # If DATABASE_URL is defined, use it. If not, the default sqlite is used (which is the case when test is run via TravisCI)
  import dj_database_url
  DATABASES['default'] = dj_database_url.config(conn_max_age=600)

# For test suites (ENV variables imported from travis-ci)
ZAIM_USER = os.environ.get('ZAIM_USER')
ZAIM_PASSWORD = os.environ.get('ZAIM_PASSWORD')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    # ログ出力フォーマットの設定
    'formatters': {
        'production': {
            'format': '%(asctime)s [%(levelname)s] %(process)d %(thread)d '
                      '%(pathname)s:%(lineno)d %(message)s'
        },
    },
    # ハンドラの設定
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, "logs", "django.log"),
            'formatter': 'production',
        },
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'production',
        },
    },
    # ロガーの設定
    'loggers': {
        # 自分で追加したアプリケーション全般のログを拾うロガー
        '': {
            'handlers': ['console','file'],
            'level': 'INFO',
            'propagate': False,
        },
        # Django自身が出力するログ全般を拾うロガー
        'django': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

django_heroku.settings(locals())