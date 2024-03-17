from abc import ABCMeta, abstractmethod
import math
import time
import pprint
import ccxt
from modules import message_sender 


def generate_timestamp():
    timestamp = int(time.time() * 1000)
    return timestamp

class AbstractFutureBuyer(metaclass = ABCMeta):
    def __init__(self, exchange):
        self.exchange = exchange

    def on_new_coin_listing_detected(self, symbols, money):
        self.future_buy(symbols=symbols, money=money)

    def future_buy(self, symbols, money):
        try:
            self.try_future_buy(symbols=symbols, money=money)
        except Exception as e:
            error_message = f"*future_buy 오류 발생*\n심볼: {symbols}\n{e}"
            message_sender.send_telegram_message(error_message)

    @abstractmethod
    def try_future_buy(self, symbols, money):
        pass

    @abstractmethod
    def adjust_leverage(self):
        pass


class BinanceFutureBuyer(AbstractFutureBuyer):
    def __init__(self, exchange:ccxt.binance):
        self.exchange = exchange
        self.future_market_info = self.exchange.fetch_tickers()
        self.future_market_tickers = self.future_market_info.keys()
    
    def calculate_binance_order_amount(self, ticker, money): #money는 달러 기준, 가격이 오른채로 주문될수도 있음, 바이낸스는 future 주문만 계산하면 댐
        order_amount = round(money / self.future_market_info[ticker]["close"])
        return str(order_amount)

    def try_future_buy(self, symbols, money):
        order_messages = []
        big_cap_money = money / 5
        small_cap_money = money / 10
        orders_big_cap = []
        orders_small_cap = []
        for symbol in symbols:
            order_ticker = symbol + "USDT"
            order_ticker_for_amount = symbol + "/USDT:USDT"
            order_big_cap = {
                "symbol": order_ticker,
                "side": "BUY",
                "positionSide": "BOTH",
                "type": "MARKET",
                "quantity": self.calculate_binance_order_amount(order_ticker_for_amount, big_cap_money)
            }
            orders_big_cap.append(order_big_cap)
            order_small_cap = {
                "symbol": order_ticker,
                "side": "BUY",
                "positionSide": "BOTH",
                "type": "MARKET",
                "quantity": self.calculate_binance_order_amount(order_ticker_for_amount, small_cap_money)
            }
            orders_small_cap.append(order_small_cap)
        orders = orders_big_cap + orders_small_cap + orders_big_cap + orders_small_cap + orders_big_cap
        orders_to_send = orders[:5]
        pprint.pprint(orders_to_send)
        for i in range(20):
            params = {
                # 최대 주문 5개
                'batchOrders': orders_to_send
            }
            order_message = (self.exchange.fapiPrivatePostBatchOrders(params))
            order_messages.append(order_message)
        pprint.pprint(order_message)
        return order_messages
        
    

    def adjust_leverage(self, leverage=10):
        loaded_markets = self.exchange.load_markets()
        keys = loaded_markets.keys()
        for key in keys:
            timestamp = generate_timestamp()
            try:
                self.exchange.fapiPrivatePostLeverage({
                    'symbol': loaded_markets[key]['id'],
                    'leverage': leverage,
                    'timestamp': timestamp,
                })
                self.exchange.fapiPrivatePostMarginType({
                    'symbol': loaded_markets[key]['id'],
                    'marginType': 'ISOLATED',
                    'timestamp': timestamp,
                })
            except Exception as e:
                print(str(loaded_markets[key]['id']) + " : " + str(e))