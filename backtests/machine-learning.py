from py.functions import *
import numpy as np
import pandas as pd

btc = pd.read_csv('data/bitfinex/BTC.csv')
signals = pd.DataFrame()
features = ['rsi', 'macd', 'avg_diff']
tp_pcts = [-1, 0.05, 0.15, 0.35, 2.45, 0]
# emafast, mamid, emaslow = 5, 8, 40

for ticker in ['BTC/USD', 'ETH/USD', 'ETH/BTC', 'LTC/BTC', 'EOS/BTC', 'XRP/BTC']:
    coin = ticker[:ticker.find('/')]
    df = pd.read_csv('data/bitfinex/' + coin + '.csv', usecols=['date', 'open', 'high', 'low', 'close'])

    if '/BTC' in ticker:
        btc_slice = btc[btc['date'] >= df['date'][0]]
        for col in ['open', 'high', 'low', 'close']:
            df[col] /= btc_slice['close']

    # df['mamid'] = df['close'].rolling(window=?).mean().fillna(0)
    # df['emaslow'] = df['close'].ewm(span=emaslow, adjust=False).mean()

    # df['rsi'] = rsi(df['close'])
    # df['macd'] = macd(df['close'])
    # df['mamid_slope'] = roc(df['mamid'], 1)
    # df['mamid_slope'] = np.subtract(df['mamid'][1:], df['mamid'][:-1]) / df['mamid'][:-1] * 100
    # df['avg_diff'] = abs(np.subtract(df['mamid'], df['emaslow'])) / df['mamid'] * 100

    coin_signals = find_signals(df, window_fast=21, window_mid=30, window_slow=50)
    tp, index_closed, index_tp_hit = determine_TP(df, coin_signals, compound=True)
    coin_signals['tp'] = tp
    # coin_signals['index_closed'] = index_closed
    # coin_signals['macd'] = df.iloc[coin_signals.index]['macd']
    # coin_signals['rsi'] = df.iloc[coin_signals.index]['rsi']
    # coin_signals['avg_diff'] = df.iloc[coin_signals.index]['avg_diff']

    coin_signals['ticker'] = [ticker for i in range(len(coin_signals))]
    coin_signals = coin_signals.reset_index()
    signals = signals.append(coin_signals, ignore_index=True, sort=False)


profit_pct = abs(signals['price'] - signals['stop_loss']) / signals['price']
signals['tp'] = signals['tp'].astype('int')
end_pct = list(map(lambda x: tp_pcts[x], signals['tp']))
signals['net_profit'] = end_pct * profit_pct

signals['net_profit'].sum()
len(signals)


signals.groupby('tp').count()

bad_calls = signals[signals['tp'] == 0]
good_calls = signals[signals['tp'] != 0]
long_calls = signals[signals['signal'] == 'Long']
short_calls = signals[signals['signal'] == 'Short']







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
from sklearn.ensemble import RandomForestClassifier
import matplotlib.pyplot as plt

tree = RandomForestClassifier(n_estimators=100)
x = signals[features]
y = signals['tp'] != 0

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

# ------------------------------------------------------------------------------

# Finding new features

df = pd.read_csv('data/bitfinex/BTC.csv')

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
