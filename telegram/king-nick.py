from datetime import datetime
import pandas as pd
import numpy as np
from group_candles import group_candles


# Read in data
ltc = pd.read_csv('data/LTC-BTC.csv')
btc = pd.read_csv('data/BTC-USDT.csv')

# To clarify, we're looking at 1 min price data
btc.head()

# Date range used for backtests
ltc['date'].iat[0]
ltc['date'].iat[-1]

# Group 1 min data into 5 min candlesticks
ltc_5min = group_candles(ltc, 5)
btc_5min = group_candles(btc, 5)


# Add column for price change of LTC using the open and close
ltc_5min['delta'] = (ltc_5min['close'] - ltc_5min['open']) / ltc_5min['open']

# - Only take LTC candles that have a change from open to close greater than 99% of candles
# - If we have 100 rows of data, we want to remove 99 rows.  This calculates the
#       same number of rows to remove based on the size of our data
# - Note: we are using data from a mini bull run, so we only want to look at LTC
#       candles that have a positive movement in price

# How many rows of prices do we have?
print(len(ltc_5min))
# If we want to remove 99% of those rows, how many rows will we remove?
print(len(ltc_5min) * 0.99)
# We can't remove 60290.01 rows because it's impossible to remove a fraction of a row,
# so we'll take the nearest integer
print(int(len(ltc_5min) * 0.99))

# Set the number of rows to remove as a variable
bottom_99pct_count = int(len(ltc_5min) * 0.99)

# Sort the candles in order by their change in price
ltc_delta_sorted = ltc_5min['delta'].sort_values().reset_index(drop=True)
print(ltc_delta_sorted)

# After sorting LTC 5min price changes, find the price change at the 99th percentile
ltc_delta_top_1pct = ltc_delta_sorted[bottom_99pct_count]
# So what is that 99th percentile?  (Answer: 0.7% price change in 5 min)
print(ltc_delta_top_1pct)

# Now that we know the top 1 percent of LTC price movement is at least 0.7% in 5 min,
#   only take LTC rows with price that change at least 0.7%
ltc_5min_top = ltc_5min[ltc_5min['delta'] >= ltc_delta_top_1pct]
# To validate, let's check the first five rows and make sure "delta" (price movement)
#   is at least 0.7% 
ltc_5min_top.head()



# Wait 5 min, then see what the following BTC candle looks like (LTC candle closed 5 min after date)
start_pos = ltc_5min_top.iloc[0].name + 2

# Group BTC window for the next 15 minutes
btc_window = btc_5min.iloc[start_pos:start_pos+3]

#
btc_window_delta = (btc_window['close'].iat[-1] - btc_window['open'].iat[0]) / btc_window['open'].iat[0]
