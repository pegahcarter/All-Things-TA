

# Code to figure out profit by month
signals['date'] = pd.to_datetime(signals['date'])
signals.index = signals['date']

df_2018 = signals[signals['date'] < '2019-01-01 00:00:00']
df_2019 = signals[signals['date'] >= '2019-01-01 00:00:00']
df_2018.groupby(pd.Grouper(freq='M'))['net_profit'].sum()
df_2019.groupby(pd.Grouper(freq='M'))['net_profit'].sum()

date
01-18:   0.050
02-18:   0.318
...


# ------------------------------------------------------------------------------

# Finding new features

df['ma20'] = df['close'].rolling(window=20).mean().fillna(0)
df['ema40'] = df['close'].ewm(span=40, adjust=False).mean()

df['ma20_slope'] = np.subtract(df['ma20'][1:], df['ma20'][:-1]) / df['ma20'][:-1] * 100
df['ma20_slope_direction'] = df['ma20_slope'] > 0
df['ema40_slope'] = np.subtract(df['ema40'][1:], df['ema40'][:-1]) / df['ema40'][:-1] * 100
df['ema40_slope_direction'] = df['ema40_slope'] > 0
df['ma20_ema40_same_direction'] = df['ma20_slope_direction'] == df['ema40_slope_direction']
df['ma20_ema40_diff'] = np.subtract(df['ma20'], df['ema40']) / df['ma20']


signals = find_signals(df)
signals['tp'] = determine_TP(df, signals)

for feature in features:
    signals[feature] = None

for i in signals.index:
    signals.loc[i, features] = df.loc[i, features]

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
