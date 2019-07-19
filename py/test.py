import ccxt
import pandas as pd
from datetime import datetime, timedelta
from py.logic import *

b = ccxt.binance()
coins = ['BTC', 'ETH']
signal_df = []

for coin in coins:

    data = b.fetch_ohlcv(coin + '/USDT', '4h')
    df = pd.DataFrame(data=data, columns=['date', 'open', 'high', 'low', 'close', 'volume'])
    df['date'] = [datetime.fromtimestamp(x/1000) for x in df['date']]
    prices = df['close']

    ema3 = calc_ema(prices, window=3)
    ma20 = calc_ma(prices, window=20)
    ema40 = calc_ema(prices, window=40)
    ema3_gt_ma20 = ema3 > ma20

    intersections = cross(ema3, ma20)
    intersections = pd.Series(intersections)

    cross_indices = list(intersections[intersections == True].index)
    last_signal = None

    for cross_index in cross_indices:
        signal = None

        for index, close in prices[cross_index:].iteritems():
            rng = ema3_gt_ma20[cross_index:index+1]
            if len(set(rng)) == 2:
                break

            if True in set(rng):
                if close > ema3[index] and ma20[index] > ema40[index] and last_signal != 'BUY':
                    signal = True
                    last_signal = 'BUY'
                    break
            else:
                if close < ema3[index] and ma20[index] < ema40[index] and last_signal != 'BUY':
                    signal = True
                    last_signal = 'SELL'
                    break

        if signal:
            signal_df.append([df['date'][index], last_signal, coin, close])

signal_df = pd.DataFrame(signal_df, columns=['date', 'signal', 'coin', 'price'])
signal_df = signal_df.sort_values('date').reset_index(drop=True)

old_signal_df = pd.read_csv('signals.csv')
new_signals = signal_df.loc[signal_df['date'] > old_signal_df['date'].iloc[-1]]

old_signal_df = old_signal_df.append(new_signals, ignore_index=True)
old_signal_df.to_csv('signals.csv', index=False)
