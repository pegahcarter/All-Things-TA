# Code to create bitmex prices
import pandas as pd
import numpy as np
import ccxt
from datetime import datetime, timedelta
import time

signals = pd.read_csv('../../data/signals/atta_insiders.csv')

bitmex = ccxt.bitmex()
# tickers_traded_2020 = [x for x in signals['ticker'].unique() if '/H20' in x or '/USD' in x]

start = datetime(year=2020, month=1, day=1, hour=0)

for ticker in ['XRP/USD']:
    start_date = start
    df = []

    while start_date < datetime.now():
        data = bitmex.fetch_ohlcv(ticker, '1h', limit=500, since=int(time.mktime(start_date.timetuple())*1000))
        df += data

        last_date = datetime.fromtimestamp(np.array(data)[-1, 0]/1000)
        start_date = last_date + timedelta(hours=1)
        time.sleep(.5)

    df = pd.DataFrame(df, columns=['date', 'open', 'high', 'low', 'close', 'volume'])
    df['date'] = [datetime.fromtimestamp(x/1000) for x in df['date']]

    df.to_csv(f"{ticker.replace('/','')}.csv", index=False)
