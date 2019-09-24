# Code to create bitfinex prices
import pandas as pd
import numpy as np
import ccxt
from datetime import datetime, timedelta
import time

bitfinex = ccxt.bitfinex()

btc = pd.read_csv('data/bitfinex/BTC.csv')
start = datetime.strptime(btc['date'].iat[-1], '%Y-%m-%d %H:%M:%S')
# start = datetime(year=2019,month=1,day=1,hour=1)  # BCH exception
start_date = start


for ticker in ['BTC/USDT', 'EOS/BTC', 'ETH/BTC', 'LTC/BTC', 'XRP/BTC', 'ADA/BTC']:
# for ticker in ['BCH/BTC']:  # BCH exception
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
    if coin == 'BTC':
        btc_price = df['close'].copy()
    else:
        for col in ['open', 'high', 'low', 'close', 'volume']:
            df[col] *= btc_price

    df_old = pd.read_csv('data/bitfinex/' + coin + '.csv')
    df_new = df_old.append(df, ignore_index=True, sort=False)
    df_new.to_csv('data/bitfinex/' + coin + '.csv', index=False)
    # df_new.to_csv('data/bitfinex/' + coin + '.csv', index=False)   # BCH exception
