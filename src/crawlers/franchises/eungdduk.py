from urllib import parse
import time
from src.apps.place.models import Place
from src.crawlers.base import BaseCrawler
from src.utils.chromedriver import setup_chrome
from src.utils.map import get_latlng


class EungDdukCrawler(BaseCrawler):
    base_url = 'http://www.eungdduk.kr/sub/store.php?ptype=&code=store&page='
    page_number = 1
    brand = None
    last_page = None

    def __init__(self):
        self.brand_name = '응급실국물떡볶이'

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
        if not self.last_page:
            last_page_link = str(self.driver.find_element_by_xpath('//*[@id="section-1"]/div/div/table[2]/tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td[5]/a').get_attribute('href'))
            query_params = parse.parse_qs(last_page_link.split('?')[1])
            self.last_page = int(query_params['page'][0])
        elif self.page_number - 1 > self.last_page:
            return []

        elements = self.driver.find_elements_by_xpath('//*[@id="section-1"]/div/div/table[1]/tbody/tr')
        places = []
        row_num = 0
        for element in elements:
            row_num += 1
            if row_num % 2 == 1:
                continue
            place_name = str(element.find_element_by_xpath('./td[2]/a').text)
            if place_name.startswith('(오픈준비중)'):
                place_name = place_name.split('(오픈준비중)')[1]
            name = '%s %s' % (self.brand_name, place_name)
            telephone = element.find_element_by_xpath('./td[4]/a').text
            address = element.find_element_by_xpath('./td[3]/a').text
            print(name)
            latitude, longitude = get_latlng(address, name)
            if not latitude or not longitude:
                print('[failed] %s\n%s\n%s' % (name, address, telephone))
                continue
            places.append(Place(name=name, address=address, latitude=latitude, longitude=longitude,
                                telephone=telephone, brand=self.get_brand()))
            time.sleep(0.5)
        return places
