# Determine the best SL and TP levels for 3EMA, 20MA, and 40EMA
import pandas as pd
from py.functions import find_signals, determine_TP, drop_extra_signals

df = pd.read_csv('ohlcv/BTC.csv')
signals = find_signals(df)
signals['profit_pct'] = abs(signals['price'] - signals['stop_loss']) / signals['price']

signals[0] = determine_TP(df, signals, cushion=0.003)
signals = signals.sort_values('profit_pct')

tp_pcts = [-1, 0.125, 0.375, 0.875, 1.375, 0]
# tp_pcts = [-1, -0.625, 0.375, 0.875, 1.375, 0]
signals['end_pct'] = list(map(lambda x: tp_pcts[x], signals[0]))
signals['net_profit'] = signals['end_pct'] * signals['profit_pct']

for cushion in range(0, 51, 5):
    cushion /= 10000
    tps_hit = determine_TP(df, signals, cushion)
    end_pct = list(map(lambda x: tp_pcts[x], tps_hit))
    profit_pct = signals['profit_pct'] * (1 - cushion)
    signals[cushion] = end_pct * profit_pct

summary = {}
for col in signals.drop(['date', 'signal', 'price', 'stop_loss', 'profit_pct', 'end_pct', 'net_profit'], axis=1):
    summary[col] = signals[col].sum()

summary

'''{
 0: 0.2297598448773858,
 0.0005: 0.26016622740659945,
 0.001: 0.19741595926986252,
 0.0015: 0.24263105736006668,
 0.002: 0.2561520884225171,
 0.0025: 0.32029263384297646,
 0.003: 0.36954038118571375,
 0.0035: 0.3243062764494977,
 0.004: 0.3391283021998393,
 0.0045: 0.298829787977541,
 0.005: 0.2665775667329772
}'''
