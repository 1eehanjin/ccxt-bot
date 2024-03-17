import sys, os
import unittest

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from modules.private_exchange_factory import PrivateExchangeFactory
from modules.future_buyer import *

class CcxtTests(unittest.TestCase): 
    def setUp(self):
        self.private_exchange_factory = PrivateExchangeFactory()
        self.future_buy_binance = self.private_exchange_factory.create_future_buy_binance()
        self.binance_future_buyer = BinanceFutureBuyer(self.future_buy_binance)
    
    
    def test_binance_adjust_leverage(self):
        self.binance_future_buyer.adjust_leverage(leverage=10)

    @unittest.skip
    def test_binance_on_new_coin_listing_detected(self):
        symbols = ["APT", "STX"]
        money = 100
        if len(symbols) != 0:
            result_message = self.binance_future_buyer.on_new_coin_listing_detected(symbols=symbols, money=money)
        pprint.pprint(result_message)

        
    
if __name__ == '__main__':  
    unittest.main()