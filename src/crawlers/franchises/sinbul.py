import time

from src.apps.place.models import Place
from src.crawlers.base import BaseCrawler
from src.utils.chromedriver import setup_chrome
from src.utils.map import get_latlng
from selenium.webdriver.common.by import By


class SinBulCrawler(BaseCrawler):
    base_url = 'http://sinbul.co.kr/bbs/board.php?bo_table=store'
    is_last_page = False

    def __init__(self):
        self.brand_name = '신불떡볶이'

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

    def get_place_data(self) -> [Place]:
        if self.is_last_page:
            return []
        elements = self.driver.find_elements(by=By.XPATH, value=('//*[@id="fboardlist"]/div/div[3]/ul/li'))
        time.sleep(1)
        places = []
        num = 1
        for element in elements:
            name = '%s %s' % (self.brand_name, element.find_element(by=By.XPATH, value='./a/p[1]').text)
            print(name)
            address_and_telephone = element.find_element(by=By.XPATH, value='./a/p[2]').text
            address = address_and_telephone.split('\n')[0]
            telephone = address_and_telephone.split('\n')[1]
            latitude, longitude = get_latlng(address.split('(')[0], name.split('H')[0])
            if not latitude or not longitude:
                print('[failed] %s\n%s\n%s' % (name, address, telephone))
                continue
            print(latitude, longitude)
            places.append(Place(name=name, address=address, latitude=latitude, longitude=longitude,
                                telephone=telephone, brand=self.get_brand()))
            time.sleep(0.5)
            num += 1
        self.is_last_page = True
        return places
