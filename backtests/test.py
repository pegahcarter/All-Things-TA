import pandas as pd
import numpy as np

df = pd.read_csv('backtests/BTC.csv')
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

df['signal'] = signals

test = df[df['signal'] == 'Long']
results = [None for i in range(len(df))]


for signal_index, signal in enumerate(signals):
    if signal is None:
        continue

    if signal == 'Long':
        midrange = _open
        l_bounds = low
        u_bounds = high
    else:  # signal == 'Short'
        midrange = -_open
        l_bounds = -high
        u_bounds = -low

    purchase_price = midrange[signal_index+1]
    SL = l_bounds[signal_index-10:signal_index].min()

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





# # ------------------------------------------------------------------------------
# # Testing for single signal
#
# buy = df.iloc[13165]
# SL = df[13155:13165]['low'].min() * .9975
# purchase_price = buy['open']
# diff = purchase_price - SL
# diff_pct = diff / purchase_price
#
# tp1 = purchase_price + diff/2
# tp2 = purchase_price + diff
# tp3 = purchase_price + diff*2
# tp4 = purchase_price + diff*3
#
# tp_targets = iter([tp1, tp2, tp3, tp4])
# tp_target = next(tp_targets, None)
# result = 0
#
# for i, row in df[13165:].iterrows():
#
#     if row['open'] < SL or row['low'] < SL or result == 4:
#         break
#
#     while result != 4 and row['high'] > tp_target:
#         result += 1
#         tp_target = next(tp_targets, None)
#
#     if result == 2:
#         SL = purchase_price
#
# result
