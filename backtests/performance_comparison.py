# Determine the best SL and TP levels for 3EMA, 20MA, and 40EMA
import pandas as pd
import numpy as np
import os


# Fixed variable declarations
tp_pcts = {
    0: -1,
    1: -5./8.,
    2: 3./8.,
    3: 7./8.,
    4: 11./8.
}

df = pd.read_csv('backtests/BTC.csv').drop(['date', 'volume'], axis=1)
_open = np.array(df['open'])
_high = np.array(df['high'])
_low = np.array(df['low'])
_close = np.array(df['close'])

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
signals = [None for i in range(len(df))]
for cross_index in cross_indices:
    for index in range(cross_index, len(df)):
        rng = ema3_gt_ma20[cross_index:index+1]
        # End if True and False are in this set, ema3 and ma20 had another intersection
        if True in rng and False in rng:
            break
        # True in rng means the ema3 crossed above ma20
        elif True in rng:
            if _close[index] > ema3[index]:
                if ma20[index] > ema40[index]:
                    if abs(_close[index] - _open[index])/_open[index] > .02:
                        signals[index] = 'Long'
                break
        else:   # False in rng means ema3 crossed below ma20
            if _close[index] < ema3[index]:
                if ma20[index] < ema40[index]:
                    if abs(_close[index] - _open[index])/_open[index] > .02:
                        signals[index] = 'Short'

# Now that we have our signals, test out the different SL & TP levels
# By increments of .05%, find the SL that returns the most profit
for SL_interval in range(.0005, .01, .0005):
    pass








#
