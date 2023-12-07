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

    def test_binance_get_flexible_loan_data(self):
        timestamp = generate_timestamp()
        params_loanable_assets = {
            'loanCoin': 'ETH',
            'timestamp': timestamp
        }
        print(self.binance_with_key.sapiGetLoanFlexibleLoanableData(params=params_loanable_assets))

    def test_binance_loan_borrow(self):
        timestamp = generate_timestamp()
        params_loan_borrow = {
        'loanCoin' : 'AAVE',
        'collateralCoin': 'USDT',
        'collateralAmount' : 500, #USDT 기준이다.
        'timestamp': timestamp,
        }
        print(self.binance_with_key.sapiPostLoanFlexibleBorrow(params=params_loan_borrow))

    def test_binance_cross_margin_borrow(self): 
        timestamp = generate_timestamp()
        params_margin_loan = {
        'asset' : 'AAVE',
        'amount': 1, #USDT 기준이 아닌 빌리는 코인 기준으로 수량 입력해야 한다.
        'timestamp': timestamp,
        }
        print(self.binance_with_key.sapiPostMarginLoan(params=params_margin_loan))

# unittest를 실행
if __name__ == '__main__':  
    # 테스트 스위트 생성
    suite = unittest.TestSuite()
    suite.addTest(CcxtTests('test_binance_cross_margin_borrow'))  # 실행할 테스트 추가
    # suite.addTest(MyTestCase('test_two'))  # 다른 테스트 추가

    # 테스트 실행
    runner = unittest.TextTestRunner()
    runner.run(suite)
