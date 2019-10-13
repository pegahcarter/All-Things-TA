from py.functions import *
from collections import Counter


tickers = ['BTC/USD', 'ETH/USD', 'ETH/BTC', 'LTC/BTC', 'EOS/BTC', 'XRP/BTC']
tp_pcts = [-1, .05, .15, .35, 2.45]

avg1 = [5, 8, 10, 13, 15, 21]
avg2 = [13, 15, 21, 25, 30, 34, 40, 55, 60, 75, 89]
avg3 = [34, 40, 50, 55, 60, 75, 89, 100, 144, 150, 200, 233]
avgs_combined = [[a1, a2, a3] for a1 in avg1 for a2 in avg2 for a3 in avg3 if a1 < a2 and a2 < a3]

btc = pd.read_csv('data/bitfinex/BTC.csv')
results = pd.DataFrame(columns=['average'] + tickers + [0, 1, 2, 3, 4])
results['average'] = avgs_combined

tps_hit = np.array([np.array([0, 0, 0, 0, 0]) for _ in range(len(avgs_combined))])
tps_hit = []

for ticker in tickers:
    coin = ticker[:ticker.find('/')]
    df = pd.read_csv('data/bitfinex/' + coin + '.csv', usecols=['date', 'open', 'high', 'low', 'close'])

    if '/BTC' in ticker and ticker != 'BCH/BTC':
        for col in ['open', 'high', 'low', 'close']:
            df[col] /= btc['close']

    net_profit = []
    coin_tps_hit = []
    for avg in avgs_combined:
        coin_signals = find_signals(df, window_fast=avg[0], window_mid=avg[1], window_slow=avg[2])
        tp = determine_TP(df, coin_signals)

        profit_pct = abs(coin_signals['price'] - coin_signals['stop_loss']) / coin_signals['price']
        end_pct = list(map(lambda x: tp_pcts[x], tp))

        net_profit.append(np.dot(profit_pct, end_pct))
        coin_tps_hit.append(Counter(tp).values())

    results[ticker] = net_profit
    tps_hit.append(coin_tps_hit)

test = np.array(tps_hit)
a = test[0]

new_arr = [[0, 0, 0, 0, 0]]*len(results)
new_arr = np.array(new_arr)
df = pd.DataFrame(data=new_arr, columns=[0, 1, 2, 3, 4])

for i in range(len(tps_hit)):
    for row in range(len(results)):
        if len(tps_hit[i][row]) == 4:
            tps_hit[i][row] = tps_hit[i][row] + [0]
        df.iloc[row] += tps_hit[i][row]

for col in [0, 1, 2, 3, 4]:
    results[col] = df[col]

results.to_csv('data/optimize_moving_avg_new.csv', index=False)

# Analyzing results
df = pd.read_csv('data/optimize_moving_avg_new.csv')

mean_performance = [row.mean() for _, row in df.drop(['average', '0', '1', '2', '3', '4'], axis=1).iterrows()]
total_performance = [row.sum() for _, row in df.drop(['average', '0', '1', '2', '3', '4'], axis=1).iterrows()]

df['mean'] = mean_performance
df['total'] = total_performance

df = df.sort_values('mean', ascending=False)

df['total_trades'] = df[['0', '1', '2', '3', '4']].sum(axis=1)
df.to_csv('data/optimize_moving_avg_new.csv', index=False)
