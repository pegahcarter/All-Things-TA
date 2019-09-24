# Code to create bitmex prices
import pandas as pd
import numpy as np
import ccxt
from datetime import datetime, timedelta
import time
from py.variables import tickers

bitmex = ccxt.bitmex()
start = datetime(year=2019, month=6, day=14, hour=3)


for ticker in tickers:
    start_date = start
    df = []

    while start_date < datetime.now():
        data = bitmex.fetch_ohlcv(ticker, '1h', limit=500, since=int(time.mktime(start_date.timetuple())*1000))
        df += data
        start_date += timedelta(hours=len(data))
        time.sleep(.5)

    df = pd.DataFrame(df, columns=['date', 'open', 'high', 'low', 'close', 'volume'])
    df['date'] = [datetime.fromtimestamp(x/1000) for x in df['date']]

    df.to_csv('data/bitmex/' + ticker.replace('/','') + '.csv', index=False)
