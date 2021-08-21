from src.crawlers.base import FranchiseType, get_crawlers


def run():
    crawlers = get_crawlers([
        FranchiseType.SINJEON
    ])
    for crawler in crawlers:
        crawler.run()
