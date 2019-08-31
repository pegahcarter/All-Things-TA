from py.functions import *
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import matplotlib.pyplot as plt

btc = pd.read_csv('ohlcv/BTC.csv')
signals = pd.DataFrame()
coins = ['BTC', 'BCH', 'BNB', 'EOS', 'ETH', 'LTC', 'XRP']
features = [ 'ma20_slope', 'ma20_slope_direction', 'ema40_slope', 'ema40_slope_direction', 'ma20_ema40_same_direction', 'ma20_ema40_diff']
tp_pcts = [-1, 0.05, 0.15, 0.35, 2.45, 0]

for coin in coins:
    # for price in ['USD', 'BTC']:
    df = pd.read_csv('ohlcv/' + coin + '.csv')
    # if coin == 'BTC' and price == 'BTC':
    #     continue
    # elif price == 'BTC':
    #     for col in ['open', 'high', 'low', 'close']:
    #         df[col] /= btc[col]

    df['ma20'] = df['close'].rolling(window=20).mean().fillna(0)
    df['ema40'] = df['close'].ewm(span=40, adjust=False).mean()

    df['ma20_slope'] = np.subtract(df['ma20'][1:], df['ma20'][:-1]) / df['ma20'][:-1] * 100
    df['ma20_slope_direction'] = df['ma20_slope'] > 0
    df['ema40_slope'] = np.subtract(df['ema40'][1:], df['ema40'][:-1]) / df['ema40'][:-1] * 100
    df['ema40_slope_direction'] = df['ema40_slope'] > 0
    df['ma20_ema40_same_direction'] = df['ma20_slope_direction'] == df['ema40_slope_direction']
    df['ma20_ema40_diff'] = np.subtract(df['ma20'], df['ema40']) / df['ma20']

    coin_signals = find_signals(df)
    coin_signals['tp'] = determine_TP(df, coin_signals, cushion=0.003)

    for feature in features:
        coin_signals[feature] = None

    for i in coin_signals.index:
        coin_signals.loc[i, features] = df.loc[i, features]

    coin_signals['ticker'] = [coin + '/USD' for i in range(len(coin_signals))]
    signals = signals.append(coin_signals, ignore_index=True, sort=False)


# tree = RandomForestClassifier()
# x = signals[['ema40_slope', 'ma20_slope', 'ma20_ema40_diff']]
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
signals = signals[signals['tp'] < 5]
signals['profit_pct'] = abs(signals['price'] - signals['stop_loss']) / signals['price']
signals['end_pct'] = list(map(lambda x: tp_pcts[x], signals['tp']))
signals['net_profit'] = signals['end_pct'] * signals['profit_pct']
signals['net_profit'].sum()
# W/ only 4% limit on SL
# 6.8356

# W/ 5% limit on SL and high compared to price
# 8.19

# W/ 5% ... & at least .75% between price and SL
# 7.532

signals.groupby('tp')['tp'].count()
len(signals)



plt.hist(signals['ma20_slope'], bins=50)
plt.show()

signals[signals['ma20_slope'] > .1]['net_profit'].sum()
test = signals[(.0005 > signals['ma20_slope']) & (-.0005 < signals['ma20_slope'])]
test['net_profit'].sum()



plt.hist(signals['ema40_slope'], bins=40)
plt.show()


# Slope difference between averages
signals['slope'] = abs(signals['ma20_slope'] - signals['ema40_slope'])
plt.hist(signals['slope'], bins=40)
plt.show()
signals[signals['slope'] < .3]['net_profit'].sum()
signals[signals['slope'] > .3]['net_profit'].sum()


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
test = signals[(.0001 > signals['ma20_ema40_diff']) & (-.0001 < signals['ma20_ema40_diff'])]
test.groupby('tp')['tp'].count()
test['net_profit'].sum()

x = signals[signals['tp'] == 0]
y = signals[signals['tp'] > 0]



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
