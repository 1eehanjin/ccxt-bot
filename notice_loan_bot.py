import json
import upbit_notice_crawler
import time
import ccxt
import math

def generate_timestamp():
    timestamp = int(time.time() * 1000)
    return timestamp

class CcxtBinance(): 
    def __init__(self):
        with open('./secrets.json') as f:
            secrets = json.load(f)

        api_key = secrets['binance']['api_key']
        secret = secrets['binance']['secret']
        self.binance_with_key = ccxt.binance({
            'apiKey': api_key,
            'secret':secret
        })
        self.binance = ccxt.binance()


    def on_new_coin_listing_detected(self, symbols):
        for symbol in symbols:
                self.binance_borrow_all(symbol)

    def binance_borrow_all(self, symbol):
        self.binance_loan_borrow(symbol)
        self.binance_cross_margin_borrow(symbol, 1)

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
        print(result_message)
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