from py.functions import *
import numpy as np
import pandas as pd

tickers = ['BTC/USD', 'ETH/USD', 'ETH/BTC', 'LTC/BTC', 'EOS/BTC', 'XRP/BTC']
tp_pcts = [-1, .05, .15, .35, 2.45]

avg1 = range(2,8)
avg2 = range(6,36,2)
avg3 = range(20, 80, 4)
avgs_combined = [[a1, a2, a3] for a1 in avg1 for a2 in avg2 for a3 in avg3]
avgs_combined = [[a1, a2, a3] for a1 in avg1 for a2 in avg2 for a3 in avg3 if a1 != a2 and a2 != a3]
len(avgs_combined)



btc = pd.read_csv('ohlcv/BTC.csv')
results = pd.DataFrame(columns=['average'] + tickers)
results['average'] = avgs_combined

for ticker in tickers:
    coin = ticker[:ticker.find('/')]
    df = pd.read_csv('ohlcv/' + coin + '.csv', usecols=['date', 'open', 'high', 'low', 'close'])

    if '/BTC' in ticker and ticker != 'BCH/BTC':
        for col in ['open', 'high', 'low', 'close']:
            df[col] /= btc['close']

    net_profit = []
    for avg in avgs_combined:
        coin_signals = find_signals(df, gap=0, ema_fast=avg[0], ma_mid=avg[1], ema_slow=avg[2])
        tp = determine_TP(df, coin_signals)

        profit_pct = abs(coin_signals['price'] - coin_signals['stop_loss']) / coin_signals['price']
        end_pct = list(map(lambda x: tp_pcts[x], tp))
        net_profit.append(np.dot(profit_pct, end_pct))

    results[ticker] = net_profit


results.to_csv('backtests/optimize_moving_avg.csv', index=False)

# Analyzing results
df = pd.read_csv('backtests/optimize_moving_avg.csv')

mean_performance = [row.mean() for _, row in df.drop(['average'], axis=1).iterrows()]
total_performance = [row.sum() for _, row in df.drop(['average'], axis=1).iterrows()]

df['mean'] = mean_performance
df['total'] = total_performance

df.sort_values('mean', ascending=False)[61:120]

btc = pd.read_csv('ohlcv/BTC.csv')
coin_signals = find_signals(btc, ema_fast=5, ma_mid=8, ema_slow=68)


tp, index_closed = determine_TP(btc, coin_signals, compound=True)
coin_signals['tp'] = tp
coin_signals['hrs_open'] = np.subtract(index_closed, coin_signals.index)

len(coin_signals)

# BTC
# 6, 8, 68 = 707: 11.67
