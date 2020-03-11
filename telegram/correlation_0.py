from datetime import datetime
import pandas as pd
import numpy as np
from group_candles import group_candles


# Read in data
ltc = pd.read_csv('data/LTC-BTC.csv')
btc = pd.read_csv('data/BTC-USDT.csv')


# Group 1 min data into 5 min candlesticks
ltc_5min = group_candles(ltc, 5)
btc_5min = group_candles(btc, 5)

# Add column for price change of LTC using the open and close
ltc_5min['delta'] = (ltc_5min['close'] - ltc_5min['open']) / ltc_5min['open']

# Set the number of rows to remove as a variable
bottom_99pct_count = int(len(ltc_5min) * 0.99)

# Sort the candles in order by their change in price
ltc_delta_sorted = abs(ltc_5min['delta']).sort_values().reset_index(drop=True)

# After sorting LTC 5min price changes, find the price change at the 99th percentile
ltc_delta_top_1pct = ltc_delta_sorted[bottom_99pct_count]

# Now that we know the top 1 percent of LTC price movement, only take take those candles
ltc_5min_top = ltc_5min[abs(ltc_5min['delta']) >= ltc_delta_top_1pct]

# Wait 5 min, then see what the following BTC candle looks like (LTC candle closed 5 min after date)
start_pos = ltc_5min_top.iloc[0].name + 2

# Group BTC window for the next 15 minutes
btc_window = btc_5min.iloc[start_pos:start_pos+3]

# Compare deltas
btc_window_delta = (btc_window['close'].iat[-1] - btc_window['open'].iat[0]) / btc_window['open'].iat[0]
