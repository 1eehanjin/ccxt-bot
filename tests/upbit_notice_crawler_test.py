import time
import unittest
import requests
import pprint
import sys, os

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from notice import Notice
import upbit_notice_crawler

titles = [
            "[거래] BTC 마켓 디지털 자산 추가 (AXL)",
            "[거래] BTC 마켓 디지털 자산 추가 (ID)",
            "[거래] KRW 마켓 디지털 자산 추가 (MINA)",
            "[거래] BTC 마켓 디지털 자산 추가 (GLMR) (GLMR 출금 수수료 일시 상향 안내)",
            "[거래] BTC 마켓 디지털 자산 추가 (CYBER)",
            "[거래] KRW, BTC 마켓 디지털 자산 추가 (SEI) (매도 주문 제한 기준 가격 변경 안내)",
            "[거래] BTC 마켓 디지털 자산 추가 (STG)",
            "[거래] KRW 마켓 디지털 자산 추가 (IMX)",
            "[거래] BTC 마켓 디지털 자산 추가 (MINA)",
            "[거래] KRW 마켓 디지털 자산 추가 (BLUR)",
            "[거래] KRW 마켓 디지털 자산 추가 (GRT)",
            "[거래] KRW, BTC 마켓 디지털 자산 추가 (SUI) (매도 주문 제한 기준 가격 안내)",
            "[거래] KRW, BTC 마켓 디지털 자산 추가 (EGLD)",
            "[거래] KRW, BTC 마켓 디지털 자산 추가 (ARB)",
            "[거래] BTC 마켓 디지털 자산 추가 (MAGIC)",
            "[거래] KRW, BTC 마켓 디지털 자산 추가 (MASK, ACS)",
            "[거래] BTC 마켓 디지털 자산 추가 (BLUR)",
            "[거래] BTC 마켓 디지털 자산 추가 (ASTR) (거래지원 개시 시점 연기 안내)"
        ]
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