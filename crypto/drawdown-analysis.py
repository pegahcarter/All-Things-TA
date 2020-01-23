# Analyzing results of drawdown.py
import pandas as pd
import numpy as np
from TAcharts.indicators import rolling


df = pd.read_csv('../backtests/crypto/drawdown.csv')

# How many hours in a month? Used for rolling drawdown
hrs_per_day = 24
days_per_month = 30
hrs_per_month = hrs_per_day * days_per_month   # 720

total_capital = df['total_capital']

# Rolling puts values at end of period instead of beginning
# So align the first real with first row
thirty_day_min = np.zeros(len(df))
thirty_day_max = np.zeros(len(df))

thirty_day_min[:-719] = rolling(total_capital, n=720, fn='min', axis=1)[719:]
thirty_day_max[:-719] = rolling(total_capital, n=720, fn='max', axis=1)[719:]

df['thirty_day_min'] = thirty_day_min
df['thirty_day_max'] = thirty_day_max

# Calculate rolling monthly max drawdown
df['drawdown_pct'] = (df['thirty_day_min'] - df['total_capital']) / df['total_capital']
df['upside_pct'] =  (df['thirty_day_max'] - df['total_capital']) / df['total_capital']

# Drop rows that do not have a month of data for drawdowns/upside
df = df[:-719].reset_index(drop=True)

df['drawdown_pct'].describe()
df['upside_pct'].describe()

# Calculate how much of portfolio is locked in trade
df['pct_locked_in_trades'] = df['capital_locked_in_trades'] / df['total_capital']

df['pct_locked_in_trades'].max()

df['trades_open'].describe()
df.head()
