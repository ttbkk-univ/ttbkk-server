from enum import Enum

from src.apps.place.models import Place
from src.utils.chromedriver import setup_chrome
from src.crawlers.franchises.gamtan import GamtanCrawler
from src.crawlers.franchises.sinjeon import SinjeonCrawler


class FranchiseType(Enum):
    SINJEON = 'sinjeon'
    GAMTAN = 'gamtan'


def get_crawlers(types):
    result = []
    for crawler_type in types:
        if crawler_type == FranchiseType.SINJEON:
            result.append(SinjeonCrawler())
        elif crawler_type == FranchiseType.GAMTAN:
            result.append(GamtanCrawler())
        raise TypeError('invalid crawler type')
    return result


class BaseCrawler:
    driver = None
    map_util = None
    url = None
    crawler_name = None

    def __init__(self):
        self.driver = setup_chrome()

    def set_next_page(self):
        raise NotImplementedError

    def get_place_data(self):
        # return Place(name, description, latitude, longitude)
        raise NotImplementedError

    def run(self):
        if not self.url:
            raise NotImplementedError

        while True:
            places = self.get_place_data()
            if not len(places):
                break
            Place.objects.bulk_create(places)
            self.set_next_page()
        print('%s finished' % self.crawler_name)
