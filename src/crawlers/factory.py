from src.crawlers.franchise_type import FranchiseType
from src.crawlers.franchises.baedduck import BaeDduckCrawler
from src.crawlers.franchises.daldduk import DalDdukCrawler
from src.crawlers.franchises.dookki import DookkiCrawler
from src.crawlers.franchises.esottuk import EsottukCrawler
from src.crawlers.franchises.eungdduk import EungDdukCrawler
from src.crawlers.franchises.gamtan import GamtanCrawler
from src.crawlers.franchises.jawsfood import JawsFoodCrawler
from src.crawlers.franchises.kang import KangCrawler
from src.crawlers.franchises.myungranghotdog import MyungrangHotDogCrawler
from src.crawlers.franchises.samcheop import SamCheopCrawler
from src.crawlers.franchises.sinbul import SinBulCrawler
from src.crawlers.franchises.sincham import SinChamCrawler
from src.crawlers.franchises.sinjeon import SinjeonCrawler
from src.crawlers.franchises.terryroze import TerryRozeCrawler
from src.crawlers.franchises.tteokcham import TteokChamCrawler
from src.crawlers.franchises.youngdabang import YoungDaBangCrawler
from src.crawlers.franchises.yupdduk import YupddukCrawler
from src.crawlers.franchises.zzing import ZzingCrawler


def get_crawlers(types):
    crawlers = []
    for crawler_type in types:
        crawlers.append(get_crawler(crawler_type))
    return crawlers


def get_crawler(crawler_type):
    if crawler_type == FranchiseType.SINJEON:
        return SinjeonCrawler()
    elif crawler_type == FranchiseType.GAMTAN:
        return GamtanCrawler()
    elif crawler_type == FranchiseType.YUPDDUK:
        return YupddukCrawler()
    elif crawler_type == FranchiseType.BAEDDUCK:
        return BaeDduckCrawler()
    elif crawler_type == FranchiseType.MYUNGRANG:
        return MyungrangHotDogCrawler()
    elif crawler_type == FranchiseType.YOUNGDABANG:
        return YoungDaBangCrawler()
    elif crawler_type == FranchiseType.SINCHAM:
        return SinChamCrawler()
    elif crawler_type == FranchiseType.SINBUL:
        return SinBulCrawler()
    elif crawler_type == FranchiseType.EUNGDDUK:
        return EungDdukCrawler()
    elif crawler_type == FranchiseType.JAWSFOOD:
        return JawsFoodCrawler()
    elif crawler_type == FranchiseType.TTEOKCHAM:
        return TteokChamCrawler()
    elif crawler_type == FranchiseType.SAMCHEOP:
        return SamCheopCrawler()
    elif crawler_type == FranchiseType.DALDDUK:
        return DalDdukCrawler()
    elif crawler_type == FranchiseType.DOOKKI:
        return DookkiCrawler()
    elif crawler_type == FranchiseType.KANG:
        return KangCrawler()
    elif crawler_type == FranchiseType.ESOTTUK:
        return EsottukCrawler()
    elif crawler_type == FranchiseType.ZZING:
        return ZzingCrawler()
    elif crawler_type == FranchiseType.TERRYROZE:
        return TerryRozeCrawler()
    else:
        raise TypeError('invalid crawler type')
