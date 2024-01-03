import ccxt
import telegram
import requests
from datetime import datetime
import time
import json

#참고용 2021년 돌렸던 봇 

#TODO 실행 전 레버리지 확인
binance_leverage = 10


#텔레그램, 거래소 api
telegram_api_key = ''
telegram_bot = telegram.Bot(token = telegram_api_key)
telegram_chat_id = ""

binance_future = ccxt.binance(config={
    'apiKey': '',
    'secret': '',
    'enableRateLimit': False,
    'options': {
        'defaultType': 'future',
    }
})


def sendTelegramMessage(message):
    chat_id = telegram_chat_id
    message = str(message)
    print(len(message))
    if len(message) > 4096:
        for x in range(0, len(message), 4096):
            telegram_bot.send_message(chat_id, message[x:x + 4096])
    else:
        telegram_bot.send_message(chat_id, message)


def binance_set_leverage(leverage):
    # loaded_market 은 레버리지 설정에만 사용하는 마켓 정보(키)
    loaded_markets = binance_future.load_markets()
    keys = loaded_markets.keys()
    for key in keys:
        try:
            binance_future.fapiPrivate_post_leverage({
             'symbol': loaded_markets[key]['id'],
             'leverage': leverage,
            })
            binance_future.fapiPrivatePostMarginType({
                'symbol': loaded_markets[key]['id'],
                'marginType': 'ISOLATED',
            })
        except:
            print(loaded_markets[key]['id'])




def calculate_binance_order_amount(ticker, money): #money는 달러 기준, 가격이 오른채로 주문될수도 있음, 바이낸스는 future 주문만 계산하면 댐
    order_amount = round(money / future_market_info[ticker]["close"])
    return str(order_amount)

def buy_binance_coins_future_per_money(tokens, per_money):
    order_messages = []
    tokens = tokens[:5]
    big_cap_money = per_money / 5
    small_cap_money = per_money / 10
    orders_big_cap = []
    orders_small_cap = []
    for token in tokens:
        order_ticker = token + "USDT"
        order_ticker_for_amount = token + "/USDT"
        order_big_cap = {
            "symbol": order_ticker,
            "side": "BUY",
            "positionSide": "BOTH",
            "type": "MARKET",
            "quantity": calculate_binance_order_amount(order_ticker_for_amount, big_cap_money)
        }
        orders_big_cap.append(order_big_cap)
        order_small_cap = {
            "symbol": order_ticker,
            "side": "BUY",
            "positionSide": "BOTH",
            "type": "MARKET",
            "quantity": calculate_binance_order_amount(order_ticker_for_amount, small_cap_money)
        }
        orders_small_cap.append(order_small_cap)
    orders = orders_big_cap + orders_small_cap + orders_big_cap + orders_small_cap + orders_big_cap
    orders_to_send = orders[:5]
    print(datetime.now())
    for i in range(40):
        params = {
            # 최대 주문 5개
            'batchOrders': binance_future.json(orders_to_send)
        }
        order_message = (binance_future.fapiPrivatePostBatchOrders(params))
        order_messages.append(order_message)
    print(datetime.now())
    return order_messages

def getUpbitNotice(per_page):
    resp = requests.get("https://api-manager.upbit.com/api/v1/notices?page=1&per_page="+per_page+"&thread_name=general").json()
    title = resp['data']['list'][0]['title']
    return title

def categorizeNotice(notice):
    if notice.find("디지털 자산 추가") != -1:
        return "상장"
    if notice.find("에어드랍 지급") != -1:
        return "에어드랍"
    if notice.find("에어드랍 지원") != -1:
        return "에어드랍"
    return "기타"

def categorize_new_market(notice):
    if notice.find("KRW") != -1:
        return "KRW"
    if notice.find("원화") != -1:
        return "KRW"
    return "BTC"

def wait_before_close(notice):
    market_category = categorize_new_market(notice)
    if market_category == "BTC":
        time.sleep(10)
    else:
        time.sleep(120)

#공지사항 받아서 바이낸스 선물 시장에 있는 티커만 뽑아오기
def get_future_tokens(notice):
    start = notice.find('(')
    notice = notice[start + 1:]
    end = notice.find(')')
    notice = notice[:end]
    notice = notice.replace(', ', ' ')
    notice_tickers = notice.split(' ')
    valid_tickers = []
    for notice_ticker in notice_tickers:
        if (notice_ticker+"/USDT") in future_market_tickers:
            valid_tickers.append(notice_ticker)
    return valid_tickers




def buy_tokens(notice, binance_per_money):
        # 바이낸스 주문
    try:
        future_order_tokens = get_future_tokens(notice)
        if len(future_order_tokens) != 0:
            binance_order_message = buy_binance_coins_future_per_money(tokens=future_order_tokens,per_money=binance_per_money)
        else:
            binance_order_message = "선물 코인 갯수 0개"
    except:
        binance_order_message = "바이낸스 에러"
    sendTelegramMessage("aws 매수 완료!!!!!!!!!!!!")

def close_position():
    balance = binance_future.fetch_balance()
    positions = balance['info']['positions']
    for position in positions:
        if float(position['positionAmt']) != 0:
            print(position['symbol'])
            for i in range(10):
                binance_future.create_market_sell_order(symbol=position['symbol'], amount= str(round(float(position['positionAmt'])/10)), params={"reduceOnly": True})
    sendTelegramMessage("aws 매도 완료!!!!!!!!!!!!")


print("---------------------------초기화 시작---------------------------")
prevHour = -1
previousNotice = getUpbitNotice("20")
future_market_info = binance_future.fetch_tickers()
future_market_tickers = future_market_info.keys()


binance_set_leverage(binance_leverage) #todo: 레버리지 설정됐는지 체크
print("---------------------------초기화 완료: " + str(datetime.now()) +"---------------------------")

per_page = []
init_count = 1
for i in range(0, 15):
    per_page.append(str(init_count))
    init_count = init_count + 1
count = 0


# testNotice = '[거래] KRW, BTC 마켓 디지털 자산 추가 (NEAR, YGG)'
# buy_tokens(testNotice, binance_per_money= 50)
# wait_before_close(testNotice)
# close_position()

while True:
    try:
        nowNotice = getUpbitNotice(per_page[count])
        time.sleep(0.3)
        count = count + 1
        count = count % 15
    except:
        print("인터넷 에러")
        continue
    if (nowNotice != previousNotice): #신규 공지
        if(categorizeNotice(nowNotice) == '상장' ):
            # todo: 주문 금액 수정
            # todo: (notice, binance_per_money = 85000 (<= 100000) )
            buy_tokens(notice=nowNotice, binance_per_money=91000)
            wait_before_close(nowNotice)
            close_position()
            break
            # todo: @@@@@@@@@@@@@@@@@@@@@@@@@상장공지가 맨위에서 넘어가고 다시 시작해야 함@@@@@@@@@@@@@@@@@@@
        else:
            now = datetime.now()
            sendTelegramMessage("aws "+ str(now) + nowNotice)
        previousNotice = nowNotice

    now = datetime.now()
    if (now.minute == 13 and prevHour != now.hour):
        prevHour = now.hour

        future_market_info = binance_future.fetch_tickers()
        future_market_tickers = future_market_info.keys()

        message = "aws 정상 구동중" + "\n" + str(now)
        print(message)
        sendTelegramMessage(message)

sendTelegramMessage("aws 재시작 요청")
# todo:@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@멈춘거 다시 시작해야함@@@@@@@@@@@@@@@@@@@@