import pandas as pd
from py.functions import *

btc = pd.read_csv('ohlcv/BTC.csv')
signals = pd.DataFrame()


for ticker in ['BTC/USD', 'ETH/USD', 'ETH/BTC', 'LTC/BTC', 'EOS/BTC', 'XRP/BTC', 'ADA/BTC']:
    coin = ticker[:ticker.find('/')]
    df = pd.read_csv('ohlcv/' + coin + '.csv', usecols=['date', 'open', 'high', 'low', 'close'])

    if '/BTC' in ticker:
        for col in ['open', 'high', 'low', 'close']:
            df[col] /= btc['close']

    coin_signals = find_signals(df)
    tp, index_closed = determine_TP(df, coin_signals, compound=True)
    coin_signals['tp'] = tp
    coin_signals['index_closed'] = index_closed

    coin_signals['ticker'] = [ticker for i in range(len(coin_signals))]
    coin_signals = coin_signals.reset_index()

    signals = signals.append(coin_signals, ignore_index=True, sort=False)


tp_pcts = [-1, .05, .15, .35, 2.45]
profit_pct = abs(signals['price'] - signals['stop_loss']) / signals['price']
signals['tp'] = signals['tp'].astype('int')
end_pct = list(map(lambda x: tp_pcts[x], signals['tp']))
signals['net_profit'] = end_pct * profit_pct

signals = signals.sort_values('date')
signals['hrs_open'] = signals['index_closed'] - signals['index']

signals.to_csv('ohlcv/WORLD CLASS TRADERS BACKTEST RESULTS.csv', index=False)
