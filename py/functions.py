from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import ccxt
import os


# Find intersections indices between two lines
def find_intersections(line1, line2):
    line1_gt_line2 = line1 > line2
    intersections = []
    current_val = line1_gt_line2[0]

    for i, val in line1_gt_line2.items():
        if val != current_val:
            intersections.append(i)
        current_val = val

    return intersections


def find_signals(df):
    '''
    Determine signals from OHLCV dataframe
    '''

    ema3 = df['close'].ewm(span=3, adjust=False).mean()
    ma20 = df['close'].rolling(window=20).mean().fillna(0)
    ema40 = df['close'].ewm(span=40, adjust=False).mean()

    intersections = find_intersections(ema3, ma20)
    signals = []

    for i in intersections:
        if abs(df[i]['open'] - df[i]['close']) / df[i]['open'] > 0.02:
            continue

        signal = None
        if df[i]['close'] > ema3[i] and ma20[i] > ema40[i]:
            signal = 'Long'
            stop_loss = df[i-10:i]['low'] * 1.003
        elif df['close'][i] < ema3[i] and ma20[i] < ema40[i]:
            signal = 'Short'
            stop_loss = df[i-10:i]['high'] * .997

        if signal:
            purchase_price = df[i+1]['open']
            signals.append([df[i]['date'], signal, round(stop_loss, 8), round(purchase_price, 8)])

    return signals


# ------------------------------------------------------------------------------
# Old functions

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
