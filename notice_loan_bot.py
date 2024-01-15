import time
from modules.private_exchange_factory import PrivateExchangeFactory
from modules.loan_borrower import *
from modules.notice_crawler import *
import modules.message_sender

#TODO: 론봇 성공 피드백 텔레그램 메시지 수정
#TODO: 업비트 공지 조회하는 방식 바꾸고 공지 조회 텀 줄이기

class NoticeLoanBot():
    def __init__(self):
        self.upbit_notice_crawler = UpbitNoticeCrawler()
        self.bithumb_notice_crawler = BithumbNoticeCrawler()

        self.private_exchange_factory = PrivateExchangeFactory()
        self.private_binance = self.private_exchange_factory.create_binance_exchange()
        self.private_bitget = self.private_exchange_factory.create_bitget_exchange()

        self.binance_loan_borrower = BinanceLoanBorrower(self.private_binance)
        self.bitget_loan_borrower = BitgetLoanBorrower(self.private_bitget)

    def work(self):
        while True:
            symbols = self.upbit_notice_crawler.crawl_new_listing_symbols()
            if len(symbols) != 0:
                self.binance_loan_borrower.on_new_coin_listing_detected(symbols)
                self.bitget_loan_borrower.on_new_coin_listing_detected(symbols)
            #print(datetime.datetime.now())
            symbols = self.bithumb_notice_crawler.crawl_new_listing_symbols()
            if len(symbols) != 0:
                self.binance_loan_borrower.on_new_coin_listing_detected(symbols)
                self.bitget_loan_borrower.on_new_coin_listing_detected(symbols)
            #print(datetime.datetime.now())
            #time.sleep(5)

    
if __name__ == '__main__': 
    notice_loan_bot = NoticeLoanBot()
    message_sender.send_telegram_message("* 공지 론 봇 작동을 시작합니다.")
    try:
        notice_loan_bot.work()
    except Exception as e:
        error_message = f"* 오류로 공지 론 봇 작동이 종료되었습니다.\n{e}"
        message_sender.send_telegram_message(error_message)