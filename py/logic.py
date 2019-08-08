import pandas as pd
import numpy as np
from variables import *


def run(ticker, candle_abv, file=False):

    if file:
        data = pd.read_csv(file)
    else:
        data = exchange.fetch_ohlcv(ticker, candle_abv, limit=500, since=since)
        df = pd.DataFrame(data, columns=['date', 'open', 'high', 'low', 'close', 'volume'])
    prices = df['close'].copy()

    ema3 = prices.ewm(span=3, adjust=False).mean()
    ema40 = prices.ewm(span=40, adjust=False).mean()
    ma20 = prices.rolling(window=20).mean().fillna(0)
    ema3_gt_ma20 = ema3 > ma20

    current_val = ema3_gt_ma20[0]
    intersections = [False]

    for val in ema3_gt_ma20[1:]:
        intersections.append(val != current_val)
        current_val = val

    coin_signals = []
    for cross_index, intersection in enumerate(intersections):
        signal = None
        if intersection:
            for index, close in prices[cross_index:]:
                rng = set(ema3_gt_ma20[cross_index:index + 1])
                if True in rng and False in rng:
                    break
                elif True in rng:
                    if close > ema3[index]:
                        if ma20[index] > ema40[index]:
                            signal = 'BUY'
                        break
                else:
                    if close < ema3[index]:
                        if ma20[index] < ema40[index]:
                            signal = 'SELL'
                        break
            if signal:
                coin_signals.append([df['date'][index], signal, ticker, round(close, 8)])

    return coin_signals


def calc_macd(prices, fast=12, slow=26):
    '''
    macd line = fast_ema - slow_ema
    signal line = 9ema of macd line
    histogram = macd line - signal line
    '''
    ema_fast = prices.ewm(span=fast, adjust=False).mean()
    ema_slow = prices.ewm(span=slow, adjust=False).mean()
    return ema_fast - ema_slow


def calc_rsi(prices):
    n = 14
    deltas = np.diff(prices)
    seed = deltas[:n+1]
    up = seed[seed > 0].sum()/n
    down = -seed[seed < 0].sum()/n
    rsi = np.zeros_like(prices)
    rsi[:n] = 100. - 100./(1.+ up/down)
    for i in range(n, len(prices)):
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
