# Base code for compounding
from functions import find_signals, determine_TP
from portfolio import Portfolio
import itertools
import os
import pandas as pd


tp_pcts = [1, .05, .95, 0, 0]
avgs = [21, 30, 55]
signals = []

for f in os.listdir('../data/binance/'):

    df = pd.read_csv('../data/binance/' + f)
    coin_signals = find_signals(df, 21, 30, 55, 0.0075, 0.04)

    # Add `tp`, `index_tp_hit`, and `index_closed`
    determine_TP(df, coin_signals)

    # Add ticker to signal & remove unused keys
    ticker = f[:f.find('.')]
    for x in coin_signals:
        x.update({'ticker': ticker})

    # Add coin signals to the primary signal list
    signals.extend(coin_signals)

# Re-order signals by index opened
signals = sorted(signals, key=lambda x: x['index_opened'])
df = pd.DataFrame(signals)

df['hrs_open'] = df['index_closed'] - df['index_opened']

df['hrs_open'].median()

df['hrs_open'].describe()

# Average time between trades
16476 / len(df)
len(df)
