import pandas as pd
from py.functions import *
from py.variables import tickers
from datetime import datetime, timedelta

signals = pd.read_csv('data/signals/Hourly.csv')
signals = signals.loc[signals['ticker'] != 'ADAU19']

signals['ticker'] = signals['ticker'].apply(lambda x: x.replace('/', ''))
signals['tp'] = None
signals['index_closed'] = None

for ticker in set(signals['ticker']):

    coin_df = pd.read_csv('data/bitmex/' + ticker + '.csv')
    dates = coin_df['date'].tolist()

    coin_signals = signals.loc[signals['ticker'] == ticker]
    coin_signals.index = [dates.index(i) for i in coin_signals['date']]

    tp, index_closed = determine_TP(coin_df, coin_signals, compound=True)
    signals.loc[signals['ticker'] == ticker, 'tp'] = tp
    signals.loc[signals['ticker'] == ticker, 'hrs_open'] = np.subtract(index_closed, coin_signals.index)


tp_pcts = [-1, .05, .15, .35, 2.45]
profit_pct = abs(signals['price'] - signals['stop_loss']) / signals['price']
signals['tp'] = signals['tp'].astype('int')
end_pct = list(map(lambda x: tp_pcts[x], signals['tp']))
signals['net_profit'] = end_pct * profit_pct

signals['date'] = signals['date'].apply(lambda x: datetime.strptime(x, '%Y-%m-%d %H:%M:%S'))

signals.to_csv('data/bitmex/backtests.csv', index=False)
