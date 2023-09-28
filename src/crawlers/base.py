from src.apps.brand.models import Brand
from src.apps.place.models import Place
from src.utils.chromedriver import setup_chrome
from selenium.webdriver.chrome.webdriver import WebDriver


class BaseCrawler:
    map_util = None
    crawler_name = None
    brand_name = None
    brand = None
    url = None
    driver = None

    def _set_brand(self):
        if not self.brand_name:
            raise NotImplementedError
        brand, created = Brand.objects.get_or_create(name=self.brand_name)
        self.brand = brand

    def get_brand(self):
        if not self.brand:
            self._set_brand()
        return self.brand

    def set_next_page(self):
        raise NotImplementedError

    def get_place_data(self) -> [Place]:
        # return Place(name, description, latitude, longitude)
        raise NotImplementedError

    def run(self):
        if not self.driver:
            self.driver = setup_chrome()
        self.driver.switch_to.new_window('window')
        while True:
            self.set_next_page()
            print(self.url)
            places = self.get_place_data()
            if not len(places):
                break
            place_names = [place.name for place in places]
            place_unique_keys = [place.unique_key for place in places]
            exist_match_places = Place.objects.filter(name__in=place_names)
            exist_places = [place for place in exist_match_places if place.unique_key in place_unique_keys]

            for exist_place in exist_places:
                for place in places:
                    if place.unique_key == exist_place.unique_key:
                        exist_place.description = place.description
                        exist_place.address = place.address
                        exist_place.telephone = place.telephone
                        exist_place.latitude = place.latitude
                        exist_place.longitude = place.longitude
                        exist_place.save()
            exist_place_names = [place.name for place in exist_places]
            new_places = [place for place in places if place.name not in exist_place_names]
            Place.objects.bulk_create(new_places)
            print('new %s places are created' % str(len(new_places)))
        print('%s finished' % self.crawler_name)
