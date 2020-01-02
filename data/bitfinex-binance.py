# Code to create bitfinex prices
import pandas as pd
import numpy as np
import ccxt
from datetime import datetime, timedelta
import time


# New code to pull binance prices
# NOTE: some date discrepencies before 2018.02.10 22:00, between 2018.06.25 21:00 and
#   2018.06.26 6:00, and after 2019.11.29 17:00:00 (current date- 2019.11.30 12:30)
binance = ccxt.binance()

for ticker in ['BTC/USDT', 'ETH/BTC', 'ETH/USDT', 'EOS/BTC', 'LTC/BTC', 'XRP/BTC', 'ADA/BTC']:

    start_date = datetime(year=2018,month=2,day=10,hour=22)
    df = []

    while start_date < datetime(year=2019,month=11,day=28,hour=0):
        data = binance.fetch_ohlcv(ticker, '1h', limit=500, since=int(time.mktime(start_date.timetuple())*1000))
        df += data

        # fetching last date to
        data = np.array(data)
        last_date = datetime.fromtimestamp(data[-1, 0]/1000)
        start_date = last_date + timedelta(hours=1)

        time.sleep(.1)

    df = pd.DataFrame(df, columns=['date', 'open', 'high', 'low', 'close', 'volume'])
    df['date'] = df['date'].apply(lambda x: datetime.fromtimestamp(x/1000))

    df.to_csv('binance/' + ticker.replace('/', '-') + '.csv', index=False)



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
