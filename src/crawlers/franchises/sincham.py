import time
from src.apps.place.models import Place
from src.crawlers.base import BaseCrawler
from src.utils.chromedriver import setup_chrome
from src.utils.map import get_latlng


class SinChamCrawler(BaseCrawler):
    base_url = 'https://www.sincham.com/pg/bbs/board.php?bo_table=store01&page='
    page_number = 1
    brand = None

    def __init__(self):
        self.brand_name = '신참떡볶이'

    def set_next_page_url(self):
        self.url = self.base_url + str(self.page_number)
        self.page_number += 1

    def get_place_data(self):
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
        elements = self.driver.find_elements_by_xpath('//*[@id="fboardlist"]/div/table/tbody/tr')
        try:
            if elements[0].find_element_by_class_name('empty_table'):
                print('추가 데이터가 없습니다.')
                return []
        except:
            pass
        places = []
        for element in elements:
            place_name = str(element.find_element_by_xpath('./td[2]/div/a/div[2]').text)
            print(place_name)
            name = '%s %s' % (self.brand_name, place_name)
            telephone = element.find_element_by_xpath('./td[5]/div[2]').text
            address = element.find_element_by_xpath('./td[3]/div[2]').text
            working_time = element.find_element_by_xpath('./td[4]/div[2]').text
            description = '주소: %s\n전화번호: %s\n영업시간: %s' % (address, telephone, working_time)
            latitude, longitude = get_latlng(address, name)
            if not latitude or not longitude:
                print('[failed] %s\n%s' % (name, description))
                continue
            places.append(Place(name=name, description=description, latitude=latitude, longitude=longitude,
                                brand=self.get_brand()))
            time.sleep(0.5)
        return places
