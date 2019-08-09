import pandas as pd
import numpy as np
from backtests import logic


df = pd.read_csv('backtests/BTC.csv')
df['signal'] = None
prices = df['close'].copy()

ema3 = prices.ewm(span=3, adjust=False).mean()
ma20 = prices.rolling(window=20).mean().fillna(0)
ema40 = prices.ewm(span=40, adjust=False).mean()
ema3_gt_ma20 = ema3 > ma20

cross_indices = []
current_val = ema3_gt_ma20[0]

for i, val in enumerate(ema3_gt_ma20[1:]):
    if val != current_val:
        cross_indices.append(i)
    current_val = val


for cross_index in cross_indices:
    for index, close in enumerate(prices[cross_index:]):
        rng = ema3_gt_ma20[cross_index:index+1]
        if len(set(rng)) == 2:
            break

        if True in set(rng):
            if close > ema3[index]:
                if ma20[index] > ema40[index]:
                    df.loc[index, 'signal'] = 'BUY'
                break
        else:   # False in set(rng)
            if close < ema3[index]:
                if ma20[index] < ema40[index]:
                    df.loc[index, 'signal'] = 'SELL'
                break

df.loc[df['signal'] == 'SELL']


cross_indices

# if signal:
#     coin_signals.append([df['date'][index], last_signal, ticker, round(close, 8)])
#
#     ema3 = prices.ewm(span=3, adjust=False).mean()
#     ema40 = prices.ewm(span=40, adjust=False).mean()
#     ma20 = prices.rolling(window=20).mean().fillna(0)
#     ema3_gt_ma20 = ema3 > ma20
#
#     current_val = ema3_gt_ma20[0]
#     intersections = [False]
#
#     for val in ema3_gt_ma20[1:]:
#         intersections.append(val != current_val)
#         current_val = val
#
#     coin_signals = []
#     for cross_index, intersection in enumerate(intersections):
#         signal = None
#         if intersection:
#             for index, close in enumerate(prices[cross_index:]):
#                 rng = set(ema3_gt_ma20[cross_index:index + 1])
#                 if len(rng) == 2:
#                     break
#                 elif True in rng:
#                     if close > ema3[index]:
#                         if ma20[index] > ema40[index]:
#                             signal = 'BUY'
#                         break
#                 else:
#                     if close < ema3[index]:
#                         if ma20[index] < ema40[index]:
#                             signal = 'SELL'
#                         break
#         if signal:
#             coin_signals.append([df['date'][index], signal, ticker, round(close, 8)])
