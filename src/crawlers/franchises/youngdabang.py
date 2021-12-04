import time
from src.apps.place.models import Place
from src.crawlers.base import BaseCrawler
from src.utils.chromedriver import setup_chrome
from src.utils.map import get_latlng


class YoungDaBangCrawler(BaseCrawler):
    base_url = 'http://www.youngdabang.com/board/index.php?board=map_01&sca=all&type=list&select=&search=&page='
    page_number = 1
    brand = None

    def __init__(self):
        self.brand_name = '청년다방'

    def set_next_page(self):
        self.url = self.base_url + str(self.page_number)
        is_success = False
        while not is_success:
            try:
                self.driver.get(self.url)
                time.sleep(3)
            except Exception as e:
                print(e)
                self.driver = setup_chrome()
                continue
            is_success = True
        self.page_number += 1

    def get_place_data(self):
        try:
            elements = self.driver.find_elements_by_xpath('//*[@id="boardWrap"]/ul/li')
        except:
            print('추가 데이터가 없습니다.')
            return []
        places = []
        for element in elements:
            place_name = str(element.find_element_by_xpath('./p[1]').text)
            print(place_name)
            if place_name.startswith('NEW'):
                place_name = place_name.split('NEW')[1]
            name = '%s %s' % (self.brand_name, place_name)
            telephone = element.find_element_by_xpath('./p[3]').text
            address = element.find_element_by_xpath('./p[2]').text
            latitude, longitude = get_latlng(address, name)
            if not latitude or not longitude:
                print('[failed] %s\n%s\n%s' % (name, address, telephone))
                continue
            places.append(Place(name=name, address=address, latitude=latitude, longitude=longitude,
                                telephone=telephone, brand=self.get_brand()))
            time.sleep(0.5)
        return places
