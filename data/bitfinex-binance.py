# Code to create bitfinex prices
import pandas as pd
import numpy as np
import ccxt
from datetime import datetime, timedelta
import time


# New code to pull binance prices
# NOTE: some date discrepencies before 2018.02.10 22:00 & between 2018.06.25 21:00 - 2018.06.26 6:00


# for ticker in ['BTC/USDT', 'ETH/BTC', 'ETH/USDT', 'EOS/BTC', 'LTC/BTC', 'XRP/BTC', 'ADA/BTC']:
for ticker in ['BTC/USDT']:


    # df_old = pd.read_csv(f'binance/{ticker.replace("/", "-")}.csv')
    start_date = datetime(year=2018, month=2, day=10, hour=22)
    # start_date = pd.to_datetime(df_old['date'].iat[-1]) + timedelta(hours=1)
    df = []

    while start_date < datetime(year=2020, month=1, day=1, hour=1):
        data = binance.fetch_ohlcv(ticker, '1h', limit=500, since=int(time.mktime(start_date.timetuple())*1000))
        df.extend(data)

        # fetching last date to
        data = np.array(data)
        last_date = datetime.fromtimestamp(data[-1, 0]/1000)
        start_date = last_date + timedelta(hours=1)

        time.sleep(.1)

    df = pd.DataFrame(df, columns=['date', 'open', 'high', 'low', 'close', 'volume'])
    df['date'] = df['date'].apply(lambda x: datetime.fromtimestamp(x/1000))

    # df_old = df_old.append(df, ignore_index=True)
    df.to_csv(f'binance/{ticker.replace("/", "-")}.csv', index=False)
    # df_old.to_csv(f'binance/{ticker.replace("/", "-")}.csv', index=False)




# Messy old code that pulled bitfinex prices
bitfinex = ccxt.bitfinex()

for ticker in ['BTC/USDT', 'EOS/BTC', 'ETH/BTC', 'LTC/BTC', 'XRP/BTC', 'ADA/BTC']:
    coin = ticker[:ticker.find('/')]
    start_date = start
    df = []

    while start_date < datetime.now():
        data = bitfinex.fetch_ohlcv(ticker, '1h', limit=500, since=int(time.mktime(start_date.timetuple())*1000))
        df += data
        start_date += timedelta(hours=len(data))
        time.sleep(1)

    df = pd.DataFrame(df, columns=['date', 'open', 'high', 'low', 'close', 'volume'])
    df['date'] = [datetime.fromtimestamp(x/1000) for x in df['date']]

    df_old = pd.read_csv('data/bitfinex/' + coin + '.csv')
    df_new = df_old.append(df, ignore_index=True, sort=False)
    df_new.to_csv('data/bitfinex/' + coin + '.csv', index=False)
    # df_new.to_csv('data/bitfinex/' + coin + '.csv', index=False)   # BCH exception
