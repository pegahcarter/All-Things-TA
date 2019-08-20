# Determine the best SL and TP levels for 3EMA, 20MA, and 40EMA
import pandas as pd
import numpy as np
import os

# Fixed variable declarations
tp_pcts = [-1, -5./8., 3./8., 7./8., 13./8.]

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

df = pd.DataFrame()
# Now that we have our signals, test out the different SL & TP levels
# By increments of .05%, find the SL that returns the most profit
for multiplier in range(15, 75, 2):
    multiplier /= 10000.
    profit_pct_list = []
    for index in signals:
        if signals[index] == 'Long':
            l_bounds = _low
            midrange = _open
            u_bounds = _high
            cushion = 1. + multiplier
        else:  # Signal == 'Short'
            l_bounds = -_high
            midrange = -_open
            u_bounds = -_low
            cushion = 1. - multiplier

        purchase_price = midrange[index+1]
        stop_loss = min(l_bounds[index-10:index]) * cushion
        stop_loss_pct = (purchase_price - stop_loss) / purchase_price

        diff = purchase_price - stop_loss
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
                while tp < 4 and u_bounds[x] > tp_targets[tp]:
                    tp += 1
                if tp >= 2:
                    stop_loss = purchase_price
                if tp == 4 or l_bounds[x] < stop_loss:
                    break
            profit_pct = stop_loss_pct * tp_pcts[tp]

        profit_pct_list.append(profit_pct)
    df[abs(multiplier)] = profit_pct_list


results = {}
for col in df.columns:
    results[col] = round(df[col].dropna().sum(), 4)

results
