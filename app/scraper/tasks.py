from celery import shared_task, current_task

import logging
logger = logging.getLogger(__name__)

import time
@shared_task
def add(x1, x2):
    time.sleep(10)
    y = x1 + x2
    print('処理完了', y, __file__)
    return y


from .services.google import upload_to_google
import pandas as pd
@shared_task
# Output: success message if succeed, raise Exception if failed
def scrape_and_upload(username, password, year, month):

  file_name = '{}-{}.csv'.format(year, month)
  folder_ids = ['1yhw2cEo5nQ7Ym3oZ3mNIpCMuA6qmiwGB']

  current_task.update_state(
    state="RUNNING",
    meta={"Step": "Fetching zaim data"}
  )
  data = scrape(username, password, year, month)
  
  current_task.update_state(
    state="RUNNING",
    meta={"Step": "Writing fetched data to CSV"}
  )
  try:
    df = pd.json_normalize(data['items'])
    df.to_csv(file_name, encoding='utf-8')
  except Exception as e:
    raise CsvWriteException("CSV write exception:" + str(e) )

  current_task.update_state(
    state="RUNNING",
    meta={"Step": "Uploading CSV to Google Drive"}
  )
  file_id = upload_to_google(file_name, "text/csv", file_name, folder_ids)

  return "{} (id: {}) has been uploaded to folder: {}".format(file_name, file_id, ' and '.join(folder_ids))

from .services.zaim import ZaimCrawler
from selenium.common.exceptions import WebDriverException
# Output: json data or exception
def scrape(username, password, year, month):
  
  try:
    crawler = ZaimCrawler(username, password,
                          driver_path='/usr/local/bin/chromedriver',
                          poor=True)
  except WebDriverException:
    import chromedriver_binary
    crawler = ZaimCrawler(username, password,
                          poor=True)

  data = crawler.get_json_data(year, month) 
  crawler.close()
  
  return data

from .services.google import upload_to_google
def upload_file(file_path, mimetype, new_name, parent_ids):
  file_id = upload_to_google(file_path, mimetype, new_name, parent_ids)
  return file_id

from .services.rakuten import RakutenCrawler
# Output: json data or exception
@shared_task
def scrape_rakuten(username, password, month, year):
  
  try:
    crawler = RakutenCrawler(username, password, driver_path='/usr/local/bin/chromedriver')
  except WebDriverException:
    crawler = RakutenCrawler(username, password)

  # data = crawler.get_point_history()
  data = crawler.get_point_history(month, year)
  crawler.close()
  
  return data
class TaskException(Exception):
    def __init__(self, message):
        self.message = message

    def log(self):
        logger.exception(self.message + ':')

class CsvWriteException(TaskException):
    def __init__(self):
        self.log()