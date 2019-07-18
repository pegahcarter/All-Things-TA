import ccxt
import pandas as pd
from datetime import datetime, timedelta
from py.logic import *

b = ccxt.binance()
data = b.fetch_ohlcv('BTC/USDT', '1h')
df = pd.DataFrame(data=data, columns=['date', 'open', 'high', 'low', 'close', 'volume'])
df['date'] = [datetime.fromtimestamp(x/1000) for x in df['date']]
df = pd.read_csv('prices/BTC.csv')[-500:]
df.drop(['open', 'high', 'low', 'volume', 'signal'], axis=1, inplace=True)
df.reset_index(drop=True, inplace=True)
prices = df['close']

df['ema3'] = calc_ema(prices, window=3)
df['ma20'] = calc_ma(prices, window=20)
df['ema40'] = calc_ema(prices, window=40)
df['ema3_gt_ma20'] = df['ema3'] > df['ma20']
df['ma20_gt_ema40'] = df['ma20'] > df['ema40']

intersections = cross(df['ema3'], df['ma20'])
intersections = pd.Series(intersections)

cross_indices = list(intersections[intersections == True].index)
last_cross = cross_indices[-1]
signal = None

for index, close in prices[last_cross:].iteritems():
    segment = df[last_cross:index+1]
    if True and False in set(segment['ema3_gt_ma20']):
        break

    if True in set(segment['ema3_gt_ma20']):
        if segment['close'][index] > segment['ema3'][index] and segment['ma20'][index] > segment['ema40'][index]:
            signal = 'BUY'
            break
    else:   # False in set(segment['ema3_gt_ma20'])
        if segment['close'][index] < segment['ema3'][index] and segment['ma20'][index] < segment['ema40'][index]:
            signal = 'SELL'
            break


index
