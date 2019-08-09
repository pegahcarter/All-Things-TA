import pandas as pd
import numpy as np

df = pd.read_csv('backtests/BTC.csv')
df['signal'] = None
df['result'] = None
prices = df['close'].copy()

ema3 = prices.ewm(span=3, adjust=False).mean()
ma20 = prices.rolling(window=20).mean().fillna(0)
ema40 = prices.ewm(span=40, adjust=False).mean()
ema3_gt_ma20 = ema3 > ma20

cross_indices = []
current_val = ema3_gt_ma20[0]

for i, val in ema3_gt_ma20[1:].items():
    if val != current_val:
        cross_indices.append(i)
    current_val = val

for cross_index in cross_indices:
    for index, close in prices[cross_index:].iteritems():
        rng = set(ema3_gt_ma20[cross_index:index+1])
        if len(rng) == 2:
            break
        elif True in rng:
            if close > ema3[index]:
                if ma20[index] > ema40[index]:
                    df.loc[index, 'signal'] = 'BUY'
                break
        else:   # False in rng
            if close < ema3[index]:
                if ma20[index] < ema40[index]:
                    df.loc[index, 'signal'] = 'SELL'
                break


test = df[df['signal'] == 'BUY']
test.head()
for signal_index in test.index:
    purchase_price = test.loc[signal_index, 'open']
    SL = df[signal_index-10:signal_index]['low'].min()
    diff = purchase_price - SL

    tp1 = purchase_price + diff/2
    tp2 = purchase_price + diff
    tp2 = purchase_price + diff*2
    tp3 = purchase_price + diff*3

    tp_targets = iter([tp1, tp2, tp3, tp4])
    tp_target = next(tp_targets, None)
    result = 0




# ------------------------------------------------------------------------------

# Testing for single signal
buy = df.iloc[57]
SL = df[47:57]['low'].min()
purchase_price = buy['open']
diff = purchase_price - SL
diff_pct = diff / purchase_price

tp1 = purchase_price + diff/2
tp2 = purchase_price + diff
tp3 = purchase_price + diff*2
tp4 = purchase_price + diff*3

tp_targets = iter([tp1, tp2, tp3, tp4])
tp_target = next(tp_targets, None)
result = 0

for i, row in df[57:].iterrows():

    if row['open'] < SL or row['low'] < SL or result == 4:
        break

    while result != 4 and row['high'] > tp_target:
        result += 1
        tp_target = next(tp_targets, None)

    if result == 2:
        SL = purchase_price

test = {}
test[i] = result
