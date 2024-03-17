import json
import ccxt


class PrivateExchangeFactory:
    def __init__(self):
        with open('./secrets.json') as f:
            self.secret_data = json.load(f)
            self.secret_data_binances = self.secret_data['binances']
            self.secret_data_bitgets = self.secret_data['bitgets']
            self.secret_data_okxs = self.secret_data['okxs']

    def create_binance_exchanges(self):
        binances_with_key = []
        for secret_data in self.secret_data_binances:
            binance_with_key = ccxt.binance({
                'apiKey': secret_data['api_key'],
                'secret': secret_data['secret'],
            })
            binances_with_key.append(binance_with_key)
        return binances_with_key
    
    def create_bitget_exchanges(self):
        bitgets_with_key = []
        for secret_data in self.secret_data_bitgets:
            bitget_with_key = ccxt.bitget({
                'apiKey': secret_data['api_key'],
                'secret': secret_data['secret'],
                'password': secret_data['password']
            })
            bitgets_with_key.append(bitget_with_key)
        
        return bitgets_with_key
    
    def create_okx_exchanges(self):
        okxs_with_key = []
        for secret_data in self.secret_data_okxs:
            okx_with_key = ccxt.okx({
                'apiKey': secret_data['api_key'],
                'secret': secret_data['secret'],
                'password': secret_data['password']
            })
            okxs_with_key.append(okx_with_key)
        
        return okxs_with_key
    
    def create_future_buy_binance(self):
        future_buy_binance = ccxt.binance({
            'apiKey': self.secret_data['future_buy_binance']['api_key'],
            'secret': self.secret_data['future_buy_binance']['secret'],
            'options': {
                    'defaultType': 'swap'
                }
        })
        return future_buy_binance
    