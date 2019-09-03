import pandas as pd
from py.functions import *

btc = pd.read_csv('ohlcv/BTC.csv')
signals = pd.DataFrame()
tickers = {
    'BTC/USD': 5,
    'ETH/USD': 7,
    'ETH/BTC': 3,
    'LTC/BTC': 4,
    'EOS/BTC': 1,
    'XRP/BTC': 6,
    'ADA/BTC': 2
}

for ticker in tickers.keys():
    coin = ticker[:ticker.find('/')]
    df = pd.read_csv('ohlcv/' + coin + '.csv', usecols=['date', 'open', 'high', 'low', 'close'])

    if '/BTC' in ticker:
        for col in ['open', 'high', 'low', 'close']:
            df[col] /= btc['close']

    coin_signals = find_signals(df)
    coin_signals['tp'] = determine_TP(df, coin_signals)

    coin_signals['ticker'] = [tickers[ticker] for i in range(len(coin_signals))]

    signals = signals.append(coin_signals, ignore_index=True, sort=False)


tp_pcts = [-1, .05, .15, .35, 2.45]
profit_pct = abs(signals['price'] - signals['stop_loss']) / signals['price']
signals['tp'] = signals['tp'].astype('int')
end_pct = list(map(lambda x: tp_pcts[x], signals['tp']))
signals['net_profit'] = end_pct * profit_pct

signals['stop_loss'] /= signals['price']
signals['price'] = 1
signals = signals.sort_values('date')
signals.to_csv('ohlcv/WORLD CLASS TRADERS BACKTEST RESULTS.csv', index=False)
