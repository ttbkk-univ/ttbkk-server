from urllib import parse
import time
from src.apps.place.models import Place
from src.crawlers.base import BaseCrawler
from src.utils.chromedriver import setup_chrome
from src.utils.map import get_latlng


class KangCrawler(BaseCrawler):
    base_url = 'http://k-ang.co.kr/landing/index.html?search=&select=&store_page='
    page_number = 1
    brand = None
    last_page = None

    def __init__(self):
        self.brand_name = '크앙분식'

    def set_next_page(self):
        self.url = self.base_url + str(self.page_number)
        is_success = False
        while not is_success:
            try:
                self.driver.get(self.url)
                time.sleep(3)
            except Exception as e:
                self.driver = setup_chrome()
                continue
            is_success = True
        self.page_number += 1

    def get_place_data(self):
        try:
            elements = self.driver.find_elements_by_xpath('//*[@id="wrap"]/div[15]/div[2]/ul/li')
        except:
            return []
        places = []
        for element in elements:
            place_name = str(element.find_element_by_xpath('./a/div[2]/p[1]').text)
            name = '%s %s' % (self.brand_name, place_name)
            try:
                address = element.find_element_by_xpath('./a/div[2]/p[2]').text.split('주소 : ')[1]
            except:
                address = None
            try:
                telephone = element.find_element_by_xpath('./a/div[2]/p[3]').text.split('TEL : ')[1]
            except:
                telephone = None
            print(name)
            latitude, longitude = get_latlng(address, name)
            if not latitude or not longitude:
                print('[failed] %s\n%s\n%s' % (name, address, telephone))
                continue
            places.append(Place(name=name, address=address, latitude=latitude, longitude=longitude,
                                telephone=telephone, brand=self.get_brand()))
            time.sleep(0.5)
        return places
