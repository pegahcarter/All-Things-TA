# This file will simulate a portfolio and return the end total value.
# Hopefully, the gains will compound and we'll see a higher ending value than
#   just the %

import numpy as np
import pandas as pd
from py.functions import *
from backtests.simulations.portfolio import Portfolio

df = pd.read_csv('ohlcv/ETH.csv')
signals = find_signals(df)

# Step 1: figure out how long the position is open
tp, index_tp_hit = determine_TP(df, signals, compound=True)
signals = signals.reset_index()
signals['tp'] = tp
signals['hrs_position_open'] = np.subtract(index_tp_hit, signals['index'])
signals['index_closed'] = index_tp_hit

# Step 2: figure out the most # of positions open at one time
signals['total_positions_open'] = [sum(signals['index'][i] + signals['hrs_position_open'][i] > signals['index'][i:]) for i in signals.index]

# Step 3: figure out net profit
tp_pcts = [-1, .05, .15, .35, 2.45]
profit_pct = abs(signals['price'] - signals['stop_loss']) / signals['price']
end_pct = list(map(lambda x: tp_pcts[x], signals['tp']))
signals['net_profit'] = profit_pct * end_pct

# Step 4: simulate trading the first signal
signals.head()

ticker = 'ETH/USD'
portfolio = Portfolio()

for i in range(len(df)):
    if i in signals.index:
        portfolio.open_position(ticker, **dict(signals.iloc[list(signals.index).index(i)]))
    elif len(portfolio.positions[ticker]) == 0:
        continue

    if i in map(lambda x: x['index_closed'], portfolio.positions[ticker]):
        for position in list(filter(lambda x: x['index_closed'] == i, portfolio.positions[ticker])):
            portfolio.close_position(ticker, position)


portfolio.positions
portfolio.available_capital

# ETH/USD (2018.08.30)
# 99362.49622200451


signals
