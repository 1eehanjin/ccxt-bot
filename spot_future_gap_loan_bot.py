import time
from modules.private_exchange_factory import PrivateExchangeFactory
from modules.loan_borrower import *
from modules.arbitrage_finder import *
import modules.message_sender

MIN_VOLUME = 50000
MIN_GAP = 1.02


class SpotFutureGapLoanBot():
    def __init__(self):
        self.arbitrage_finder = ArbitrageFinder(min_volume=MIN_VOLUME, min_gap=MIN_GAP)


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
            spot_future_gaps = self.arbitrage_finder.retrieve_spot_future_gaps()
            symbols = []

            for spot_future_gap in spot_future_gaps:
                if spot_future_gap.count == 5:
                    pprint.pprint(spot_future_gap)
                    symbol = spot_future_gap.symbol.split('/')[0]
                    symbols.append(symbol)
            
            if len(symbols) != 0:
                for binance_loan_borrower in self.binance_loan_borrowers:
                    binance_loan_borrower.on_new_coin_listing_detected(symbols)
                for bitget_loan_borrower in self.bitget_loan_borrowers:
                    bitget_loan_borrower.on_new_coin_listing_detected(symbols)
            #print(datetime.datetime.now())

            time.sleep(5)

    
if __name__ == '__main__': 
    spot_future_gap_loan_bot = SpotFutureGapLoanBot()
    message_sender.send_telegram_message("* 현선갭 론 봇 작동을 시작합니다.")
    try:
        spot_future_gap_loan_bot.work()
    except Exception as e:
        error_message = f"* 오류로 현선갭 론 봇 작동이 종료되었습니다.\n{e}"
        message_sender.send_telegram_message(error_message)