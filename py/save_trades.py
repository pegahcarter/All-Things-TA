import pandas as pd
from py.functions import *
from datetime import datetime, timedelta

btc = pd.read_csv('ohlcv/BTC.csv')
signals = pd.DataFrame()


for ticker in ['BTC/USD', 'ETH/USD', 'ETH/BTC', 'LTC/BTC', 'EOS/BTC', 'XRP/BTC', 'BCH/BTC']:
    coin = ticker[:ticker.find('/')]
    df = pd.read_csv('ohlcv/' + coin + '.csv', usecols=['date', 'open', 'high', 'low', 'close'])

    if '/BTC' in ticker and ticker != 'BCH/BTC':
        for col in ['open', 'high', 'low', 'close']:
            df[col] /= btc['close']

    coin_signals = find_signals(df)
    # tp, index_closed = determine_TP(df, coin_signals, compound=True)
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

signals['date'] = signals['date'].apply(lambda x: datetime.strptime(x, '%Y-%m-%d %H:%M:%S'))
hrs_open = signals['index_closed'] - signals['index']
signals['date_closed'] = [date + timedelta(seconds=hrs*60*60) for date, hrs in zip(signals['date'], hrs_open)]

signals = signals.sort_values('date').reset_index(drop=True)

signals.to_csv('ohlcv/backtests.csv', index=False)
