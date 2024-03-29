import time
from src.apps.place.models import Place
from src.crawlers.base import BaseCrawler
from src.utils.chromedriver import setup_chrome
from src.utils.map import get_latlng
from selenium.webdriver.common.by import By


class ZzingCrawler(BaseCrawler):
    base_url = 'http://www.zzing.co.kr/sub/sub04_01.php'
    page_number = 1
    brand = None

    def __init__(self):
        self.brand_name = '찡떡'

    def set_next_page(self):
        self.url = self.base_url
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
        if self.brand:
            return []  # 첫페이지만 있으니까 추가해두는 임시코드
        try:
            elements = self.driver.find_elements(by=By.XPATH, value=('/html/body/div[2]/div[3]/div/div[2]/div[2]/table/tbody/tr'))
        except:
            print('추가 데이터가 없습니다.')
            return []
        places = []
        for element in elements:
            name = '%s %s' % (self.brand_name, element.find_element(by=By.XPATH, value='./td[2]').text)
            address = element.find_element(by=By.XPATH, value='./td[3]').text
            telephone = element.find_element(by=By.XPATH, value='./td[4]').text
            latitude, longitude = get_latlng(address, name)
            if not latitude or not longitude:
                print('[failed] %s\n%s\n%s' % (name, address, telephone))
                continue
            places.append(Place(name=name, address=address, latitude=latitude, longitude=longitude,
                                telephone=telephone, brand=self.get_brand()))
            time.sleep(0.5)
        return places
