from .base import * # base.pyを読み込む 

# 開発、本番で分けたい設定を記載
DEBUG = True
ALLOWED_HOSTS = ['localhost','127.0.0.1','.herokuapp.com']

CELERY_BROKER_URL = 'redis://redis:6379'
CELERY_RESULT_BACKEND = 'redis://redis:6379'

if os.getenv("DB") == "postgres":
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'postgres',
            'USER': 'postgres',
            'PASSWORD': 'postgres',
            'HOST': 'db',
            'PORT': 5432,
        }
    }

try:
    from .local_settings import *
except ImportError:
    pass