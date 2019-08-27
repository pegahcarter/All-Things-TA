import pandas as pd
from py.functions import find_signals, determine_TP, drop_extra_signals

df = pd.read_csv('ohlcv/BTC.csv')
signals = find_signals(df)
# signals = signals.drop('date', axis=1)

signals[0] = determine_TP(df, signals)
signals['profit_pct'] = abs(signals['price'] - signals['stop_loss']) / signals['price']
tp_pcts = [-1, 0.125, 0.375, 0.875, 1.375]
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
{2: 0.21951263336354462,
 3: 0.12657982144011717,
 4: 0.03910937407662689,
 5: 0.10469911140255642,
 6: 0.1081623571350957,
 7: 0.09190192820910452,
 8: 0.10032542644091526,
 9: 0.09250534818904821}
'''
