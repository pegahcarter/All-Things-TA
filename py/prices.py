# Code to create prices.csv
import pandas as pd
import numpy as np
import ccxt
from datetime import datetime, timedelta

btc = pd.read_csv('ohlcv/BTC.csv')
binance = ccxt.binance()
start = datetime(year=2018,month=1,day=1)

for coin in ['ETH' ,'BCH', 'XRP', 'BCH', 'LTC']:
    start_date = start
    df = []
    while start_date < datetime.now():
        data = binance.fetch_ohlcv(coin + '/BTC', '1h', limit=1000, since=int(start_date.timestamp()*1000))
        df += data
        start_date += timedelta(hours=len(data))

    df = pd.DataFrame(df, columns=['date', 'open', 'high', 'low', 'close', 'volume'])
    df['date'] = [start + timedelta(hours=i) for i in range(len(df))]
    for col in ['open', 'high', 'low', 'close', 'volume']:
        df[col] *= btc['close']
        
    df.to_csv('ohlcv/' + coin + '.csv', index=False)
