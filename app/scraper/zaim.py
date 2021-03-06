import os
import datetime
import time
import calendar
import requests, json

from requests_oauthlib import OAuth1Session
from selenium.webdriver import Chrome, ChromeOptions, Remote
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from tqdm import tqdm

import logging
logger = logging.getLogger(__name__)

# Entirely copied from https://github.com/MagicalLiebe/pyzaim/blob/master/pyzaim/pyzaim.py
# Credits to https://github.com/MagicalLiebe

request_token_url = "https://api.zaim.net/v2/auth/request"
authorize_url = "https://auth.zaim.net/users/auth"
access_token_url = "https://api.zaim.net/v2/auth/access"
callback_uri = "https://www.zaim.net/"
login_url = "https://auth.zaim.net/"

MAX_RETRY = 3

def get_access_token():
    consumer_id = input("Please input consumer ID : ")
    consumer_secret = input("Please input consumer secret : ")
    print("\n")

    auth = OAuth1Session(
        client_key=consumer_id, client_secret=consumer_secret, callback_uri=callback_uri
    )

    auth.fetch_request_token(request_token_url)

    # Redirect user to zaim for authorization
    authorization_url = auth.authorization_url(authorize_url)
    print("Please go here and authorize : ", authorization_url)

    oauth_verifier = input("Please input oauth verifier : ")
    access_token_res = auth.fetch_access_token(
        url=access_token_url, verifier=oauth_verifier
    )
    access_token = access_token_res.get("oauth_token")
    access_token_secret = access_token_res.get("oauth_token_secret")

    print("\n")
    print("access token : {}".format(access_token))
    print("access token secret : {}".format(access_token_secret))
    print("oauth verifier : {}".format(oauth_verifier))


class ZaimAPI:
    def __init__(
        self,
        consumer_id,
        consumer_secret,
        access_token,
        access_token_secret,
        oauth_verifier,
    ):
        self.consumer_id = consumer_id
        self.consumer_secret = consumer_secret

        self.verify_url = "https://api.zaim.net/v2/home/user/verify"
        self.money_url = "https://api.zaim.net/v2/home/money"
        self.payment_url = "https://api.zaim.net/v2/home/money/payment"
        self.income_url = "https://api.zaim.net/v2/home/money/income"
        self.transfer_url = "https://api.zaim.net/v2/home/money/transfer"
        self.category_url = "https://api.zaim.net/v2/home/category"
        self.genre_url = "https://api.zaim.net/v2/home/genre"
        self.account_url = "https://api.zaim.net/v2/home/account"
        self.currency_url = "https://api.zaim.net/v2/currency"

        self.auth = OAuth1Session(
            client_key=self.consumer_id,
            client_secret=self.consumer_secret,
            resource_owner_key=access_token,
            resource_owner_secret=access_token_secret,
            callback_uri=callback_uri,
            verifier=oauth_verifier,
        )

        self._build_id_table()

    def verify(self):
        return self.auth.get(self.verify_url).json()

    def get_data(self):
        return self.auth.get(self.money_url).json()["money"]

    def insert_payment_simple(
        self,
        date,
        amount,
        genre,
        from_account=None,
        comment=None,
        name=None,
        place=None,
    ):
        genre_id = self.genre_stoi[genre]
        category_id = self.genre_to_category[genre_id]
        if from_account is not None:
            from_account_id = self.account_stoi[from_account]
        else:
            from_account_id = None
        return self.insert_payment(
            date, amount, category_id, genre_id, from_account_id, comment, name, place
        )

    def insert_payment(
        self,
        date,
        amount,
        category_id,
        genre_id,
        from_account_id=None,
        comment=None,
        name=None,
        place=None,
    ):
        data = {
            "mapping": 1,
            "category_id": category_id,
            "genre_id": genre_id,
            "amount": amount,
            "date": date.strftime("%Y-%m-%d"),
        }
        if from_account_id is not None:
            data["from_account_id"] = from_account_id
        if comment is not None:
            data["comment"] = comment
        if name is not None:
            data["name"] = name
        if place is not None:
            data["place"] = place
        return self.auth.post(self.payment_url, data=data)

    def update_payment_simple(
        self,
        data_id,
        date,
        genre,
        amount,
        from_account=None,
        comment=None,
        name=None,
        place=None,
    ):
        genre_id = self.genre_stoi[genre]
        category_id = self.genre_to_category[genre_id]
        if from_account is not None:
            from_account_id = self.account_stoi[from_account]
        else:
            from_account_id = None
        return self.update_payment(
            data_id,
            date,
            amount,
            category_id,
            genre_id,
            from_account_id,
            comment,
            name,
            place,
        )

    def update_payment(
        self,
        data_id,
        date,
        amount,
        category_id,
        genre_id,
        from_account_id=None,
        comment=None,
        name=None,
        place=None,
    ):
        data = {
            "mapping": 1,
            "id": data_id,
            "category_id": category_id,
            "genre_id": genre_id,
            "amount": amount,
            "date": date.strftime("%Y-%m-%d"),
        }
        if from_account_id is not None:
            data["from_account_id"] = from_account_id
        if comment is not None:
            data["comment"] = comment
        if name is not None:
            data["name"] = name
        if place is not None:
            data["place"] = place
        return self.auth.put("{}/{}".format(self.payment_url, data_id), data=data)

    def delete_payment(self, data_id):
        return self.auth.delete("{}/{}".format(self.payment_url, data_id))

    def insert_income_simple(
        self, date, category, amount, to_account=None, comment=None, place=None
    ):
        category_id = self.category_stoi[category]
        if to_account is not None:
            to_account_id = self.account_stoi[to_account]
        else:
            to_account_id = None
        return self.insert_income(
            date, category_id, amount, to_account_id, comment, place
        )

    def insert_income(
        self, date, category_id, amount, to_account_id=None, comment=None, place=None
    ):
        data = {
            "mapping": 1,
            "category_id": category_id,
            "amount": amount,
            "date": date.strftime("%Y-%m-%d"),
        }
        if to_account_id is not None:
            data["to_account_id"] = to_account_id
        if comment is not None:
            data["comment"] = comment
        if place is not None:
            data["place"] = place
        return self.auth.post(self.income_url, data=data)

    def update_income_simple(
        self, data_id, date, category, amount, to_account=None, comment=None, place=None
    ):
        category_id = self.category_stoi[category]
        if to_account is not None:
            to_account_id = self.account_stoi[to_account]
        else:
            to_account_id = None
        return self.update_income(
            data_id, date, category_id, amount, to_account_id, comment, place
        )

    def update_income(
        self,
        data_id,
        date,
        category_id,
        amount,
        to_account_id=None,
        comment=None,
        place=None,
    ):
        data = {
            "mapping": 1,
            "id": data_id,
            "category_id": category_id,
            "amount": amount,
            "date": date.strftime("%Y-%m-%d"),
        }
        if to_account_id is not None:
            data["to_account_id"] = to_account_id
        if comment is not None:
            data["comment"] = comment
        if place is not None:
            data["place"] = place
        return self.auth.put("{}/{}".format(self.income_url, data_id), data=data)

    def delete_income(self, data_id):
        return self.auth.delete("{}/{}".format(self.income_url, data_id))

    def insert_transfer_simple(
        self, date, amount, from_account, to_account, comment=None
    ):
        from_account_id = self.account_stoi[from_account]
        to_account_id = self.account_stoi[to_account]
        return self.insert_transfer(
            date, amount, from_account_id, to_account_id, comment
        )

    def insert_transfer(
        self, date, amount, from_account_id, to_account_id, comment=None
    ):
        data = {
            "mapping": 1,
            "amount": amount,
            "date": date.strftime("%Y-%m-%d"),
            "from_account_id": from_account_id,
            "to_account_id": to_account_id,
        }
        if comment is not None:
            data["comment"] = comment
        return self.auth.post(self.transfer_url, data=data)

    def update_transfer_simple(
        self, data_id, date, amount, from_account, to_account, comment=None
    ):
        from_account_id = self.account_stoi[from_account]
        to_account_id = self.account_stoi[to_account]
        return self.update_transfer(
            data_id, date, amount, from_account_id, to_account_id, comment
        )

    def update_transfer(
        self, data_id, date, amount, from_account_id, to_account_id, comment=None
    ):
        data = {
            "mapping": 1,
            "id": data_id,
            "amount": amount,
            "date": date.strftime("%Y-%m-%d"),
            "from_account_id": from_account_id,
            "to_account_id": to_account_id,
        }
        if comment is not None:
            data["comment"] = comment
        return self.auth.put("{}/{}".format(self.transfer_url, data_id), data=data)

    def delete_transfer(self, data_id):
        return self.auth.delete("{}/{}".format(self.transfer_url, data_id))

    def _build_id_table(self):
        self.genre_itos = {}
        self.genre_stoi = {}
        self.genre_to_category = {}
        genre = self._get_genre()["genres"]
        for g in genre:
            self.genre_itos[g["id"]] = g["name"]
            self.genre_stoi[g["name"]] = g["id"]
            self.genre_to_category[g["id"]] = g["category_id"]
        self.category_itos = {}
        self.category_stoi = {}
        category = self._get_category()["categories"]
        for c in category:
            self.category_itos[c["id"]] = c["name"]
            self.category_stoi[c["name"]] = c["id"]
        self.account_stoi = {}
        self.account_itos = {}
        account = self._get_account()["accounts"]
        for a in account:
            self.account_itos[a["id"]] = a["name"]
            self.account_stoi[a["name"]] = a["id"]

    def _get_account(self):
        return self.auth.get(self.account_url).json()

    def _get_category(self):
        return self.auth.get(self.category_url).json()

    def _get_genre(self):
        return self.auth.get(self.genre_url).json()


class ZaimCrawler:
    def __init__(self, user_id, password, driver_path=None, headless=False, poor=False, gcf=False):
        options = ChromeOptions()

        if gcf:
            options.add_argument('--headless')
            options.add_argument('--disable-gpu')
            options.add_argument('--window-size=480x270')
            options.add_argument('--no-sandbox')
            options.add_argument('--hide-scrollbars')
            options.add_argument('--enable-logging')
            options.add_argument('--log-level=0')
            options.add_argument('--v=99')
            options.add_argument('--single-process')
            options.add_argument('--ignore-certificate-errors')

            options.binary_location = os.getcwd() + "/headless-chromium"
            self.driver = Chrome(
                os.getcwd() + "/chromedriver", options=options)
        else:
            if poor:
                options.add_argument("--disable-gpu")
                options.add_argument("--no-sandbox")
                options.add_argument("--disable-dev-shm-usage")
                options.add_argument("--remote-debugging-port=9222")
                options.add_argument("--headless")
            if headless:
                options.add_argument("--headless")
            if driver_path == 'remote':  # ??????????????????????????????docker-selenium?????????????????????
                self.driver = Remote(
                    command_executor='http://localhost:4444/wd/hub',
                    desired_capabilities=options.to_capabilities(),
                    options=options,
                )
            elif driver_path is not None:
                self.driver = Chrome(
                    executable_path=driver_path, options=options)
            else:
                self.driver = Chrome(options=options)
            if poor:
                self.driver.set_window_size(480, 270)

        if self.login(user_id, password):
            print("Login succeeded.")
            self.data = []
            self.current = 0
        else:
            self.close()
            raise ZaimCrawlerException("Login failed for unknown reason.")

    def login(self, user_id, password):
        retry = 1
        print("Start Chrome Driver.")
        self.driver.get(login_url)
        while( retry <= MAX_RETRY ):
            time.sleep(1 * retry)
            print("Logging into Zaim. Attempt #{}".format(retry))
            try:
                self.driver.find_element_by_id("UserEmail").send_keys(user_id)
                self.driver.find_element_by_id("UserPassword").send_keys(password, Keys.ENTER)
                time.sleep(1 * retry)
                if len(self.driver.find_elements_by_xpath("//*[starts-with(@class, 'nav-profile')]")) > 0: # if profile pic element exists, then login would have succeeded
                    print("Successfully logged in as {}".format(user_id))
                    return True
                elif len(self.driver.find_elements_by_id("UserLoginForm")) > 0: # if login form is still displayed after entering user credentials, then login would have failed due to incorrect user/password
                    self.close()
                    raise ZaimCrawlerException("Failed to log in as '{}'. Check your user and/or password".format(user_id))
                else:
                    logger.warning("It's unclear whether login succeeded or failed.")
                    self.driver.get(login_url)
            except NoSuchElementException as e: # if "UserEmail" and "UserPassword" are not found, maybe the page is taking long to load, so we wait and try again
                logger.warning("NoSuchElementException with attempt #{}".format(retry), e)
            retry += 1
        return False

    def get_json_data(self, year, month):
        year = str(year)
        month = str(month).zfill(2)
        print("Getting data of {}/{}.".format(year, month))

        session = requests.session()

        #??????????????????????????????
        for cookie in self.driver.get_cookies():
            session.cookies.set(cookie["name"], cookie["value"])

        result = session.get("https://zaim.net/money/details?month={}{}".format(year, month))
        data = json.loads(result.text)
        return data

    def get_data(self, year, month, progress=True):
        day_len = calendar.monthrange(int(year), int(month))[1]
        year = str(year)
        month = str(month).zfill(2)
        print("Get Data of {}/{}.".format(year, month))
        self.driver.get(
            "https://zaim.net/money?month={}{}".format(year, month))
        time.sleep(10)

        # ???????????????????????????????????????????????????????????????
        print("Found {} days in {}/{}.".format(day_len, year, month))
        self.current = day_len
        if progress:
            self.pbar = tqdm(total=day_len)

        # ?????????????????????????????????????????????????????????????????????????????????????????????????????????
        loop = True
        while loop:
            loop = self.crawler(year, progress)

        if progress:
            self.pbar.update(self.current)
            self.pbar.close()

        return reversed(self.data)

    def close(self):
        self.driver.close()

    def crawler(self, year, progress):
        table = self.driver.find_element_by_xpath(
            "//*[starts-with(@class, 'SearchResult-module__list___')]")
        lines = table.find_elements_by_xpath(
            "//*[starts-with(@class, 'SearchResult-module__body___')]")

        for line in lines:
            items = line.find_elements_by_tag_name("div")

            item = {}
            item["id"] = (
                items[0]
                .find_element_by_tag_name("i")
                .get_attribute("data-url")
                .split("/")[2]
            )

            # ??????????????????????????????????????????????????????????????????????????????
            flg_duplicate = next(
                (data["id"] for data in self.data if data["id"] == item["id"]), None)
            if flg_duplicate:
                continue

            item["count"] = (
                items[1]
                .find_element_by_tag_name("i")
                .get_attribute("title")
                .split("???")[0]
            )
            date = items[2].text.split("???")[0]
            item["date"] = datetime.datetime.strptime(
                "{}???{}".format(year, date), "%Y???%m???%d???"
            )
            item["category"] = (
                items[3].find_element_by_tag_name(
                    "span").get_attribute("data-title")
            )
            item["genre"] = items[3].find_elements_by_tag_name("span")[1].text
            item["amount"] = int(items[4].find_element_by_tag_name(
                "span").text.strip("??").replace(",", ""))
            m_from = items[5].find_elements_by_tag_name("img")
            if len(m_from) != 0:
                item["from_account"] = m_from[0].get_attribute("data-title")
            else:
                item["from_account"] = ""
            m_to = items[6].find_elements_by_tag_name("img")
            if len(m_to) != 0:
                item["to_account"] = m_to[0].get_attribute("data-title")
            else:
                item["to_account"] = ""
            item["type"] = (
                "transfer" if item["from_account"]!="" and item["to_account"]!="" else "payment" if item["from_account"]!="" and item["to_account"]=="" else "income" if item["from_account"]=="" and item["to_account"]!="" else None
            )
            item["place"] = (
                items[7].find_element_by_tag_name("span").text
            )
            item["name"] = (
                items[8].find_element_by_tag_name(
                    "span").text
            )
            item["comment"] = (
                items[9].find_element_by_tag_name(
                    "span").text
            )
            self.data.append(item)
            tmp_day = item["date"].day

            if progress:
                self.pbar.update(self.current - tmp_day)
                self.current = tmp_day

        # ?????????????????????????????????????????????????????????????????????????????????????????????????????????
        current_id = lines[0].find_elements_by_tag_name(
            "div")[0].find_element_by_tag_name("i").get_attribute("data-url").split("/")[2]
        self.driver.execute_script(
            "arguments[0].scrollIntoView(true);", lines[len(lines)-1])
        time.sleep(0.1)
        next_id = self.driver.find_element_by_xpath(
            "//*[starts-with(@class, 'SearchResult-module__list___')]").find_elements_by_xpath(
            "//*[starts-with(@class, 'SearchResult-module__body___')]")[0].find_elements_by_tag_name("div")[0].find_element_by_tag_name("i").get_attribute("data-url").split("/")[2]

        if current_id == next_id:
            return False
        else:
            return True

class ZaimCrawlerException(Exception):
    def __init__(self, message=''):
        self.message = 'ZaimCrawlerException: {0}'.format(message)
        logger.exception(self.message)

    def __str__(self):
       return self.message