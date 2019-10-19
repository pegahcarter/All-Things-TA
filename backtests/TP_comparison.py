# Determine the best SL and TP levels for 3EMA, 20MA, and 40EMA
from itertools import permutations
import pandas as pd
import numpy as np
from py.functions import find_signals, determine_TP, drop_extra_signals

btc = pd.read_csv('data/bitfinex/BTC.csv')
signals = pd.DataFrame()

for ticker in ['BTC/USD', 'ETH/USD', 'ETH/BTC', 'LTC/BTC', 'EOS/BTC', 'XRP/BTC']:
    coin = ticker[:ticker.find('/')]
    df = pd.read_csv('data/bitfinex/' + coin + '.csv', usecols=['date', 'open', 'high', 'low', 'close'])
    if '/BTC' in ticker:
        btc_slice = btc[btc['date'] >= df['date'][0]]
        for col in ['open', 'high', 'low', 'close']:
            df[col] /= btc_slice['close']

    coin_signals = find_signals(df, window_fast=5, window_mid=20, window_slow=56)
    coin_signals['tp'] = determine_TP(df, coin_signals)
    coin_signals['ticker'] = [ticker for i in range(len(coin_signals))]
    coin_signals = coin_signals.reset_index()
    signals = signals.append(coin_signals, ignore_index=True, sort=False)


signals['profit_pct'] = abs(signals['price'] - signals['stop_loss']) / signals['price']
signals = signals.sort_values('profit_pct')
signals.groupby('tp').count()['date'] / len(signals)
tp_pcts = [-1, 0.05, 0.15, 0.35, 2.45, 0]
end_pct = list(map(lambda x: tp_pcts[x], signals['tp']))
signals['net_profit'] = end_pct * signals['profit_pct']
signals['net_profit'].sum()

# Current
1181, 3.8

0    340
1    414
2    168
3     67
4    192


# Ignoring a lot
len(signals)




results = {}
pcts = list(range(0, 101, 10))
pcts *= 4
perms = permutations(pcts, 4)
# good_results = [x for x in perms if sum(x) == 100 and len(x) == 4]
good_results = [x for x in perms if sum(x) == 100]
tp_combos = set(good_results)
# tp_combos.add((25, 25, 25, 25))

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

sorted(results.items(), key=lambda x: x[1], reverse=True)

sorted(results.items(), key=lambda x: x[1], reverse=True)


# BTC
[
 ('10-20-30-40', 0.4193),
 ('20-10-20-50', 0.4376),
 ('10-10-50-30', 0.4467),
 ('10-20-20-50', 0.4479),
 ('20-10-10-60', 0.4662),
 ('10-10-40-40', 0.4753),
 ('10-20-10-60', 0.4765),
 ('10-10-30-50', 0.5039),
 ('10-10-20-60', 0.5325),
 ('10-10-10-70', 0.5611)
]


# ETH
[
 ('10-20-30-40', 1.2017),
 ('10-20-20-50', 1.2056),
 ('10-20-10-60', 1.2094),
 ('10-10-70-10', 1.2452),
 ('10-10-60-20', 1.2491),
 ('10-10-50-30', 1.2530),
 ('10-10-40-40', 1.2568),
 ('10-10-30-50', 1.2607),
 ('10-10-20-60', 1.2645),
 ('10-10-10-70', 1.2684)
]
