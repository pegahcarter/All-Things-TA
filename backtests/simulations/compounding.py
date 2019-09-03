# This file will simulate a portfolio and return the end total value.
# Hopefully, the gains will compound and we'll see a higher ending value than
#   just the %

import pandas as pd
from py.functions import *
from backtests.simulations.portfolio import Portfolio

btc = pd.read_csv('ohlcv/BTC.csv')
signals = pd.read_csv('signals.csv')

portfolio = Portfolio()
for i, date in enumerate(btc['date']):

    if sum(signals['date'] == date):
        for _, position in signals[signals['date'] == date].iterrows():
            portfolio.open_position(pct_capital=.05, **position)

    if sum(signals['index_closed'] == i):
        for position in list(filter(lambda x: x['index_closed'] == i, portfolio.positions)):
            portfolio.close_position(x_leverage=20, **position)


for position in portfolio.positions:
    portfolio.close_position(x_leverage=20, **position)


portfolio.available_capital



20x @ 5%
495571.1494007507




btc['date'][57] in signals['date']
signals['date'][0] == btc['date'][57]
btc['date'][57] in signals['date']
