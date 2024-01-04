
import ccxt
import time
import json


destination_addresses = [
    "0xd1A5fDbf51798A1201e73A6BCAED2cc3Fcd570e9",
    "0x59E970465Dc722817b35779a307cf3855b0818F2",
    "0xa1d51fc41B34a6222Bc633dbD75DE42053b3E471",
    "0x06049648c6f68c95a6D88bfEC5CB80E13f689131",
    "0xB5f96F96DcaE4BfBA642d8d9B4C0faa785FA55E2",
    "0x39348c29b7d06C066f93eF786b938F484bb4b92d"
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
        
        for destination_address in destination_addresses:
            timestamp = generate_timestamp()
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
