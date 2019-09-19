# Merges real backtest signals with actual sent signals

import pandas as pd

signals = pd.read_csv('ohlcv/WORLD CLASS TRADERS BACKTEST RESULTS.csv')

signals_clean = signals.drop(['index', 'tp', 'index_closed', 'net_profit', 'hrs_open'], axis=1)

old_signals = signals_clean[signals_clean['date'] < '2019-08-03 11:00:00']

real_signals = pd.read_csv('signals/Hourly.csv')
merged_signals = old_signals.append(real_signals, sort=False).reset_index(drop=True)

merged_signals.to_csv('signals/Hourly-merged.csv', index=False)
