from enum import Enum
from src.crawlers.franchises.gamtan import GamtanCrawler
from src.crawlers.franchises.sinjeon import SinjeonCrawler
from src.crawlers.franchises.yupdduk import YupddukCrawler


class FranchiseType(Enum):
    SINJEON = 'sinjeon'
    GAMTAN = 'gamtan'
    YUPDDUK = 'yupdduk'


def get_crawlers(types):
    result = []
    for crawler_type in types:
        if crawler_type == FranchiseType.SINJEON:
            result.append(SinjeonCrawler())
        elif crawler_type == FranchiseType.GAMTAN:
            result.append(GamtanCrawler())
        elif crawler_type == FranchiseType.YUPDDUK:
            result.append(YupddukCrawler())
        else:
            raise TypeError('invalid crawler type')
    return result


def run():
    crawlers = get_crawlers([
        FranchiseType.YUPDDUK
    ])
    for crawler in crawlers:
        crawler.run()
