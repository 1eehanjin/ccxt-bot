import sys, os
import unittest

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from modules.private_exchange_factory import PrivateExchangeFactory
from modules.funding_fee_retriever import *

class FundingFeeRetrieverTests(unittest.TestCase): 
    def setUp(self):
        self.funding_fee_retriever = FundingFeeRetriever()
    def test_print_funding_fee(self):
        self.funding_fee_retriever.print_funding_fee()
    
if __name__ == '__main__':  
    unittest.main()