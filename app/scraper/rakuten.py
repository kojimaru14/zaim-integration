from selenium.webdriver import Chrome, ChromeOptions
import chromedriver_binary
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import pandas as pd
import time

# Ref: https://massu-keiei.com/python_automation_rakuten_point/

import logging
logger = logging.getLogger(__name__)

MAX_RETRY = 3
RAKUTEN_POINT_URL = "https://point.rakuten.co.jp/history/"

class RakutenCrawler:
    def __init__(self, user_id, password, driver_path):
        options = ChromeOptions()
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--remote-debugging-port=9222")
        options.add_argument("--headless")

        if driver_path is not None:
            self.driver = Chrome(executable_path=driver_path, options=options)
        else:
            self.driver = Chrome(options=options)

        if self.login(user_id, password):
            print("Login succeeded.")
            self.data = []
            self.current = 0
        else:
            self.close()
            raise RakutenCrawlerException("Login failed for unknown reason.")

    def login(self, user_id, password):
        retry = 1
        print("Start Chrome Driver.")
        self.driver.get(RAKUTEN_POINT_URL)
        while( retry <= MAX_RETRY ):
            time.sleep(1 * retry)
            print("Logging into Rakuten. Attempt #{}".format(retry))
            try:
                self.driver.find_element_by_id("loginInner_u").send_keys(user_id)
                self.driver.find_element_by_id("loginInner_p").send_keys(password, Keys.ENTER)
                time.sleep(1 * retry)
                if len(self.driver.find_elements_by_id("point_information")) > 0: # if "point_information" element exists, then login would have succeeded
                # if len(self.driver.find_elements_by_xpath("//*[starts-with(@class, 'point_num')]")) > 0: # if "point_num" element exists, then login would have succeeded
                    print("Successfully logged in as {}".format(user_id))
                    return True
                elif len(self.driver.find_elements_by_id("loginInner_u")) > 0: # if login form is still displayed after entering user credentials, then login would have failed due to incorrect user/password
                    self.close()
                    raise RakutenCrawlerException("Failed to log in as '{}'. Check your user and/or password".format(user_id))
                else:
                    logger.warning("It's unclear whether login succeeded or failed.")
                    self.driver.get(RAKUTEN_POINT_URL)
            except NoSuchElementException as e: # if "loginInner_u" and "loginInner_p" are not found, maybe the page is taking long to load, so we wait and try again
                logger.warning("NoSuchElementException with attempt #{}".format(retry), e)
            retry += 1
        return False

    def close(self):
        self.driver.close()

    def get_point_history(self, year, month):

        # 表示ページの定義
        page = 1
        confirm_page = 'NEXT'
        
        # リストを作成
        columns = ['date', 'service', 'detail', 'rankup', 'action', 'point', 'note']
        
        # 配列名を指定する
        df = pd.DataFrame(columns=columns)
        count = 1

        # 実行
        try:
            while(str(confirm_page) == 'NEXT'):
                    
                if count > 1 :
                    self.driver.get(url)         

                print(str(page) + "ページを取得中．．．")

                # ポイントの獲得情報を取得            
                posts = self.driver.find_elements_by_css_selector('.get')

                for post in posts:
                    # 日付
                    date = post.find_element_by_css_selector('td.detail .date').text
                    date = date.replace("[", "")
                    date = date.replace("]", "")

                    service = post.find_element_by_css_selector('.service a').text

                    detail = post.find_element_by_css_selector('td.detail').text

                    try:                      
                        rankup = post.find_element_by_css_selector('.label-rankup').text
                    
                    except:
                        rankup = 0

                    action = post.find_element_by_css_selector('.action').text
                    
                    point = post.find_element_by_css_selector('.point').text
                    point = point.replace(',','')


                    note = post.find_element_by_css_selector('.note').text
            
                    # スクレイピングした情報をリストに追加
                    se = pd.Series([date, service, detail, rankup, action, point, note], columns)
                    df = df.append(se, columns)
                
                # ポイントの利用情報を取得
                posts = self.driver.find_elements_by_css_selector('.use')

                for post in posts:
                    # 日付
                    date = post.find_element_by_css_selector('td.detail .date').text
                    date = date.replace("[", "")
                    date = date.replace("]", "")
                    
                    # サービス
                    service = post.find_element_by_css_selector('.service a').text
                    market = 0

                    # else :
                    detail = post.find_element_by_css_selector('td.detail').text
                    product = ''
    
                    # ランクアップ
                    try:                      
                        rankup = post.find_element_by_css_selector('.label-rankup').text
                    
                    except:
                        rankup = 0

                    # アクション
                    action = post.find_element_by_css_selector('.action').text
                    
                    # ポイント
                    point = post.find_element_by_css_selector('.point').text
                    point = int(point.replace(',','')) * -1
                        
                    # 備考
                    note = post.find_element_by_css_selector('.note').text 
            
                    # スクレイピングした情報をリストに追加
                    se = pd.Series([date, service, detail, rankup, action, point, note], columns)
                    df = df.append(se, columns)
                    
                # ページ数を1増やす
                page += 1
                # 次のページに進むためのURLを取得
                confirm_page = self.driver.find_element_by_css_selector("ul.pagination li:last-child a").text
                url = self.driver.find_element_by_css_selector("ul.pagination li:last-child a").get_attribute("href")
            
                count += 1
                print('次のページを開いています・・・')
                time.sleep(3)

        
        except:
            print("最終ページです")
            self.driver.close()

        # 最後に得たデータをCSVにして保存
        filename = "rakuten_point.csv"
        # csv形式で出力
        df.to_csv(filename, encoding="utf-8-sig")
        print("終了しました！！")
        return 1


class RakutenCrawlerException(Exception):
    def __init__(self, message=''):
        self.message = 'RakutenCrawlerException: {0}'.format(message)
        logger.exception(self.message)

    def __str__(self):
       return self.message