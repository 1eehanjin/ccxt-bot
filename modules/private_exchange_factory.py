import json
import ccxt


class PrivateExchangeFactory:
    def __init__(self):
        with open('./secrets.json') as f:
            secret_data = json.load(f)

        self.binance_api_key = secret_data['binance']['api_key']
        self.binance_secret = secret_data['binance']['secret']
        
        self.bitget_api_key = secret_data['bitget']['api_key']
        self.bitget_secret = secret_data['bitget']['secret']
        self.bitget_password = secret_data['bitget']['password']
        

    def create_binance_exchange(self):
        binance_with_key = ccxt.binance({
            'apiKey': self.binance_api_key,
            'secret': self.binance_secret
        })
        return binance_with_key
    
    def create_bitget_exchange(self):
        bitget_with_key = ccxt.bitget({
            'apiKey': self.bitget_api_key,
            'secret': self.bitget_secret,
            'password': self.bitget_password,
        })
        return bitget_with_key
    
