import time

from src.crawlers.base import BaseCrawler
from src.apps.place.models import Place
from selenium.webdriver.common.by import By
import re

from src.utils.chromedriver import setup_chrome
from src.utils.map import get_latlng


class EungkeumCrawler(BaseCrawler):
    crawler_name = 'EungkeumCrawler'
    brand_name = '응큼떡볶이'
    url = 'https://xn--331b22lg9ice657b.com/location/?sort=TIME&keyword_type=all&page=1'
    page_number = 1
    page_numbers = []

    def __init__(self):
        super().__init__()

    def get_page_numbers(self):
        page_elements = self.driver.find_elements(By.XPATH,"/html/body/div[4]/main/div[2]/div[1]/div/div/div/div[2]/div[1]/div[2]/nav/ul/li/a")
        # previous, 1,2,3, ... , next
        page_numbers = []
        for page_element in page_elements:
            page_number = page_element.text
            if re.match(r'\d+', page_number):
                page_numbers.append(int(page_number))

        return page_numbers

    def set_next_page(self):
        self.url = 'https://xn--331b22lg9ice657b.com/location/?sort=TIME&keyword_type=all&page=%s' % self.page_number
        is_success = False
        while not is_success:
            try:
                self.driver.get(self.url)
                time.sleep(10)
            except Exception as e:
                self.driver = setup_chrome()
                continue
            is_success = True
        self.page_number += 1

    def get_place_data(self) -> [Place]:
        places = []
        elements = self.driver.find_elements(By.XPATH,
                                             '/html/body/div[4]/main/div[2]/div[1]/div/div/div/div[2]/div[1]/div[2]/div/div/div')
        if self.page_number not in self.get_page_numbers():
            return []
        for element in elements:
            name = element.find_element(By.XPATH, './a[2]/div/div').text
            address = element.find_element(By.XPATH, './div[1]/p').text
            latitude, longitude = get_latlng(address, name)
            places.append(Place(
                name=name,
                address=address,
                latitude=latitude,
                longitude=longitude,
                brand=self.get_brand(),
            ))
        return places
