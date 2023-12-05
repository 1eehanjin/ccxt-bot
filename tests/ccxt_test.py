import unittest
import ccxt
import time
import json

def generate_timestamp():
    # 타임스탬프 생성
    timestamp = int(time.time() * 1000)
    return timestamp
# TestCase를 작성
class CcxtTests(unittest.TestCase): 
    def setUp(self):
        with open('./secrets.json') as f:
            secrets = json.load(f)

        api_key = secrets['binance']['api_key']
        secret = secrets['binance']['secret']

        self.binance_with_key = ccxt.binance({
            'apiKey': api_key,
            'secret':secret
        })

    def test_print_exchanges(self):
        print(ccxt.exchanges)
        
    def test_print_available_binance_functions(self):
        print(dir(ccxt.binance())) 

    def test_get_flexible_loan_data(self):
        timestamp = generate_timestamp()
        params_loanable_assets = {
            'loanCoin': 'ETH',
            'timestamp': timestamp
        }
        print(self.binance_with_key.sapiGetLoanFlexibleLoanableData(params=params_loanable_assets))

    def test_loan_borrow(self):
        timestamp = generate_timestamp()
        params_loan_borrow = {
        'loanCoin' : 'BNT',
        'collateralCoin': 'USDT',
        'collateralAmount' : 500,
        'timestamp': timestamp,
    }
        print(self.binance_with_key.sapiPostLoanFlexibleBorrow(params=params_loan_borrow))

# unittest를 실행
if __name__ == '__main__':  
    # 테스트 스위트 생성
    suite = unittest.TestSuite()
    suite.addTest(CcxtTests('test_loan_borrow'))  # 실행할 테스트 추가
    # suite.addTest(MyTestCase('test_two'))  # 다른 테스트 추가

    # 테스트 실행
    runner = unittest.TextTestRunner()
    runner.run(suite)
