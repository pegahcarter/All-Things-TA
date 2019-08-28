import numpy as np
import pandas as pd
from py.functions import *

btc = pd.read_csv('ohlcv/BTC.csv')
signals = pd.DataFrame()
coins = ['BTC', 'BCH', 'BNB', 'EOS', 'ETH', 'LTC', 'XRP']
features = [ 'ma20_slope', 'ma20_slope_direction', 'ema40_slope', 'ema40_slope_direction', 'ma20_ema40_same_direction', 'ma20_ema40_diff']

for coin in coins:
    for price in ['USD', 'BTC']:
        df = pd.read_csv('ohlcv/' + coin + '.csv')
        if coin == 'BTC' and price == 'BTC':
            continue
        elif price == 'BTC':
            for col in ['open', 'high', 'low', 'close']:
                df[col] /= btc[col]

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

        coin_signals['ticker'] = [coin + '/' + price for i in range(len(coin_signals))]

        signals = signals.append(coin_signals, ignore_index=True, sort=False)


from sklearn.ensemble import RandomForestClassifier
import matplotlib.pyplot as plt
tree = RandomForestClassifier()
x = signals[['ema40_slope', 'ma20_slope', 'ma20_ema40_diff']]
y = signals['tp'] > 0

tree.fit(x, y)
feature_importance = tree.feature_importances_
feature_importance = 100 * (feature_importance / max(feature_importance))
feature_sorted = np.argsort(feature_importance)
pos = np.arange(feature_sorted.shape[0]) + .5
plt.barh(pos, feature_importance[feature_sorted], align='center', color='crimson')
plt.title('Variable Importance')
plt.xlabel('Relative Importance of Variable')
plt.yticks(pos, x.columns[feature_sorted])
plt.show()
