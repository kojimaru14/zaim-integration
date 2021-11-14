from celery import shared_task

import time
# タスクとして利用する関数の引数に直接クエリセットのオブジェクトを渡すことはできない
@shared_task
def add(x1, x2):
    time.sleep(30)
    y = x1 + x2
    print('処理完了', y, __file__)
    return y