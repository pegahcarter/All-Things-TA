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



results, purchase_prices, stop_losses, stop_losses_pct = [], [], [], []

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

    purchase_price = midrange[signal_index+1]
    SL = min(l_bounds[signal_index-10:signal_index])
    purchase_prices.append(abs(purchase_price))
    stop_losses.append(abs(SL))

    diff = purchase_price - SL
    stop_losses_pct.append(abs(diff / purchase_price))

    tp1 = purchase_price + diff/2.
    tp2 = purchase_price + diff
    tp3 = purchase_price + diff*2.
    tp4 = purchase_price + diff*3.

    tp_targets = [tp1, tp2, tp3, tp4]
    tp = 0

    for i in range(signal_index, len(df)):
        if tp == 4 or midrange[i] < SL or l_bounds[i] < SL:
            break

        while tp != 4 and u_bounds[i] > tp_targets[tp]:
            tp += 1

        if tp >= 2:
            SL = purchase_price



    results.append(tp)



end_pct =  list(map(lambda x: tp_dict[x], results))
np.dot(stop_losses_pct, end_pct)


unique, counts = np.unique(results, return_counts=True)
dict(zip(unique, counts))


hours_since_last_cross = [signal_indices[0]]

hrs_since_cross = list(np.subtract(signal_indices[1:], signal_indices[:-1]))
hrs_since_cross.insert(0, None)
