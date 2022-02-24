import pyupbit
import numpy as np
import telegram

telegram_token = "5299852358:AAHne7CII-uH4x8Vk1xOkAZQjAeMMtCUti4"
telegram_chat_id = 5012920181
bot = telegram.Bot(token = telegram_token)

def get_ror(k=0.5):
    df = pyupbit.get_ohlcv("KRW-BTC", interval="minute60",count=100)
    df['ma5'] = df['close'].rolling(window=20).mean().shift(1)
    df['range'] = (df['high'] - df['low']) * k
    df['target'] = df['open'] + df['range'].shift(1)
    df['bull'] = df['open'] > df['ma5']

    fee = 0.001
    df['ror'] = np.where((df['high'] > df['target']) & df['bull'],
                      df['close'] / df['target'] - fee,
                      1)

    ror = df['ror'].cumprod()[-2]
    return ror


for k in np.arange(0.01, 1.0, 0.01):
    ror = get_ror(k)
    profit = (ror - 1) * 100
    # bot.sendMessage(chat_id = telegram_chat_id, text = "K value: %.2f\n%f\nProfit: %.2f %%" % (k, ror, profit))
    print("k value: %.2f  %f \nProfit: %.2f %%\n" % (k, ror, 
profit))