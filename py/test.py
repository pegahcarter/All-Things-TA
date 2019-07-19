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

ema3 = calc_ema(prices, window=3)
ma20 = calc_ma(prices, window=20)
ema40 = calc_ema(prices, window=40)
ema3_gt_ma20 = ema3 > ma20

intersections = cross(ema3, ma20)
intersections = pd.Series(intersections)

cross_indices = list(intersections[intersections == True].index)

signal_df = []

for cross_index in cross_indices:
    # last_cross = cross_indices[-1]
    signal = None

    # for index, close in prices[last_cross:].iteritems():
    for index, close in prices[cross_index:].iteritems():
        rng = ema3_gt_ma20[cross_index:index+1]
        if True and False in set(rng):
            break

        if True in set(rng):
            # if close > ema3[index] and ma20[index] > ema40[index]:
            if close > ema3[index]:
                signal = 'BUY'
                break
        else:   # False in set(rng)
            # if close < ema3[index] and ma20[index] < ema40[index]:
            if close < ema3[index]:
                signal = 'SELL'
                break

    if signal:
        signal_df.append([df['date'][index], 'BTC', signal, close])
        # temp = signal_df.loc[signal_df['date'] == df['date'][index]]
        # if len(temp) == 0 or coin not in temp['coin']:
        #     add_signal(coin, date, signal)
