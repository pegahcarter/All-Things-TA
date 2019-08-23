# Determine the best SL and TP levels for 3EMA, 20MA, and 40EMA
import pandas as pd
import numpy as np
import os
from py.functions import find_signals, determine_TP


BTC = pd.read_csv('backtests/BTC.csv')
signals = find_signals(BTC)


test = signals[0]


df = pd.DataFrame()

# By increments of .05%, find the SL that returns the most profit
for cushion in range(15, 100, 5):
    cushion /= 10000.

    df[cushion] = [determine_TP(BTC, index, signal, price, cushion) for index, (signal, price) in signals.iterrows()]

    # 1. Determine stop loss ($)
    # 2.


results = {}
for col in df.columns:
    results[col] = round(df[col].dropna().sum(), 4)

results
