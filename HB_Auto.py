import time
import pyupbit
import datetime
import telegram

telegram_token = "5299852358:AAHne7CII-uH4x8Vk1xOkAZQjAeMMtCUti"
telegram_chat_id = -1001765690834
bot = telegram.Bot(token = telegram_token)

access = "PfJMaEniVO0YB7vpIzo3ZoZvxFKDVJ6JrADN8pS"
secret = "ykOxRbyyDO6BCR9zp7Axy3wnd6xW0p0fBgx2jMy"
win = 0
lose = 0

def get_target_price(ticker, k):
    """변동성 돌파 전략으로 매수 목표가 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="minute60", count=2)
    target_price = df.iloc[0]['close'] + (df.iloc[0]['high'] - df.iloc[0]['low']) * k
    return target_price

def get_start_time(ticker):
    """시작 시간 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="minute60", count=1)
    start_time = df.index[0]
    return start_time

def get_ma15(ticker):
    """33일 이동 평균선 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="minute60", count=33)
    ma15 = df['close'].rolling(33).mean().iloc[-1]
    return ma15

def get_balance(ticker):
    """잔고 조회"""
    balances = upbit.get_balances()
    for b in balances:
        if b['currency'] == ticker:
            if b['balance'] is not None:
                return float(b['balance'])
            else:
                return 0
    return 0

def get_current_price(ticker):
    """현재가 조회"""
    return pyupbit.get_orderbook(ticker=ticker)["orderbook_units"][0]["ask_price"]

# 로그인
upbit = pyupbit.Upbit(access, secret)
print("autotrade start")
start_balance = get_balance("KRW")
bot.sendMessage(chat_id = telegram_chat_id, text = "_____H.B Trading Bot_____\n\nSetting : ma-33 / k = 0.01\n\nStart Balance : %d WON\n\n______Start Trading______\n\nmade by HB." % start_balance)


# 자동매매 시작
while True:
    try:
        now = datetime.datetime.now()
        start_time = get_start_time("KRW-BTC")
        end_time = start_time + datetime.timedelta(minutes=60)

        if start_time < now < end_time - datetime.timedelta(seconds=10):
            target_price = get_target_price("KRW-BTC", 0.01)
            ma15 = get_ma15("KRW-BTC")
            current_price = get_current_price("KRW-BTC")
            if target_price < current_price and ma15 < current_price:
                krw = get_balance("KRW")
                if krw > 5000:
                    upbit.buy_market_order("KRW-BTC", krw*0.9995)
                    krwa = get_balance("KRW")
                    if krwa < krw:
                        bot.sendMessage(chat_id = telegram_chat_id, text = "매수 완료.\n목표금액 %.1f 원 " % target_price)
        else:
            btc = get_balance("BTC")
            if btc > 0.00015:
                upbit.sell_market_order("KRW-BTC", btc*0.9995)
                afkrw = get_balance("KRW")
                total_profit = ((afkrw / start_balance) - 1) * 100
                now_profit = ((afkrw / krw) - 1) * 100
                if krw > afkrw:
                    lose =+ 1
                    winrate = (win / (win + lose)) * 100
                    bot.sendMessage(chat_id = telegram_chat_id, text = "매도 완료.\n거래 전 잔고: %.1f  원\n거래 후 잔고: %.1f 원\n최근거래 수익률: %.2f %%\n총 수익률: %.1f %%\n승 : %d , 패 : %d\n승률: %.2f %%" % (krw, afkrw, now_profit, total_profit, win, lose, winrate))
                if krw < afkrw:
                    win =+ 1
                    winrate = (win / (win + lose)) * 100
                    bot.sendMessage(chat_id = telegram_chat_id, text = "매도 완료.\n거래 전 잔고: %.1f  원\n거래 후 잔고: %.1f 원\n최근거래 수익률: %.2f %%\n총 수익률: %.1f %%\n승 : %d , 패 : %d\n승률: %.2f %%" % (krw, afkrw, now_profit, total_profit, win, lose, winrate))
        time.sleep(1)
    except Exception as e:
        print(e)
        bot.sendMessage(chat_id = telegram_chat_id, text = "Bot ERROR")
        time.sleep(1)
