import time
from modules.private_exchange_factory import PrivateExchangeFactory
from modules.loan_borrower import *
from modules.notice_crawler import *
import modules.message_sender

class NoticeLoanBot():
    def __init__(self):
        self.upbit_notice_crawler = UpbitNoticeCrawler()
        self.bithumb_notice_crawler = BithumbNoticeCrawler()

        self.private_exchange_factory = PrivateExchangeFactory()
        self.private_binances = self.private_exchange_factory.create_binance_exchanges()
        self.private_bitgets = self.private_exchange_factory.create_bitget_exchanges()

        self.binance_loan_borrowers = []
        self.bitget_loan_borrowers = []
        for private_binance in self.private_binances:
            self.binance_loan_borrowers.append(BinanceLoanBorrower(private_binance))

        for private_bitget in self.private_bitgets:
            self.bitget_loan_borrowers.append(BitgetLoanBorrower(private_bitget))

    def work(self):
        while True:
            symbols = self.upbit_notice_crawler.crawl_new_listing_symbols()
            if len(symbols) != 0:
                for binance_loan_borrower in self.binance_loan_borrowers:
                    binance_loan_borrower.on_new_coin_listing_detected(symbols)
                for bitget_loan_borrower in self.bitget_loan_borrowers:
                    bitget_loan_borrower.on_new_coin_listing_detected(symbols)
            #print(datetime.datetime.now())
            symbols = self.bithumb_notice_crawler.crawl_new_listing_symbols()
            if len(symbols) != 0:
                for binance_loan_borrower in self.binance_loan_borrowers:
                    binance_loan_borrower.on_new_coin_listing_detected(symbols)
                for bitget_loan_borrower in self.bitget_loan_borrowers:
                    bitget_loan_borrower.on_new_coin_listing_detected(symbols)
            #print(datetime.datetime.now())
            time.sleep(5)

    
if __name__ == '__main__': 
    notice_loan_bot = NoticeLoanBot()
    message_sender.send_telegram_message("* 공지 론 봇 작동을 시작합니다.")
    try:
        notice_loan_bot.work()
    except Exception as e:
        error_message = f"* 오류로 공지 론 봇 작동이 종료되었습니다.\n{e}"
        message_sender.send_telegram_message(error_message)