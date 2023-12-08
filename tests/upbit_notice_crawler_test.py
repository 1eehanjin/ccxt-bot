import time
import unittest
import requests
import pprint
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

import upbit_notice_crawler


class UpbitNoticeCrawlerTests(unittest.TestCase): 
    def setUp(self):
        self.upbit_notice_crawler = upbit_notice_crawler.UpbitNoticeCrawler()

    def test_get_upbit_notices(self):
        upbit_notices = self.upbit_notice_crawler.get_upbit_notices()
        print(upbit_notices)
    
    def test_extract_latest_notice_title(self):
        upbit_notices = self.upbit_notice_crawler.get_upbit_notices()
        latest_notice_title = self.upbit_notice_crawler.extract_latest_notice_title(upbit_notices)
        print(latest_notice_title)

    def test_is_listing_notice(self):
        upbit_notices = self.upbit_notice_crawler.get_upbit_notices()
        latest_notice = self.upbit_notice_crawler.extract_latest_notice_title(upbit_notices)
        print(self.upbit_notice_crawler.is_listing_notice(latest_notice))

    def test_abstract_symbol_from_listing_notice(self):
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
        for title in titles:
            print(self.upbit_notice_crawler.extract_symbol_from_listing_notice(title))
        



if __name__ == '__main__':  
    suite = unittest.TestSuite()
    suite.addTest(UpbitNoticeCrawlerTests('test_abstract_symbol_from_listing_notice'))  # 실행할 테스트 추가
    # suite.addTest(MyTestCase('test_two'))  # 다른 테스트 추가

    # 테스트 실행
    runner = unittest.TextTestRunner()
    runner.run(suite)