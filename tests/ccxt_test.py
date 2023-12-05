import unittest
import ccxt

# TestCase를 작성
class CcxtTests(unittest.TestCase): 

    def test_print_exchanges(self):
        print(ccxt.exchanges)
        


# unittest를 실행
if __name__ == '__main__':  
    unittest.main()