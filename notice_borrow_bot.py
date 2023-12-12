import json
import upbit_notice_crawler
import time
import ccxt

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
    
    def on_new_coin_listing_detected(self, symbols):
        for symbol in symbols:
                ccxtBinance.binance_borrow_all(symbol)

    def binance_borrow_all(self, symbol):
        self.binance_loan_borrow(symbol, 50)
        self.binance_cross_margin_borrow(symbol, 1)

if __name__ == '__main__': 
    upbit_notice_crawler = upbit_notice_crawler.UpbitNoticeCrawler()
    ccxtBinance = CcxtBinance()
    while True:
        symbols = upbit_notice_crawler.crawl_listing_symbol()
        if len(symbols) != 0:
            ccxtBinance.on_new_coin_listing_detected(symbols)
        time.sleep(1)