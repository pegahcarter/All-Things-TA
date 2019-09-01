from py.functions import *
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import matplotlib.pyplot as plt

btc = pd.read_csv('ohlcv/BTC.csv')
signals = pd.DataFrame()
coins = ['BTC', 'BCH', 'ETH', 'LTC', 'XRP']
features = [ 'ma20_slope', 'ma20_slope_direction', 'ema40_slope', 'ema40_slope_direction', 'ma20_ema40_same_direction', 'ma20_ema40_diff']
tp_pcts = [-1, 0.05, 0.15, 0.35, 2.45, 0]

for coin in coins:
    for price in ['USD', 'BTC']:
        df = pd.read_csv('ohlcv/' + coin + '.csv')

        if coin == 'BTC' and price == 'BTC':
            continue
        elif price == 'BTC':
            btc_slice = btc[btc['date'] >= df['date'][0]]
            for col in ['open', 'high', 'low', 'close']:
                df[col] /= btc_slice[col]

        df['ma20'] = df['close'].rolling(window=20).mean().fillna(0)
        df['ema40'] = df['close'].ewm(span=40, adjust=False).mean()

        df['ma20_slope'] = np.subtract(df['ma20'][1:], df['ma20'][:-1]) / df['ma20'][:-1] * 100
        df['ma20_slope_direction'] = df['ma20_slope'] > 0
        df['ema40_slope'] = np.subtract(df['ema40'][1:], df['ema40'][:-1]) / df['ema40'][:-1] * 100
        df['ema40_slope_direction'] = df['ema40_slope'] > 0
        df['ma20_ema40_same_direction'] = df['ma20_slope_direction'] == df['ema40_slope_direction']
        df['ma20_ema40_diff'] = np.subtract(df['ma20'], df['ema40']) / df['ma20']

        coin_signals = find_signals(df)
        coin_signals['tp'] = determine_TP(df, coin_signals)

        for feature in features:
            coin_signals[feature] = None

        for i in coin_signals.index:
            coin_signals.loc[i, features] = df.loc[i, features]

        coin_signals['ticker'] = [coin + '/' + price for i in range(len(coin_signals))]
        signals = signals.append(coin_signals, ignore_index=True, sort=False)


# tree = RandomForestClassifier()
# x = signals[features]
# y = signals['tp'] == 4
#
# tree.fit(x, y)
# feature_importance = tree.feature_importances_
# feature_importance = 100 * (feature_importance / max(feature_importance))
# feature_sorted = np.argsort(feature_importance)
# pos = np.arange(feature_sorted.shape[0]) + .5
# plt.barh(pos, feature_importance[feature_sorted], align='center', color='crimson')
# plt.title('Variable Importance')
# plt.xlabel('Relative Importance of Variable')
# plt.yticks(pos, x.columns[feature_sorted])
# plt.show()

# ------------------------------------------------------------------------------
# Testing out eliminating trades based on slope
# signals = signals[signals['tp'] < 5]
signals['profit_pct'] = abs(signals['price'] - signals['stop_loss']) / signals['price']
signals['tp'] = signals['tp'].astype('int')
signals['end_pct'] = list(map(lambda x: tp_pcts[x], signals['tp']))
signals['net_profit'] = signals['end_pct'] * signals['profit_pct']
signals['net_profit'].sum()

# 5% on high/low and minimum of .75% SL spread w/o EOS
# 4.909

sl_pct = {}
for ticker in set(signals['ticker']):
    df = signals[signals['ticker'] == ticker]
    # sl_pct[ticker] = len(df[df['tp'] == 0]) / len(df)
    sl_pct[ticker] = round(df['net_profit'].sum(), 3)

sorted(sl_pct.items(), key=lambda x: x[1])
[('BCH/USD', -0.117),
 ('XRP/USD', -0.001),
 ('BTC/USD', 0.541),
 ('LTC/BTC', 0.647),
 ('ETH/BTC', 0.673),
 ('LTC/USD', 0.964),
 ('XRP/BTC', 1.011),
 ('ETH/USD', 1.191)]


plt.hist(signals['ma20_slope'], bins=50)
plt.show()

plt.hist(signals['ema40_slope'], bins=40)
plt.show()

# Slope difference between averages
signals['slope'] = abs(signals['ma20_slope'] - signals['ema40_slope'])
plt.hist(signals['slope'], bins=40)
plt.show()


slope = []
for i, row in signals.iterrows():
    if row['signal'] == 'Long':
        if row['ma20_slope_direction'] and row['ema40_slope_direction']:
            slope.append(i)
    else:
        if not row['ma20_slope_direction'] and not row['ema40_slope_direction']:
            slope.append(i)

test = signals.drop([i for i in signals.index if i not in slope])

test.groupby('tp')['tp'].count()
test['net_profit'].sum()


plt.hist(signals['ma20_ema40_diff'], bins=50)
plt.show()







# ------------------------------------------------------------------------------

# Finding new features

df = pd.read_csv('ohlcv/BTC.csv')

df['ma20'] = df['close'].rolling(window=20).mean().fillna(0)
df['ema40'] = df['close'].ewm(span=40, adjust=False).mean()

df['ma20_slope'] = np.subtract(df['ma20'][1:], df['ma20'][:-1]) / df['ma20'][:-1] * 100
df['ma20_slope_direction'] = df['ma20_slope'] > 0
df['ema40_slope'] = np.subtract(df['ema40'][1:], df['ema40'][:-1]) / df['ema40'][:-1] * 100
df['ema40_slope_direction'] = df['ema40_slope'] > 0
df['ma20_ema40_same_direction'] = df['ma20_slope_direction'] == df['ema40_slope_direction']
df['ma20_ema40_diff'] = np.subtract(df['ma20'], df['ema40']) / df['ma20']


'hours_since_last_signal'


signals = find_signals(df)
signals['tp'] = determine_TP(df, signals, cushion=0.003)

for feature in features:
    signals[feature] = None

for i in signals.index:
    signals.loc[i, features] = df.loc[i, features]


signals

# ------------------------------------------------------------------------------
