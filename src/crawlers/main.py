from enum import Enum
from threading import Thread

<<<<<<< Updated upstream
import env
from manage import main
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
from src.crawlers.franchises.tteokcham import TteokChamCrawler
from src.crawlers.franchises.youngdabang import YoungDaBangCrawler
from src.crawlers.franchises.yupdduk import YupddukCrawler
from src.crawlers.franchises.zzing import ZzingCrawler

=======
>>>>>>> Stashed changes

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
    KANG = '크앙'
    ESOTTUK = '이소떡'
    ZZING = '찡떡'


def get_crawlers(types):
    crawlers = []
    for crawler_type in types:
        crawlers.append(get_crawlers(crawler_type))
    return crawlers


def run():
    crawlers = get_crawlers([
<<<<<<< Updated upstream

        # FranchiseType.KANG,
        # FranchiseType.DALDDUK,
        # FranchiseType.JAWSFOOD,
        # FranchiseType.EUNGDDUK,
        # FranchiseType.SINBUL,
        # FranchiseType.SINCHAM,
        # FranchiseType.ESOTTUK,
        # FranchiseType.YOUNGDABANG,
        # FranchiseType.DOOKKI,
        # FranchiseType.SINJEON,
        # FranchiseType.GAMTAN,
        # FranchiseType.YUPDDUK,
        # FranchiseType.BAEDDUCK,
        # FranchiseType.MYUNGRANG,
        # FranchiseType.TTEOKCHAM,
        # FranchiseType.SAMCHEOP,
        # FranchiseType.ZZING,
=======
        FranchiseType.BAEDDUCK,
        FranchiseType.DALDDUK,
        FranchiseType.DOOKKI,
        FranchiseType.EUNGDDUK,
        FranchiseType.ESOTTUK,
        FranchiseType.GAMTAN,
        FranchiseType.JAWSFOOD,
        FranchiseType.KANG,
        FranchiseType.MYUNGRANG,
        FranchiseType.SAMCHEOP,
        FranchiseType.SINBUL,
        FranchiseType.SINCHAM,
        FranchiseType.SINJEON,
        FranchiseType.TTEOKCHAM,
        FranchiseType.YOUNGDABANG,
        FranchiseType.YUPDDUK,
        FranchiseType.ZZING,
>>>>>>> Stashed changes
    ])

    if env.MULTI_THREAD_MODE:
        threads = []
        for crawler in crawlers:
            try:
                thread = Thread(target=crawler.run)
                thread.start()
                threads.append(thread)
            except Exception as e:
                print(e)
                continue
        for thread in threads:
            thread.join()

    else:
        for crawler in crawlers:
            try:
                crawler.run()
            except Exception as e:
                print(e)
                continue

    print('done')
