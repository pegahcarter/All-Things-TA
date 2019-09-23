import pandas as pd
from py.functions import *


tp_pcts = [-1, 0.05, 0.15, 0.35, 2.45, 0]
df = pd.read_csv('data/bitfinex/XRP.csv')
df['rsi'] = calc_rsi(df['close'])

signals = find_signals(df)
signals['tp'] = determine_TP(df, signals, cushion=0)
signals['end_pct'] = list(map(lambda x: tp_pcts[x], signals['tp']))
signals['profit_pct'] = abs(signals['price'] - signals['stop_loss']) / signals['price']
signals['net_profit'] = signals['end_pct'] * signals['profit_pct']

signals['rsi'] = df.iloc[signals.index]['rsi']

_long = signals[signals['signal'] == 'Long']
_short = signals[signals['signal'] == 'Short']

_long[_long['rsi'] > 60]['net_profit'].sum()
_long[_long['rsi'] < 60]['net_profit'].sum()


_short[_short['rsi'] > 35]['net_profit'].sum()
_short[_short['rsi'] < 35]['net_profit'].sum()
