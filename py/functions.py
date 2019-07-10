from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import ccxt
import os

# Loop to update CSV's with recent OHLCV data
def refresh_ohlcv(file):

    df = pd.read_csv('prices/' + file).drop('signal', axis=1)
    df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d %H:%M:%S')

    binance = ccxt.binance()
    coin = file[:file.find('.')]

    df_new = []
    start_date = df.iloc[-1]['date']
    while start_date < datetime.now():
        results = binance.fetch_ohlcv(coin + '/USDT', '1h', since=int(start_date.timestamp()*1000))
        df_new += results
        start_date += timedelta(hours=len(results))

    df_new = pd.DataFrame(df_new, columns=df.columns)
    df_new['date'] = df_new['date'].apply(lambda x: datetime.fromtimestamp(x/1000))
    df_new = df_new[df_new['date'] > df.iloc[-1]['date']]
    df = df.append(df_new, ignore_index=True)
    df.to_csv('prices/' + file, index=False)

    return coin, df


# Group hourly candle into candle intervals
def group_candles(candles):
    candles = np.array(candles)
    return ([
        candles[0, 0],         # date
        candles[0, 1],         # open
        candles[:, 2].max(),   # high
        candles[:, 3].min(),   # low
        candles[-1, 4],        # close
        candles[:, 5].sum()    # volume
    ])


# Combine signals to save into one CSV
def combine_signals(df_signal, df, coin):
    df = df.dropna()
    df['coin'] = coin
    df_signal = df_signal.append(df[['coin', 'date', 'signal']], ignore_index=True)
    return df_signal
