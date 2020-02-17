# Code to create bitmex prices
import pandas as pd
import numpy as np
import ccxt
from datetime import datetime, timedelta
import time


bitmex = ccxt.bitmex()
# tickers = [t for t in bitmex.fetchTickers() if 'H20' in t]
# tickers = [t for t in bitmex.fetchTickers() if '/USD' in t]
# tickers = [t for t in bitmex.fetchTickers() if 'H20' in t or '/USD' in t]


# for ticker in tickers:
for ticker in ['ETH/USD', 'BTC/USD']:
    filename = f"{ticker.replace('/', '')}.csv"
    df = []

    try:
        df_old = pd.read_csv(filename)
        start_date = datetime.strptime(df_old['date'].iat[-1], '%Y-%m-%d %H:%M:%S')
        df_old['date'] = pd.to_datetime(df_old['date'])
    except:
        start_date = datetime(year=2020, month=1, day=1, hour=0)


    while start_date < datetime.now():
        data = bitmex.fetch_ohlcv(ticker, '1h', limit=500, since=int(time.mktime(start_date.timetuple())*1000))
        df += data

        last_date = datetime.fromtimestamp(np.array(data)[-1, 0]/1000)
        start_date = last_date + timedelta(hours=1)
        time.sleep(.5)

    df = pd.DataFrame(df, columns=['date', 'open', 'high', 'low', 'close', 'volume'])
    df['date'] = [datetime.fromtimestamp(x/1000) for x in df['date']]

    # NOTE: add / remove this line as needed
    df = df_old.append(df, ignore_index=True)

    df.to_csv(f"{ticker.replace('/','')}.csv", index=False)
