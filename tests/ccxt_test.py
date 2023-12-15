import logging
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
            secret_data = json.load(f)

        binance_api_key = secret_data['binance']['api_key']
        binance_secret = secret_data['binance']['secret']
        self.binance_with_key = ccxt.binance({
            'apiKey': binance_api_key,
            'secret': binance_secret
        })
        bitget_api_key = secret_data['bitget']['api_key']
        bitget_secret = secret_data['bitget']['secret']
        bitget_password = secret_data['bitget']['password']
        self.bitget_with_key = ccxt.bitget({
            'apiKey': bitget_api_key,
            'secret': bitget_secret,
            'password': bitget_password,
            
        })
        self.binance = ccxt.binance()
        self.bitget = ccxt.bitget()

    @unittest.skip
    def test_print_exchanges(self):
        print(ccxt.exchanges)

    #@unittest.skip   
    def test_print_available_binance_functions(self):
        pprint.pprint(dir(self.binance)) 
        #pprint.pprint(dir(self.bitget))

    @unittest.skip
    def test_bitget_get_all_loan_infos(self):
        pprint.pprint(self.bitget.public_spot_get_spot_v1_public_loan_coininfos())

    @unittest.skip
    def test_bitget_get_loan_max_limit(self):
        symbol = "IMX"
        bitget_loan_infos = self.bitget.public_spot_get_spot_v1_public_loan_coininfos()['data']['loanInfos']
        for info in bitget_loan_infos:
            if info['coin'] == symbol:
                pprint.pprint(info)
                print(str(info['maxUsdt']))
    @unittest.skip    
    def test_bitget_calculate_colleteral_max_limit(self):
        symbol = "IMX"
        bitget_loan_infos = self.bitget.public_spot_get_spot_v1_public_loan_coininfos()['data']['loanInfos']
        loan_max_limit = 0
        for info in bitget_loan_infos:
            if info['coin'] == symbol:
                
                loan_max_limit = float(info['maxUsdt'])
        print(loan_max_limit)
        
    @unittest.skip
    def test_bitget_revise_pledge(self):
        orderId = "1118376454952226817"
        colleteral_add_amount = 6
        params_revise_pledge = {
        "orderId" : orderId,
        "amount" : str(colleteral_add_amount),
        "pledgeCoin" : "USDT",
        "reviseType" : 'IN',
        }

        result_message = self.bitget_with_key.privateSpotPostSpotV1LoanRevisePledge(params=params_revise_pledge)

        print(result_message)

    @unittest.skip
    def test_binance_calculate_colleteral_max_limit(self):
        timestamp = generate_timestamp()
        params_loanable_assets = {
            'loanCoin': 'IMX',
            'timestamp': timestamp
        }
        loan_data = self.binance_with_key.sapiGetLoanFlexibleLoanableData(params=params_loanable_assets)
        loan_max_limit = loan_data['rows'][0]['flexibleMaxLimit']
        print(loan_max_limit)
        colleteral_max_limit = float(loan_max_limit) * 10 / 7
        colleteral_max_limit = math.floor(colleteral_max_limit)
        print(colleteral_max_limit)

    @unittest.skip
    def test_binance_get_flexible_loan_data(self):
        timestamp = generate_timestamp()
        params_loanable_assets = {
            'loanCoin': 'SLP',
            'timestamp': timestamp
        }
        print(self.binance_with_key.sapiGetLoanFlexibleLoanableData(params=params_loanable_assets))


    @unittest.skip
    def test_get_account_balance(self):
        account_balance = self.binance_with_key.fetch_balance()
        pprint.pprint(account_balance)

    @unittest.skip
    def test_get_account_free_usdt(self):
        account_balance = self.binance_with_key.fetch_balance()
        free_usdt_balance =  account_balance['USDT']['free']
        pprint.pprint(free_usdt_balance)

    @unittest.skip
    def test_bitget_loan_borrow(self):
        symbol = "IMX"
        pledge_usdt_amount = 100
        params = {"loanCoin": symbol, "pledgeCoin": "USDT", "daily": "THIRTY", "pledgeAmount": str(pledge_usdt_amount)}
        print(params)
        print(self.bitget_with_key.private_spot_post_spot_v1_loan_borrow(params=params))

    @unittest.skip
    def test_binance_loan_borrow(self):
        timestamp = generate_timestamp()
        params_loan_borrow = {
        'loanCoin' : 'AAVE',
        'collateralCoin': 'USDT',
        'collateralAmount' : 500, #USDT 기준이다.
        'timestamp': timestamp,
        }
        print(self.binance_with_key.sapiPostLoanFlexibleBorrow(params=params_loan_borrow))

    @unittest.skip
    def test_binance_cross_margin_borrow(self): 
        timestamp = generate_timestamp()
        params_margin_loan = {
        'asset' : 'AAVE',
        'amount': 1, #USDT 기준이 아닌 빌리는 코인 기준으로 수량 입력해야 한다.
        'timestamp': timestamp,
        }
        print(self.binance_with_key.sapiPostMarginLoan(params=params_margin_loan))

    @unittest.skip
    def test_binance_funding_rate(self):   
        fund = self.binance.fapiPublicGetFundingInfo()
        print(fund)

    @unittest.skip
    def test_binance_get_all_coin_information(self):
        timestamp = generate_timestamp()
        params_all_coin_information = {
            'timestamp': timestamp,
        }
        print(self.binance_with_key.sapiGetCapitalConfigGetall(params=params_all_coin_information))
    

    @unittest.skip
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





if __name__ == '__main__':  
    #logging.basicConfig(level=logging.DEBUG)
    unittest.main()
