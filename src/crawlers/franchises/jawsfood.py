import time
from src.apps.place.models import Place
from src.crawlers.base import BaseCrawler
from src.utils.chromedriver import setup_chrome
from src.utils.map import get_latlng


class JawsFoodCrawler(BaseCrawler):
    base_url = 'http://www.jawsfood.co.kr/store/store_search.html'
    brand = None
    last_page = None

    def __init__(self):
        self.brand_name = '죠스떡볶이'

    def set_next_page(self):
        self.url = self.base_url
        self.last_page = bool(self.brand)
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
        if self.last_page:
            return []
        elements = self.driver.find_elements_by_xpath('//*[@id="datalist"]/li')
        places = []
        for element in elements:
            place_name = str(element.find_element_by_xpath('./a/p[1]').text)
            name = '%s %s' % (self.brand_name, place_name)
            address = element.find_element_by_xpath('./a/p[2]').text
            print(name)
            latitude, longitude = get_latlng(address, name)
            if not latitude or not longitude:
                print('[failed] %s\n%s' % (name, address))
                continue
            places.append(Place(name=name, address=address, latitude=latitude, longitude=longitude,
                                brand=self.get_brand()))
            time.sleep(0.5)
        return places
