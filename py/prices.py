# Code to create prices.csv
import pandas as pd
import numpy as np
import ccxt
from datetime import datetime, timedelta
from time import sleep


btc = pd.read_csv('ohlcv/BTC.csv')
binance = ccxt.binance()
start = datetime(year=2018,month=1,day=1)

# for coin in ['ETH' ,'BCH', 'XRP', 'BCH', 'LTC']:
start_date = start
df = []
while start_date < datetime.now():
    data = binance.fetch_ohlcv('ADA/BTC', '1h', limit=500, since=int(start_date.timestamp()*1000))
    df += data
    start_date += timedelta(hours=len(data))
    sleep(1)

df = pd.DataFrame(df, columns=['date', 'open', 'high', 'low', 'close', 'volume'])
df['date'] = [datetime.fromtimestamp(x/1000) for x in df['date']]

for col in ['open', 'high', 'low', 'close', 'volume']:
    df[col] *= btc['close']

df.dropna().to_csv('ohlcv/' + coin + '.csv', index=False)
