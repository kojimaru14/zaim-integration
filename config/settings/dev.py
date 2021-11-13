from .base import * # base.pyを読み込む 

# 開発、本番で分けたい設定を記載
DEBUG = True
ALLOWED_HOSTS = ['localhost','127.0.0.1','.herokuapp.com']

try:
    from .local_settings import *
except ImportError:
    pass