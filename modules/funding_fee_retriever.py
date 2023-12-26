import pprint
import ccxt


class FundingFeeRetriever():
    def __init__(self) -> None:
        self.binance = ccxt.binance()
        self.bingx = ccxt.bingx()

    def print_funding_fee(self):
        pprint.pprint(self.binance.fapiPublicGetFundingInfo())
        pprint.pprint(self.bingx.fapiPublicGetFundingInfo())