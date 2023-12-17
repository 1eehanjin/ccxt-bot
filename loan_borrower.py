from abc import ABCMeta, abstractmethod
import math
import time

import ccxt

import message_sender


def generate_timestamp():
    timestamp = int(time.time() * 1000)
    return timestamp

class AbstractLoanBorrower(metaclass = ABCMeta):
    def __init__(self, exchange):
        self.exchange = exchange

    def on_new_coin_listing_detected(self, symbols):
        for symbol in symbols:
            self.loan_borrow(symbol)

    def loan_borrow(self, symbol):
        try:
            self.try_loan_borrow(symbol)
        except Exception as e:
            error_message = f"*loan borrow 오류 발생*\n심볼: {symbol}\n{e}"
            message_sender.send_telegram_message(error_message)

    @abstractmethod
    def try_loan_borrow(self, symbol):
        pass

    @abstractmethod
    def calcaulte_collateral(self, symbol):
        pass
    @abstractmethod
    def retrieve_collateral_max_limit(self, symbol):
        pass
    @abstractmethod
    def retrieve_account_free_usdt(self):
        pass

class BitgetLoanBorrower(AbstractLoanBorrower):
    def __init__(self, exchange:ccxt.bitget):
            self.exchange = exchange
        
    def try_loan_borrow(self, symbol): 
        colleteral_amount = self.calcaulte_collateral(symbol)
        params = {"loanCoin": symbol, "pledgeCoin": "USDT", "daily": "THIRTY", "pledgeAmount": str(colleteral_amount)}
        print("비트겟 loan" + str(params))
        result_message = self.exchange.private_spot_post_spot_v1_loan_borrow(params=params)
        message_sender.send_telegram_message(result_message)
        return(result_message)
    
    def calcaulte_collateral(self, symbol):
        collateral_max_limit = self.retrieve_collateral_max_limit(symbol)
        account_free_usdt = self.retrieve_account_free_usdt()
        collateralAmount = min(collateral_max_limit, account_free_usdt)
        return collateralAmount

    def retrieve_collateral_max_limit(self, symbol):
        bitget_loan_infos = self.exchange.public_spot_get_spot_v1_public_loan_coininfos()['data']['loanInfos']
        collateral_max_limit = 0
        for info in bitget_loan_infos:
            if info['coin'] == symbol:
                collateral_max_limit = info['maxUsdt']
        collateral_max_limit = float(collateral_max_limit)
        collateral_max_limit = math.floor(collateral_max_limit)
        return collateral_max_limit

    def retrieve_account_free_usdt(self):
        account_balance = self.exchange.fetch_balance()
        free_usdt_balance =  float(account_balance['USDT']['free'])
        free_usdt_balance = math.floor(free_usdt_balance)
        return free_usdt_balance
        
class BinanceLoanBorrower(AbstractLoanBorrower):
    def __init__(self, exchange:ccxt.binance):
        self.exchange = exchange
    
    def try_loan_borrow(self, symbol):
        timestamp = generate_timestamp()
        collateral_amount = self.calcaulte_collateral(symbol)
        params_loan_borrow = {
        'loanCoin' : symbol,
        'collateralCoin': 'USDT',
        'collateralAmount' : collateral_amount, #USDT 기준이다.
        'timestamp': timestamp,
        }
        print("바이낸스 loan" + str(params_loan_borrow))
        result_message = self.exchange.sapiPostLoanFlexibleBorrow(params=params_loan_borrow)
        message_sender.send_telegram_message(result_message)
        return(result_message)
    
    def calcaulte_collateral(self, symbol):
        collateral_max_limit = self.retrieve_collateral_max_limit(symbol)
        account_free_usdt = self.retrieve_account_free_usdt()
        collateral_amount = min(collateral_max_limit, account_free_usdt)
        return collateral_amount

    def retrieve_collateral_max_limit(self, symbol):
        timestamp = generate_timestamp()
        params_loanable_assets = {
            'loanCoin': symbol,
            'timestamp': timestamp
        }
        loan_data = self.exchange.sapiGetLoanFlexibleLoanableData(params=params_loanable_assets)
        loan_max_limit = loan_data['rows'][0]['flexibleMaxLimit']
        collateral_max_limit = float(loan_max_limit) * 10 / 7
        collateral_max_limit = math.floor(collateral_max_limit)
        return collateral_max_limit
    
    def retrieve_account_free_usdt(self):
        account_balance = self.exchange.fetch_balance()
        free_usdt_balance =  float(account_balance['USDT']['free'])
        free_usdt_balance = math.floor(free_usdt_balance)
        return free_usdt_balance