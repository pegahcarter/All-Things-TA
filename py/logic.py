import numpy as np
from datetime import datetime


def run(df):
    prices = df['close'].copy()
    ema_3 = calc_ema(prices, window=3)
    ema_40 = calc_ema(prices, window=40)
    ma_20 = calc_ma(prices, window=20)
    macd = calc_macd(prices)
    rsi = calc_rsi(prices)

    intersections = cross(ema_3, ma_20)
    ma_20_supported = ma_20 > ema_40
    ema_3_supported = ema_3 > ma_20
    rsi_above = rsi > 50
    macd_above = macd > 0

    signal = [None for x in range(len(df))]
    for i, intersection in enumerate(intersections):
        if intersection:
            if (ma_20_supported[i] and ema_3_supported[i] and rsi_above[i] and macd_above[i]):
                signal[i] = 'SELL'
            elif (not ma_20_supported[i] and not ema_3_supported[i] and not rsi_above[i] and not macd_above[i]):
                signal[i] = 'BUY'

    df['signal'] = signal
    df['date'] = [datetime.fromtimestamp(x/1000) for x in df['date']]
    return df


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

    return crosses
