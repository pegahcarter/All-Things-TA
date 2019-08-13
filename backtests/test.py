import pandas as pd
import numpy as np

df = pd.read_csv('backtests/BTC.csv').drop('volume', axis=1)
_close = np.array(df['close'])
_open = np.array(df['open'])
low = np.array(df['low'])
high = np.array(df['high'])

ema3 = df['close'].ewm(span=3, adjust=False).mean()
ma20 = df['close'].rolling(window=20).mean().fillna(0)
ema40 = df['close'].ewm(span=40, adjust=False).mean()
ema3_gt_ma20 = ema3 > ma20

cross_indices = []
current_val = ema3_gt_ma20[0]

for i, val in ema3_gt_ma20[1:].items():
    if val != current_val:
        cross_indices.append(i)
    current_val = val

signals = [None for i in range(len(df))]
for cross_index in cross_indices:
    for index in range(cross_index, len(df)):
        rng = set(ema3_gt_ma20[cross_index:index+1])
        if len(rng) == 2:
            break
        elif abs(_close[index] - _open[index])/_close[index] > .02:
            break
        elif True in rng:
            if _close[index] > ema3[index]:
                if ma20[index] > ema40[index]:
                    signals[index] = 'Long'
                break
        else:   # False in rng
            if _close[index] < ema3[index]:
                if ma20[index] < ema40[index]:
                    signals[index] = 'Short'
                break


results = [None for i in range(len(df))]
purchase_prices = [None for i in range(len(df))]
stop_losses = [None for i in range(len(df))]

for signal_index, signal in enumerate(signals):
    if signal is None:
        continue

    if signal == 'Long':
        l_bounds = low
        midrange = _open
        u_bounds = high
        multiplier = .0025
    else:  # signal == 'Short'
        l_bounds = -high
        midrange = -_open
        u_bounds = -low
        multiplier = -.0025

    purchase_price = midrange[signal_index+1] * (1 + multiplier)
    purchase_prices[signal_index] = abs(purchase_price)
    SL = min(l_bounds[signal_index-10:signal_index]) * (1 + multiplier)
    stop_losses[signal_index] = abs(SL)

    diff = purchase_price - SL

    tp1 = purchase_price + diff/2.
    tp2 = purchase_price + diff
    tp3 = purchase_price + diff*2.
    tp4 = purchase_price + diff*3.

    tp_targets = iter([tp1, tp2, tp3, tp4])
    tp_target = next(tp_targets, None)
    result = 0

    for i in range(signal_index, len(df)):
        if result == 4 or midrange[i] < SL or l_bounds[i] < SL:
            break

        while result != 4 and u_bounds[i] > tp_target:
            result += 1
            tp_target = next(tp_targets, None)

        if result == 2:
            SL = purchase_price

    results[signal_index] = result

df['result'] = results
df['purchase-price'] = purchase_prices
df['stop-loss'] = stop_losses

df['stop-loss %'] = abs(df['purchase-price'] - df['stop-loss']) / df['purchase-price']

test = df[['signal', 'result', 'purchase-price', 'stop-loss %']].dropna().reset_index(drop=True)



end_pct =  np.array(map(lambda x: tp_pcts[x], test['result']))
test['gain-loss (%)'] = end_pct * test['stop-loss %']

signal_index = np.array(test.index)
hours_since_last_cross = [signal_index[0]]
hours_since_last_cross += list(signal_index[1:] - signal_index[:-1])

test['hours_since_last_cross'] = hours_since_last_cross
