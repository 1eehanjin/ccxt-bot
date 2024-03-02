from abc import ABCMeta, abstractmethod
import math
import time
import ccxt
from modules import message_sender 


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
        order_id = result_message['data']['orderId']
        self.add_colleteral(order_id, colleteral_amount)
        return(result_message)
    
    def calcaulte_collateral(self, symbol):
        collateral_max_limit = self.retrieve_collateral_max_limit(symbol)
        account_free_usdt = self.retrieve_account_free_usdt()
        available_usdt = account_free_usdt / 2 #담보 추가를 위해 사용할 수 있는 usdt의 절반만 사용
        collateralAmount = min(collateral_max_limit, available_usdt)
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
    
    def add_colleteral(self, order_id, colleteral_add_amount):
        params_revise_pledge = {
        "orderId" : order_id,
        "amount" : str(colleteral_add_amount),
        "pledgeCoin" : "USDT",
        "reviseType" : 'IN',
        }
        result_message = self.exchange.privateSpotPostSpotV1LoanRevisePledge(params=params_revise_pledge)
        print(result_message)
        
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
        self.add_colleteral(symbol, collateral_amount)
        
        return(result_message)
    
    def calcaulte_collateral(self, symbol):
        collateral_max_limit = self.retrieve_collateral_max_limit(symbol)
        account_free_usdt = self.retrieve_account_free_usdt()
        available_usdt = account_free_usdt / 2
        collateral_amount = min(collateral_max_limit, available_usdt)
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
    
    def add_colleteral(self, symbol, colleteral_add_amount):
        timestamp = generate_timestamp()
        params_add_colleteral = {
            "loanCoin": symbol,
            "collateralCoin": "USDT",
            "direction": "ADDITIONAL",
            "adjustmentAmount": colleteral_add_amount,
            "timestamp": timestamp,
        }
        self.exchange.sapi_post_loan_flexible_adjust_ltv(params=params_add_colleteral)
