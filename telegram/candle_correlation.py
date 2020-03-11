from datetime import datetime
import pandas as pd
import numpy as np
from group_candles import group_candles


def candle_correlation(alt_coin, candle_period, delay_period, btc_window_period, bottom_percentile=0.99):

    df_btc = group_candles(pd.read_csv('data/BTC-USDT.csv'), candle_period)
    df_alt = group_candles(pd.read_csv(f'data/{alt_coin}-BTC.csv'), candle_period)

    # Add column for price change of alt coin using open and close
    df_alt['delta'] = (df_alt['close'] - df_alt['open']) / df_alt['open']

    # Set the number of rows to remove as a variable
    bottom_percentile_cnt = int(len(df_alt) * bottom_percentile)

    # Sort the candles in order by their change in price
    alt_delta_sorted = abs(df_alt['delta']).sort_values().reset_index(drop=True)

    # After sorting alt price changes, remove the any candlw within the bottom_percentile
    alt_delta_top_percentile = alt_delta_sorted[bottom_percentile_cnt]

    # Now that we know the top percent of alt price movement, only take take those candles
    df_alt_top = df_alt[abs(df_alt['delta']) >= alt_delta_top_percentile]

    # Wait 5 min, then see what the following BTC candle looks like (LTC candle closed 5 min after date)
    start_pos = df_alt_top.iloc[0].name + 2

    # Group BTC window for the next 15 minutes
    btc_window = df_btc.iloc[start_pos:start_pos+3]

    # Compare deltas
    btc_window_delta = (btc_window['close'].iat[-1] - btc_window['open'].iat[0]) / btc_window['open'].iat[0]
