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


# Determine signals from OHLCV dataframe
def find_signals(df):
    ema3 = df['close'].ewm(span=3, adjust=False).mean()
    ma20 = df['close'].rolling(window=20).mean().fillna(0)
    ema40 = df['close'].ewm(span=40, adjust=False).mean()

    intersections = find_intersections(ema3, ma20)
    signals = []

    for i in intersections:
        if abs(df['open'][i] - df['close'][i]) / df['open'][i] > 0.02:
            continue

        signal = None
        if df['close'][i] > ema3[i] and ma20[i] > ema40[i]:
            signal = 'Long'
            stop_loss = df['low'][i-10:i].min() * 1.003
        elif df['close'][i] < ema3[i] and ma20[i] < ema40[i]:
            signal = 'Short'
            stop_loss = df['high'][i-10:i].max() * .997

        if signal:
            purchase_price = df['open'][i+1]
            signals.append([df['date'][i], signal, round(stop_loss, 8), round(purchase_price, 8)])

    signals = pd.DataFrame(signals, columns=['date', 'signal', 'stop_loss', 'price'])
    return signals


# Figure out which TP level is hit
def determine_TP(signal, index, df, cushion=0.003):
    if signal == 'Long':
        l_bounds = df['low']
        midrange = df['open']
        u_bounds = df['high']
        cushion = 1. + cushion
    else:   # signal == 'Short'
        l_bounds = -df['high']
        midrange = -df['open']
        u_bounds = -df['low']
        cushion = 1. - cushion

    purchase_price = midrange[index+1]
    stop_loss = min(l_bounds[index-10:index]) * cushion

    diff = abs(purchase_price) - abs(stop_loss)
    tp1 = purchase_price + diff/2.
    tp2 = purchase_price + diff
    tp3 = purchase_price + diff*2
    tp4 = purchase_price + diff*3

    tp_targets = [tp1, tp2, tp3, tp4]
    TP = 0

    for x in range(index+1, len(df)):
        if TP > 0:
            stop_loss = purchase_price
        while TP != 4 and u_bounds[x] > tp_targets[TP]:
            TP += 1
        if TP == 4 or stop_loss > l_bounds[x]:
            break

    return TP


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


def calc_macd(_close, fast=12, slow=26):
    '''
    macd line = fast_ema - slow_ema
    signal line = 9ema of macd line
    histogram = macd line - signal line
    '''
    ema_fast = _close.ewm(window=fast, adjust=False).mean()
    ema_slow = _close.ewm(window=slow, adjust=False).mean()
    return ema_fast - ema_slow


def calc_rsi(_close):
    n = 14
    deltas = np.diff(_close)
    seed = deltas[:n+1]
    up = seed[seed > 0].sum()/n
    down = -seed[seed < 0].sum()/n
    rsi = np.zeros_like(_close)
    rsi[:n] = 100. - 100./(1.+ up/down)
    for i in range(n, len(_close)):
        delta = deltas[i-1]
        if delta > 0:
            up_val = delta
            down_val = 0
        else:
            up_val = 0
            down_val = -delta

        up = (up*(n-1) + up_val)/n
        down = (down*(n-1) + down_val)/n

        rsi[i] = 100. - 100./(1. + up/down)

    return rsi
