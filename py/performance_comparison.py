import pandas as pd
import numpy as np
import os

# Concept:
# Compare signal price with 6, 12, 24, 48, 72, and 168 trailing candle price


windows = [6, 12, 24, 48, 72, 168]

coin = 'BTC'
df = pd.read_csv('prices/' + coin + '.csv')
df_signal = df.dropna()
df.head()
df_signal.head()
