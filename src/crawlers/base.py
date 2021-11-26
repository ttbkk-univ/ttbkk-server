from src.apps.brand.models import Brand
from src.apps.place.models import Place
from src.utils.chromedriver import setup_chrome


class BaseCrawler:
    map_util = None
    crawler_name = None
    brand_name = None
    brand = None
    driver = setup_chrome()
    url = None

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
            raise ModuleNotFoundError('selenium driver required')
        while True:
            self.set_next_page()
            print(self.url)
            places = self.get_place_data()
            if not len(places):
                break
            place_names = [place.name for place in places]
            exist_places = Place.objects.filter(name__in=place_names)
            for exist_place in exist_places:
                for place in places:
                    if place.name == exist_place.name and (place.latitude != exist_place.latitude or place.longitude != exist_place.longitude):
                        exist_place.latitude = place.latitude
                        exist_place.longitude = place.longitude
                        exist_place.save()
            exist_place_names = [place.name for place in exist_places]
            new_places = [place for place in places if place.name not in exist_place_names]
            Place.objects.bulk_create(new_places)
            print('new %s places are created' % str(len(new_places)))
        print('%s finished' % self.crawler_name)
