#지정가 매수 걸고
#체결됐는지 확인
#체결됐으면 지정가 매도
#확인하는데 체결 5초이상 안되면 지정가 주문 취소하고 다시 걸기?

import json
import math
import pybithumb
import time

order_btc_amount = 0.002

with open('./secrets.json') as f:
    secrets = json.load(f)

api_key = secrets['bithumb']['api_key']
secret = secrets['bithumb']['secret']
bithumb = pybithumb.Bithumb(api_key, secret)

initial_balance = bithumb.get_balance('btc')[2]
print(initial_balance)
trade_krw = 0

while True:
    if trade_krw > 890000000:
        break


    remain_btc_amount = bithumb.get_balance('btc')[0]
    remain_btc_amount = math.floor(remain_btc_amount * 1000) / 1000 

    if remain_btc_amount < order_btc_amount:
        orderbook_data = bithumb.get_orderbook('BTC')
        bid_price = orderbook_data['bids'][0]['price']

        result = bithumb.buy_limit_order('BTC', bid_price, order_btc_amount - remain_btc_amount)
        time.sleep(0.5)
        outstanding_order_data = bithumb.get_outstanding_order(order_desc=result)
        count = 0
        while outstanding_order_data != None:
            if count > 5 :
                print("지정가  매수 주문 미체결로 취소 뒤 재주문합니다.")
                count = 0
                bithumb.cancel_order(order_desc=result)
                orderbook_data = bithumb.get_orderbook('BTC')
                bid_price = orderbook_data['bids'][0]['price']
                remain_btc_amount = bithumb.get_balance('btc')[0]
                remain_btc_amount = math.floor(remain_btc_amount * 1000) / 1000
                if remain_btc_amount == order_btc_amount:
                    break
                else:
                    result = bithumb.buy_limit_order('BTC', bid_price, order_btc_amount - remain_btc_amount)

            time.sleep(1)
            count += 1
            outstanding_order_data = bithumb.get_outstanding_order(order_desc=result)
        print("지정가 매수 주문 체결 확인")
        trade_krw += bid_price * order_btc_amount

    remain_btc_amount = bithumb.get_balance('btc')[0]
    remain_btc_amount = math.floor(remain_btc_amount * 1000) / 1000 

    if remain_btc_amount > 0:
        orderbook_data = bithumb.get_orderbook('BTC')
        ask_price = orderbook_data['asks'][0]['price']

        result = bithumb.sell_limit_order('BTC', ask_price, remain_btc_amount)
        time.sleep(0.5)
        outstanding_order_data = bithumb.get_outstanding_order(order_desc=result)
        count = 0
        while outstanding_order_data != None:
            if count > 5 :
                print("지정가 매도 주문 미체결로 취소 뒤 재주문합니다.")
                count = 0
                bithumb.cancel_order(order_desc=result)
                remain_btc_amount = bithumb.get_balance('btc')[0]
                orderbook_data = bithumb.get_orderbook('BTC')
                ask_price = orderbook_data['asks'][0]['price']
                remain_btc_amount = math.floor(remain_btc_amount * 1000) / 1000
                if remain_btc_amount == 0:
                    break
                else:
                    result = bithumb.sell_limit_order('BTC', ask_price, remain_btc_amount)
            time.sleep(1)
            count += 1
            outstanding_order_data = bithumb.get_outstanding_order(order_desc=result)
        print("지정가 매도 주문 체결 확인")
        trade_krw += bid_price * order_btc_amount
    print(f"현재 사용금액: {bithumb.get_balance('btc')[2] - initial_balance}")
    print(f"현재 거래량: {trade_krw}")


print(bithumb.get_balance('btc')[2])