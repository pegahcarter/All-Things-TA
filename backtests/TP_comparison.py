# Determine the best SL and TP levels for 3EMA, 20MA, and 40EMA
import pandas as pd
import numpy as np
from itertools import permutations
import os

df = pd.read_csv('backtests/BTC.csv').drop(['date', 'volume'], axis=1)
_open, _high, _low, _close = df.T.values

ema3 = df['close'].ewm(span=3, adjust=False).mean()
ma20 = df['close'].rolling(window=20).mean().fillna(0)
ema40 = df['close'].ewm(span=40, adjust=False).mean()
ema3_gt_ma20 = ema3 > ma20

cross_indices = []
current_val = ema3_gt_ma20[0]

# TODO: instead of this next loop, add it into cross_index loop AND make it easy to read
# Find the index of each ema3 and ma20 intersection
for i, val in ema3_gt_ma20[1:].items():
    if val != current_val:
        cross_indices.append(i)
    current_val = val

# Determine which ema3 and ma20 intersections are actually signals
signals = {}
for cross_index in cross_indices:
    for index in range(cross_index, len(df)):
        rng = set(ema3_gt_ma20[cross_index:index+1])
        candle_body_pct = abs(_close[index] - _open[index])/_open[index]
        # End if:
        #   1. True and False are in this set, ema3 and ma20 had another intersection
        #   2. Any candle body after cross is > 2% of price
        if len(rng) == 2 or candle_body_pct > .02:
            break
        # True in rng means the ema3 crossed above ma20
        elif True in rng:
            if _close[index] > ema3[index]:
                if ma20[index] > ema40[index]:
                    signals[index] = 'Long'
                    break
        else:   # False in rng means ema3 crossed below ma20
            if _close[index] < ema3[index]:
                if ma20[index] < ema40[index]:
                    signals[index] = 'Short'
                    break


df = []
for index in signals:
    if signals[index] == 'Long':
        l_bounds = _low
        midrange = _open
        u_bounds = _high
        cushion = 1. + 0.003
    else:  # Signal == 'Short'
        l_bounds = -_high
        midrange = -_open
        u_bounds = -_low
        cushion = 1. - 0.003

    purchase_price = midrange[index+1]
    stop_loss = min(l_bounds[index-10:index]) * cushion
    # stop_loss_pct = abs((purchase_price - stop_loss) / purchase_price)
    stop_loss_pct = abs(1 - stop_loss / purchase_price)

    diff = abs(purchase_price) - abs(stop_loss)
    tp1 = purchase_price + diff/2.
    tp2 = purchase_price + diff
    tp3 = purchase_price + diff*2
    tp4 = purchase_price + diff*3
    tp_targets = [tp1, tp2, tp3, tp4]

    if stop_loss > tp1:
        profit_pct = None
    else:
        tp = 0
        for x in range(index, len(_open)):
            if tp > 0:
                stop_loss = purchase_price
            if tp == 4 or l_bounds[x] < stop_loss:
                break
            while tp < 4 and u_bounds[x] > tp_targets[tp]:
                tp += 1

    df.append([stop_loss_pct, tp])


df = pd.DataFrame(df, columns=['stop_loss_pct', 'tp'])
df.groupby('tp').count()
# df = df[df['tp'] > 0].reset_index(drop=True)

results = {}
pcts = list(range(10, 71, 10))
pcts *= 4
perms = permutations(pcts, 4)
good_results = [x for x in perms if sum(x) == 100 and len(x) == 4]
tp_combos = set(good_results)
for tp_combo in tp_combos:

    tp_combo_pct = np.divide(tp_combo, 100)
    tp1_pct = tp_combo_pct[0]/2.
    tp2_pct = tp1_pct + tp_combo_pct[1]
    tp3_pct = tp2_pct + 2. * tp_combo_pct[2]
    tp4_pct = tp3_pct + 3. * tp_combo_pct[3]
    tp_pcts = [-1, tp1_pct, tp2_pct, tp3_pct, tp4_pct]

    col = '-'.join([str(x) for x in tp_combo])
    df[col] = df['tp'].map(lambda x: tp_pcts[x]) * df['stop_loss_pct']
    results[col] = df[col].sum()

sorted(results.items(), key=lambda x: x[1])



# 10.  10-20-30-40
# 9.   10-50-10-30
# 8.   10-30-20-40
# 7.   10-10-30-50
# 6.   10-40-10-40
# 5.   10-20-20-50
# 4.   10-30-10-50
# 3.   10-10-20-60
# 2.   10-20-10-60
# 1.   10-10-10-70
