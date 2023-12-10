import unittest
import ccxt
import time
import json
import math
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

    def test_binance_calculate_colleteral_max_limit(self):
        timestamp = generate_timestamp()
        params_loanable_assets = {
            'loanCoin': 'SLP',
            'timestamp': timestamp
        }
        loan_data = self.binance_with_key.sapiGetLoanFlexibleLoanableData(params=params_loanable_assets)
        loan_max_limit = loan_data['rows'][0]['flexibleMaxLimit']
        print(loan_max_limit)
        colleteral_max_limit = float(loan_max_limit) * 10 / 7
        colleteral_max_limit = math.floor(colleteral_max_limit)
        print(colleteral_max_limit)

    def test_binance_get_flexible_loan_data(self):
        timestamp = generate_timestamp()
        params_loanable_assets = {
            'loanCoin': 'SLP',
            'timestamp': timestamp
        }
        print(self.binance_with_key.sapiGetLoanFlexibleLoanableData(params=params_loanable_assets))

    def test_binance_calculate_colleteral_max_limit(self):
        timestamp = generate_timestamp()
        params_loanable_assets = {
            'loanCoin': 'SLP',
            'timestamp': timestamp
        }
        loan_data = self.binance_with_key.sapiGetLoanFlexibleLoanableData(params=params_loanable_assets)
        loan_max_limit = loan_data['rows'][0]['flexibleMaxLimit']
        print(loan_max_limit)
        colleteral_max_limit = float(loan_max_limit) * 10 / 7
        colleteral_max_limit = math.floor(colleteral_max_limit)
        print(colleteral_max_limit)

    def test_get_account_balance(self):
        account_balance = self.binance_with_key.fetch_balance()
        pprint.pprint(account_balance)

    def test_get_account_free_usdt(self):
        account_balance = self.binance_with_key.fetch_balance()
        free_usdt_balance =  account_balance['USDT']['free']
        pprint.pprint(free_usdt_balance)

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
        'coin':'HIGH',
        'network':'BSC',
        'address':'0x8dd0f272737b908b8ADcb931fD38145265154cF3',
        'amount': 40,
        'timestamp': timestamp,
        }
        print(self.binance_with_key.sapiPostCapitalWithdrawApply(params=params_withdraw))



# unittest를 실행
if __name__ == '__main__':  
    # 테스트 스위트 생성
    suite = unittest.TestSuite()
    suite.addTest(CcxtTests('test_get_account_free_usdt'))  # 실행할 테스트 추가
    # suite.addTest(MyTestCase('test_two'))  # 다른 테스트 추가

    # 테스트 실행
    runner = unittest.TextTestRunner()
    runner.run(suite)
