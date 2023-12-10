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

        api_key = secrets['binance']['api_key']
        secret = secrets['binance']['secret']
        self.binance_with_key = ccxt.binance({
            'apiKey': api_key,
            'secret':secret
        })
        self.binance = ccxt.binance()

    def keep_binance_withdraw(self):
        while True:
            try:
                self.binance_withdraw()
                break
            except Exception as e: 
                print('예외가 발생했습니다.', e)
                time.sleep(0.2)


    def binance_withdraw(self):
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
    ccxtBinance = CcxtBinance()
    ccxtBinance.keep_binance_withdraw()
