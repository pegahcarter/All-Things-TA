import pandas as pd
from py.functions import *

df = pd.read_csv('ohlcv/BTC.csv')
signals = find_signals(df)
# signals = signals.drop('date', axis=1)

signals[0] = determine_TP(df, signals)
signals['profit_pct'] = abs(signals['price'] - signals['stop_loss']) / signals['price']
tp_pcts = [-1, 0.05, 0.15, 0.35, 2.45, 0]
signals['end_pct'] = list(map(lambda x: tp_pcts[x], signals[0]))
signals['net_profit'] = signals['end_pct'] * signals['profit_pct']

for gap in range(1,10):
    results = drop_extra_signals(signals, gap=gap)
    signals[gap] = results['net_profit']

summary = {}
for col in signals:
    try:
        if col >=2:
            summary[col] = signals[col].sum()
    except:
        pass


summary
'''
{2: 0.4822496155545545,
 3: 0.388323820452304,
 4: 0.26414628236455484,
 5: 0.2854036248615147,
 6: 0.25582056820183,
 7: 0.2411610864182584,
 8: 0.279613639895204,
 9: 0.2658648850561355}
'''
