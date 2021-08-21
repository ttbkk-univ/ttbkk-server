import time
from src.apps.place.models import Place
from src.crawlers.base import BaseCrawler
from src.utils.map import get_latlng_by_address


class SinjeonCrawler(BaseCrawler):
    base_url = 'http://sinjeon.co.kr/pg/bbs/board.php?bo_table=store&page='
    page_number = 1
    url = base_url + str(page_number)

    def set_next_page(self):
        self.page_number += 1

    def get_place_data(self):
        self.driver.get(self.url)
        time.sleep(1)

        elements = self.driver.find_elements_by_xpath('//*[@id="fboardlist"]/div/table/tbody/tr')

        places = []
        for element in elements:
            name = '신전떡볶이 %s' % element.find_element_by_xpath('./td[2]/a').text
            telephone = element.find_element_by_xpath('./td[3]').text
            address = element.find_element_by_xpath('./td[4]').text
            description = '주소: %s\n전화번호: %s' % (address, telephone)
            latitude, longitude = get_latlng_by_address(address)
            places.append(Place(name, description, latitude, longitude))
        return places
