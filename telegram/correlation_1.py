# Correlation between BTC and LTC for top 1% of candles using one set of parameters
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

# Remove bottom 99 percent of candle bodies
bottom_99pct_count = int(len(ltc_5min) * 0.99)

# Sort the candles in order by their change in price
ltc_delta_sorted = ltc_5min['delta'].sort_values().reset_index(drop=True)
ltc_delta_top_1pct = ltc_delta_sorted[bottom_99pct_count]

# Only take top LTC deltas
ltc_5min_top = ltc_5min[ltc_5min['delta'] >= ltc_delta_top_1pct]

df = []

for index, row in ltc_5min_top.iterrows():
    # Wait 5 min after close
    start_pos = index + 2

    # Group BTC window for the next 15 minutes
    btc_window = btc_5min.iloc[start_pos:start_pos+3]

    # Get BTC delta
    btc_window_delta = (btc_window['close'].iat[-1] - btc_window['open'].iat[0]) / btc_window['open'].iat[0]

    df.append({
        'delta_LTC': row['delta'],
        'delta_BTC': btc_window_delta
    })

df = pd.DataFrame().from_records(df)
np.corrcoef(df['delta_LTC'], df['delta_BTC'])[1][0]