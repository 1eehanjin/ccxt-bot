import json
import time

import ccxt


def generate_timestamp():
    timestamp = int(time.time() * 1000)
    return timestamp

#TODO: 구조 생각해보기
class BinanceController(): 
    def setUp(self):
        with open('/secrets.json') as f:
            secrets = json.load(f)
        api_key = secrets['binance']['api_key']
        secret = secrets['binance']['secret']
        self.binance_with_key = ccxt.binance({
            'apiKey': api_key,
            'secret':secret
        })
        self.binance = ccxt.binance()
        
    def get_available_ccxt_functions(self):
        return(dir(self.binance())) 

    def get_flexible_loan_data(self):
        timestamp = generate_timestamp()
        params_loanable_assets = {
            'loanCoin': 'ETH',
            'timestamp': timestamp
        }
        return(self.binance_with_key.sapiGetLoanFlexibleLoanableData(params=params_loanable_assets))

    def binance_loan_borrow(self, loanCoin, collateralAmount):
        timestamp = generate_timestamp()
        params_loan_borrow = {
        'loanCoin' : loanCoin,
        'collateralCoin': 'USDT',
        'collateralAmount' : collateralAmount, #USDT 기준이다.
        'timestamp': timestamp,
        }
        return(self.binance_with_key.sapiPostLoanFlexibleBorrow(params=params_loan_borrow))

    def binance_cross_margin_borrow(self, asset, amount): 
        timestamp = generate_timestamp()
        params_margin_loan = {
        'asset' : asset,
        'amount': amount, #USDT 기준이 아닌 빌리는 코인 기준으로 수량 입력해야 한다.
        'timestamp': timestamp,
        }
        return(self.binance_with_key.sapiPostMarginLoan(params=params_margin_loan))

    def get_binance_funding_rate(self):   
        fund = self.binance.fapiPublicGetFundingInfo()
        print(fund)

    def get_all_coin_information(self):
        timestamp = generate_timestamp()
        params_all_coin_information = {
            'timestamp': timestamp,
        }
        print(self.binance_with_key.sapiGetCapitalConfigGetall(params=params_all_coin_information))

    def test_binance_withdraw(self): #TODO: 코인 이름하고 양만 넣으면 네트워크랑 내 주소 자동으로 찾아서 출금하도록
        timestamp = generate_timestamp()
        params_withdraw = {
        'coin':'HIGH',
        'network':'BSC',
        'address':'0x8dd0f272737b908b8ADcb931fD38145265154cF3',
        'amount': 40,
        'timestamp': timestamp,
        }
        print(self.binance_with_key.sapiPostCapitalWithdrawApply(params=params_withdraw))