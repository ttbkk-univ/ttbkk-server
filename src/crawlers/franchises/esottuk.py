import time
from src.apps.place.models import Place
from src.crawlers.base import BaseCrawler
from src.utils.chromedriver import setup_chrome
from src.utils.map import get_latlng
from selenium.webdriver.common.by import By


class EsottukCrawler(BaseCrawler):
    base_url = 'http://2so.co.kr/bbs/board.php?bo_table=store&city=&gu=&dong=&page='
    page_number = 1
    brand = None

    def __init__(self):
        self.brand_name = '이소떡'

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
            elements = self.driver.find_elements(by=By.XPATH, value=('//*[@id="addList"]/ul/li'))
        except:
            print('추가 데이터가 없습니다.')
            return []
        places = []
        for element in elements:
            place_name = str(element.find_element(by=By.XPATH, value='./div[1]/a/div/p[1]').text).replace('이소 ', '')

            name = '%s %s' % (self.brand_name, place_name)
            print(name)
            address = element.find_element(by=By.XPATH, value='./div[1]/a/div/p[2]').text
            latitude, longitude = get_latlng(address, name)
            if not latitude or not longitude:
                print('[failed] %s\n%s' % (name, address))
                continue
            telephone = str(element.find_element(by=By.XPATH, value='./div[1]/a/div/p[3]').text)
            telephone = telephone.replace('전화번호 : ', '')
            places.append(Place(name=name, address=address, telephone=telephone, latitude=latitude, longitude=longitude,
                                brand=self.get_brand()))
            time.sleep(0.5)
        return places
