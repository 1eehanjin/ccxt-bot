import pprint
import time
import ccxt

def generate_timestamp():
    timestamp = int(time.time() * 1000)
    return timestamp
class FundingFeeRetriever():
    def __init__(self) -> None:
        self.binance = ccxt.binance()
        self.bingx = ccxt.bingx()

    def print_funding_fee(self):
        #pprint.pprint(self.binance.fetch_funding_rates().keys())
        # bingx_markets = self.bingx.load_markets()
        # pprint.pprint(bingx_markets.keys())
        # for key in bingx_markets.keys():
        #     print(bingx_markets[key])
        params = {
            'symbol':"ETH-USDT",
            'timestamp': generate_timestamp()
        }
        #history
        pprint.pprint(self.bingx.fetch_funding_rate("ETH/USDT:USDT"))
        pprint.pprint(self.bingx.swap_v2_public_get_quote_fundingrate(params=params))
        #current
        pprint.pprint(self.bingx.swapV2PublicGetQuotePremiumIndex(params=params))