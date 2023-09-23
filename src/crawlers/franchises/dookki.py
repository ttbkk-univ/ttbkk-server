# http://www.gamtan.co.kr/main/store_list.php?page_i
import time

from src.apps.place.models import Place
from src.crawlers.base import BaseCrawler
from src.utils.chromedriver import setup_chrome
from src.utils.map import get_latlng
from selenium.webdriver.common.by import By


class DookkiCrawler(BaseCrawler):
    base_url = 'https://www.dookki.co.kr/store/domestic?page=%s'
    page = 1

    def __init__(self):
        self.brand_name = '두끼'

    def set_next_page(self):
        self.url = self.base_url % str(self.page)
        is_success = False
        while not is_success:
            try:
                self.driver.get(self.url)
                time.sleep(3)
            except Exception as e:
                self.driver = setup_chrome()
                continue
            is_success = True
        self.page += 1

    def get_place_data(self) -> [Place]:
        try:
            elements = self.driver.find_elements(by=By.XPATH, value=('//*[@id="fboardlist"]/div[2]/table/tbody/tr'))
            time.sleep(1)
            if elements[0].find_element(by=By.XPATH, value='./td').text == '게시물이 없습니다.':
                return []
        except:
            print('추가 데이터가 없습니다.')
            return []
        places = []
        for element in elements:
            element.find_element(by=By.XPATH, value='./td[3]/a[1]').click()
            time.sleep(1)

            name = element.find_element(by=By.XPATH, value='/html/body/div[4]/div[2]/div[1]/div[2]/h6').text
            if '두끼' in name:
                name = name.split('두끼')[1].lstrip()
            name = '%s %s' % (self.brand_name, name.split('(')[0])
            address = element.find_element(by=By.XPATH, value='/html/body/div[4]/div[2]/div[1]/div[2]/p').text
            telephone = element.find_element(by=By.XPATH, value='/html/body/div[4]/div[2]/div[1]/div[2]/table/tbody/tr[1]/td').text
            latitude, longitude = get_latlng(address.split(',')[0], name)
            print('[%s] %s\n%s (%s, %s)' % (name, telephone, address, latitude, longitude))
            if not latitude or not longitude:
                print('[failed] %s\n%s\n%s' % (name, address, telephone))
            else:
                print(latitude, longitude)
                places.append(Place(name=name, address=address, latitude=latitude, longitude=longitude,
                                    telephone=telephone, brand=self.get_brand()))
            element.find_element(by=By.XPATH, value='/html/body/div[4]/div[2]/i').click()
            time.sleep(0.5)
        return places

