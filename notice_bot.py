from abc import ABCMeta, abstractmethod
import json
import pprint
from bithumb_notice_crawler import BithumbNoticeCrawler
from upbit_notice_crawler import UpbitNoticeCrawler
from private_exchange_factory import PrivateExchangeFactory
import time
import ccxt
import math
import message_sender
from loan_borrower import *

#TODO: 론봇 작동 피드백 텔레그램 메시지 수정
#TODO: 론 담보 비율 조정하는 코드
#TODO: 업비트 공지 조회하는 방식 바꾸고 공지 조회 텀 줄이기

    
if __name__ == '__main__': 
    upbit_notice_crawler = UpbitNoticeCrawler()
    bithumb_notice_crawler = BithumbNoticeCrawler()

    private_exchange_factory = PrivateExchangeFactory()
    private_binance = private_exchange_factory.create_binance_exchange()
    private_bitget = private_exchange_factory.create_bitget_exchange()

    binance_loan_borrower = BinanceLoanBorrower(private_binance)
    bitget_loan_borrower = BitgetLoanBorrower(private_bitget)

    while True:
        symbols = upbit_notice_crawler.crawl_new_listing_symbols()
        if len(symbols) != 0:
            binance_loan_borrower.on_new_coin_listing_detected(symbols)
            bitget_loan_borrower.on_new_coin_listing_detected(symbols)

        symbols = bithumb_notice_crawler.crawl_new_listing_symbols()
        if len(symbols) != 0:
            binance_loan_borrower.on_new_coin_listing_detected(symbols)
            bitget_loan_borrower.on_new_coin_listing_detected(symbols)

        time.sleep(10)