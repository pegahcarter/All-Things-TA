# Determine the best SL and TP levels for 3EMA, 20MA, and 40EMA
from itertools import permutations
import pandas as pd
import numpy as np
from py.functions import find_signals, determine_TP, drop_extra_signals

df = pd.read_csv('ohlcv/BTC.csv')
signals = find_signals(df)
signals['profit_pct'] = abs(signals['price'] - signals['stop_loss']) / signals['price']

signals['tp'] = determine_TP(df, signals, cushion=0.003)
signals = signals.sort_values('profit_pct')


results = {}
pcts = list(range(10, 71, 10))
pcts *= 4
perms = permutations(pcts, 4)
good_results = [x for x in perms if sum(x) == 100 and len(x) == 4]
tp_combos = set(good_results)
tp_combos.add((25, 25, 25, 25))

for tp_combo in tp_combos:
    tp_combo_pct = np.divide(tp_combo, 100)
    tp1_pct = tp_combo_pct[0]/2.
    tp2_pct = tp1_pct + tp_combo_pct[1]
    tp3_pct = tp2_pct + 2. * tp_combo_pct[2]
    tp4_pct = tp3_pct + 3. * tp_combo_pct[3]
    tp_pcts = [-1, tp1_pct, tp2_pct, tp3_pct, tp4_pct, 0]

    col = '-'.join([str(x) for x in tp_combo])
    signals[col] = signals['tp'].map(lambda x: tp_pcts[x]) * signals['profit_pct']
    results[col] = signals[col].sum()

sorted(results.items(), key=lambda x: x[1])

# BTC
[
 ('10-10-60-20', 0.5074741123070703),
 ('10-20-30-40', 0.5112037499560433),
 ('20-10-10-60', 0.5241633657869483),
 ('10-10-50-30', 0.5293384422077009),
 ('10-20-20-50', 0.533068079856674),
 ('10-10-40-40', 0.5512027721083326),
 ('10-20-10-60', 0.5549324097573052),
 ('10-10-30-50', 0.5730671020089633),
 ('10-10-20-60', 0.594931431909594),
 ('10-10-10-70', 0.6167957618102251)
]

# ETH
]
 ('10-20-30-40', 0.9019411632437655),
 ('10-30-10-50', 0.909113738049395),
 ('20-10-10-60', 0.9268115422443439),
 ('10-10-40-40', 0.9332487030130023),
 ('10-20-20-50', 0.9404212778186314),
 ('10-10-30-50', 0.971728817587868),
 ('10-20-10-60', 0.9789013923934978),
 ('10-10-20-60', 1.0102089321627337),
 ('10-10-10-70', 1.0486890467376)
]
