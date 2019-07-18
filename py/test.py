import ccxt
import pandas as pd
from datetime import datetime, timedelta
from py.logic import *

b = ccxt.binance()
data = b.fetch_ohlcv('BTC/USDT', '1h')
df = pd.DataFrame(data=data, columns=['date', 'open', 'high', 'low', 'close', 'volume'])
df['date'] = [datetime.fromtimestamp(x/1000) for x in df['date']]
df.drop(['open', 'high', 'low', 'volume'], axis=1, inplace=True)

prices = df['close']

ema3 = calc_ema(prices, window=3)
# ema40 = calc_ema(prices, window=40)
ma20 = calc_ma(prices, window=20)
ema3_gt_ma20 = ema3 > ma20
df['ema3'] = ema3
df['ma20'] = ma20
df['ema3_gt_ma20'] = ema3_gt_ma20

intersections = cross(ema3, ma20)
intersections = pd.Series(intersections)

cross_indices = list(intersections[intersections == True].index)
last_cross = cross_indices[-1]

df[last_cross-1:]

prices_test = df[last_cross:]['close']

for index, close in prices_test.iteritems():
    segment = ema3_gt_ma20[last_cross+1:index+1]
    print(len(segment))
    # print(len(segment[segment==True]))
