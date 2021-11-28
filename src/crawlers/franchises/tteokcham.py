import time
from src.apps.place.models import Place
from src.crawlers.base import BaseCrawler
from src.utils.chromedriver import setup_chrome
from src.utils.map import get_latlng


class TteokChamCrawler(BaseCrawler):
    base_url = 'http://www.tteokcham.com/'
    page_number = 1
    brand = None

    def __init__(self):
        self.brand_name = '떡참'

    def set_next_page(self):
        self.url = self.base_url
        if self.page_number == 1:
            is_success = False
            while not is_success:
                self.driver.get(self.url)
                try:
                    time.sleep(3)
                    is_success = True
                except Exception as e:
                    self.driver = setup_chrome()
                    continue
        else:
            self.driver.execute_script('ajaxCompanyArea(%s)' % self.page_number)
            time.sleep(1)
        self.page_number += 1

    def get_place_data(self):
        elements = self.driver.find_elements_by_xpath('//*[@id="sb-list"]/table/tbody/tr')
        if elements[0].find_element_by_xpath('./td').text == '매장이 없습니다.':
            return []

        places = []
        for element in elements:
            place_name = element.find_element_by_xpath('./td[1]').text

            name = '%s %s' % (self.brand_name, place_name)
            address = element.find_element_by_xpath('./td[2]').text
            telephone = element.find_element_by_xpath('./td[3]').text

            latitude, longitude = get_latlng(address, name)
            print('[%s] %s %s (%s,%s)' % (name, address, telephone, latitude, longitude))
            if not latitude or not longitude:
                print('[failed] %s\n%s\n%s' % (name, address, telephone))
                continue
            places.append(
                Place(name=name, address=address, latitude=latitude, longitude=longitude,
                      telephone=telephone, brand=self.get_brand()))
            time.sleep(0.5)
        return places
