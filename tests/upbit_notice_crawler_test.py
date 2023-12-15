import time
import unittest
import requests
import pprint
import sys, os

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from notice import Notice
import upbit_notice_crawler

class UpbitNoticeCrawlerTests(unittest.TestCase): 
    def setUp(self):
        self.upbit_notice_crawler = upbit_notice_crawler.UpbitNoticeCrawler()

    def test_crawl_notices(self):
        notices = self.upbit_notice_crawler.crawl_notices()
        for notice in notices:
            print(notice.id + " : " + notice.title)

    def test_is_listing_notice(self):
        notices = self.upbit_notice_crawler.crawl_notices()
        for notice in notices:
            print(notice.id + " : " + str(self.upbit_notice_crawler.is_listing_notice(notice)))
    
    def test_extract_symbol(self):
        notices = self.upbit_notice_crawler.crawl_notices()
        for notice in notices:
            print(self.upbit_notice_crawler.extract_symbol(notice))

    def test_find_new_listing_symbols(self):
        notices = self.upbit_notice_crawler.crawl_notices()
        print(self.upbit_notice_crawler.find_new_listing_symbols(notices))

        new_listing_notice = Notice("123", "테스트 공지")
        notices.insert(0,new_listing_notice)
        print(self.upbit_notice_crawler.find_new_listing_symbols(notices))

        new_listing_notice = Notice("1234", "[거래] KRW, BTC 마켓 디지털 자산 추가 (TEST, TEST123)")
        notices.insert(0,new_listing_notice)
        print(self.upbit_notice_crawler.find_new_listing_symbols(notices))


if __name__ == '__main__':  
    unittest.main()