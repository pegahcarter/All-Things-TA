# Helper functions
import pandas as pd
import numpy as np
import timeit
import requests
import time
import os
from urllib.parse import urlencode
from datetime import datetime, timedelta
from py.variables import *


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


def args_to_dtype(dtype):
    ''' Convert arguments in a function to a specific data type, depending on what
        actions will be done with the arguments '''

    def format_args(fn):
        def wrapper(*args, **kwargs):
            args = [dtype(x) if type(x) != dtype else x for x in args]
            return fn(*args, **kwargs)
        return wrapper
    return format_args


@args_to_dtype(pd.Series)
def ema(line, span=2):
    ''' Returns the "exponential moving average" for a list '''
    return line.ewm(span=span, min_periods=1, adjust=False).mean().tolist()


@args_to_dtype(np.array)
def sma(close, window=14):
    ''' Returns the "simple moving average" for a list '''
    arr = close.cumsum()
    arr[window:] = arr[window:] - arr[:-window]
    arr[:window] = 0
    return arr / window

# def sma(line, window, attribute='mean'):
#     line = pd.Series(line)
#     return getattr(line.rolling(window=window, min_periods=1), attribute)()


@args_to_dtype(np.array)
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


@args_to_dtype(pd.Series)
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

    return list(rsi)


def maxmin(max_or_min, *args):
    ''' Compare lists and return the max or min value at each index '''
    if max_or_min == 'max':
        return np.amax(args, axis=0)
    elif max_or_min == 'min':
        return np.amin(args, axis=0)
    else:
        raise ValueError('Enter "max" or "min" as max_or_min parameter.')


@args_to_dtype(np.array)
def crossover(x1, x2):
    ''' Find all instances of intersections between two lines '''
    x1_gt_x2 = x1 > x2
    cross = np.diff(x1_gt_x2)
    cross = np.insert(cross, 0, False)
    cross_indices = np.flatnonzero(cross)
    return cross_indices


def profit_per_tp(*tp_pcts):
    '''
    Take-profit levels:  .5:1, 1:1, 2:1, 3:1
    '''

    profit_levels = [0.5, 1, 2, 3]
    results = [0 for _ in tp_pcts]

    tp_pcts = np.divide(tp_pcts, 100)

    for x in range(len(tp_pcts)):
        results[x] = tp_pcts[x] * profit_levels[x] * sum(tp_pcts[x:])
        if x > 0:
            results[x] += results[x - 1]

    results.insert(0, -1)
    return results


def net_profit(signals, tp_pcts):

    tp_profit_pcts = profit_per_tp(*tp_pcts.values())
    trade_profits = list(map(lambda x: x['pct'] * tp_profit_pcts[x['tp']], signals))

    return sum(trade_profits)
