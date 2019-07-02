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


def rsi(prices, n=24):
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
            upval = delta
            downval = 0.
        else:
            upval = 0.
            downval = -delta

        up = (up*(n-1) + upval)/n
        down = (down*(n-1) + downval)/n

        rs = up/down
        rsi[i] = 100. - 100./(1.+rs)

    return rsi






def main():

    ''' EMA '''
    # 3 period EMA
    ema(prices, period=3)
    # 40 period EMA
    ema(prices, period=40)

    ''' MA '''
    # 20 period MA
    ma(prices, period=20)

    ''' MACD '''
    # What period should this be?
    macd(prices)

    ''' RSI '''
    # What period should this be?
    rsi(prices)

    ''' Logic '''



if __name__ == '__name__':
    main()
