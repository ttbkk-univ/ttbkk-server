# http://www.gamtan.co.kr/main/store_list.php?page_i
from src.crawlers.base import BaseCrawler


class GamtanCrawler(BaseCrawler):
    base_url = 'http://www.gamtan.co.kr/main/store_list.php?page_idx=166&gubun=&add_code=&keyword=&startPage='
    start_page = 0
    url = base_url + str(start_page)

    def get_next_page(self):
        self.start_page += 15
