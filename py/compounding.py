from functions import *
from portfolio import Portfolio

btc = pd.read_csv('../data/bitfinex/backtests.csv')





signals.head()


portfolio = Portfolio()
for i, date in enumerate(btc['date']):

    if sum(signals['date'] == date):
        for _, position in signals[signals['date'] == date].iterrows():
            portfolio.open_position(pct_capital=.05, **position)

    if sum(signals['index_closed'] == i):
        for position in list(filter(lambda x: x['index_closed'] == i, portfolio.positions)):
            portfolio.close_position(x_leverage=5, **position)


for position in portfolio.positions:
    portfolio.close_position(x_leverage=5, **position)
