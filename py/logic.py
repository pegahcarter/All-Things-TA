import pandas as pd
import numpy as np
from variables import *
import requests
from urllib.parse import urlencode


def run(ticker, candle_abv):

    data = exchange.fetch_ohlcv(ticker, candle_abv, limit=500, since=since)
    df = pd.DataFrame(data, columns=['date', 'open', 'high', 'low', 'close', 'volume'])
    _close = df['close'].copy()
    _open = df['open'].copy()

    ema3 = calc_ema(_close, window=3)
    ma20 = calc_ma(_close, window=20)
    ema40 = calc_ema(_close, window=40)
    ema3_gt_ma20 = ema3 > ma20

    cross_indices = []
    current_val = ema3_gt_ma20[0]

    for i, val in ema3_gt_ma20[1:].items():
        if val != current_val:
            cross_indices.append(i)
        current_val = val

    coin_signals = []

    for cross_index in cross_indices:
        signal = None
        for index, price in _close[cross_index:].iteritems():
            rng = set(ema3_gt_ma20[cross_index:index+1])
            if len(rng) == 2:
                break
            elif abs(_open[index] - _close[index]) / _open[index] > 0.02:
                break
            elif True in rng:
                if price > ema3[index]:
                    if ma20[index] > ema40[index]:
                        signal = 'Long'
                        SL = df[index-10:index]['low'].min() * .9975
                    break
            else:   # False in rng
                if price < ema3[index]:
                    if ma20[index] < ema40[index]:
                        signal = 'Short'
                        SL = df[index-10:index]['high'].max() * 1.0025
                    break

        if signal:
            coin_signals.append([df['date'][index], ticker, signal, round(price, 8), round(SL, 8)])

    return coin_signals


def send_signal(row, date):

    if row['ticker'] == 'BTC/USD':
        row['price'] = int(row['price'])
        row['Stop Loss'] = int(row['Stop Loss'])
    else:
        row['Stop Loss'] = round(row['Stop Loss'], 4)
    text = date + '\n'
    text += row['ticker'] + '\n'
    text += 'Bitfinex\n'
    text += row['signal'] + ' ' + str(row['price']) + '\n'

    diff = row['price'] - row['Stop Loss']
    tp1 = row['price'] + diff/2
    tp2 = row['price'] + diff
    tp3 = row['price'] + diff*2
    tp4 = row['price'] + diff*3

    if row['ticker'] == 'BTC/USD':
        tp1 = int(tp1)
        tp2 = int(tp2)
        tp3 = int(tp3)
        tp4 = int(tp4)
    else:
        tp1 = round(tp1, 4)
        tp2 = round(tp2, 4)
        tp3 = round(tp3, 4)
        tp4 = round(tp4, 4)

    text += 'Take profit ' + str(tp1) + ', ' + str(tp2) + ', ' + str(tp3) + ', ' + str(tp4) + '\n'
    text += 'Stop loss ' + str(row['Stop Loss'])

    requests.get(url + urlencode({'chat_id': chat_id, 'text': text}))



def calc_ma(_close, window):
    return _close.rolling(window=window).mean().fillna(0)


def calc_ema(_close, window):
    return _close.ewm(span=window, adjust=False).mean()


def calc_macd(_close, fast=12, slow=26):
    '''
    macd line = fast_ema - slow_ema
    signal line = 9ema of macd line
    histogram = macd line - signal line
    '''
    ema_fast = calc_ema(_close, window=fast)
    ema_slow = calc_ema(_close, window=slow)
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


# def cross(line1, line2):
#     nan_count = max(line1.isna().sum(), line2.isna().sum())
#     crosses = [False for i in range(nan_count)]
#     l1_gt_l2 = line1 > line2
#     current_val = l1_gt_l2[nan_count]
#     for next_val in l1_gt_l2[nan_count+1:]:
#         crosses.append(current_val != next_val)
#         current_val = next_val
#     crosses.insert(0, False)
#     return crosses
