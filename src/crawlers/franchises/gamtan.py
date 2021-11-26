# http://www.gamtan.co.kr/main/store_list.php?page_i
import time

from src.apps.place.models import Place
from src.crawlers.base import BaseCrawler
from src.utils.chromedriver import setup_chrome
from src.utils.map import get_latlng


class GamtanCrawler(BaseCrawler):
    base_url = 'http://www.gamtan.co.kr/main/store_list.php?page_idx=166&gubun=&add_code=&keyword=&startPage='
    offset = 0

    def __init__(self):
        self.brand_name = '감탄떡볶이'

    def set_next_page(self):
        self.url = self.base_url + str(self.offset)
        is_success = False
        while not is_success:
            try:
                self.driver.get(self.url)
                time.sleep(3)
            except Exception as e:
                self.driver = setup_chrome()
                continue
            is_success = True
        self.offset += 15

    def get_place_data(self) -> [Place]:
        try:
            elements = self.driver.find_elements_by_xpath('//*[@id="content"]/section/div[2]/div/div[2]/div/table/tbody/tr')
            time.sleep(1)
            if elements[0].find_element_by_xpath('./td').text == '등록된 매장이 없습니다.':
                return []
        except:
            print('추가 데이터가 없습니다.')
            return []
        places = []
        num = 1
        for element in elements:
            print(num)
            name = '%s %s' % (self.brand_name, element.find_element_by_xpath('./td[1]/span').text.split('-')[1])
            address = element.find_element_by_xpath('./td[2]/span').text
            telephone = element.find_element_by_xpath('./td[3]/a').text
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

