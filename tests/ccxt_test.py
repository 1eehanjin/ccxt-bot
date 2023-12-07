import unittest
import ccxt
import time
import json
import pprint

def generate_timestamp():
    timestamp = int(time.time() * 1000)
    return timestamp
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
        self.binance = ccxt.binance()

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

    def test_binance_funding_rate(self):   
        fund = self.binance.fapiPublicGetFundingInfo()
        print(fund)

    def test_binance_get_all_coin_information(self):
        timestamp = generate_timestamp()
        params_all_coin_information = {
            'timestamp': timestamp,
        }
        print(self.binance_with_key.sapiGetCapitalConfigGetall(params=params_all_coin_information))

    def test_binance_withdraw(self):
        timestamp = generate_timestamp()
        params_withdraw = {
        'coin':'USDT',
        'network':'MATIC',
        'address':'0x700A0F4442D1F0fa1ee02bE1fE897f32d4A4AB39',
        'amount': 5,
        'timestamp': timestamp,
        }
        print(self.binance_with_key.sapiPostCapitalWithdrawApply(params=params_withdraw))

# unittest를 실행
if __name__ == '__main__':  
    # 테스트 스위트 생성
    suite = unittest.TestSuite()
    suite.addTest(CcxtTests('test_binance_withdraw'))  # 실행할 테스트 추가
    # suite.addTest(MyTestCase('test_two'))  # 다른 테스트 추가

    # 테스트 실행
    runner = unittest.TextTestRunner()
    runner.run(suite)
