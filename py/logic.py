import pandas as pd
import numpy as np


def run(ticker, df):

    prices = df['close'].copy()

    ema3 = calc_ema(prices, window=3)
    ma20 = calc_ma(prices, window=20)
    ema40 = calc_ema(prices, window=40)
    ema3_gt_ma20 = ema3 > ma20

    intersections = pd.Series(cross(ema3, ma20))
    cross_indices = list(intersections[intersections == True].index)
    last_signal = None
    coin_signals = []

    for cross_index in cross_indices:
        signal = None
        for index, close in prices[cross_index:].iteritems():
            rng = ema3_gt_ma20[cross_index:index+1]
            if len(set(rng)) == 2:
                break

            if True in set(rng):
                if last_signal != 'BUY':
                    if close > ema3[index]:
                        if ma20[index] > ema40[index]:
                            signal = True
                            last_signal = 'BUY'
                        break
            else:   # False in set(rng)
                if last_signal != 'SELL':
                        if close < ema3[index]:
                            if ma20[index] < ema40[index]:
                                signal = True
                                last_signal = 'SELL'
                            break

        if signal:
            coin_signals.append([df['date'][index], last_signal, ticker, '{:.8f}'.format(close)])

    return coin_signals


def calc_ma(prices, window):
    return prices.rolling(window=window).mean().fillna(0)


def calc_ema(prices, window):
    return prices.ewm(span=window, adjust=False).mean()


def calc_macd(prices, fast=12, slow=26):
    '''
    macd line = fast_ema - slow_ema
    signal line = 9ema of macd line
    histogram = macd line - signal line
    '''
    ema_fast = calc_ema(prices, window=fast)
    ema_slow = calc_ema(prices, window=slow)
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


def cross(line1, line2):
    nan_count = max(line1.isna().sum(), line2.isna().sum())
    crosses = [False for i in range(nan_count)]
    l1_gt_l2 = line1 > line2
    current_val = l1_gt_l2[nan_count]
    for next_val in l1_gt_l2[nan_count+1:]:
        crosses.append(current_val != next_val)
        current_val = next_val
    crosses.insert(0, False)
    return crosses
