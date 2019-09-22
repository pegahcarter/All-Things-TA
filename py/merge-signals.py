# Merges real backtest signals with actual sent signals
import pandas as pd

# NOTE: this takes backtests.csv signals as previous signals
# signals = pd.read_csv('ohlcv/WORLD CLASS TRADERS BACKTEST RESULTS.csv')
signals = pd.read_csv('ohlcv/backtests.csv')

signals_clean = signals.drop(['index', 'tp', 'index_closed', 'net_profit', 'hrs_open'], axis=1)

real_signals = pd.read_csv('signals/Hourly.csv')
old_signals = signals_clean[signals_clean['date'] < real_signals['date'][0]]

merged_signals = old_signals.append(real_signals, sort=False).reset_index(drop=True)

merged_signals.to_csv('signals/Hourly-merged.csv', index=False)


btc = pd.read_csv('ohlcv/BTC.csv')
dates = btc['date'].tolist()

merged_signals.index = merged_signals['date'].apply(lambda x: dates.index(x))
merged_signals['tp'] = None
merged_signals['index_closed'] = None

for ticker in set(merged_signals['ticker']):
    coin = ticker[:ticker.find('/')]
    df = pd.read_csv('ohlcv/' + coin + '.csv')
    coin_signals = merged_signals.loc[merged_signals['ticker'] == ticker]

    if '/BTC' in ticker:
        for col in ['open', 'high', 'low', 'close']:
            df[col] /= btc['close']

    tp, index_closed = determine_TP(df, coin_signals, compound=True)
    coin_signals['tp'] = tp
    coin_signals['index_closed'] = index_closed








test.head()









coin_signals = merged_signals[merged_signals['ticker'] == 'BTC/USD']
