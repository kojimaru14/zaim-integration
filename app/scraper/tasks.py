from celery import shared_task

import logging
logger = logging.getLogger(__name__)

import time
@shared_task
def add(x1, x2):
    time.sleep(10)
    y = x1 + x2
    print('処理完了', y, __file__)
    return y


from .google import upload_to_google
import csv
@shared_task
# Output: 1 if succeed, 0 if failed
def scrape_and_upload(username, password, year, month):

  file_name = '{}-{}.csv'.format(year, month)

  try:
    data = scrape(username, password, year, month)
    to_csv = list(data)
  except Exception as e:
    logger.error("Zaim login exception", e)
    return 0
  
  try:
    with open(file_name, 'w', encoding='utf8', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, to_csv[0].keys())
        dict_writer.writeheader()
        dict_writer.writerows(to_csv)
  except Exception as e:
    logger.error("CSV write exception", e)
    return 0

  try:
    upload_to_google(file_name, "text/csv", file_name, ['1yhw2cEo5nQ7Ym3oZ3mNIpCMuA6qmiwGB'])
  except Exception as e:
    logger.error("GDrive upload exception", e)
    return 0

  return 1

from .zaim import ZaimCrawler
from selenium.common.exceptions import WebDriverException
# Output: list_reverseiterator or exception
def scrape(username, password, year, month):
  
  try:
    crawler = ZaimCrawler(username, password,
                          driver_path='/usr/local/bin/chromedriver',
                          poor=True)
  except WebDriverException:
    import chromedriver_binary
    crawler = ZaimCrawler(username, password,
                          poor=True)

  # データの取得 (データの取得には少し時間がかかります、時間はデータ件数による)
  data = crawler.get_data(year, month, progress=True) # progressをFalseにするとプログレスバーを非表示にできる
 
   # 終了処理
  crawler.close()
  
  return data

from .google import upload_to_google
def upload_file(file_path, mimetype, new_name, parent_ids):
  upload_to_google(file_path, mimetype, new_name, parent_ids)
  return True
