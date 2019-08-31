# This file will simulate a portfolio and return the end total value.
# Hopefully, the gains will compound and we'll see a higher ending value than
#   just the %

import numpy as np
import pandas as pd
from py.functions import *
from backtests.simulations.portfolio import Portfolio

tp_pcts = [-1, .05, .15, .35, 2.45]
signals = pd.DataFrame()


for coin in ['BTC', 'ETH', 'LTC']:
    ticker = coin + '/USD'
    df = pd.read_csv('ohlcv/' + coin + '.csv')
    coin_signals = find_signals(df)
    tp, index_tp_hit = determine_TP(df, coin_signals, compound=True)
    coin_signals['tp'] = tp
    coin_signals['index_tp_hit'] = index_tp_hit
    coin_signals['ticker'] = [coin + '/USD' for i in range(len(coin_signals))]
    coin_signals = coin_signals.reset_index()

    profit_pct = abs(coin_signals['price'] - coin_signals['stop_loss']) / coin_signals['price']
    end_pct = list(map(lambda x: tp_pcts[x], coin_signals['tp']))
    coin_signals['net_profit'] = profit_pct * end_pct

    signals = signals.append(coin_signals, ignore_index=True, sort=False)

# Sort signals by date
signals = signals.sort_values('date').reset_index(drop=True)

# Step 2: figure out the most # of positions open at one time
signals['hrs_position_open'] = np.subtract(signals['index_tp_hit'], signals['index'])
signals['total_positions_open'] = [sum(signals['index'][i] + signals['hrs_position_open'][i] > signals['index'][i:]) for i in signals.index]
# list(signals['total_positions_open']).index(signals['total_positions_open'].max())

portfolio = Portfolio()
for i in range(len(df)):
    if i in signals['index']:
        for _, position in signals[signals['index'] == i].iterrows():
            portfolio.open_position(**position)
    elif len(portfolio.positions) == 0:
        continue

    if i in map(lambda x: x['index_tp_hit'], portfolio.positions):
        for position in list(filter(lambda x: x['index_tp_hit'] == i, portfolio.positions)):
            portfolio.close_position(position)


len(df)

signals[10:20]

signals['index'][15] in range(0, 1200)


i
portfolio.positions
portfolio.available_capital
portfolio.num_positions
