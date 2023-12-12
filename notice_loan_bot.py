import json
import upbit_notice_crawler
import time
import ccxt
import math
import message_sender

def generate_timestamp():
    timestamp = int(time.time() * 1000)
    return timestamp

class CcxtBinance(): 
    def __init__(self):
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


    def on_new_coin_listing_detected(self, symbols):
        for symbol in symbols:
                #self.binance_borrow_all(symbol)
                self.bitget_loan_borrow(symbol)

    def binance_borrow_all(self, symbol):
        self.binance_loan_borrow(symbol)
        self.binance_cross_margin_borrow(symbol, 1) #TODO: 수량 계산해야함 !

    def binance_loan_borrow(self, symbol):
        timestamp = generate_timestamp()
        collateralAmount = min(self.binance_calculate_colleteral_max_limit(symbol), self.binance_get_account_free_usdt())
        params_loan_borrow = {
        'loanCoin' : symbol,
        'collateralCoin': 'USDT',
        'collateralAmount' : collateralAmount, #USDT 기준이다.
        'timestamp': timestamp,
        }
        print("바이낸스 loan" + str(params_loan_borrow))
        result_message = self.binance_with_key.sapiPostLoanFlexibleBorrow(params=params_loan_borrow)
        message_sender.send_telegram_message(result_message)
        return(result_message)
    
    def binance_calculate_colleteral_max_limit(self, symbol):
        timestamp = generate_timestamp()
        params_loanable_assets = {
            'loanCoin': symbol,
            'timestamp': timestamp
        }
        loan_data = self.binance_with_key.sapiGetLoanFlexibleLoanableData(params=params_loanable_assets)
        loan_max_limit = loan_data['rows'][0]['flexibleMaxLimit']
        colleteral_max_limit = float(loan_max_limit) * 10 / 7
        colleteral_max_limit = math.floor(colleteral_max_limit)
        return colleteral_max_limit


    def binance_get_account_free_usdt(self):
        account_balance = self.binance_with_key.fetch_balance()
        free_usdt_balance =  float(account_balance['USDT']['free'])
        free_usdt_balance = math.floor(free_usdt_balance)
        return free_usdt_balance

    def bitget_loan_borrow(self, symbol):
        collateralAmount = min(self.bitget_calculate_colleteral_max_limit(symbol), self.bitget_get_account_free_usdt())
        params = {"loanCoin": symbol, "pledgeCoin": "USDT", "daily": "THIRTY", "pledgeAmount": str(collateralAmount)}
        print("비트겟 loan" + str(params))
        result_message = self.bitget_with_key.private_spot_post_spot_v1_loan_borrow(params=params)
        message_sender.send_telegram_message(result_message)
        return(result_message)

    def bitget_calculate_colleteral_max_limit(self, symbol):
        bitget_loan_infos = self.bitget.public_spot_get_spot_v1_public_loan_coininfos()['data']['loanInfos']
        colleteral_max_limit = 0
        for info in bitget_loan_infos:
            if info['coin'] == symbol:
                colleteral_max_limit = info['maxUsdt']
        colleteral_max_limit = float(colleteral_max_limit)
        colleteral_max_limit = math.floor(colleteral_max_limit)
        return colleteral_max_limit

    def bitget_get_account_free_usdt(self):
        account_balance = self.bitget_with_key.fetch_balance()
        free_usdt_balance =  float(account_balance['USDT']['free'])
        free_usdt_balance = math.floor(free_usdt_balance)
        return free_usdt_balance

    def binance_cross_margin_borrow(self, symbol, amount): 
        timestamp = generate_timestamp()
        params_margin_loan = {
        'asset' : symbol,
        'amount': amount, #USDT 기준이 아닌 빌리는 코인 기준으로 수량 입력해야 한다.
        'timestamp': timestamp,
        }
        return(self.binance_with_key.sapiPostMarginLoan(params=params_margin_loan))
    

if __name__ == '__main__': 
    upbit_notice_crawler = upbit_notice_crawler.UpbitNoticeCrawler()
    ccxtBinance = CcxtBinance()
    while True:
        symbols = upbit_notice_crawler.crawl_listing_symbol()
        if len(symbols) != 0:
            ccxtBinance.on_new_coin_listing_detected(symbols)
        time.sleep(1)