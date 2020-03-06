import pandas as pd
import numpy as np
import ccxt
from datetime import datetime, timedelta
import time
import os


binance = ccxt.binance()


for ticker in ['ETH/BTC', 'LTC/BTC', 'EOS/BTC', 'BCH/BTC']:
    ticker = 'BTC/USDT'

    start_date = datetime(year=2018, month=12, day=1, hour=1, minute=0)
    df = []

    # Run until Valentine's Day, 2020
    while start_date < datetime(year=2019, month=6, day=30, hour=23, minute=0):

        data = binance.fetch_ohlcv(ticker, '1m', limit=500, since=int(time.mktime(start_date.timetuple())*1000))
        df.extend(data)

        # fetching last date to
        data = np.array(data)
        last_date = datetime.fromtimestamp(data[-1, 0]/1000)
        start_date = last_date + timedelta(minutes=1)

        time.sleep(.1)

    df = pd.DataFrame(df, columns=['date', 'open', 'high', 'low', 'close', 'volume'])
    df['date'] = df['date'].apply(lambda x: datetime.fromtimestamp(x/1000))

    df.to_csv(ticker.replace('/', '-') + '.csv', index=False)
