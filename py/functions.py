from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import ccxt
import os

# Loop to update CSV's with recent OHLCV data
def refresh_ohlcv(file, offline=False):

    df = pd.read_csv('prices/' + file)
    if 'signal' in df.columns:
        df.drop('signal', axis=1,inplace=True)
    df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d %H:%M:%S')
    coin = file[:file.find('.')]

    if offline:
        return coin, df

    start_date = df.iloc[-1]['date']
    df_new = []
    binance = ccxt.binance()

    while start_date < datetime.now():
        results = binance.fetch_ohlcv(coin + '/USDT', '1h', since=int(start_date.timestamp()*1000))
        df_new += results
        start_date += timedelta(hours=len(results))

    df_new = pd.DataFrame(df_new, columns=df.columns)
    df_new['date'] = df_new['date'].apply(lambda x: datetime.fromtimestamp(x/1000))
    df_new = df_new[df_new['date'] > df.iloc[-1]['date']]
    df = df.append(df_new, ignore_index=True)
    df.to_csv('prices/' + file, index=False)

    return coin, df


# Group hourly candle into candle intervals
def group_candles(candles):
    candles = np.array(candles)
    return ([
        candles[0, 0],         # date
        candles[0, 1],         # open
        candles[:, 2].max(),   # high
        candles[:, 3].min(),   # low
        candles[-1, 4],        # close
        candles[:, 5].sum()    # volume
    ])


# Find intersections indices between two lines
def find_intersections(line1, line2):
    line1_gt_line2 = line1 > line2
    intersections = []
    current_val = line1_gt_line2[0]

    for index, val in line1_gt_line2.items():
        if val != current_val:
            intersections.append(index)
        current_val = val

    return intersections
