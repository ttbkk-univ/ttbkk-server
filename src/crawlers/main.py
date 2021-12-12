from enum import Enum

from src.crawlers.franchises.baedduck import BaeDduckCrawler
from src.crawlers.franchises.daldduk import DalDdukCrawler
from src.crawlers.franchises.dookki import DookkiCrawler
from src.crawlers.franchises.eungdduk import EungDdukCrawler
from src.crawlers.franchises.gamtan import GamtanCrawler
from src.crawlers.franchises.jawsfood import JawsFoodCrawler
from src.crawlers.franchises.myungranghotdog import MyungrangHotDogCrawler
from src.crawlers.franchises.samcheop import SamCheopCrawler
from src.crawlers.franchises.sinbul import SinBulCrawler
from src.crawlers.franchises.sincham import SinChamCrawler
from src.crawlers.franchises.sinjeon import SinjeonCrawler
from src.crawlers.franchises.tteokcham import TteokChamCrawler
from src.crawlers.franchises.youngdabang import YoungDaBangCrawler
from src.crawlers.franchises.yupdduk import YupddukCrawler


class FranchiseType(Enum):
    SINJEON = '신전'
    GAMTAN = '감탄'
    YUPDDUK = '엽떡'
    BAEDDUCK = '배떡'
    MYUNGRANG = '명랑'
    YOUNGDABANG = '청년다방'
    SINCHAM = '신참'
    SINBUL = '신불'
    EUNGDDUK = '응떡'
    JAWSFOOD = '죠스떡볶이'
    TTEOKCHAM = '떡참'
    SAMCHEOP = '삼첩분식'
    DALDDUK = '달토끼의떡볶이흡입구역'
    DOOKKI = '두끼'


def get_crawlers(types):
    crawlers = []
    for crawler_type in types:
        if crawler_type == FranchiseType.SINJEON:
            crawlers.append(SinjeonCrawler())
        elif crawler_type == FranchiseType.GAMTAN:
            crawlers.append(GamtanCrawler())
        elif crawler_type == FranchiseType.YUPDDUK:
            crawlers.append(YupddukCrawler())
        elif crawler_type == FranchiseType.BAEDDUCK:
            crawlers.append(BaeDduckCrawler())
        elif crawler_type == FranchiseType.MYUNGRANG:
            crawlers.append(MyungrangHotDogCrawler())
        elif crawler_type == FranchiseType.YOUNGDABANG:
            crawlers.append(YoungDaBangCrawler())
        elif crawler_type == FranchiseType.SINCHAM:
            crawlers.append(SinChamCrawler())
        elif crawler_type == FranchiseType.SINBUL:
            crawlers.append(SinBulCrawler())
        elif crawler_type == FranchiseType.EUNGDDUK:
            crawlers.append(EungDdukCrawler())
        elif crawler_type == FranchiseType.JAWSFOOD:
            crawlers.append(JawsFoodCrawler())
        elif crawler_type == FranchiseType.TTEOKCHAM:
            crawlers.append(TteokChamCrawler())
        elif crawler_type == FranchiseType.SAMCHEOP:
            crawlers.append(SamCheopCrawler())
        elif crawler_type == FranchiseType.DALDDUK:
            crawlers.append(DalDdukCrawler())
        elif crawler_type == FranchiseType.DOOKKI:
            crawlers.append(DookkiCrawler())
        else:
            raise TypeError('invalid crawler type')
    return crawlers


def run():
    crawlers = get_crawlers([
        # FranchiseType.SINJEON,
        # FranchiseType.GAMTAN,
        # FranchiseType.YUPDDUK,
        # FranchiseType.BAEDDUCK,
        # FranchiseType.MYUNGRANG,
        # FranchiseType.YOUNGDABANG,
        # FranchiseType.SINCHAM,
        # FranchiseType.SINBUL,
        # FranchiseType.EUNGDDUK,
        # FranchiseType.JAWSFOOD,
        # FranchiseType.TTEOKCHAM,
        # FranchiseType.SAMCHEOP,
        # FranchiseType.DALDDUK,
        FranchiseType.DOOKKI
    ])
    for crawler in crawlers:
        crawler.run()
