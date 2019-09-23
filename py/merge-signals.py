# Merges real backtest signals with actual sent signals
import pandas as pd
from py.functions import *
from datetime import datetime, timedelta

real_signals = pd.read_csv('data/signalsHourly.csv')
backtest_signals = pd.read_csv('data/bitfinex/backtests.csv', usecols=real_signals.columns)

old_signals = backtest_signals[backtest_signals['date'] < real_signals['date'][0]]
merged_signals = old_signals.append(real_signals, sort=False).reset_index(drop=True)

# Save merged signals
merged_signals.to_csv('data/signalsHourly-merged.csv', index=False)
merged_signals['tp'] = None
merged_signals['index_closed'] = None

btc = pd.read_csv('data/bitfinex/BTC.csv')
signals = pd.DataFrame()


for ticker in ['BTC/USD', 'ETH/USD', 'ETH/BTC', 'LTC/BTC', 'EOS/BTC', 'XRP/BTC']:
    coin = ticker[:ticker.find('/')]

    df = pd.read_csv('data/bitfinex/' + coin + '.csv')
    dates = df['date'].tolist()

    coin_signals = merged_signals.loc[merged_signals['ticker'] == ticker]
    coin_signals.index = [dates.index(i) for i in coin_signals['date']]

    if '/BTC' in ticker and ticker != 'BCH/BTC':
        for col in ['open', 'high', 'low', 'close']:
            df[col] /= btc['close']

    tp, index_closed = determine_TP(df, coin_signals, compound=True)
    coin_signals['tp'] = tp
    coin_signals['index_closed'] = index_closed
    coin_signals.reset_index(inplace=True)

    signals = signals.append(coin_signals, ignore_index=True, sort=False)


tp_pcts = [-1, .05, .15, .35, 2.45]
profit_pct = abs(signals['price'] - signals['stop_loss']) / signals['price']
signals['tp'] = signals['tp'].astype('int')
end_pct = list(map(lambda x: tp_pcts[x], signals['tp']))
signals['net_profit'] = end_pct * profit_pct

signals['date'] = signals['date'].apply(lambda x: datetime.strptime(x, '%Y-%m-%d %H:%M:%S'))
hrs_open = signals['index_closed'] - signals['index']
signals['date_closed'] = [date + timedelta(seconds=hrs*60*60) for date, hrs in zip(signals['date'], hrs_open)]

signals = signals\
            .sort_values('date')\
            .reset_index(drop=True)\
            .drop(['index', 'index_closed'], axis=1)\
            .rename(columns={'date': 'date_opened'})

signals.to_csv('data/bitfinex/WORLD CLASS TRADERS BACKTEST RESULTS.csv', index=False)
