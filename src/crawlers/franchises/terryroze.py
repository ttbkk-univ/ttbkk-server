import time
from src.apps.place.models import Place
from src.crawlers.base import BaseCrawler
from src.utils.chromedriver import setup_chrome
from src.utils.map import get_latlng
from selenium.webdriver.common.by import By


class TerryRozeCrawler(BaseCrawler):
    base_url = 'https://태리로제.com/front/store/store'
    page_number = 1
    brand = None
    browser_open = False

    def __init__(self):
        self.brand_name = '태리로제떡볶이'

    def set_next_page(self):
        while not self.browser_open:
            try:
                self.driver.get(self.base_url)
                time.sleep(3)
            except Exception as e:
                self.driver = setup_chrome()
                continue
            self.browser_open = True

        is_success = False
        while not is_success:
            try:
                self.driver.execute_script('javascript:Store.search_store(\'%s\')' % self.page_number)
                time.sleep(1)
            except Exception as e:
                self.driver = setup_chrome()
                continue
            is_success = True
        self.page_number += 1

    def get_place_data(self):
        try:
            # class name fake-table-column rows
            elements = self.driver.find_elements(
                by=By.CSS_SELECTOR,
                value='#container-block > div.container > div > div.fake-table > div.fake-table-column',
            )
        except:
            print('추가 데이터가 없습니다.')
            return []
        places = []
        for element in elements:
            name = '%s %s' % (self.brand_name, element.find_element(by=By.XPATH, value='./div[3]').text)
            address = element.find_element(by=By.XPATH, value='./div[4]').text
            telephone = element.find_element(by=By.XPATH, value='./div[5]').text
            latitude, longitude = get_latlng(address, name)
            if not latitude or not longitude:
                print('[failed] %s\n%s\n%s' % (name, address, telephone))
                continue
            places.append(Place(name=name, address=address, latitude=latitude, longitude=longitude,
                                telephone=telephone, brand=self.get_brand()))
            time.sleep(0.5)
        return places
