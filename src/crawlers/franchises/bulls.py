import time
from src.apps.place.models import Place
from src.crawlers.base import BaseCrawler
from src.utils.chromedriver import setup_chrome
from src.utils.map import get_latlng
from selenium.webdriver.common.by import By


class BullsCrawler(BaseCrawler):
    base_url = 'http://www.불스떡볶이.kr/store/page/%s/'
    page_number = 1
    brand = None
    browser_open = False

    def __init__(self):
        self.brand_name = '불스떡볶이'

    def set_next_page(self):
        is_success = False
        while not is_success:
            try:
                self.driver.get(self.base_url % self.page_number)
                time.sleep(3)
            except Exception as e:
                self.driver = setup_chrome()
                continue
            is_success = True
        self.page_number += 1

    def get_place_data(self):
        try:
            # class name fake-table-column rows
            elements = self.driver.find_elements(
                by=By.XPATH,
                value='//*[@id="post-25"]/div/div[3]/div/div/div/div[1]/div[2]/table/tbody/tr',
            )

            if '지점 없음.' in elements[0].find_element(by=By.XPATH, value='./td').text:
                return []
        except:
            print('추가 데이터가 없습니다.')
            return []
        places = []
        for element in elements:
            name = '%s %s' % (self.brand_name, element.find_element(by=By.XPATH, value='./td[2]/a[1]').text.replace('불스 ', ''))
            address = element.find_element(by=By.XPATH, value='./td[3]/a/span[1]').text
            telephone = element.find_element(by=By.XPATH, value='./td[4]').text
            latitude, longitude = get_latlng(address, name)
            if not latitude or not longitude:
                print('[failed] %s\n%s\n%s' % (name, address, telephone))
                continue
            places.append(Place(name=name, address=address, latitude=latitude, longitude=longitude,
                                telephone=telephone, brand=self.get_brand()))
            time.sleep(0.5)
        return places
