import numpy as np
import pandas as pd
from py.functions import *

df = pd.read_csv('ohlcv/BTC.csv')
df['ma20'] = df['close'].rolling(window=20).mean().fillna(0)
df['ema40'] = df['close'].ewm(span=40, adjust=False).mean()

df['ma20_slope'] = np.subtract(df['ma20'][1:], df['ma20'][:-1]) / df['ma20'][:-1] * 100
df['ma20_slope_direction'] = df['ma20_slope'] > 0
df['ema40_slope'] = np.subtract(df['ema40'][1:], df['ema40'][:-1]) / df['ema40'][:-1] * 100
df['ema40_slope_direction'] = df['ema40_slope'] > 0
df['ma20_ema40_same_direction'] = df['ma20_slope_direction'] == df['ema40_slope_direction']
df['ma20_ema40_diff'] = np.subtract(df['ma20'], df['ema40']) / df['ma20']

signals = find_signals(df)
signals['tp'] = determine_TP(df, signals, cushion=0.003)

signals['ma20_slope'] = None
signals['ma20_slope_direction'] = None
signals['ema40_slope'] = None
signals['ema40_slope_direction'] = None
signals['ma20_ema40_same_direction'] = None
signals['ma20_ema40_diff'] = None

cols = [
    'ma20_slope',
    'ma20_slope_direction',
    'ema40_slope',
    'ema40_slope_direction',
    'ma20_ema40_same_direction',
    'ma20_ema40_diff'
]

for i in signals.index:
    signals.loc[i, cols] = df.loc[i, cols]

from sklearn.ensemble import RandomForestClassifier
import matplotlib.pyplot as plt
tree = RandomForestClassifier()
x = signals[cols]
y = signals['tp'] == 4

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
