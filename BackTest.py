import pyupbit

import numpy as np



df = pyupbit.get_ohlcv("KRW-BTC", interval="minute120",count=300)



df['ma5'] = df['close'].rolling(window=15).mean().shift(1)

df['range'] = (df['high'] - df['low']) * 0.5

df['target'] = df['open'] + df['range'].shift(1)

df['bull'] = df['open'] > df['ma5']



fee = 0.001

df['ror'] = np.where((df['high'] > df['target']) & df['bull'],

                      df['close'] / df['target'] - fee,

                      1)



df['hpr'] = df['ror'].cumprod()

df['dd'] = (df['hpr'].cummax() - df['hpr']) / df['hpr'].cummax() * 100

profit = (df['hpr'][-1] - 1) * 100

print("MDD: ", df['dd'].max())

print("HPR: ", df['hpr'][-1])

print("Profit: %.2f" % profit,"%")