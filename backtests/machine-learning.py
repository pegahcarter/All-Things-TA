from py.functions import *
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import matplotlib.pyplot as plt

btc = pd.read_csv('ohlcv/BTC.csv')
signals = pd.DataFrame()
# features = ['rsi', 'macd', 'ma20_slope', 'ma20_slope_direction', 'ema40_slope', 'ema40_slope_direction', 'ma20_ema40_same_direction', 'ma20_ema40_diff']
features = ['rsi', 'macd', 'ma20_ema40_diff', 'ma20_slope_direction']
tp_pcts = [-1, 0.05, 0.15, 0.35, 2.45, 0]

for ticker in ['BTC/USD', 'ETH/USD', 'ETH/BTC', 'LTC/BTC', 'EOS/BTC', 'XRP/BTC', 'ADA/BTC']:
    coin = ticker[:ticker.find('/')]
    df = pd.read_csv('ohlcv/' + coin + '.csv', usecols=['date', 'open', 'high', 'low', 'close'])

    if '/BTC' in ticker:
        btc_slice = btc[btc['date'] >= df['date'][0]]
        for col in ['open', 'high', 'low', 'close']:
            df[col] /= btc_slice['close']


    df['ma20'] = df['close'].rolling(window=20).mean().fillna(0)
    df['ema40'] = df['close'].ewm(span=40, adjust=False).mean()

    df['rsi'] = calc_rsi(df['close'])
    df['macd'] = calc_macd(df['close'])
    # df['ma20_slope'] = np.subtract(df['ma20'][1:], df['ma20'][:-1]) / df['ma20'][:-1] * 100
    df['ma20_slope_direction'] = df['ma20_slope'] > 0
    # df['ema40_slope'] = np.subtract(df['ema40'][1:], df['ema40'][:-1]) / df['ema40'][:-1] * 100
    # df['ema40_slope_direction'] = df['ema40_slope'] > 0
    # df['ma20_ema40_same_direction'] = df['ma20_slope_direction'] == df['ema40_slope_direction']
    df['ma20_ema40_diff'] = abs(np.subtract(df['ma20'], df['ema40'])) / df['ma20']

    coin_signals = find_signals(df)
    tp, index_closed = determine_TP(df, coin_signals, compound=True)
    coin_signals['tp'] = tp
    coin_signals['index_closed'] = index_closed


    # for feature in features:
    #     coin_signals[feature] = None
    #
    # coin_signals[features] = df.iloc[coin_signals.index][features]

    coin_signals['ticker'] = [ticker for i in range(len(coin_signals))]
    coin_signals = coin_signals.reset_index()
    signals = signals.append(coin_signals, ignore_index=True, sort=False)


profit_pct = abs(signals['price'] - signals['stop_loss']) / signals['price']
signals['tp'] = signals['tp'].astype('int')
end_pct = list(map(lambda x: tp_pcts[x], signals['tp']))
signals['net_profit'] = end_pct * profit_pct
signals['net_profit'].sum()  # 5.03


# How many positions do we have open when we take the trade?
x = signals[signals['ticker'] == 'BTC/USD'].drop(['price', 'stop_loss', 'ticker'], axis=1)
x.head()

test = x[:10]


row = test.iloc[0]

row_rng = range(row['index'], row['index_closed'])

test.iloc[1]['index'] in row_rng

import timeit
%timeit x = test.at[0, 'index']

%timeit x = test['index'][0]

test.a


for i, row in test[1:].iterrows():















sl_pct = {}
for ticker in set(signals['ticker']):
    df = signals[signals['ticker'] == ticker]
    sl_pct[ticker] = round(len(df[df['tp'] == 0]) / len(df), 5)
    # sl_pct[ticker] = round(df['net_profit'].sum(), 3)

sorted(sl_pct.items(), key=lambda x: x[1])
# sl_pct[ticker] = round(len(df[df['tp'] == 0]) / len(df), 4)
 [('ETH/BTC', 0.19592), ('LTC/BTC', 0.21586), ('XRP/BTC', 0.29368), ('EOS/BTC', 0.30435), ('ADA/BTC', 0.3097), ('ETH/USD', 0.31915), ('BTC/USD', 0.32301)]
# sl_pct[ticker] = round(len(df[df['tp'] == 4]) / len(df), 4)
[('LTC/BTC', 0.07048), ('ETH/BTC', 0.08163), ('ADA/BTC', 0.17164), ('BTC/USD', 0.17257), ('ETH/USD', 0.18298), ('XRP/BTC', 0.19703), ('EOS/BTC', 0.21739)]
# sl_pct[ticker] = round(df['net_profit'].sum(), 3)
[('ETH/BTC', 0.083), ('LTC/BTC', 0.155), ('BTC/USD', 0.594), ('ADA/BTC', 0.865), ('XRP/BTC', 1.004), ('EOS/BTC', 1.048), ('ETH/USD', 1.243)]

slope = []
for i, row in signals.iterrows():
    # if row['signal'] == 'Long' and not row['ma20_slope_direction']:
    #     slope.append(i)
    if row['signal'] == 'Short' and row['ma20_slope_direction']:
        slope.append(i)

test = signals.drop([i for i in signals.index if i not in slope])

test.groupby('tp')['tp'].count()
len(test)

test['net_profit'].sum()
test[test['ma20_ema40_diff'] < .002][:60]








test.sort_values('rsi')










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

# ------------------------------------------------------------------------------

# Random Forest

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
