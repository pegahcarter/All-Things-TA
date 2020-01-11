from TAcharts.indicators import ema, sma, rsi
from TAcharts.utils import crossover

import numpy as np
import pandas as pd


def base(df, window_fast=8, window_mid=30, window_slow=50, trade_min=0,
                 trade_max=1, cushion=0, ticker=None, **kwargs):
    ''' Determine signals from OHLCV dataframe '''

    _open = df['open'].values
    high = df['high'].values
    low = df['low'].values
    close = df['close'].values

    emaslow = ema(close, n=window_slow)
    mamid = sma(close, n=window_mid)
    emafast = ema(close, n=window_fast)
    mabase = sma(close, n=200)

    signals = []

    for i in crossover(emafast, mamid):
        if i < 200:
            continue

        price = float(close[i])
        signal = None

        if price > emafast[i]:
            if price > mabase[i] and mamid[i] > emaslow[i]:
                signal = 'long'
                stop_loss = float(min(low[i-10:i]) * (1 + cushion))
        else:   # price < emafast[i]
            if price < mabase[i] and mamid[i] < emaslow[i]:
                signal = 'short'
                stop_loss = float(max(high[i-10:i]) * (1 - cushion))

        if signal and trade_min < abs(1 - stop_loss/price) < trade_max:
            signals.append({'index_opened': int(i),
                            'date': df['date'][i],
                            'signal': signal,
                            'ticker': ticker,
                            'price': price,
                            'stop_loss': stop_loss,
                            'pct': abs(stop_loss - price) / price})

    return signals
