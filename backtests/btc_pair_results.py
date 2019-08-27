import pandas as pd
from py.functions import *


coins = ['ETH', 'LTC', 'BCH']
btc = pd.read_csv('ohlcv/BTC.csv')
tp_pcts = [-1, 0.125, 0.375, 0.875, 1.375, 0]
results = {}

for coin in coins:
    df = pd.read_csv('ohlcv/' + coin + '.csv')
    for col in ['open', 'high', 'low', 'close']:
        df[col] /= btc[col]

    signals = find_signals(df)
    tps_hit = determine_TP(df, signals, cushion=0)
    end_pct = list(map(lambda x: tp_pcts[x], tps_hit))
    profit_pct = abs(signals['price'] - signals['stop_loss']) / signals['price']
    net_profit = (end_pct * profit_pct).sum()
    results[coin] = net_profit

# results
{
 'ETH': 0.5635863250096147,
 'LTC': -0.12686260535912774,
 'BCH': -0.05134174055429305
}
