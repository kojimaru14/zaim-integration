from celery import shared_task

import time
# タスクとして利用する関数の引数に直接クエリセットのオブジェクトを渡すことはできない
@shared_task
def add(x1, x2):
    time.sleep(30)
    y = x1 + x2
    print('処理完了', y, __file__)
    return y

'''
from selenium.webdriver import Chrome, ChromeOptions, Remote
@shared_task
def scrape():
    print("Test haha1234")

    options = ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    # pythonファイルと同じディレクトリにchromeriver.exeがある場合引数は空でOK
    driver = Chrome(executable_path='/usr/local/bin/chromedriver', options=options)

    driver.get('https://point.rakuten.co.jp/history/?l-id=point_top_history_pc')
    
'''
from .zaim import ZaimCrawler
@shared_task
def scrape(username, password):
  # Chrome Driverの起動とZaimへのログイン、ログインには少し時間がかかります
  crawler = ZaimCrawler(username, password,
                        driver_path='/usr/local/bin/chromedriver',
                        poor=True)

  try:
    # データの取得 (データの取得には少し時間がかかります、時間はデータ件数による)
    data = crawler.get_data('2021', '11', progress=True) # progressをFalseにするとプログレスバーを非表示にできる
  except Exception as e:
    print(e)
    crawler.close()
    return 
  
  for el in data:
    # {'id': '5419217736', 'count': '常に含める', 'date': datetime.datetime(2021, 11, 3, 0, 0), 'category': '税金', 'genre': '住民税', 'amount': 7000, 'from_account': 'PayPay', 'type': 'payment', 'place': 'さとふる', 'name': 'レーズンサンド3…', 'comment': ''}
    print(el)

  # 終了処理
  crawler.close()
  return