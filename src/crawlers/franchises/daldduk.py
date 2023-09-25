import time
from src.apps.place.models import Place
from src.crawlers.base import BaseCrawler
from src.utils.chromedriver import setup_chrome
from src.utils.map import get_latlng
from selenium.webdriver.common.by import By


class DalDdukCrawler(BaseCrawler):
    base_url = 'https://daldduk.com/store/?page='
    page_number = 1
    brand = None

    def __init__(self):
        self.brand_name = '달토끼의떡볶이흡입구역'

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
            elements = self.driver.find_elements(by=By.XPATH, value=('//*[@id="map_list_fold_b2022022287c91b6e03de1"]/div[1]/div[2]/div/div'))
        except:
            return []

        places = []
        for element in elements[1::]:
            place_name = element.find_element(by=By.XPATH, value='./div/a[2]/div/div').text
            splited_name = place_name.split('달토끼의떡볶이흡입구역 ')
            if len(splited_name) > 1:
                place_name = ' '.join(splited_name[1:])
            splited_name = place_name.split('달토끼의 떡볶이 흡입구역 ')
            if len(splited_name) > 1:
                place_name = ' '.join(splited_name[1:])
            name = '%s %s' % (self.brand_name, place_name)
            address = element.find_element(by=By.XPATH, value='./div/div/p[1]').text
            telephone = element.find_element(by=By.XPATH, value='./div/div/p[2]').text.split('\n')[0]
            latitude, longitude = get_latlng(address.split('(')[0], name)
            print('[%s] %s %s (%s,%s)' % (name, address, telephone, latitude, longitude))
            if not latitude or not longitude:
                print('[failed] %s\n%s\n%s' % (name, address, telephone))
                continue
            places.append(
                Place(name=name, address=address, latitude=latitude, longitude=longitude,
                      telephone=telephone, brand=self.get_brand()))
            time.sleep(0.5)
        return places
