from py.variables import coins, hr_intervals, periods, relationship
from py.functions import refresh_ohlcv_df, group_candles
from py.ichimoku import ichimoku
from datetime import datetime
import numpy as np
import pandas as pd

# Note: some coins don't have data from 2018.01.01.
# BCH: 2018.11.16
# EOS: 2018.05.28
# XRP: 2018.05.06


for coin in coins:

    # Update CSV's with most recent hourly OHCLV data
    df = refresh_ohlcv_df(coin)

    # Group candles into each hour interval
    for interval in hr_intervals:
        df_interval = []
        for i in range(0, len(df)-interval, interval):
            candles = df[i:i+interval]
            dohlcv = group_candles(candles)
            # Insert index to front
            dohlcv = [i] + dohlcv
            df_interval.append(dohlcv)

        df_interval = pd.DataFrame(df_interval, columns=['index', 'date', 'open', 'high', 'low', 'close', 'volume'])

        # Create ichimoku cloud columns for each ichi period
        for period in periods:
            period *= relationship
            ichimoku(df_interval, period[0], period[1], period[2], period[3])
            # Add signal logic
            signal = [False for i in range(len(df_interval))]
            # Loop through where...
            # a. Cloud is green (Span A > Span B == green cloud)
            green_cloud = list(df_interval['senkou_a'] > df_interval['senkou_b'])

            # b. Tenkan > Kijun
            tk_gt_kj = list(df_interval['tenkan'] > df_interval['kijun'])

            # c. Price is below tk
            price_lt_tk = list(df_interval['price'] < df_interval['tenkan'])

            # d. price has already been above tk
            price_gt_tk = list(df_interval['price'] > df_interval['tenkan'])

            price_reached_tk = False

            for i in range(len(df_interval)):
                if price_reached_tk & green_cloud[i] & tk_gt_kj[i] & price_lt_tk[i]:
                    price_diff = (df_interval['low'][i] - df_interval['kijun'][i])/df_interval['kijun'][i]
                    if price_diff <= 0.01:
                        signal[i] = True
                        price_reached_tk = False
                else:
                    if not price_reached_tk:
                        price_reached_tk = price_gt_tk[i]

            col_name = str(period[0]) + '-' + str(period[1]) + '-' + str(period[2]) + '-' + str(period[3])
            df_interval[col_name] = signal


        # Save
        df_interval = df_interval.drop(['price', 'tenkan', 'kijun', 'senkou_a', 'senkou_b', 'chikou'], axis=1)
        df_interval.to_csv('data/' + str(interval) + '/' + coin + '.csv', index=False)
