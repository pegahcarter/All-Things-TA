from datetime import datetime
import pandas as pd
import numpy as np


df = pd.read_csv('prices/BTC.csv')
df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d %H:%M:%S')

ema_3 = ema(df['close'], 3)
ma_20 = ma(df['close'], 20)

len(ma_20) - ma_20.count()
ma_20.isna().sum()

ema_3 = ema_3[20:]
ma_20 = ma_20[20:]


intersections = cross(ema_3, ma_20)


def ma(prices, window):
    return prices.rolling(window=window).mean()


def ema(prices, window):
    return prices.ewm(span=window, adjust=False).mean()


def macd(prices):
    pass


def rsi(prices):
    # Based on last two weeks
    n = 24 * 14
    deltas = np.diff(prices)
    seed = deltas[:n+1]
    up = seed[seed > 0].sum()/n
    down = -seed[seed < 0].sum()/n
    rs = up/down
    rsi = np.zeros_like(prices)
    rsi[:n] = 100. - 100./(1.+rs)
    for i in range(n, len(prices)):
        delta = deltas[i-1]
        if delta > 0:
            up_val = delta
            down_val = 0.
        else:
            up_val = 0.
            down_val = -delta

        up = (up*(n-1) + up_val)/n
        down = (down*(n-1) + down_val)/n

        rs = up/down
        rsi[i] = 100. - 100./(1.+rs)

    return rsi


def cross(line1, line2):
    nan_count = max(line1.isna().sum(), line2.isna().sum())
    crosses = [None for i in range(nan_count)]
    l1_gt_l2 = line1 > line2
    current_val = l1_gt_l2[nan_count]
    for next_val in l1_gt_l2[nan_count+1:]:
        crosses.append(current_val != next_val)
        current_val = next_val

    return crosses



def main():

    ema_3 = ema(prices, window=3)
    ema_40 = ema(prices, window=40)
    ma_20 = ma(prices, window=20)
    macd(prices)
    rsi(prices)

    # Logic
    intersections = cross(ema_3, ma_20)
    ema_40_above = ema_40 > ema_3 & ema_40 > ma_20
    rsi_above = rsi > 50
    macd_above = macd > 0

    for intersection in intersections:
        if intersection:
            if ema_40_above[i] & rsi_above[i] & macd_above[i]:
                signal = "buy"
            elif not ema_40_above[i] & not rsi_above[i] & not macd_above[i]:
                signal = "sell"



if __name__ == '__name__':
    main()
