
import ccxt
import time
import json


destination_addresses = [
    '0xd17f61Fd1EB2DE9989f2594fD3d734c99Cc419e8',
    '0xE01495dE5385b315d597Af8Da1266244BeC10a67',
    '0xf36284246d02A8E58736d68365829408d8e66451',
    '0x7800B5822Eb4cBaFBA05aa88a0D5F3302d03F172',
    '0xbDb2b74f28E3b22ad28b96f025f5cd17384123a1',
    '0xaBdAAbff32d318654CE5ea398EC39f0F429F0c47',
]

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

    def distribute(self):
        timestamp = generate_timestamp()
        for destination_address in destination_addresses:
            params_withdraw = {
            'coin':'BNB',
            'network':'BSC',
            'address':destination_address,
            'amount': 0.009,
            'timestamp': timestamp,
            }
            print(self.binance_with_key.sapiPostCapitalWithdrawApply(params=params_withdraw))
            params_withdraw = {
            'coin':'BNB',
            'network':'OPBNB',
            'address':destination_address,
            'amount': 0.009,
            'timestamp': timestamp,
            }
            print(self.binance_with_key.sapiPostCapitalWithdrawApply(params=params_withdraw))



if __name__ == '__main__':  
    ccxtBinance = CcxtBinance()
    ccxtBinance.distribute()
