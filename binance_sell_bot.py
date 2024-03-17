import unittest
import ccxt
import time
import json
import pprint
import requests

def generate_timestamp():
    timestamp = int(time.time() * 1000)
    return timestamp

class CcxtBinance(): 
    def __init__(self):
        with open('./secrets.json') as f:
            secrets = json.load(f)

        api_key = secrets['binances'][0]['api_key']
        secret = secrets['binances'][0]['secret']
        self.binance_with_key = ccxt.binance({
            'apiKey': api_key,
            'secret':secret
        })
        self.binance = ccxt.binance()

    def keep_binance_sell(self):
        while True:
            try:
                self.binance_sell()
                break
            except Exception as e: 
                print('예외가 발생했습니다.', e)
                time.sleep(0.2)


    def binance_sell(self):
        result = self.binance_with_key.create_limit_sell_order(symbol="JUP/USDT",amount=1, price=1)
        print(result)



if __name__ == '__main__':  
    CcxtBinance = CcxtBinance()
    CcxtBinance.keep_binance_sell()
