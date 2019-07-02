from datetime import datetime
import pandas as pd
import numpy as np


df = pd.read_csv('prices/BTC.csv')
df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d %H:%M:%S')


def ma(prices, window):
    return prices.rolling(window=window)


def ema(prices, window):
    return prices.ewm(span=window, adjust=False)


def macd(prices):
    pass


def rsi(prices):
    # Based on last two weeks
    n = 24 * 14
    deltas = np.diff(prices)
    seed = deltas[:n+1]
    up = seed[seed>0].sum()/n
    down = -seed[seed<0].sum()/n
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
    cross = []
    l1_gt_l2 = line1 > line2
    current_val = l1_gt_l2[0]
    for next_val in l1_gt_l2[1:]:
        cross.append(current_val != next_val)
        current_val = next_val

    return cross



def main():

    ema(prices, window=40)
    macd(prices)
    rsi(prices)

    # Logic
    intersections = cross(ema(prices, window=3), ma(prices, window=20))



if __name__ == '__name__':
    main()
