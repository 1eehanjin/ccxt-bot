import unittest
import ccxt
import time
import json
import pprint
import requests

def generate_timestamp():
    timestamp = int(time.time() * 1000)
    return timestamp

class CcxtBithumb: 
    def __init__(self):
        with open('./secrets.json') as f:
            secrets = json.load(f)

        api_key = secrets['bithumb']['api_key']
        secret = secrets['bithumb']['secret']
        self.bithumb_with_key = ccxt.bithumb({
            'apiKey': api_key,
            'secret':secret
        })


    def keep_bithumb_sell(self):
        while True:
            try:
                self.bithumb_sell()
                break
            except Exception as e: 
                print('예외가 발생했습니다.', e)
                time.sleep(0.2)


    def bithumb_sell(self):
        result = self.bithumb_with_key.create_limit_sell_order(symbol="ETH/KRW",amount=0.0013, price=5319000)
        print(result)



if __name__ == '__main__':  
    ccxtUpbit = CcxtBithumb()
    ccxtUpbit.keep_bithumb_sell()
