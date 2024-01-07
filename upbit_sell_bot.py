import unittest
import ccxt
import time
import json
import pprint
import requests

def generate_timestamp():
    timestamp = int(time.time() * 1000)
    return timestamp

class CcxtUpbit(): 
    def __init__(self):
        with open('./secrets.json') as f:
            secrets = json.load(f)

        api_key = secrets['upbit']['api_key']
        secret = secrets['upbit']['secret']
        self.upbit_with_key = ccxt.upbit({
            'apiKey': api_key,
            'secret':secret
        })
        self.upbit = ccxt.upbit()

    def keep_upbit_sell(self):
        while True:
            try:
                self.upbit_sell()
                break
            except Exception as e: 
                print('예외가 발생했습니다.', e)
                time.sleep(0.2)


    def upbit_sell(self):
        result = self.upbit_with_key.create_limit_sell_order("POWR/KRW",6500, 850)
        result = self.upbit_with_key.create_limit_sell_order("POWR/KRW",6500, 800)
        print(result)



if __name__ == '__main__':  
    ccxtUpbit = CcxtUpbit()
    ccxtUpbit.keep_upbit_sell()
