import time

from selenium.webdriver.common.keys import Keys

from src.apps.place.models import Place
from src.crawlers.base import BaseCrawler
from src.utils.chromedriver import setup_chrome
from src.utils.map import get_latlng


class MyungrangHotDogCrawler(BaseCrawler):
    base_url = 'https://myungranghotdog.com/kor/store/list.do'
    is_last_page = False
    brand = None

    def __init__(self):
        self.brand_name = '명랑핫도그'

    def set_next_page_url(self):
        self.url = self.base_url
        self.is_last_page = True
        is_success = False
        while not is_success:
            try:
                self.driver.get(self.url)
                time.sleep(3)
            except Exception as e:
                self.driver = setup_chrome()
                continue
            is_success = True

    def get_place_data(self):
        if self.is_last_page:
            return []
        try:
            self.driver.find_element_by_xpath('//*[@id="search2"]').click()
            self.driver.find_element_by_xpath('//*[@id="searchKeyword"]').send_keys('%%')
            self.driver.find_element_by_xpath('//*[@id="txt"]/div/div[1]/ul/li[2]/div/div/form/input[3]').click()
            time.sleep(5)
            elements = self.driver.find_elements_by_xpath('//*[@id="txt"]/div/div[1]/div/ul/li')
            time.sleep(1)
        except:
            print('추가 데이터가 없습니다.')
            return []
        places = []
        num = 1
        for element in elements:
            print(num)
            name = '%s %s' % (self.brand_name, element.find_element_by_xpath('./p[1]/a').text)
            address = element.find_element_by_xpath('./p[2]').text
            telephone = element.find_element_by_xpath('./p[3]/a').text
            description = '주소: %s\n전화번호: %s' % (address, telephone)
            latitude, longitude = get_latlng(address.split('(')[0], name)
            if not latitude or not longitude:
                print('[failed] %s\n%s' % (name, description))
                continue
            print(latitude, longitude)
            places.append(Place(name=name, description=description, latitude=latitude, longitude=longitude,
                                brand=self.get_brand()))
            time.sleep(0.5)
            num += 1
        return places
