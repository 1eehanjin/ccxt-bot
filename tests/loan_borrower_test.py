import sys, os
import unittest

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from modules.private_exchange_factory import PrivateExchangeFactory
from modules.loan_borrower import *

class CcxtTests(unittest.TestCase): 
    def setUp(self):
        self.private_exchange_factory = PrivateExchangeFactory()
        self.private_binances = self.private_exchange_factory.create_binance_exchanges()
        self.private_bitgets = self.private_exchange_factory.create_bitget_exchanges()
        self.private_okxs = self.private_exchange_factory.create_okx_exchanges()

        self.binance_loan_borrowers = []
        self.bitget_loan_borrowers = []
        for private_binance in self.private_binances:
            self.binance_loan_borrowers.append(BinanceLoanBorrower(private_binance))

        for private_bitget in self.private_bitgets:
            self.bitget_loan_borrowers.append(BitgetLoanBorrower(private_bitget))


    
    def test_binance_on_new_coin_listing_detected(self):
        for binance_loan_borrower in self.binance_loan_borrowers:
                binance_loan_borrower.on_new_coin_listing_detected(['SLP'])

    @unittest.skip
    def test_bitget_on_new_coin_listing_detected(self):
        for bitget_loan_borrower in self.bitget_loan_borrowers:
                bitget_loan_borrower.on_new_coin_listing_detected(['IMX'])

    @unittest.skip
    def test_exchanges_on_new_coin_listing_detected(self):
        symbols = ["APT"]
        if len(symbols) != 0:
            for binance_loan_borrower in self.binance_loan_borrowers:
                binance_loan_borrower.on_new_coin_listing_detected(symbols)
            for bitget_loan_borrower in self.bitget_loan_borrowers:
                bitget_loan_borrower.on_new_coin_listing_detected(symbols)



        
    
if __name__ == '__main__':  
    unittest.main()