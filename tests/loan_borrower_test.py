import sys, os
import unittest

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from modules.private_exchange_factory import PrivateExchangeFactory
from modules.loan_borrower import *

class CcxtTests(unittest.TestCase): 
    def setUp(self):
        private_exchange_factory = PrivateExchangeFactory()
        self.private_binance = private_exchange_factory.create_binance_exchange()
        self.private_bitget = private_exchange_factory.create_bitget_exchange()

    def test_binance_on_new_coin_listing_detected(self):
        loan_borrower = BinanceLoanBorrower(self.private_binance)
        loan_borrower.on_new_coin_listing_detected(["SLP"])

    def test_bitget_on_new_coin_listing_detected(self):
        loan_borrower = BitgetLoanBorrower(self.private_bitget)
        loan_borrower.on_new_coin_listing_detected(["IMX"])
    
if __name__ == '__main__':  
    unittest.main()