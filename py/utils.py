# Helper functions
import pandas as pd
import numpy as np
import timeit
import requests
import time
import os
# from urllib.parse import urlencode
from datetime import datetime, timedelta
from variables import *


def group_candles(df, interval):
    ''' Combine candles so instead of needing one dataset for each time interval,
        you can form time intervals using more precise data.

    Example: You have 15-min candlestick data but want to test a strategy based
        on 1-hour candlestick data  (interval=4).
    '''
    columns = ['date', 'open', 'high', 'low', 'close', 'volume']
    candles = np.array(df[columns])
    results = []
    for i in range(0, len(df)-interval, interval):
        results.append([
            candles[i, 0],                      # date
            candles[i, 1],                      # open
            candles[i:i+interval, 2].max(),     # high
            candles[i:i+interval, 3].min(),     # low
            candles[i+interval, 4],             # close
            candles[i:i+interval, 5].sum()      # volume
        ])
    return pd.DataFrame(results, columns=columns)


def args_to_numpy_array(fn):
    def wrapper(*args, **kwargs):
        args = [np.array(x) if not isinstance(x, np.ndarray) else x for x in args]
        return fn(*args, **kwargs)
    return wrapper


def ema(line, span):
    ''' Returns the "exponential moving average" for a list '''
    line = pd.Series(line)
    return line.ewm(span=span, min_periods=1, adjust=False).mean()


@args_to_numpy_array
def sma(close, window=14):
    ''' Returns the "simple moving average" for a list '''
    arr = close.cumsum()
    arr[window:] = arr[window:] - arr[:-window]
    arr[:window] = 0
    return arr / window


@args_to_numpy_array
def roc(close, n=1):
    ''' Returns the rate of change in price over n periods '''

    pct_diff = np.zeros_like(close)
    pct_diff[n:] = np.diff(close, n) / close[:-n] * 100
    return pct_diff


def macd(close, fast=8, slow=21):
    ''' Returns the "moving average convergence/divergence" (MACD) '''
    ema_fast = ema(close, fast)
    ema_slow = ema(close, slow)
    return (ema_fast/ema_slow - 1) * 100


def rsi(close, n=14):
    ''' Returns the "relative strength index", which is used to measure the velocity
    and magnitude of directional price movement.
    https://www.tradingview.com/scripts/relativestrengthindex/

    Args:
        close(pandas.Series): dataset 'close' column
        n(int): n period
    Returns:
        np.array: New feature generated.
    '''
    deltas = np.diff(close)
    seed = deltas[:n+1]
    up = seed[seed > 0].sum()/n
    down = -seed[seed < 0].sum()/n
    rsi = np.zeros_like(close)
    rsi[:n] = 100. - 100./(1.+ up/down)
    for i in range(n, len(close)):
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


def maxmin(max_or_min, *args):
    ''' Compare lists and return the max or min value at each index '''
    if max_or_min == 'max':
        return np.amax(args, axis=0)
    elif max_or_min == 'min':
        return np.amin(args, axis=0)
    else:
        raise ValueError('Enter "max" or "min" as max_or_min parameter.')


@args_to_numpy_array
def crossover(x1, x2):
    ''' Find all instances of intersections between two lines '''
    x1_gt_x2 = x1 > x2
    cross = np.diff(x1_gt_x2)
    cross = np.insert(cross, 0, False)
    cross_indices = np.flatnonzero(cross)
    return cross_indices


# def sma(line, window, attribute='mean'):
#     ''' Returns the "simple moving average" for a list '''
#     line = pd.Series(line)
#     return getattr(line.rolling(window=window, min_periods=1), attribute)()
