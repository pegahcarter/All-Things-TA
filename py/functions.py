from TAcharts.py.ta import ema, sma
from TAcharts.py.momentum import rsi
from TAcharts.py.utils import crossover

import numpy as np
import pandas as pd


def find_signals(df, window_fast, window_mid, window_slow):
    ''' Determine signals from OHLCV dataframe '''

    _open = df['open'].values
    high = df['high'].values
    low = df['low'].values
    close = df['close'].values

    emaslow = ema(close, n=window_slow)
    mamid = sma(close, n=window_mid)
    emafast = ema(close, n=window_fast)
    mabase = sma(close, n=200)

    mamid_emaslow_diff = abs(mamid - emaslow) / mamid

    candle_body = np.abs(close - _open) / _open
    candle_sdev = pd.Series(candle_body).rolling(168).std().values
    relative_strength = rsi(close)

    signals = []

    for i in crossover(emafast, mamid):
        if i < 300:
            continue

        body_sorted = np.sort(candle_body[i-36:i])
        window_sdev = np.mean(candle_sdev[i-36:i])
        candle_median = np.median(candle_body[i-36:i])

        if (max(high[i-12:i]) - min(low[i-12:i])) / max(high[i-12:i]) > 0.04 \
        or max(candle_body[i-24:i]) > .04 \
        or sum(body_sorted[-2:]) - (candle_median * 3) > 8 * window_sdev:
            continue

        price = float(close[i])
        signal = None

        if price > emafast[i]:
            if price > mabase[i] and mamid[i] > emaslow[i] and relative_strength[i] > 50:
                signal = 'long'
                stop_loss = float(min(low[i-10:i]))
        else:   # price < emafast[i]
            if price < mabase[i] and mamid[i] < emaslow[i] and relative_strength[i] < 50:
                signal = 'short'
                stop_loss = float(max(high[i-10:i]))

        if signal and mamid_emaslow_diff[i] > .001 and 0.0075 < abs(1 - stop_loss/price) < .04:
            signals.append({'index_opened': int(i),
                            'date': df['date'][i],
                            'signal': signal,
                            'price': price,
                            'stop_loss': stop_loss,
                            'pct': abs(stop_loss - price) / price})

    return signals


def determine_TP(df, signals, cushion=0):
    ''' Figure out which TP level is hit '''

    low = df['low'].values
    low_inverse = -low
    high = df['high'].values
    high_inverse = -high

    for i, row in enumerate(signals):
        price = row['price']
        stop_loss = row['stop_loss']
        if row['signal'] == 'long':
            l_bounds = low
            u_bounds = high
        else:   # signal == 'short'
            l_bounds = high_inverse
            u_bounds = low_inverse
            cushion *= -1
            price *= -1
            stop_loss *= -1

        diff = price - stop_loss
        # stop_loss *= (1. + cushion)

        tp1 = price + diff/2.
        tp2 = price + diff
        tp3 = price + diff*2
        tp4 = price + diff*3

        tp_targets = [tp1, tp2, tp3, tp4]
        index_tp_hit = [None, None, None, None, None]
        tp = 0

        for x in range(row['index_opened'] + 1, len(df)):
            while tp != 4 and u_bounds[x] > tp_targets[tp]:
                tp += 1
                index_tp_hit[tp] = x
            if tp == 4 or l_bounds[x] < stop_loss:
                # Add index hit for stop loss
                if tp == 0:
                    index_tp_hit[0] = x
                break
            if tp > 0:
                stop_loss = price

        # Remove signal if position never fully closes before end of price data
        # NOTE: Could this fuck up logic if we pop the second to last signal, but
        #   keep the last signal?  `i` could be referencing a non-existing index.
        if x == len(df):
            signals.pop(i)
        signals[i]['tp'] = tp
        signals[i]['index_tp_hit'] = index_tp_hit
        signals[i]['index_closed'] = x
