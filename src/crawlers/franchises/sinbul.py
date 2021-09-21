import time

from src.apps.place.models import Place
from src.crawlers.base import BaseCrawler
from src.utils.chromedriver import setup_chrome
from src.utils.map import get_latlng


class SinBulCrawler(BaseCrawler):
    base_url = 'http://sinbul.co.kr/bbs/board.php?bo_table=store'
    is_last_page = False

    def __init__(self):
        self.brand_name = '신불떡볶이'

    def set_next_page_url(self):
        self.url = self.base_url

    def get_place_data(self) -> [Place]:
        if self.is_last_page:
            return []
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
        elements = self.driver.find_elements_by_xpath('//*[@id="fboardlist"]/div/div[3]/ul/li')
        time.sleep(1)
        places = []
        num = 1
        for element in elements:
            name = '%s %s' % (self.brand_name, element.find_element_by_xpath('./a/p[1]').text)
            print(name)
            address_and_telephone = element.find_element_by_xpath('./a/p[2]').text
            address = address_and_telephone.split('\n')[0]
            telephone = address_and_telephone.split('\n')[1]
            description = '주소: %s\n전화번호: %s' % (address, telephone)
            latitude, longitude = get_latlng(address.split('(')[0], name.split('H')[0])
            if not latitude or not longitude:
                print('[failed] %s\n%s' % (name, description))
                continue
            print(latitude, longitude)
            places.append(Place(name=name, description=description, latitude=latitude, longitude=longitude,
                                brand=self.get_brand()))
            time.sleep(0.5)
            num += 1
        return places
