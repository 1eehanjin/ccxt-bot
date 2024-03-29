import logging
import unittest
import ccxt
import time
import json
import math
import pprint

from modules.private_exchange_factory import PrivateExchangeFactory

def generate_timestamp():
    timestamp = int(time.time() * 1000)
    return timestamp
class CcxtTests(unittest.TestCase): 
    def setUp(self):
        self.private_exchange_factory = PrivateExchangeFactory()
        self.private_binances = self.private_exchange_factory.create_binance_exchanges()
        self.private_bitgets = self.private_exchange_factory.create_bitget_exchanges()
        self.private_okxs = self.private_exchange_factory.create_okx_exchanges()


        private_binance = self.private_binances[0]
        private_bitget = self.private_bitgets[0]
        private_okx = self.private_okxs[0]
            
        self.binance = ccxt.binance()
        self.bitget = ccxt.bitget()

    @unittest.skip
    def test_print_exchanges(self):
        print(ccxt.exchanges)

    @unittest.skip   
    def test_print_available_binance_functions(self):
        pprint.pprint(dir(self.binance)) 
        pprint.pprint(dir(self.bitget))

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

        result_message = self.private_bitget.privateSpotPostSpotV1LoanRevisePledge(params=params_revise_pledge)

        print(result_message)

    @unittest.skip
    def test_binance_calculate_colleteral_max_limit(self):
        timestamp = generate_timestamp()
        params_loanable_assets = {
            'loanCoin': 'IMX',
            'timestamp': timestamp
        }
        loan_data = self.private_binance.sapiGetLoanFlexibleLoanableData(params=params_loanable_assets)
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
        print(self.private_binance.sapiGetLoanFlexibleLoanableData(params=params_loanable_assets))


    @unittest.skip
    def test_get_account_balance(self):
        account_balance = self.private_binance.fetch_balance()
        pprint.pprint(account_balance)

    @unittest.skip
    def test_get_account_free_usdt(self):
        account_balance = self.private_binance.fetch_balance()
        free_usdt_balance =  account_balance['USDT']['free']
        pprint.pprint(free_usdt_balance)

    @unittest.skip
    def test_bitget_loan_borrow(self):
        symbol = "IMX"
        pledge_usdt_amount = 100
        params = {"loanCoin": symbol, "pledgeCoin": "USDT", "daily": "THIRTY", "pledgeAmount": str(pledge_usdt_amount)}
        print(params)
        print(self.private_bitget.private_spot_post_spot_v1_loan_borrow(params=params))

    @unittest.skip
    def test_binance_loan_borrow(self):
        timestamp = generate_timestamp()
        params_loan_borrow = {
        'loanCoin' : 'AAVE',
        'collateralCoin': 'USDT',
        'collateralAmount' : 500, #USDT 기준이다.
        'timestamp': timestamp,
        }
        print(self.private_binance.sapiPostLoanFlexibleBorrow(params=params_loan_borrow))
    

    @unittest.skip
    def test_binance_cross_margin_borrow(self): 
        timestamp = generate_timestamp()
        params_margin_loan = {
        'asset' : 'AAVE',
        'amount': 1, #USDT 기준이 아닌 빌리는 코인 기준으로 수량 입력해야 한다.
        'timestamp': timestamp,
        }
        print(self.private_binance.sapiPostMarginLoan(params=params_margin_loan))

    @unittest.skip
    def test_binance_funding_rate(self):   
        fund = self.binance.fapiPublicGetFundingInfo()
        print(fund)

    @unittest.skip
    def test_binance_get_coin_network(self):
        timestamp = generate_timestamp()
        symbol = "POWR"
        params_all_coin_information = {
            'timestamp': timestamp,
        }
        all_coin_info = self.private_binance.sapiGetCapitalConfigGetall(params=params_all_coin_information)
        for coin_info in all_coin_info:
            if coin_info['coin'] == symbol:
                print( "<"+coin_info['coin'] +">")
                for network_info in coin_info['networkList']:
                    if network_info["isDefault"]:
                        print("*"+ network_info['network'] )
                    else:
                        print(network_info['network'])
                print("\n")
                
        
    

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
        print(self.private_binance.sapiPostCapitalWithdrawApply(params=params_withdraw))





if __name__ == '__main__':  
    #logging.basicConfig(level=logging.DEBUG)
    unittest.main()
