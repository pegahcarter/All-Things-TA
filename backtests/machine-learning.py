from py.functions import *
import numpy as np
import pandas as pd

btc = pd.read_csv('data/bitfinex/BTC.csv')
signals = pd.DataFrame()
features = ['rsi', 'macd', 'avg_diff']
tp_pcts = [-1, 0.05, 0.15, 0.35, 2.45, 0]

for ticker in ['BTC/USD', 'ETH/USD', 'ETH/BTC', 'LTC/BTC', 'EOS/BTC', 'XRP/BTC']:
    coin = ticker[:ticker.find('/')]
    df = pd.read_csv('data/bitfinex/' + coin + '.csv', usecols=['date', 'open', 'high', 'low', 'close'])

    if '/BTC' in ticker:
        btc_slice = btc[btc['date'] >= df['date'][0]]
        for col in ['open', 'high', 'low', 'close']:
            df[col] /= btc_slice['close']

    coin_signals = find_signals(df, 21, 30, 50)
    tp = determine_TP(df, coin_signals)
    coin_signals['tp'] = tp

    coin_signals['ticker'] = [ticker for i in range(len(coin_signals))]
    coin_signals = coin_signals.reset_index()
    signals = signals.append(coin_signals, ignore_index=True, sort=False)


profit_pct = abs(signals['price'] - signals['stop_loss']) / signals['price']
signals['tp'] = signals['tp'].astype('int')
end_pct = list(map(lambda x: tp_pcts[x], signals['tp']))
signals['net_profit'] = end_pct * profit_pct
signals = signals.drop('index', axis=1)

signals['date'] = pd.to_datetime(signals['date'])
signals.index = signals['date']


df_2018 = signals[signals['date'] < '2019-01-01 00:00:00']
df_2019 = signals[signals['date'] >= '2019-01-01 00:00:00']
df_2018.groupby(pd.Grouper(freq='M'))['net_profit'].sum()
df_2019.groupby(pd.Grouper(freq='M'))['net_profit'].sum()

date
01-18:   0.050
02-18:   0.318
03-18:   0.340
04-18:   0.253
05-18:   0.216
06-18:   0.029
07-18:   0.052
08-18:   0.319
09-18:  -0.021
10-18:   0.101
11-18:   0.195
12-18:   0.043
01-19:   0.065
02-19:   0.171
03-19:   0.047
04-19:   0.342
05-19:   0.310
06-19:   0.598
07-19:   0.049
08-19:   0.536
09-19:   0.363
10-19:  -0.232


signals['date'][0]





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
