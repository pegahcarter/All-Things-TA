from datetime import datetime
import pandas as pd
import numpy as np
from group_candles import group_candles


def candle_correlation( df_btc, df_alt, candle_period, delay_period, btc_window_period, bottom_percentile=0.99):

    # Add column for price change of alt coin using open and close
    df_alt['delta'] = (df_alt['close'] - df_alt['open']) / df_alt['open']

    # Set the number of rows to remove as a variable
    bottom_percentile_cnt = int(len(df_alt) * bottom_percentile)

    # Sort the candles in order by their change in price
    alt_delta_sorted = abs(df_alt['delta']).sort_values().reset_index(drop=True)

    # After sorting alt price changes, remove the any candlw within the bottom_percentile
    alt_delta_min_val = alt_delta_sorted[bottom_percentile_cnt]

    # Now that we know the top percent of alt price movement, only take take those candles
    alt_grouped_top = df_alt[abs(df_alt['delta']) >= alt_delta_min_val]

    # Main lists to compare correlation
    alt_delta_list = []
    btc_delta_list = []

    # Loop through top alt movements and determnine correlation with lagged btc movement
    for index, row in alt_grouped_top.iterrows():

        start_pos = index + delay_period
        btc_window = df_btc.iloc[start_pos: start_pos + btc_window_period]
        btc_window_delta = (btc_window['close'].iat[-1] - btc_window['open'].iat[0]) / btc_window['open'].iat[0]

        # Save alt and btc deltas to main lists
        alt_delta_list.append(row['delta'])
        btc_delta_list.append(btc_window_delta)

    # Determine correlation between two lists
    correlation = np.corrcoef(alt_delta_list, btc_delta_list)

    return correlation
