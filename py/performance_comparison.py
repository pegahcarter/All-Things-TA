from py.functions import group_candles
import pandas as pd
import numpy as np
import os

# Concept:
# Compare signal price with 1, 2, 3, 6, 12, 24, and 36 trailing candle price
windows = [4, 6, 12, 24, 36]

def correct(window, row):
    if row['signal'] == 'BUY':
        if row['close_' + str(window)] > row['close']:
            return True
        else:
            return False
    else:  # row['signal'] == 'SELL'
        if row['close_' + str(window)] < row['close']:
            return True
        else:
            return False



coin = 'BTC'
df_all = pd.read_csv('prices/' + coin + '.csv')

df = df_all.dropna().copy()
results = pd.DataFrame()

for window in windows:
    df['close_' + str(window)] = [group_candles(df_all[i:i+window])[4] for i in df.index]
    df['close_'+str(window)+'_delta'] = [(row['close_'+str(window)] - row['close']) / row['close'] for _, row in df.iterrows()]
    results[window] = [correct(window, row) for _, row in df.iterrows()]

df.drop(['open', 'high', 'low', 'close', 'volume'], axis=1, inplace=True)
cols = [col for col in df.columns if 'delta' in col]
df.groupby('signal')[cols].mean()
