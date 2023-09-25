from urllib import parse
import time
from src.apps.place.models import Place
from src.crawlers.base import BaseCrawler
from src.utils.chromedriver import setup_chrome
from src.utils.map import get_latlng
from selenium.webdriver.common.by import By


class EungDdukCrawler(BaseCrawler):
    base_url = 'http://www.eungdduk.kr/bbs/board.php?bo_table=store2&sca=%EC%9D%91%EA%B8%89%EC%8B%A4+%EA%B5%AD%EB%AC%BC+%EB%96%A1%EB%B3%B6%EC%9D%B4'
    page_number = 1
    brand = None
    last_page = None

    def __init__(self):
        self.brand_name = '응급실국물떡볶이'

    def set_next_page(self):
        self.url = self.base_url
        is_success = False
        while not is_success:
            try:
                self.driver.get(self.url)
                time.sleep(10)
            except Exception as e:
                self.driver = setup_chrome()
                continue
            is_success = True
        self.page_number += 1

    def get_place_data(self):
        if self.last_page:
            return []

        elements = self.driver.find_elements(by=By.XPATH, value=('//*[@id="fboardlist"]/ul/li'))
        places = []
        for element in elements:
            place_name = str(element.find_element(by=By.XPATH, value='./div/div[1]').text)
            if place_name.startswith('(오픈준비중)'):
                place_name = place_name.split('(오픈준비중)')[1]
            name = '%s %s' % (self.brand_name, place_name)

            address_and_telephone = element.find_element(by=By.XPATH, value='./div/div[2]').text
            address = address_and_telephone.split('\n')[0]
            telephone = address_and_telephone.split('\n')[1].replace('TEL : ', '')
            print(name)
            latitude, longitude = get_latlng(address, name)
            if not latitude or not longitude:
                print('[failed] %s\n%s\n%s' % (name, address, telephone))
                continue
            places.append(Place(name=name, address=address, latitude=latitude, longitude=longitude,
                                telephone=telephone, brand=self.get_brand()))
            time.sleep(0.5)
        self.last_page = True
        return places
