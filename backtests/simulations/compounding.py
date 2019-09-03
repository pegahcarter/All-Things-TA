# This file will simulate a portfolio and return the end total value.
# Hopefully, the gains will compound and we'll see a higher ending value than
#   just the %

import numpy as np
import pandas as pd
from py.functions import *
from backtests.simulations.portfolio import Portfolio

btc = pd.read_csv('ohlcv/BTC.csv')
signals = pd.DataFrame()

for ticker in ['BTC/USD', 'ETH/USD', 'ETH/BTC', 'LTC/BTC', 'EOS/BTC', 'XRP/BTC', 'ADA/BTC']:
    coin = ticker[:ticker.find('/')]
    df = pd.read_csv('ohlcv/' + coin + '.csv', usecols=['date', 'open', 'high', 'low', 'close'])

    if '/BTC' in ticker:
        btc_slice = btc[btc['date'] >= df['date'][0]]
        for col in ['open', 'high', 'low', 'close']:
            df[col] /= btc_slice['close']

    coin_signals = find_signals(df)
    tp, index_closed = determine_TP(df, coin_signals, compound=True)

    coin_signals['tp'] = tp
    coin_signals['index_closed'] = index_closed
    coin_signals['ticker'] = [ticker for i in range(len(coin_signals))]

    signals = signals.append(coin_signals, ignore_index=True, sort=False)


tp_pcts = [-1, .05, .15, .35, 2.45]
profit_pct = abs(signals['price'] - signals['stop_loss']) / signals['price']
signals['tp'] = signals['tp'].astype('int')
end_pct = list(map(lambda x: tp_pcts[x], signals['tp']))
signals['net_profit'] = end_pct * profit_pct

# Sort signals by date
signals = signals.sort_values('date').reset_index()
portfolio = Portfolio()

for i, date in enumerate(btc['date']):

    if sum(signals['date'] == date):
        for _, position in signals[signals['date'] == date].iterrows():
            portfolio.open_position(pct_capital=.10, **position)

    # if len(portfolio.positions) == 0:
    #     continue

    if sum(signals['index_closed'] == i):
        for position in list(filter(lambda x: x['index_closed'] == i, portfolio.positions)):
            portfolio.close_position(x_leverage=10, **position)


for position in portfolio.positions:
    portfolio.close_position(x_leverage=10, **position)

portfolio.num_positions

portfolio.available_capital






btc['date'][57] in signals['date']
signals['date'][0] == btc['date'][57]
btc['date'][57] in signals['date']
