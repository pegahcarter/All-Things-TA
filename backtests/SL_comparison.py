# Determine the best SL and TP levels for 3EMA, 20MA, and 40EMA
import pandas as pd
from py.functions import find_signals, determine_TP, drop_extra_signals

df = pd.read_csv('ohlcv/BTC.csv')
signals = find_signals(df)
signals['profit_pct'] = abs(signals['price'] - signals['stop_loss']) / signals['price']

signals[0] = determine_TP(df, signals)
signals = signals.sort_values('profit_pct')

tp_pcts = [-1, 0.05, 0.15, 0.35, 2.45, 0]
# tp_pcts = [-1, -0.625, 0.375, 0.875, 1.375, 0]
signals['end_pct'] = list(map(lambda x: tp_pcts[x], signals[0]))
signals['net_profit'] = signals['end_pct'] * signals['profit_pct']

signals.groupby(0).count()['signal']
signals['net_profit'].sum()


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

'''
{
 0: 0.561123106592167,
 0.0005: 0.5241086750042334,
 0.001: 0.4023262039416227,
 0.0015: 0.32273125450471796,
 0.002: 0.2925154041116961,
 0.0025: 0.3402056778481956,
 0.003: 0.2866719477718518,
 0.0035: 0.26716574848959107,
 0.004: 0.3167414860455944,
 0.0045: 0.240843386795134,
 0.005: 0.2261518376295055
}
'''
