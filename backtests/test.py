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


signals = {}
for cross_index in cross_indices:
    for index in range(cross_index, len(df)):
        rng = set(ema3_gt_ma20[cross_index:index+1])
        candle_body_pct = abs(_close[index] - _open[index])/_open[index]
        if len(rng) == 2 or candle_body_pct > .02:
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


profit_levels = [-1, -5./8., 3./8., 7./8., 11./8.]
df2 = []

for signal_index, signal in signals.items():
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

    purchase_price = midrange[signal_index+1]
    stop_loss = min(l_bounds[signal_index-10:signal_index]) * (1 - multiplier)
    SL = stop_loss

    diff = purchase_price - SL
    tp1 = purchase_price + diff/2.
    tp2 = purchase_price + diff
    tp3 = purchase_price + diff*2.
    tp4 = purchase_price + diff*3.

    tp_targets = [tp1, tp2, tp3, tp4]
    tp = 0

    for i in range(signal_index, len(df)):
        while tp != 4 and u_bounds[i] > tp_targets[tp]:
            tp += 1

        if tp == 4 or midrange[i] < SL or l_bounds[i] < SL:
            break

        if tp >= 2:
            SL = purchase_price

    df2.append([signal_index, signal, tp, profit_levels[tp], abs(purchase_price), abs(stop_loss)])

df2 = pd.DataFrame(df2, columns=['index', 'signal', 'tp_hit', 'profit_level', 'purchase_price', 'stop_loss']).sort_values('index')
df2['stop_loss_pct'] = abs(df2['stop_loss'] - df2['purchase_price']) / df2['purchase_price']
df2['profit'] = df2['profit_level'] * df2['stop_loss_pct']




hours_since_last_cross = [signal_indices[0]]
hrs_since_cross = list(np.subtract(signal_indices[1:], signal_indices[:-1]))
hrs_since_cross.insert(0, None)




test = {12: 'Long', 14: 'Short', 20: 'Long'}
