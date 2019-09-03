# Code to create prices.csv
import pandas as pd
import numpy as np
import ccxt
from datetime import datetime, timedelta
import time

binance = ccxt.binance()

btc = pd.read_csv('ohlcv/BTC.csv')
start = datetime.strptime(btc['date'].iat[-1], '%Y-%m-%d %H:%M:%S')
start_date = start


for ticker in ['BTC/USDT', 'ADA/BTC', 'EOS/BTC', 'ETH/BTC', 'LTC/BTC', 'XRP/BTC']:
    coin = ticker[:ticker.find('/')]
    start_date = start
    df = []

    while start_date < datetime.now():
        data = binance.fetch_ohlcv(ticker, '1h', limit=500, since=int(time.mktime(start_date.timetuple())*1000))
        df += data
        start_date += timedelta(hours=len(data))
        time.sleep(1)

    df = pd.DataFrame(df, columns=['date', 'open', 'high', 'low', 'close', 'volume'])
    df['date'] = [datetime.fromtimestamp(x/1000) for x in df['date']]
    if coin == 'BTC':
        btc_price = df['close'].copy()
    else:
        for col in ['open', 'high', 'low', 'close', 'volume']:
            df[col] *= btc_price

    df_old = pd.read_csv('ohlcv/' + coin + '.csv')
    df_new = df_old.append(df, ignore_index=True, sort=False)
    df_new.to_csv('ohlcv/' + coin + '.csv', index=False)
