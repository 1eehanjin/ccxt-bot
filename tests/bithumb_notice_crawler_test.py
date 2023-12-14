import time
import unittest
import requests
import pprint
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from notice import Notice
import bithumb_notice_crawler


class BithumbNoticeCrawlerTests(unittest.TestCase): 
    def setUp(self):
        self.bithumb_notice_crawler = bithumb_notice_crawler.BithumbNoticeCrawler()

    def test_retrieve_notices(self):
        notices = self.bithumb_notice_crawler.crawl_notices()
        for notice in notices:
            print(notice.id + " : " + notice.title)

    def test_is_listing_notice(self):
        notices = self.bithumb_notice_crawler.crawl_notices()
        for notice in notices:
            print(notice.id + " : " + str(self.bithumb_notice_crawler.is_listing_notice(notice)))
    
    def test_extract_symbol(self):
        notices = self.bithumb_notice_crawler.crawl_notices()
        for notice in notices:
            print(self.bithumb_notice_crawler.extract_symbol(notice))

    def test_find_new_listing_symbols(self):
        notices = self.bithumb_notice_crawler.crawl_notices()
        print(self.bithumb_notice_crawler.find_new_listing_symbols(notices))

        new_listing_notice = Notice("123", "[안내] 창립 10주년 기념 - 다섯번째, 100억 기금 '빗썸 나눔 공익재단' 출범")
        notices.insert(0,new_listing_notice)
        print(self.bithumb_notice_crawler.find_new_listing_symbols(notices))

        new_listing_notice = Notice("1234", "[마켓 추가] 테스트(TEST), 테스트123(TEST123) 원화 마켓 추가")
        notices.insert(0,new_listing_notice)
        print(self.bithumb_notice_crawler.find_new_listing_symbols(notices))
        

        

        



if __name__ == '__main__':  
    unittest.main()