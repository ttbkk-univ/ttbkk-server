import time
from src.apps.place.models import Place
from src.crawlers.base import BaseCrawler
from src.utils.chromedriver import setup_chrome
from src.utils.map import get_latlng


class JawsFoodCrawler(BaseCrawler):
    base_url = 'http://www.jawsfood.co.kr/store/store_list.html?bs=&sf=&ss=&pg='
    brand = None
    page_number = 1

    def __init__(self):
        self.brand_name = '죠스떡볶이'

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
            elements = self.driver.find_elements_by_xpath('//*[@id="contents"]/div/div[2]/ul/li')
        except:
            return []
        places = []
        for element in elements:
            place_name = str(element.find_element_by_xpath('./div/div/a').text)
            name = '%s %s' % (self.brand_name, place_name)
            address = element.find_element_by_xpath('./div/div/div/dl[1]/dd').text
            telephone = element.find_element_by_xpath('./div/div/div/dl[2]/dd').text
            print(name)
            latitude, longitude = get_latlng(address, name)
            if not latitude or not longitude:
                print('[failed] %s\n%s' % (name, address))
                continue
            places.append(Place(name=name, address=address, telephone=telephone,
                                latitude=latitude, longitude=longitude,
                                brand=self.get_brand()))
            time.sleep(0.5)
        return places
