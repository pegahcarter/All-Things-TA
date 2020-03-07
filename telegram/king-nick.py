from datetime import datetime
import pandas as pd
import numpy as np
import sys
from TAcharts.indicators import sdev, rolling
from group_candles import group_candles


# Read in data
ltc = pd.read_csv('data/LTC-BTC.csv')
btc = pd.read_csv('data/BTC-USDT.csv')


# Group by 5 min
ltc_5min = group_candles(ltc, 5)
btc_5min = group_candles(btc, 5)

# Add columns
ltc_5min['delta'] = (ltc_5min['close'] - ltc_5min['open']) / ltc_5min['open']
# btc_5min['delta'] = (btc_5min['close'] - btc_5min['open']) / btc_5min['open']


# Only take top 1% of candles
bottom_99pct_cnt = int(len(ltc_5min) * .99)
top_delta = ltc_5min['delta'].sort_values().reset_index(drop=True)[bottom_99pct_cnt]
ltc_5min_top = ltc_5min[ltc_5min['delta'] >= top_delta]


# Wait 5 min, then see what the following BTC candle looks like (LTC candle closed 5 min after date)
start_pos = ltc_5min_top.iloc[0].name + 2


#  NOTE: Testing - group together the candle above with the two following to get 15 min pct change
btc_window = btc_5min.iloc[start_pos:start_pos+3]
btc_window_delta = (btc_window['close'].iat[-1] - btc_window['open'].iat[0]) / btc_window['open'].iat[0]
