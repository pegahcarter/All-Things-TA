import pandas as pd
from py.functions import find_signals, determine_TP, drop_extra_signals

df = pd.read_csv('backtests/BTC.csv')
signals = find_signals(df)
# signals = signals.drop('date', axis=1)

signals[0] = determine_TP(df, signals)

for gap in range(6,41,2):
    results = drop_extra_signals(signals, gap=gap)
    signals[gap] = results[0]

signals.head()

cols = ['date', 'signal', 'price', 'stop_loss', 'profit_pct']
signals['profit_pct'] = abs(signals['price'] - signals['stop_loss']) / signals['price']

results = signals.drop(cols, axis=1).groupby(0).count()

summary = {}
for col in results:
    summary[col] = {
        'mean': signals[col].mean(),
        'median': signals[col].median()
    }

summary
