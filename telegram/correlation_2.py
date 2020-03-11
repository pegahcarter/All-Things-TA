# Correlation between BTC and LTC for top 1% of candles, looping through parameters
from datetime import datetime
import pandas as pd
import numpy as np
from group_candles import group_candles

# ------------------------------------------------------------------------------------
# Variables to loop through

candle_periods = [1, 3, 5, 15]
delay_periods = [1, 2, 3, 5]
btc_window_periods = [1, 2, 3, 5, 6]

# ------------------------------------------------------------------------------------


# Read in data
ltc = pd.read_csv('data/LTC-BTC.csv')
btc = pd.read_csv('data/BTC-USDT.csv')

df = pd.DataFrame()


# Loop through candle_periods
for candle_period in candle_periods:
    ltc_grouped = group_candles(ltc, candle_period)
    btc_grouped = group_candles(btc, candle_period)

    # Add column for price change of LTC using the open and close
    ltc_grouped['delta'] = (ltc_grouped['close'] - ltc_grouped['open']) / ltc_grouped['open']

    # Remove bottom 99 percent of candle bodies
    bottom_99pct_count = int(len(ltc_grouped) * 0.99)

    # Sort the candles in order by their change in price
    ltc_delta_sorted = ltc_grouped['delta'].sort_values().reset_index(drop=True)
    ltc_delta_top_1pct = ltc_delta_sorted[bottom_99pct_count]

    # Only take top LTC deltas
    ltc_grouped_top = ltc_grouped[ltc_grouped['delta'] >= ltc_delta_top_1pct]

    # Loop through delay_periods and btc_window_periods
    for delay_period in delay_periods:
        for btc_window_period in btc_window_periods:

            btc_delta_list = []
            ltc_delta_list = []

            # Iterate through the LTC
            for index, row in ltc_grouped_top.iterrows():
                start_pos = index + delay_period

                btc_window = btc_grouped.iloc[start_pos:start_pos + btc_window_period]

                # Get BTC delta
                btc_window_delta = (btc_window['close'].iat[-1] - btc_window['open'].iat[0]) / btc_window['open'].iat[0]

                # Save LTC and BTC deltas to later compare correlation of deltas
                btc_delta_list.append(btc_window_delta)
                ltc_delta_list.append(row['delta'])

            # Now that we filled our ???_delta_list variables, determine correlation coefficient
            delta_correlation = np.corrcoef(btc_delta_list, ltc_delta_list)

            # Add correlation results to main dataframe
            df = df.append({
                'candle_period': candle_period,
                'delay_period': delay_period,
                'btc_window_period': btc_window_period,
                'delta_correlation': delta_correlation
            }, ignore_index=True)

df = pd.DataFrame().from_records(df)

df.corr()
