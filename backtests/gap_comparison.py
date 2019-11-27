# Determine the best SL and TP levels for 3EMA, 20MA, and 40EMA
import pandas as pd
from py.functions import find_signals, determine_TP, drop_extra_signals
from py.utils import *


df = pd.read_csv('data/bitfinex/BTC.csv')
coin_signals = find_signals(df, window_fast=5, window_mid=20, window_slow=56)
coin_signals




for ticker in ['BTC/USD', 'ETH/USD', 'ETH/BTC', 'LTC/BTC', 'EOS/BTC', 'XRP/BTC']:
    coin = ticker[:ticker.find('/')]
    df = pd.read_csv('data/bitfinex/' + coin + '.csv', usecols=['date', 'open', 'high', 'low', 'close'])
    if '/BTC' in ticker:
        btc_slice = btc[btc['date'] >= df['date'][0]]
        for col in ['open', 'high', 'low', 'close']:
            df[col] /= btc_slice['close']

    coin_signals = find_signals(df, window_fast=5, window_mid=20, window_slow=56)
    # coin_signals['tp'] = determine_TP(df, coin_signals)
    coin_signals['ticker'] = [ticker for i in range(len(coin_signals))]
    coin_signals = coin_signals.reset_index()
    signals = signals.append(coin_signals, ignore_index=True, sort=False)


signals['profit_pct'] = abs(signals['price'] - signals['stop_loss']) / signals['price']

signals['profit_pct'] = abs(signals['price'] - signals['stop_loss']) / signals['price']
signals['end_pct'] = list(map(lambda x: tp_pcts[x], signals[0]))
signals['net_profit'] = signals['end_pct'] * signals['profit_pct']

for gap in range(1,10):
    results = drop_extra_signals(signals, gap=gap)
    signals[gap] = results['net_profit']

summary = {}
for col in signals:
    try:
        if col >=2:
            summary[col] = signals[col].sum()
    except:
        pass


summary
'''
{2: 0.4822496155545545,
 3: 0.388323820452304,
 4: 0.26414628236455484,
 5: 0.2854036248615147,
 6: 0.25582056820183,
 7: 0.2411610864182584,
 8: 0.279613639895204,
 9: 0.2658648850561355}
'''
