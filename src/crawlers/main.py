from threading import Thread
import env
from src.crawlers.factory import get_crawlers
from src.crawlers.franchise_type import FranchiseType


def run():
    crawlers = get_crawlers([
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
        FranchiseType.TERRYROZE,
        FranchiseType.TTEOKCHAM,
        FranchiseType.YOUNGDABANG,
        FranchiseType.YUPDDUK,
        FranchiseType.ZZING,
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
